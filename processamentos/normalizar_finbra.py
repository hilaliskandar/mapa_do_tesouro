"""Normalizacao auditavel das abas FINBRA para formato longo."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
import re
import unicodedata
from typing import Any

import pandas as pd


ABAS_DADOS = {
    "receitas": "receitas",
    "despesas": "despesas",
    "despesa por funcao": "despesa_por_funcao",
}
ABAS_AUXILIARES = {
    "cobertura": "cobertura",
    "dicionario": "dicionario",
    "fontes": "fontes",
    "leia me": "leia_me",
}
CANDIDATOS_IDENTIFICADORES = {
    "ano": "ano",
    "exercicio": "ano",
    "municipio": "municipio",
    "nome_municipio": "municipio",
    "codigo_ibge": "codigo_ibge",
    "cod_ibge": "codigo_ibge",
    "codigo_municipio": "codigo_ibge",
    "uf": "uf",
    "sigla_uf": "uf",
}


@dataclass
class ResultadoNormalizacaoAba:
    aba_origem: str
    tipo: str
    arquivo_saida: str
    linhas_origem: int
    colunas_origem: int
    colunas_identificadoras: list[str]
    colunas_valores: int
    celulas_candidatas: int
    valores_preservados: int
    valores_ausentes_omitidos: int
    valores_nao_numericos: int
    anos: list[int] = field(default_factory=list)
    municipios: int | None = None
    codigos_ibge: int | None = None
    alertas: list[dict[str, str]] = field(default_factory=list)


@dataclass
class ResultadoNormalizacao:
    arquivo_origem: str
    pasta_saida: str
    abas: list[ResultadoNormalizacaoAba]
    total_valores_preservados: int
    total_ausentes_omitidos: int
    total_nao_numericos: int
    alertas_criticos: int
    alertas_relevantes: int
    status: str

    def como_dicionario(self) -> dict[str, Any]:
        return asdict(self)


def normalizar_texto(valor: object) -> str:
    texto = unicodedata.normalize("NFKD", str(valor))
    texto = "".join(caractere for caractere in texto if not unicodedata.combining(caractere))
    texto = texto.strip().lower()
    texto = re.sub(r"[^a-z0-9]+", "_", texto)
    return texto.strip("_")


def _nome_aba_normalizado(nome: str) -> str:
    return normalizar_texto(nome).replace("_", " ")


def _mapear_identificadores(colunas: list[object]) -> dict[object, str]:
    mapeamento: dict[object, str] = {}
    usados: set[str] = set()
    for coluna in colunas:
        normalizado = normalizar_texto(coluna)
        destino = CANDIDATOS_IDENTIFICADORES.get(normalizado)
        if destino and destino not in usados:
            mapeamento[coluna] = destino
            usados.add(destino)
    return mapeamento


def _decompor_coluna_contabil(rotulo: object) -> tuple[str | None, str | None, str]:
    original = str(rotulo).strip()
    partes = [parte.strip() for parte in original.split("|")]
    if len(partes) >= 3:
        return partes[0] or None, partes[1] or None, " | ".join(partes[2:]).strip()
    if len(partes) == 2:
        esquerda, direita = partes
        padrao_codigo = re.compile(r"^\d+(?:[.\-]\d+)*$")
        if padrao_codigo.match(esquerda):
            return None, esquerda, direita
        return esquerda or None, None, direita

    correspondencia = re.match(r"^([\d.\-]+)\s*[-–:]\s*(.+)$", original)
    if correspondencia:
        return None, correspondencia.group(1).strip(), correspondencia.group(2).strip()
    return None, None, original


def _padronizar_identificadores(quadro: pd.DataFrame, mapeamento: dict[object, str]) -> pd.DataFrame:
    resultado = quadro.rename(columns=mapeamento).copy()
    if "ano" in resultado.columns:
        resultado["ano"] = pd.to_numeric(resultado["ano"], errors="coerce").astype("Int64")
    if "codigo_ibge" in resultado.columns:
        resultado["codigo_ibge"] = (
            resultado["codigo_ibge"]
            .astype("string")
            .str.replace(r"\.0$", "", regex=True)
            .str.strip()
            .str.zfill(7)
        )
    if "municipio" in resultado.columns:
        resultado["municipio"] = resultado["municipio"].astype("string").str.strip()
    if "uf" in resultado.columns:
        resultado["uf"] = resultado["uf"].astype("string").str.strip().str.upper()
    return resultado


def _normalizar_aba_dados(
    quadro: pd.DataFrame,
    nome_aba: str,
    bloco: str,
    pasta_saida: Path,
) -> ResultadoNormalizacaoAba:
    mapeamento = _mapear_identificadores(list(quadro.columns))
    alertas: list[dict[str, str]] = []
    obrigatorios = {"ano", "municipio", "codigo_ibge"}
    encontrados = set(mapeamento.values())
    faltantes = sorted(obrigatorios.difference(encontrados))
    if faltantes:
        alertas.append(
            {
                "nivel": "critico",
                "mensagem": f"Identificadores obrigatorios ausentes: {faltantes}",
            }
        )

    padronizado = _padronizar_identificadores(quadro, mapeamento)
    identificadores = [campo for campo in ("uf", "codigo_ibge", "municipio", "ano") if campo in padronizado.columns]
    colunas_valores = [coluna for coluna in padronizado.columns if coluna not in identificadores]
    celulas_candidatas = len(padronizado) * len(colunas_valores)

    longo = padronizado.melt(
        id_vars=identificadores,
        value_vars=colunas_valores,
        var_name="rotulo_conta_original",
        value_name="valor_original",
    )
    ausentes = int(longo["valor_original"].isna().sum())
    longo = longo[longin := longo["valor_original"].notna()].copy()
    del longin

    longo["valor"] = pd.to_numeric(longo["valor_original"], errors="coerce")
    nao_numericos = int(longo["valor"].isna().sum())
    if nao_numericos:
        alertas.append(
            {
                "nivel": "relevante",
                "mensagem": f"Foram encontrados {nao_numericos} valores nao numericos.",
            }
        )

    decomposicao = longo["rotulo_conta_original"].map(_decompor_coluna_contabil)
    longo["estagio"] = decomposicao.map(lambda item: item[0])
    longo["codigo_conta"] = decomposicao.map(lambda item: item[1])
    longo["descricao_conta"] = decomposicao.map(lambda item: item[2])
    longo.insert(0, "bloco", bloco)
    longo.insert(1, "aba_origem", nome_aba)
    longo["ordem_linha_origem"] = longo.groupby(identificadores, dropna=False).cumcount() + 1

    colunas_saida = [
        "bloco",
        "aba_origem",
        *identificadores,
        "estagio",
        "codigo_conta",
        "descricao_conta",
        "rotulo_conta_original",
        "valor",
        "valor_original",
        "ordem_linha_origem",
    ]
    longo = longo[colunas_saida]
    caminho_saida = pasta_saida / f"{bloco}_longo.parquet"
    longo.to_parquet(caminho_saida, index=False)

    anos = []
    if "ano" in longo.columns:
        anos = sorted(int(valor) for valor in longo["ano"].dropna().unique())
    municipios = int(longo["municipio"].nunique()) if "municipio" in longo.columns else None
    codigos = int(longo["codigo_ibge"].nunique()) if "codigo_ibge" in longo.columns else None

    return ResultadoNormalizacaoAba(
        aba_origem=nome_aba,
        tipo="dados",
        arquivo_saida=str(caminho_saida),
        linhas_origem=int(quadro.shape[0]),
        colunas_origem=int(quadro.shape[1]),
        colunas_identificadoras=identificadores,
        colunas_valores=len(colunas_valores),
        celulas_candidatas=celulas_candidatas,
        valores_preservados=int(len(longo)),
        valores_ausentes_omitidos=ausentes,
        valores_nao_numericos=nao_numericos,
        anos=anos,
        municipios=municipios,
        codigos_ibge=codigos,
        alertas=alertas,
    )


def _normalizar_aba_auxiliar(
    quadro: pd.DataFrame,
    nome_aba: str,
    nome_saida: str,
    pasta_saida: Path,
) -> ResultadoNormalizacaoAba:
    mapeamento = _mapear_identificadores(list(quadro.columns))
    padronizado = _padronizar_identificadores(quadro, mapeamento)
    caminho_saida = pasta_saida / f"auxiliar_{nome_saida}.parquet"
    padronizado.to_parquet(caminho_saida, index=False)
    identificadores = [campo for campo in ("uf", "codigo_ibge", "municipio", "ano") if campo in padronizado.columns]
    anos = sorted(int(valor) for valor in padronizado["ano"].dropna().unique()) if "ano" in padronizado.columns else []
    municipios = int(padronizado["municipio"].nunique()) if "municipio" in padronizado.columns else None
    codigos = int(padronizado["codigo_ibge"].nunique()) if "codigo_ibge" in padronizado.columns else None
    return ResultadoNormalizacaoAba(
        aba_origem=nome_aba,
        tipo="auxiliar",
        arquivo_saida=str(caminho_saida),
        linhas_origem=int(quadro.shape[0]),
        colunas_origem=int(quadro.shape[1]),
        colunas_identificadoras=identificadores,
        colunas_valores=max(0, quadro.shape[1] - len(identificadores)),
        celulas_candidatas=int(quadro.shape[0] * quadro.shape[1]),
        valores_preservados=int(quadro.notna().sum().sum()),
        valores_ausentes_omitidos=int(quadro.isna().sum().sum()),
        valores_nao_numericos=0,
        anos=anos,
        municipios=municipios,
        codigos_ibge=codigos,
        alertas=[],
    )


def normalizar_arquivo_finbra(caminho: Path, pasta_saida: Path) -> ResultadoNormalizacao:
    """Normaliza as abas sem alterar o arquivo de entrada e grava Parquet por aba."""
    pasta_saida.mkdir(parents=True, exist_ok=True)
    livro = pd.ExcelFile(caminho)
    resultados: list[ResultadoNormalizacaoAba] = []

    for nome_aba in livro.sheet_names:
        quadro = pd.read_excel(livro, sheet_name=nome_aba)
        nome_normalizado = _nome_aba_normalizado(nome_aba)
        if nome_normalizado in ABAS_DADOS:
            resultados.append(
                _normalizar_aba_dados(
                    quadro,
                    nome_aba,
                    ABAS_DADOS[nome_normalizado],
                    pasta_saida,
                )
            )
        elif nome_normalizado in ABAS_AUXILIARES:
            resultados.append(
                _normalizar_aba_auxiliar(
                    quadro,
                    nome_aba,
                    ABAS_AUXILIARES[nome_normalizado],
                    pasta_saida,
                )
            )
        else:
            caminho_saida = pasta_saida / f"nao_classificada_{normalizar_texto(nome_aba)}.parquet"
            quadro.to_parquet(caminho_saida, index=False)
            resultados.append(
                ResultadoNormalizacaoAba(
                    aba_origem=nome_aba,
                    tipo="nao_classificada",
                    arquivo_saida=str(caminho_saida),
                    linhas_origem=int(quadro.shape[0]),
                    colunas_origem=int(quadro.shape[1]),
                    colunas_identificadoras=[],
                    colunas_valores=int(quadro.shape[1]),
                    celulas_candidatas=int(quadro.shape[0] * quadro.shape[1]),
                    valores_preservados=int(quadro.notna().sum().sum()),
                    valores_ausentes_omitidos=int(quadro.isna().sum().sum()),
                    valores_nao_numericos=0,
                    alertas=[{"nivel": "relevante", "mensagem": "Aba nao classificada automaticamente."}],
                )
            )

    criticos = sum(1 for aba in resultados for alerta in aba.alertas if alerta["nivel"] == "critico")
    relevantes = sum(1 for aba in resultados for alerta in aba.alertas if alerta["nivel"] == "relevante")
    status = "reprovado" if criticos else "aprovado_com_alertas" if relevantes else "aprovado"
    return ResultadoNormalizacao(
        arquivo_origem=caminho.name,
        pasta_saida=str(pasta_saida),
        abas=resultados,
        total_valores_preservados=sum(aba.valores_preservados for aba in resultados),
        total_ausentes_omitidos=sum(aba.valores_ausentes_omitidos for aba in resultados),
        total_nao_numericos=sum(aba.valores_nao_numericos for aba in resultados),
        alertas_criticos=criticos,
        alertas_relevantes=relevantes,
        status=status,
    )
