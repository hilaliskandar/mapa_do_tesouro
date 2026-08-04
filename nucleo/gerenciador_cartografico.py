"""Acesso substituivel a fontes cartograficas municipais."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import geopandas as gpd


@dataclass(frozen=True)
class ConfiguracaoCartografica:
    provedor: str
    arquivo: Path
    campo_codigo: str
    campo_nome: str
    sistema_referencia: str = "EPSG:4326"


class GerenciadorCartografico:
    """Carrega, valida e recorta a malha sem acoplar o sistema a uma fonte especifica."""

    def __init__(self, configuracao: ConfiguracaoCartografica) -> None:
        self.configuracao = configuracao

    def carregar_malha(self) -> gpd.GeoDataFrame:
        if self.configuracao.provedor != "geojson_local":
            raise NotImplementedError(
                f"Provedor ainda nao implementado: {self.configuracao.provedor}"
            )
        if not self.configuracao.arquivo.exists():
            raise FileNotFoundError(self.configuracao.arquivo)

        malha = gpd.read_file(self.configuracao.arquivo)
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
