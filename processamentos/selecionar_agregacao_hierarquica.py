"""Selecao auditavel de registros para agregacao sem dupla contagem.

A selecao e calculada por bloco, municipio, ano, estagio e natureza da operacao.
Quando uma conta sintetica observada coincide com a soma de seus filhos diretos
observados, ela pode representar o ramo. Caso contrario, prevalecem as folhas
observadas do recorte. Nenhum valor original e alterado.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import pandas as pd

ARQUIVOS_QUALIFICADOS = {
    "receitas": "receitas_qualificado.parquet",
    "despesas": "despesas_qualificado.parquet",
    "despesa_por_funcao": "despesa_por_funcao_qualificado.parquet",
}

CHAVES_RECORTE = ["bloco", "codigo_ibge", "municipio", "ano", "estagio", "natureza_operacao"]


@dataclass
class ResultadoSelecaoBloco:
    bloco: str
    registros_avaliados: int
    registros_selecionados: int
    recortes: int
    pais_conciliados: int
    ramos_por_folhas: int
    divergencias_conciliacao: int


@dataclass
class ResultadoSelecaoHierarquica:
    pasta_qualificacao: str
    pasta_hierarquia: str
    pasta_saida: str
    blocos: list[ResultadoSelecaoBloco]
    total_registros_avaliados: int
    total_registros_selecionados: int
    total_divergencias_conciliacao: int
    arquivo_selecao_parquet: str
    arquivo_selecao_xlsx: str
    arquivo_resumo_json: str
    status: str

    def como_dicionario(self) -> dict[str, Any]:
        return asdict(self)


def _texto(valor: object, padrao: str = "nao_informado") -> str:
    if pd.isna(valor) or str(valor).strip() == "":
        return padrao
    return str(valor).strip()


def _tolerancia(valor_pai: float, soma_filhos: float) -> float:
    escala = max(abs(valor_pai), abs(soma_filhos), 1.0)
    return max(0.01, escala * 1e-8)


def _descendentes(codigo: str, filhos_por_pai: dict[str, set[str]]) -> set[str]:
    encontrados: set[str] = set()
    pilha = list(filhos_por_pai.get(codigo, set()))
    while pilha:
        atual = pilha.pop()
        if atual in encontrados:
            continue
        encontrados.add(atual)
        pilha.extend(filhos_por_pai.get(atual, set()))
    return encontrados


def _preparar_relacoes(relacoes: pd.DataFrame, bloco: str) -> tuple[dict[str, set[str]], dict[str, str]]:
    quadro = relacoes[relacoes["bloco"] == bloco].copy()
    filhos_por_pai: dict[str, set[str]] = {}
    pai_por_filho: dict[str, str] = {}
    for linha in quadro.itertuples(index=False):
        pai = str(linha.codigo_pai)
        filho = str(linha.codigo_filho)
        filhos_por_pai.setdefault(pai, set()).add(filho)
        pai_por_filho[filho] = pai
    return filhos_por_pai, pai_por_filho


def _selecionar_recorte(
    recorte: pd.DataFrame,
    filhos_por_pai: dict[str, set[str]],
    pai_por_filho: dict[str, str],
) -> pd.DataFrame:
    agregado = (
        recorte.groupby("codigo_conta", dropna=False)
        .agg(valor_recorte=("valor", "sum"), registros_origem=("valor", "size"))
        .reset_index()
    )
    agregado["codigo_conta"] = agregado["codigo_conta"].astype("string").str.strip()
    valores = dict(zip(agregado["codigo_conta"].astype(str), agregado["valor_recorte"].astype(float)))
    codigos = set(valores)

    selecionados: set[str] = set()
    regra: dict[str, str] = {}
    conciliado: dict[str, bool] = {}
    diferenca: dict[str, float] = {}

    raizes = sorted(codigo for codigo in codigos if pai_por_filho.get(codigo) not in codigos)

    def resolver(codigo: str) -> None:
        filhos_diretos = sorted(filhos_por_pai.get(codigo, set()) & codigos)
        if not filhos_diretos:
            selecionados.add(codigo)
            regra[codigo] = "folha_observada"
            conciliado[codigo] = True
            diferenca[codigo] = 0.0
            return

        valor_pai = valores[codigo]
        soma_filhos = sum(valores[filho] for filho in filhos_diretos)
        delta = valor_pai - soma_filhos
        confere = abs(delta) <= _tolerancia(valor_pai, soma_filhos)
        conciliado[codigo] = confere
        diferenca[codigo] = delta

        if confere:
            selecionados.add(codigo)
            regra[codigo] = "conta_pai_conciliada"
            return

        regra[codigo] = "descendentes_por_divergencia"
        for filho in filhos_diretos:
            resolver(filho)

    for raiz in raizes:
        resolver(raiz)

    linhas: list[dict[str, Any]] = []
    for codigo in sorted(codigos):
        descendentes_observados = _descendentes(codigo, filhos_por_pai) & codigos
        linhas.append(
            {
                "codigo_conta": codigo,
                "valor_recorte": valores[codigo],
                "registros_origem": int(
                    agregado.loc[agregado["codigo_conta"].astype(str) == codigo, "registros_origem"].iloc[0]
                ),
                "possui_descendente_no_recorte": bool(descendentes_observados),
                "quantidade_descendentes_no_recorte": len(descendentes_observados),
                "selecionado_para_agregacao": codigo in selecionados,
                "regra_selecao": regra.get(codigo, "suprimida_por_ancestral_conciliado"),
                "conciliacao_aplicavel": codigo in conciliado and bool(filhos_por_pai.get(codigo, set()) & codigos),
                "conciliado_com_filhos_diretos": conciliado.get(codigo, False),
                "diferenca_pai_menos_filhos": diferenca.get(codigo, 0.0),
            }
        )
    return pd.DataFrame(linhas)


def selecionar_agregacao_hierarquica(
    pasta_qualificacao: Path,
    pasta_hierarquia: Path,
    pasta_saida: Path,
) -> ResultadoSelecaoHierarquica:
    """Gera selecao por recorte e trilha de auditoria da regra hierarquica."""
    pasta_saida.mkdir(parents=True, exist_ok=True)
    relacoes = pd.read_parquet(pasta_hierarquia / "relacoes_pai_filho.parquet")

    quadros_saida: list[pd.DataFrame] = []
    resumos: list[ResultadoSelecaoBloco] = []

    for bloco, nome_arquivo in ARQUIVOS_QUALIFICADOS.items():
        quadro = pd.read_parquet(pasta_qualificacao / nome_arquivo).copy()
        quadro = quadro[quadro["codigo_conta"].notna()].copy()
        quadro["bloco"] = bloco
        for coluna in ["codigo_ibge", "municipio", "estagio", "natureza_operacao"]:
            if coluna not in quadro.columns:
                quadro[coluna] = "nao_informado"
            quadro[coluna] = quadro[coluna].map(_texto)

        filhos_por_pai, pai_por_filho = _preparar_relacoes(relacoes, bloco)
        resultados_recorte: list[pd.DataFrame] = []
        for chaves, recorte in quadro.groupby(CHAVES_RECORTE, dropna=False, sort=False):
            selecao = _selecionar_recorte(recorte, filhos_por_pai, pai_por_filho)
            for coluna, valor in zip(CHAVES_RECORTE, chaves):
                selecao[coluna] = valor
            resultados_recorte.append(selecao)

        saida_bloco = pd.concat(resultados_recorte, ignore_index=True) if resultados_recorte else pd.DataFrame()
        quadros_saida.append(saida_bloco)
        resumos.append(
            ResultadoSelecaoBloco(
                bloco=bloco,
                registros_avaliados=int(len(saida_bloco)),
                registros_selecionados=int(saida_bloco["selecionado_para_agregacao"].sum()) if not saida_bloco.empty else 0,
                recortes=int(saida_bloco[CHAVES_RECORTE].drop_duplicates().shape[0]) if not saida_bloco.empty else 0,
                pais_conciliados=int(
                    (saida_bloco["conciliacao_aplicavel"] & saida_bloco["conciliado_com_filhos_diretos"]).sum()
                ) if not saida_bloco.empty else 0,
                ramos_por_folhas=int((saida_bloco["regra_selecao"] == "descendentes_por_divergencia").sum()) if not saida_bloco.empty else 0,
                divergencias_conciliacao=int(
                    (saida_bloco["conciliacao_aplicavel"] & ~saida_bloco["conciliado_com_filhos_diretos"]).sum()
                ) if not saida_bloco.empty else 0,
            )
        )

    selecao_final = pd.concat(quadros_saida, ignore_index=True) if quadros_saida else pd.DataFrame()
    arquivo_parquet = pasta_saida / "selecao_agregacao_hierarquica.parquet"
    arquivo_xlsx = pasta_saida / "selecao_agregacao_hierarquica.xlsx"
    arquivo_json = pasta_saida / "resultado_selecao_hierarquica.json"

    selecao_final.to_parquet(arquivo_parquet, index=False)
    with pd.ExcelWriter(arquivo_xlsx, engine="openpyxl") as escritor:
        selecao_final.to_excel(escritor, sheet_name="Selecao", index=False)
        pd.DataFrame([asdict(item) for item in resumos]).to_excel(
            escritor, sheet_name="Resumo", index=False
        )

    total_avaliados = sum(item.registros_avaliados for item in resumos)
    total_selecionados = sum(item.registros_selecionados for item in resumos)
    total_divergencias = sum(item.divergencias_conciliacao for item in resumos)
    status = "aprovado" if total_avaliados > 0 else "reprovado"
    resultado = ResultadoSelecaoHierarquica(
        pasta_qualificacao=str(pasta_qualificacao),
        pasta_hierarquia=str(pasta_hierarquia),
        pasta_saida=str(pasta_saida),
        blocos=resumos,
        total_registros_avaliados=total_avaliados,
        total_registros_selecionados=total_selecionados,
        total_divergencias_conciliacao=total_divergencias,
        arquivo_selecao_parquet=str(arquivo_parquet),
        arquivo_selecao_xlsx=str(arquivo_xlsx),
        arquivo_resumo_json=str(arquivo_json),
        status=status,
    )
    pd.Series(resultado.como_dicionario()).to_json(arquivo_json, force_ascii=False, indent=2)
    return resultado
