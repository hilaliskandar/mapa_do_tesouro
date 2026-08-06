"""Fechamento do mapa semantico com correcoes historicas e controles de coerencia."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from itertools import combinations
from pathlib import Path
from typing import Any
import re

import pandas as pd

ARQUIVO_ORIGEM = "registros_qualificados_semanticos.parquet"
ARQUIVO_APERFEICOADO = "registros_qualificados_semanticos_aperfeicoados.parquet"


@dataclass
class ResultadoAperfeicoamentoSemantico:
    pasta_mapa_semantico: str
    pasta_saida: str
    registros_avaliados: int
    correcoes_historicas: int
    registros_nao_mapeados: int
    incompatibilidades: int
    combinacoes_compativeis: int
    controles_tributarios: int
    arquivo_registros_aperfeicoados: str
    arquivo_compatibilidade: str
    arquivo_componentes_tributarios: str
    arquivo_consistencia_xlsx: str
    arquivo_resultado_json: str
    status: str

    @property
    def arquivo_aperfeicoado(self) -> str:
        """Alias mantido para compatibilidade com a interface 0.6.1."""
        return self.arquivo_registros_aperfeicoados

    @property
    def arquivo_matriz_compatibilidade(self) -> str:
        """Alias mantido para compatibilidade com o manifesto da interface."""
        return self.arquivo_compatibilidade

    @property
    def arquivo_relatorio_consistencia(self) -> str:
        """Alias mantido para compatibilidade com o manifesto da interface."""
        return self.arquivo_consistencia_xlsx

    def como_dicionario(self) -> dict[str, Any]:
        return asdict(self)


def _aplicar_correcoes_historicas(registros: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    quadro = registros.copy()
    codigo = quadro["codigo_conta"].astype("string").fillna("")
    mascara = (
        quadro["id_semantico"].isna()
        & quadro["bloco"].eq("receitas")
        & pd.to_numeric(quadro["ano"], errors="coerce").le(2017)
        & codigo.str.match(r"^2\.5(?:\.|$)", na=False)
    )
    quantidade = int(mascara.sum())
    if quantidade:
        quadro.loc[mascara, "id_semantico"] = "REV_OUTRAS_RECEITAS_CAPITAL"
        quadro.loc[mascara, "grupo_semantico"] = "receita_origem"
        quadro.loc[mascara, "nivel_semantico"] = "origem"
        quadro.loc[mascara, "finalidade_semantica"] = "composicao"
        quadro.loc[mascara, "confianca_mapeamento"] = "alta"
        quadro.loc[mascara, "interpretacao"] = (
            "Outras receitas de capital na classificacao historica utilizada ate 2017."
        )
        quadro.loc[mascara, "prioridade_regra"] = 110
        quadro.loc[mascara, "status_mapeamento"] = "mapeado"
        quadro.loc[mascara, "ambiguidade"] = False
        quadro.loc[mascara, "origem_ajuste_semantico"] = "regra_historica_2_5_ate_2017"
    if "origem_ajuste_semantico" not in quadro.columns:
        quadro["origem_ajuste_semantico"] = pd.NA
    return quadro, quantidade


def _matriz_compatibilidade(registros: pd.DataFrame) -> pd.DataFrame:
    mapeados = registros[registros["id_semantico"].notna()].copy()
    linhas: list[dict[str, Any]] = []
    for identificador, grupo in mapeados.groupby("id_registro_semantico", sort=False):
        conceitos = grupo[
            ["id_semantico", "grupo_semantico", "finalidade_semantica", "nivel_semantico"]
        ].drop_duplicates()
        for primeiro, segundo in combinations(conceitos.to_dict("records"), 2):
            mesmo_grupo = primeiro["grupo_semantico"] == segundo["grupo_semantico"]
            linhas.append(
                {
                    "id_registro_semantico": identificador,
                    "conceito_a": primeiro["id_semantico"],
                    "grupo_a": primeiro["grupo_semantico"],
                    "conceito_b": segundo["id_semantico"],
                    "grupo_b": segundo["grupo_semantico"],
                    "compativel": not mesmo_grupo,
                    "motivo": (
                        "grupos_semanticos_distintos"
                        if not mesmo_grupo
                        else "conceitos_concorrentes_no_mesmo_grupo"
                    ),
                }
            )
    return pd.DataFrame(linhas)


def _componentes_tributarios(registros: pd.DataFrame) -> pd.DataFrame:
    padrao = re.compile(
        r"^REV_TRIB_(IPTU|ISS|ITBI)_(PRINCIPAL|DIVIDA_ATIVA|MULTAS_JUROS|MULTAS_JUROS_DIVIDA_ATIVA)$"
    )
    quadro = registros[registros["id_semantico"].astype("string").str.match(padrao, na=False)].copy()
    if quadro.empty:
        return pd.DataFrame()
    extracao = quadro["id_semantico"].str.extract(padrao)
    quadro["tributo"] = extracao[0]
    quadro["componente"] = extracao[1]
    chaves = ["tributo", "componente", "ano", "codigo_conta", "descricao_conta"]
    return (
        quadro.groupby(chaves, dropna=False)
        .agg(
            registros=("id_registro_semantico", "nunique"),
            municipios=("codigo_ibge", "nunique"),
            valor_absoluto=("valor", lambda serie: float(pd.to_numeric(serie, errors="coerce").abs().sum())),
        )
        .reset_index()
        .sort_values(["tributo", "componente", "ano", "codigo_conta"])
    )


def aperfeicoar_mapa_semantico(
    pasta_mapa_semantico: Path,
    pasta_saida: Path | None = None,
) -> ResultadoAperfeicoamentoSemantico:
    """Aplica correcoes historicas e produz controles auditaveis de compatibilidade."""
    pasta_saida = pasta_saida or pasta_mapa_semantico
    pasta_saida.mkdir(parents=True, exist_ok=True)
    origem = pasta_mapa_semantico / ARQUIVO_ORIGEM
    registros = pd.read_parquet(origem)
    registros, correcoes = _aplicar_correcoes_historicas(registros)

    compatibilidade = _matriz_compatibilidade(registros)
    componentes = _componentes_tributarios(registros)
    nao_mapeados = int(registros[registros["id_semantico"].isna()]["id_registro_semantico"].nunique())
    incompatibilidades = int((~compatibilidade["compativel"]).sum()) if not compatibilidade.empty else 0
    compativeis = int(compatibilidade["compativel"].sum()) if not compatibilidade.empty else 0

    arquivo_registros = pasta_saida / ARQUIVO_APERFEICOADO
    arquivo_compatibilidade = pasta_saida / "matriz_compatibilidade_semantica.parquet"
    arquivo_componentes = pasta_saida / "matriz_componentes_tributarios.parquet"
    arquivo_xlsx = pasta_saida / "relatorio_consistencia_semantica.xlsx"
    arquivo_json = pasta_saida / "resultado_aperfeicoamento_semantico.json"

    registros.to_parquet(arquivo_registros, index=False)
    compatibilidade.to_parquet(arquivo_compatibilidade, index=False)
    componentes.to_parquet(arquivo_componentes, index=False)
    with pd.ExcelWriter(arquivo_xlsx, engine="openpyxl") as escritor:
        compatibilidade.to_excel(escritor, sheet_name="Compatibilidade", index=False)
        componentes.to_excel(escritor, sheet_name="Componentes tributarios", index=False)
        registros[registros["id_semantico"].isna()].to_excel(
            escritor, sheet_name="Nao mapeados", index=False
        )

    status = "aprovado"
    if incompatibilidades > 0:
        status = "reprovado"
    elif nao_mapeados > 0:
        status = "aprovado_com_alertas"

    resultado = ResultadoAperfeicoamentoSemantico(
        pasta_mapa_semantico=str(pasta_mapa_semantico),
        pasta_saida=str(pasta_saida),
        registros_avaliados=int(registros["id_registro_semantico"].nunique()),
        correcoes_historicas=correcoes,
        registros_nao_mapeados=nao_mapeados,
        incompatibilidades=incompatibilidades,
        combinacoes_compativeis=compativeis,
        controles_tributarios=int(len(componentes)),
        arquivo_registros_aperfeicoados=str(arquivo_registros),
        arquivo_compatibilidade=str(arquivo_compatibilidade),
        arquivo_componentes_tributarios=str(arquivo_componentes),
        arquivo_consistencia_xlsx=str(arquivo_xlsx),
        arquivo_resultado_json=str(arquivo_json),
        status=status,
    )
    pd.Series(resultado.como_dicionario()).to_json(arquivo_json, force_ascii=False, indent=2)
    return resultado
