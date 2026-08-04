"""Acesso substituivel a fontes cartograficas municipais."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import geopandas as gpd


@dataclass(frozen=True)
class ConfiguracaoCartografica:
    provedor: str
    campo_codigo: str
    campo_nome: str
    sistema_referencia: str = "EPSG:4326"
    arquivo: Path | None = None
    url: str | None = None
    arquivo_cache: Path | None = None
    fonte: str | None = None
    credito: str | None = None
    atualizar_cache_automaticamente: bool = False
    tempo_limite_download_segundos: int = 120


class GerenciadorCartografico:
    """Carrega, valida, registra e recorta a malha sem acoplar o sistema a uma fonte."""

    def __init__(self, configuracao: ConfiguracaoCartografica) -> None:
        self.configuracao = configuracao

    @staticmethod
    def calcular_hash(arquivo: Path) -> str:
        resumo = hashlib.sha256()
        with arquivo.open("rb") as fluxo:
            for bloco in iter(lambda: fluxo.read(1024 * 1024), b""):
                resumo.update(bloco)
        return resumo.hexdigest()

    def _baixar_para_cache(self) -> Path:
        if not self.configuracao.url or not self.configuracao.arquivo_cache:
            raise ValueError("URL e arquivo_cache sao obrigatorios para geojson_remoto.")

        destino = self.configuracao.arquivo_cache
        destino.parent.mkdir(parents=True, exist_ok=True)
        temporario = destino.with_suffix(destino.suffix + ".parcial")
        requisicao = Request(
            self.configuracao.url,
            headers={"User-Agent": "mapa-do-tesouro/0.3.1"},
        )

        try:
            with urlopen(
                requisicao,
                timeout=self.configuracao.tempo_limite_download_segundos,
            ) as resposta:
                temporario.write_bytes(resposta.read())
        except (HTTPError, URLError, TimeoutError) as erro:
            temporario.unlink(missing_ok=True)
            raise RuntimeError(f"Falha ao baixar a cartografia: {erro}") from erro

        self._validar_geojson_basico(temporario)
        temporario.replace(destino)
        self._registrar_metadados_cache(destino)
        return destino

    def _resolver_arquivo(self) -> Path:
        if self.configuracao.provedor == "geojson_local":
            if self.configuracao.arquivo is None:
                raise ValueError("arquivo e obrigatorio para geojson_local.")
            if not self.configuracao.arquivo.exists():
                raise FileNotFoundError(self.configuracao.arquivo)
            return self.configuracao.arquivo

        if self.configuracao.provedor == "geojson_remoto":
            if self.configuracao.arquivo_cache is None:
                raise ValueError("arquivo_cache e obrigatorio para geojson_remoto.")
            cache = self.configuracao.arquivo_cache
            if cache.exists() and not self.configuracao.atualizar_cache_automaticamente:
                self._validar_geojson_basico(cache)
                return cache
            return self._baixar_para_cache()

        raise NotImplementedError(
            f"Provedor ainda nao implementado: {self.configuracao.provedor}"
        )

    @staticmethod
    def _validar_geojson_basico(arquivo: Path) -> None:
        try:
            conteudo = json.loads(arquivo.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as erro:
            raise ValueError(f"GeoJSON invalido: {arquivo}") from erro

        if conteudo.get("type") != "FeatureCollection":
            raise ValueError("A cartografia deve ser uma FeatureCollection.")
        if not isinstance(conteudo.get("features"), list) or not conteudo["features"]:
            raise ValueError("A cartografia nao contem feicoes.")

    def _registrar_metadados_cache(self, arquivo: Path) -> None:
        metadados = {
            "fonte": self.configuracao.fonte,
            "credito": self.configuracao.credito,
            "url": self.configuracao.url,
            "data_download_utc": datetime.now(timezone.utc).isoformat(),
            "arquivo": str(arquivo),
            "sha256": self.calcular_hash(arquivo),
        }
        arquivo_metadados = arquivo.with_suffix(arquivo.suffix + ".metadados.json")
        arquivo_metadados.write_text(
            json.dumps(metadados, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def carregar_malha(self) -> gpd.GeoDataFrame:
        arquivo = self._resolver_arquivo()
        self._validar_geojson_basico(arquivo)
        malha = gpd.read_file(arquivo)
        campos_obrigatorios = {
            self.configuracao.campo_codigo,
            self.configuracao.campo_nome,
            "geometry",
        }
        faltantes = campos_obrigatorios.difference(malha.columns)
        if faltantes:
            raise ValueError(f"Campos cartograficos ausentes: {sorted(faltantes)}")

        malha = malha.copy()
        malha[self.configuracao.campo_codigo] = (
            malha[self.configuracao.campo_codigo].astype(str).str.zfill(7)
        )
        if malha[self.configuracao.campo_codigo].duplicated().any():
            duplicados = sorted(
                malha.loc[
                    malha[self.configuracao.campo_codigo].duplicated(keep=False),
                    self.configuracao.campo_codigo,
                ].unique()
            )
            raise ValueError(f"Codigos cartograficos duplicados: {duplicados}")
        if malha.crs is None:
            malha = malha.set_crs(self.configuracao.sistema_referencia)
        return malha

    def selecionar_municipios(self, codigos_ibge: list[str]) -> gpd.GeoDataFrame:
        codigos = {str(codigo).zfill(7) for codigo in codigos_ibge}
        malha = self.carregar_malha()
        recorte = malha[malha[self.configuracao.campo_codigo].isin(codigos)].copy()
        encontrados = set(recorte[self.configuracao.campo_codigo])
        ausentes = sorted(codigos.difference(encontrados))
        if ausentes:
            raise ValueError(f"Codigos IBGE sem geometria: {ausentes}")
        return recorte
