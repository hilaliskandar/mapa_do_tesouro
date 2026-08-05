"""Agregacao auditavel dos conceitos semanticos por municipio e exercicio.

A etapa combina o mapa semantico com as selecoes hierarquicas adequadas a cada
finalidade. Conceitos de totalizacao usam a selecao de totalizacao; conceitos de
composicao e indicador usam a selecao de decomposicao. Cada valor agregado mantem
uma trilha de origem com codigos e identificadores dos registros utilizados.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import pandas as pd

CHAVES_RECORTE = [
    "bloco",
    "codigo_ibge",
    "municipio",
    "ano",
    "estagio",
    "natureza_operacao",
    "codigo_conta",
]

CHAVES_AGREGACAO = [
    "bloco",
    "codigo_ibge",
    "municipio",
    "ano",
    "estagio",
    "natureza_operacao",
    "grupo_semantico",
    "id_semantico",
    "nivel_semantico",
    "finalidade_semantica",
]


@dataclass
class ResultadoAgregacoesSemanticas:
    pasta_mapa_semantico: str
    pasta_selecao: str
    pasta_saida: str
    registros_semanticos_avaliados: int
    registros_semanticos_utilizados: int
    agregados_gerados: int
    conceitos_distintos: int
    municipios: int
    anos: int
    arquivo_agregados_parquet: str
    arquivo_agregados_xlsx: str
    arquivo_painel_parquet: str
    arquivo_linhagem_parquet: str
    arquivo_resultado_json: str
    status: str

    def como_dicionario(self) -> dict[str, Any]:
        return asdict(self)


def _normalizar_selecao(quadro: pd.DataFrame) -> pd.DataFrame:
    quadro = quadro.copy()
    if "selecionado_para_agregacao" in quadro.columns:
        quadro = quadro[quadro["selecionado_para_agregacao"]].copy()
    for coluna in CHAVES_RECORTE:
        if coluna not in quadro.columns:
            raise ValueError(f"Coluna obrigatoria ausente na selecao: {coluna}")
    return quadro[CHAVES_RECORTE].drop_duplicates()


def _escolher_selecao(
    registros: pd.DataFrame,
    totalizacao: pd.DataFrame,
    decomposicao: pd.DataFrame,
) -> pd.DataFrame:
    total = registros[registros["finalidade_semantica"] == "totalizacao"].copy()
    analiticos = registros[registros["finalidade_semantica"] != "totalizacao"].copy()

    total = total.merge(totalizacao.assign(_selecionado=True), on=CHAVES_RECORTE, how="inner")
    analiticos = analiticos.merge(
        decomposicao.assign(_selecionado=True), on=CHAVES_RECORTE, how="inner"
    )
    selecionados = pd.concat([total, analiticos], ignore_index=True)
    if selecionados.empty:
        return selecionados

    # Uma mesma regra pode reaparecer por correspondencias equivalentes. O valor
    # somente deve participar uma vez por registro e conceito.
    return selecionados.drop_duplicates(["id_registro_semantico", "id_semantico"])


def agregar_conceitos_semanticos(
    pasta_mapa_semantico: Path,
    pasta_selecao: Path,
    pasta_saida: Path,
) -> ResultadoAgregacoesSemanticas:
    """Gera base longa, painel largo e linhagem dos agregados semanticos."""
    pasta_saida.mkdir(parents=True, exist_ok=True)

    registros = pd.read_parquet(
        pasta_mapa_semantico / "registros_qualificados_semanticos.parquet"
    )
    registros = registros[
        registros["id_semantico"].notna() & (registros["status_mapeamento"] == "mapeado")
    ].copy()

    totalizacao = _normalizar_selecao(
        pd.read_parquet(pasta_selecao / "selecao_totalizacao.parquet")
    )
    decomposicao = _normalizar_selecao(
        pd.read_parquet(pasta_selecao / "selecao_decomposicao.parquet")
    )
    utilizados = _escolher_selecao(registros, totalizacao, decomposicao)

    if utilizados.empty:
        agregados = pd.DataFrame(columns=CHAVES_AGREGACAO + ["valor_nominal", "registros_origem"])
        linhagem = pd.DataFrame()
    else:
        utilizados["valor"] = pd.to_numeric(utilizados["valor"], errors="coerce").fillna(0.0)
        agregados = (
            utilizados.groupby(CHAVES_AGREGACAO, dropna=False)
            .agg(
                valor_nominal=("valor", "sum"),
                registros_origem=("id_registro_semantico", "nunique"),
                codigos_origem=("codigo_conta", "nunique"),
            )
            .reset_index()
        )
        agregados["id_agregado"] = range(1, len(agregados) + 1)

        chaves_linhagem = CHAVES_AGREGACAO + ["id_agregado"]
        linhagem = utilizados.merge(agregados[chaves_linhagem], on=CHAVES_AGREGACAO, how="left")
        linhagem = linhagem[
            [
                "id_agregado",
                "id_registro_semantico",
                "bloco",
                "codigo_ibge",
                "municipio",
                "ano",
                "estagio",
                "natureza_operacao",
                "id_semantico",
                "codigo_conta",
                "descricao_conta",
                "valor",
                "confianca_mapeamento",
            ]
        ].drop_duplicates()

    indices_painel = [
        "codigo_ibge",
        "municipio",
        "ano",
        "estagio",
        "natureza_operacao",
    ]
    if agregados.empty:
        painel = pd.DataFrame(columns=indices_painel)
    else:
        painel = (
            agregados.pivot_table(
                index=indices_painel,
                columns="id_semantico",
                values="valor_nominal",
                aggfunc="sum",
                fill_value=0.0,
            )
            .reset_index()
        )
        painel.columns.name = None

    arquivo_agregados_parquet = pasta_saida / "agregados_semanticos.parquet"
    arquivo_agregados_xlsx = pasta_saida / "agregados_semanticos.xlsx"
    arquivo_painel = pasta_saida / "painel_semantico_municipio_ano.parquet"
    arquivo_linhagem = pasta_saida / "linhagem_agregados_semanticos.parquet"
    arquivo_resultado = pasta_saida / "resultado_agregacoes_semanticas.json"

    agregados.to_parquet(arquivo_agregados_parquet, index=False)
    painel.to_parquet(arquivo_painel, index=False)
    linhagem.to_parquet(arquivo_linhagem, index=False)
    with pd.ExcelWriter(arquivo_agregados_xlsx, engine="openpyxl") as escritor:
        agregados.to_excel(escritor, sheet_name="Agregados", index=False)
        painel.to_excel(escritor, sheet_name="Painel", index=False)
        resumo = (
            agregados.groupby(["bloco", "grupo_semantico", "id_semantico"], dropna=False)
            .agg(
                observacoes=("id_agregado", "size"),
                municipios=("codigo_ibge", "nunique"),
                anos=("ano", "nunique"),
            )
            .reset_index()
            if not agregados.empty
            else pd.DataFrame()
        )
        resumo.to_excel(escritor, sheet_name="Resumo", index=False)

    status = "aprovado" if not agregados.empty else "reprovado"
    resultado = ResultadoAgregacoesSemanticas(
        pasta_mapa_semantico=str(pasta_mapa_semantico),
        pasta_selecao=str(pasta_selecao),
        pasta_saida=str(pasta_saida),
        registros_semanticos_avaliados=int(len(registros)),
        registros_semanticos_utilizados=int(utilizados["id_registro_semantico"].nunique())
        if not utilizados.empty
        else 0,
        agregados_gerados=int(len(agregados)),
        conceitos_distintos=int(agregados["id_semantico"].nunique()) if not agregados.empty else 0,
        municipios=int(agregados["codigo_ibge"].nunique()) if not agregados.empty else 0,
        anos=int(agregados["ano"].nunique()) if not agregados.empty else 0,
        arquivo_agregados_parquet=str(arquivo_agregados_parquet),
        arquivo_agregados_xlsx=str(arquivo_agregados_xlsx),
        arquivo_painel_parquet=str(arquivo_painel),
        arquivo_linhagem_parquet=str(arquivo_linhagem),
        arquivo_resultado_json=str(arquivo_resultado),
        status=status,
    )
    pd.Series(resultado.como_dicionario()).to_json(
        arquivo_resultado, force_ascii=False, indent=2
    )
    return resultado
