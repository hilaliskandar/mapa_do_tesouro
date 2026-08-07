"""Calculo auditavel de indicadores a partir dos agregados semanticos.

O motor nao codifica formulas fiscais diretamente em Python. As definicoes ficam em
YAML versionado e informam conceitos, operacao, unidade e interpretacao. O modulo
preserva ausencias como ausencias: um componente obrigatorio faltante nao e tratado
como zero.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any
import json

import pandas as pd
import yaml

CHAVES_PAINEL = [
    "codigo_ibge",
    "municipio",
    "ano",
    "estagio",
    "natureza_operacao",
]


@dataclass
class ResultadoIndicadores:
    arquivo_catalogo: str
    versao_catalogo: str
    pasta_agregacoes: str
    pasta_saida: str
    indicadores_definidos: int
    indicadores_calculados: int
    observacoes_calculadas: int
    observacoes_incompletas: int
    municipios: int
    anos: int
    arquivo_indicadores_parquet: str
    arquivo_indicadores_xlsx: str
    arquivo_painel_parquet: str
    arquivo_cobertura_parquet: str
    arquivo_resultado_json: str
    status: str

    def como_dicionario(self) -> dict[str, Any]:
        return asdict(self)


def _carregar_catalogo(caminho: Path) -> tuple[str, list[dict[str, Any]]]:
    if not caminho.exists():
        raise FileNotFoundError(caminho)
    conteudo = yaml.safe_load(caminho.read_text(encoding="utf-8")) or {}
    indicadores = conteudo.get("indicadores", [])
    if not isinstance(indicadores, list) or not indicadores:
        raise ValueError("O catalogo de indicadores nao possui definicoes validas.")
    obrigatorios = {"id_indicador", "nome", "operacao", "unidade"}
    ids: set[str] = set()
    for indice, indicador in enumerate(indicadores, start=1):
        faltantes = obrigatorios.difference(indicador)
        if faltantes:
            raise ValueError(
                f"Indicador {indice} sem campos obrigatorios: {sorted(faltantes)}"
            )
        identificador = str(indicador["id_indicador"])
        if identificador in ids:
            raise ValueError(f"Indicador duplicado no catalogo: {identificador}")
        ids.add(identificador)
    return str(conteudo.get("versao", "nao_informada")), indicadores


def _lista(valor: object) -> list[str]:
    if valor is None:
        return []
    if isinstance(valor, list):
        return [str(item) for item in valor]
    return [str(valor)]


def _somar_componentes(
    painel: pd.DataFrame,
    conceitos: list[str],
    exigir_todos: bool = True,
) -> tuple[pd.Series, pd.Series]:
    if not conceitos:
        vazio = pd.Series(float("nan"), index=painel.index, dtype="float64")
        return vazio, pd.Series(False, index=painel.index)

    quadro = painel.reindex(columns=conceitos)
    presentes = quadro.notna()
    completo = presentes.all(axis=1) if exigir_todos else presentes.any(axis=1)
    soma = quadro.sum(axis=1, min_count=(len(conceitos) if exigir_todos else 1))
    soma = soma.where(completo)
    return soma.astype("float64"), completo


def _formula_texto(indicador: dict[str, Any]) -> str:
    operacao = str(indicador["operacao"])
    numerador = " + ".join(_lista(indicador.get("numerador"))) or "0"
    denominador = " + ".join(_lista(indicador.get("denominador"))) or "1"
    if operacao == "soma":
        return numerador
    if operacao == "razao":
        multiplicador = float(indicador.get("multiplicador", 1.0))
        sufixo = f" x {multiplicador:g}" if multiplicador != 1.0 else ""
        return f"({numerador}) / ({denominador}){sufixo}"
    if operacao == "diferenca":
        return f"({numerador}) - ({denominador})"
    raise ValueError(f"Operacao de indicador nao suportada: {operacao}")


def _calcular_indicador(
    painel: pd.DataFrame,
    indicador: dict[str, Any],
) -> pd.DataFrame:
    numerador_ids = _lista(indicador.get("numerador"))
    denominador_ids = _lista(indicador.get("denominador"))
    exigir_todos = bool(indicador.get("exigir_todos_componentes", True))

    numerador, numerador_completo = _somar_componentes(
        painel, numerador_ids, exigir_todos=exigir_todos
    )
    operacao = str(indicador["operacao"])

    if operacao == "soma":
        valor = numerador
        completo = numerador_completo
        denominador = pd.Series(float("nan"), index=painel.index, dtype="float64")
    else:
        denominador, denominador_completo = _somar_componentes(
            painel, denominador_ids, exigir_todos=exigir_todos
        )
        completo = numerador_completo & denominador_completo
        if operacao == "razao":
            multiplicador = float(indicador.get("multiplicador", 1.0))
            denominador_valido = denominador.ne(0) & denominador.notna()
            completo = completo & denominador_valido
            valor = (numerador / denominador * multiplicador).where(completo)
        elif operacao == "diferenca":
            valor = (numerador - denominador).where(completo)
        else:
            raise ValueError(f"Operacao de indicador nao suportada: {operacao}")

    resultado = painel[CHAVES_PAINEL].copy()
    resultado["id_indicador"] = str(indicador["id_indicador"])
    resultado["nome_indicador"] = str(indicador["nome"])
    resultado["grupo_indicador"] = str(indicador.get("grupo", "nao_informado"))
    resultado["unidade"] = str(indicador["unidade"])
    resultado["valor_indicador"] = pd.to_numeric(valor, errors="coerce")
    resultado["valor_numerador"] = pd.to_numeric(numerador, errors="coerce")
    resultado["valor_denominador"] = pd.to_numeric(denominador, errors="coerce")
    resultado["formula"] = _formula_texto(indicador)
    resultado["conceitos_numerador"] = ";".join(numerador_ids)
    resultado["conceitos_denominador"] = ";".join(denominador_ids)
    resultado["interpretacao"] = str(indicador.get("interpretacao", ""))
    resultado["fonte_metodologica"] = str(indicador.get("fonte_metodologica", ""))
    resultado["status_calculo"] = "calculado"
    resultado.loc[~completo, "status_calculo"] = "dados_insuficientes"
    return resultado


def calcular_indicadores(
    pasta_agregacoes: Path,
    arquivo_catalogo: Path,
    pasta_saida: Path,
) -> ResultadoIndicadores:
    """Calcula indicadores declarativos a partir de agregados semanticos auditados."""
    pasta_saida.mkdir(parents=True, exist_ok=True)
    versao_catalogo, definicoes = _carregar_catalogo(arquivo_catalogo)

    agregados = pd.read_parquet(pasta_agregacoes / "agregados_semanticos.parquet")
    if agregados.empty:
        raise ValueError("A base de agregados semanticos esta vazia.")

    painel = (
        agregados.pivot_table(
            index=CHAVES_PAINEL,
            columns="id_semantico",
            values="valor_nominal",
            aggfunc="sum",
            dropna=False,
        )
        .reset_index()
    )
    painel.columns.name = None

    quadros = [_calcular_indicador(painel, indicador) for indicador in definicoes]
    indicadores = pd.concat(quadros, ignore_index=True)

    calculados = indicadores[indicadores["status_calculo"] == "calculado"].copy()
    painel_indicadores = (
        calculados.pivot_table(
            index=CHAVES_PAINEL,
            columns="id_indicador",
            values="valor_indicador",
            aggfunc="first",
        )
        .reset_index()
        if not calculados.empty
        else pd.DataFrame(columns=CHAVES_PAINEL)
    )
    painel_indicadores.columns.name = None

    cobertura = (
        indicadores.groupby(["id_indicador", "nome_indicador", "grupo_indicador"], dropna=False)
        .agg(
            observacoes=("status_calculo", "size"),
            calculadas=("status_calculo", lambda serie: int((serie == "calculado").sum())),
            incompletas=(
                "status_calculo",
                lambda serie: int((serie == "dados_insuficientes").sum()),
            ),
            municipios_calculados=(
                "codigo_ibge",
                lambda serie: int(
                    indicadores.loc[
                        serie.index[indicadores.loc[serie.index, "status_calculo"].eq("calculado")],
                        "codigo_ibge",
                    ].nunique()
                ),
            ),
        )
        .reset_index()
    )
    cobertura["cobertura"] = cobertura["calculadas"] / cobertura["observacoes"].where(
        cobertura["observacoes"].ne(0)
    )

    arquivo_indicadores_parquet = pasta_saida / "indicadores.parquet"
    arquivo_indicadores_xlsx = pasta_saida / "indicadores.xlsx"
    arquivo_painel = pasta_saida / "painel_indicadores_municipio_ano.parquet"
    arquivo_cobertura = pasta_saida / "cobertura_indicadores.parquet"
    arquivo_resultado = pasta_saida / "resultado_indicadores.json"

    indicadores.to_parquet(arquivo_indicadores_parquet, index=False)
    painel_indicadores.to_parquet(arquivo_painel, index=False)
    cobertura.to_parquet(arquivo_cobertura, index=False)
    with pd.ExcelWriter(arquivo_indicadores_xlsx, engine="openpyxl") as escritor:
        indicadores.to_excel(escritor, sheet_name="Indicadores", index=False)
        painel_indicadores.to_excel(escritor, sheet_name="Painel", index=False)
        cobertura.to_excel(escritor, sheet_name="Cobertura", index=False)
        pd.DataFrame(definicoes).to_excel(escritor, sheet_name="Catalogo", index=False)

    indicadores_calculados = int(
        cobertura.loc[cobertura["calculadas"].gt(0), "id_indicador"].nunique()
    )
    observacoes_calculadas = int((indicadores["status_calculo"] == "calculado").sum())
    observacoes_incompletas = int(
        (indicadores["status_calculo"] == "dados_insuficientes").sum()
    )
    status = "aprovado"
    if indicadores_calculados == 0:
        status = "reprovado"
    elif indicadores_calculados < len(definicoes) or observacoes_incompletas > 0:
        status = "aprovado_com_alertas"

    resultado = ResultadoIndicadores(
        arquivo_catalogo=str(arquivo_catalogo),
        versao_catalogo=versao_catalogo,
        pasta_agregacoes=str(pasta_agregacoes),
        pasta_saida=str(pasta_saida),
        indicadores_definidos=len(definicoes),
        indicadores_calculados=indicadores_calculados,
        observacoes_calculadas=observacoes_calculadas,
        observacoes_incompletas=observacoes_incompletas,
        municipios=int(calculados["codigo_ibge"].nunique()) if not calculados.empty else 0,
        anos=int(calculados["ano"].nunique()) if not calculados.empty else 0,
        arquivo_indicadores_parquet=str(arquivo_indicadores_parquet),
        arquivo_indicadores_xlsx=str(arquivo_indicadores_xlsx),
        arquivo_painel_parquet=str(arquivo_painel),
        arquivo_cobertura_parquet=str(arquivo_cobertura),
        arquivo_resultado_json=str(arquivo_resultado),
        status=status,
    )
    arquivo_resultado.write_text(
        json.dumps(resultado.como_dicionario(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return resultado
