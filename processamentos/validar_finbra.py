"""Ingestao e validacao estrutural de arquivos FINBRA em Excel."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from hashlib import sha256
from pathlib import Path
import re
from typing import Any

import pandas as pd


COLUNAS_IDENTIFICADORAS = {
    "ano",
    "exercicio",
    "codigo_ibge",
    "cod_ibge",
    "municipio",
    "nome_municipio",
    "uf",
}


@dataclass
class ResultadoAba:
    nome: str
    linhas: int
    colunas: int
    colunas_duplicadas: list[str] = field(default_factory=list)
    colunas_sem_nome: list[str] = field(default_factory=list)
    colunas_identificadoras: list[str] = field(default_factory=list)
    anos_encontrados: list[int] = field(default_factory=list)
    municipios_encontrados: int | None = None
    codigos_ibge_encontrados: int | None = None
    celulas_vazias: int = 0
    alertas: list[dict[str, str]] = field(default_factory=list)


@dataclass
class ResultadoValidacao:
    arquivo: str
    hash_sha256: str
    tamanho_bytes: int
    abas: list[ResultadoAba]
    anos_consolidados: list[int]
    total_municipios_estimado: int | None
    total_codigos_ibge: int | None
    alertas_criticos: int
    alertas_relevantes: int
    status: str

    def como_dicionario(self) -> dict[str, Any]:
        return asdict(self)


def calcular_hash(caminho: Path) -> str:
    digest = sha256()
    with caminho.open("rb") as arquivo:
        for bloco in iter(lambda: arquivo.read(1024 * 1024), b""):
            digest.update(bloco)
    return digest.hexdigest()


def normalizar_nome_coluna(valor: object) -> str:
    texto = str(valor).strip().lower()
    texto = re.sub(r"[^a-z0-9]+", "_", texto)
    return texto.strip("_")


def _localizar_coluna(colunas: list[object], candidatos: set[str]) -> object | None:
    for coluna in colunas:
        if normalizar_nome_coluna(coluna) in candidatos:
            return coluna
    return None


def _extrair_anos(quadro: pd.DataFrame) -> list[int]:
    anos: set[int] = set()
    coluna_ano = _localizar_coluna(list(quadro.columns), {"ano", "exercicio"})
    if coluna_ano is not None:
        valores = pd.to_numeric(quadro[coluna_ano], errors="coerce").dropna().astype(int)
        anos.update(int(valor) for valor in valores if 1900 <= int(valor) <= 2100)

    for coluna in quadro.columns:
        for correspondencia in re.findall(r"(?<!\d)(20\d{2})(?!\d)", str(coluna)):
            anos.add(int(correspondencia))
    return sorted(anos)


def _contar_distintos(quadro: pd.DataFrame, candidatos: set[str]) -> int | None:
    coluna = _localizar_coluna(list(quadro.columns), candidatos)
    if coluna is None:
        return None
    valores = quadro[coluna].dropna().astype(str).str.strip()
    valores = valores[valores.ne("")]
    return int(valores.nunique())


def validar_arquivo_finbra(caminho: Path) -> ResultadoValidacao:
    """Le todas as abas e produz diagnostico estrutural sem alterar a entrada."""
    if not caminho.exists():
        raise FileNotFoundError(caminho)
    if caminho.suffix.lower() not in {".xlsx", ".xls"}:
        raise ValueError("O arquivo FINBRA deve estar em formato XLSX ou XLS.")

    livro = pd.ExcelFile(caminho)
    resultados: list[ResultadoAba] = []
    anos_consolidados: set[int] = set()
    municipios: list[int] = []
    codigos: list[int] = []

    for nome_aba in livro.sheet_names:
        quadro = pd.read_excel(livro, sheet_name=nome_aba)
        nomes = [str(coluna) for coluna in quadro.columns]
        duplicadas = sorted({nome for nome in nomes if nomes.count(nome) > 1})
        sem_nome = [nome for nome in nomes if nome.lower().startswith("unnamed")]
        identificadoras = [
            str(coluna)
            for coluna in quadro.columns
            if normalizar_nome_coluna(coluna) in COLUNAS_IDENTIFICADORAS
        ]
        anos = _extrair_anos(quadro)
        quantidade_municipios = _contar_distintos(
            quadro, {"municipio", "nome_municipio"}
        )
        quantidade_codigos = _contar_distintos(
            quadro, {"codigo_ibge", "cod_ibge", "codigo_municipio"}
        )
        alertas: list[dict[str, str]] = []
        if quadro.empty:
            alertas.append({"nivel": "critico", "mensagem": "A aba esta vazia."})
        if duplicadas:
            alertas.append(
                {"nivel": "critico", "mensagem": "Existem colunas duplicadas."}
            )
        if sem_nome:
            alertas.append(
                {"nivel": "relevante", "mensagem": "Existem colunas sem rotulo."}
            )
        if not identificadoras:
            alertas.append(
                {
                    "nivel": "relevante",
                    "mensagem": "Nenhuma coluna identificadora padrao foi reconhecida.",
                }
            )
        if not anos:
            alertas.append(
                {"nivel": "relevante", "mensagem": "Nenhum exercicio foi reconhecido."}
            )

        resultado = ResultadoAba(
            nome=nome_aba,
            linhas=int(quadro.shape[0]),
            colunas=int(quadro.shape[1]),
            colunas_duplicadas=duplicadas,
            colunas_sem_nome=sem_nome,
            colunas_identificadoras=identificadoras,
            anos_encontrados=anos,
            municipios_encontrados=quantidade_municipios,
            codigos_ibge_encontrados=quantidade_codigos,
            celulas_vazias=int(quadro.isna().sum().sum()),
            alertas=alertas,
        )
        resultados.append(resultado)
        anos_consolidados.update(anos)
        if quantidade_municipios is not None:
            municipios.append(quantidade_municipios)
        if quantidade_codigos is not None:
            codigos.append(quantidade_codigos)

    alertas_criticos = sum(
        1
        for aba in resultados
        for alerta in aba.alertas
        if alerta["nivel"] == "critico"
    )
    alertas_relevantes = sum(
        1
        for aba in resultados
        for alerta in aba.alertas
        if alerta["nivel"] == "relevante"
    )
    status = "reprovado" if alertas_criticos else "aprovado_com_alertas" if alertas_relevantes else "aprovado"

    return ResultadoValidacao(
        arquivo=caminho.name,
        hash_sha256=calcular_hash(caminho),
        tamanho_bytes=caminho.stat().st_size,
        abas=resultados,
        anos_consolidados=sorted(anos_consolidados),
        total_municipios_estimado=max(municipios) if municipios else None,
        total_codigos_ibge=max(codigos) if codigos else None,
        alertas_criticos=alertas_criticos,
        alertas_relevantes=alertas_relevantes,
        status=status,
    )
