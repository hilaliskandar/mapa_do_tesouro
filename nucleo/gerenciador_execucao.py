"""Criacao e registro auditavel das execucoes."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
import hashlib
import json
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ContextoExecucao:
    identificador: str
    criada_em: str
    versao_sistema: str
    arquivo_finbra: str
    arquivo_cartografia: str | None
    diretorio: str

    def como_dicionario(self) -> dict[str, Any]:
        return asdict(self)


class GerenciadorExecucao:
    """Cria diretorios imutaveis e o manifesto inicial de cada execucao."""

    ETAPAS = (
        "00_entrada",
        "01_validacao_estrutural",
        "02_normalizacao",
        "03_classificacao_contabil",
        "04_agregacoes",
        "05_deflacao",
        "06_per_capita",
        "07_indicadores",
        "08_series_historicas",
        "09_cartografia",
        "10_analises_municipais",
        "11_analise_regional",
        "12_relatorios",
        "logs",
    )

    def __init__(self, diretorio_raiz: Path, versao_sistema: str = "0.1.0") -> None:
        self.diretorio_raiz = diretorio_raiz
        self.versao_sistema = versao_sistema

    def criar_execucao(
        self,
        nome_arquivo_finbra: str,
        nome_arquivo_cartografia: str | None = None,
    ) -> ContextoExecucao:
        instante = datetime.now().astimezone()
        semente = f"{instante.isoformat()}|{nome_arquivo_finbra}|{nome_arquivo_cartografia}"
        sufixo = hashlib.sha256(semente.encode("utf-8")).hexdigest()[:8]
        identificador = f"{instante:%Y%m%d_%H%M%S}_{sufixo}"
        diretorio = self.diretorio_raiz / identificador
        diretorio.mkdir(parents=True, exist_ok=False)

        for etapa in self.ETAPAS:
            (diretorio / etapa).mkdir()

        contexto = ContextoExecucao(
            identificador=identificador,
            criada_em=instante.isoformat(),
            versao_sistema=self.versao_sistema,
            arquivo_finbra=nome_arquivo_finbra,
            arquivo_cartografia=nome_arquivo_cartografia,
            diretorio=str(diretorio),
        )

        (diretorio / "manifest.json").write_text(
            json.dumps(contexto.como_dicionario(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        (diretorio / "README.md").write_text(
            self._gerar_readme_execucao(contexto), encoding="utf-8"
        )
        return contexto

    @staticmethod
    def _gerar_readme_execucao(contexto: ContextoExecucao) -> str:
        return (
            f"# Execucao {contexto.identificador}\n\n"
            f"- Criada em: {contexto.criada_em}\n"
            f"- Versao do sistema: {contexto.versao_sistema}\n"
            f"- Base FINBRA: {contexto.arquivo_finbra}\n"
            f"- Cartografia: {contexto.arquivo_cartografia or 'nao informada'}\n\n"
            "Cada subdiretorio preserva entradas, saidas, parametros, alertas e relatorios "
            "da respectiva etapa.\n"
        )
