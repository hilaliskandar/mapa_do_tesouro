"""Selecao auditavel de registros por finalidade analitica.

A etapa produz duas selecoes independentes:
- totalizacao: usa conta-pai conciliada ou desce para os descendentes;
- decomposicao: preserva as folhas observadas do recorte, mesmo quando um ancestral
  conciliado poderia representar o total.

Nenhum valor original e alterado. A conciliacao fica em produto proprio para auditoria.
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
    selecionados_totalizacao: int
    selecionados_decomposicao: int
    recortes: int
    pais_conciliados: int
    divergencias_conciliacao: int


@dataclass
class ResultadoSelecaoHierarquica:
    pasta_qualificacao: str
    pasta_hierarquia: str
    pasta_saida: str
    blocos: list[ResultadoSelecaoBloco]
    total_registros_avaliados: int
    total_selecionados_totalizacao: int
    total_selecionados_decomposicao: int
    total_divergencias_conciliacao: int
    arquivo_totalizacao_parquet: str
    arquivo_decomposicao_parquet: str
    arquivo_conciliacao_parquet: str
    arquivo_selecao_xlsx: str
    arquivo_resumo_json: str
    status: str

    @property
    def total_registros_selecionados(self) -> int:
        """Compatibilidade com a versao 0.4.2."""
        return self.total_selecionados_totalizacao

    @property
    def arquivo_selecao_parquet(self) -> str:
        """Compatibilidade com a versao 0.4.2."""
        return self.arquivo_totalizacao_parquet

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


def _agregar_recorte(recorte: pd.DataFrame) -> pd.DataFrame:
    agregado = (
        recorte.groupby("codigo_conta", dropna=False)
        .agg(valor_recorte=("valor", "sum"), registros_origem=("valor", "size"))
        .reset_index()
    )
    agregado["codigo_conta"] = agregado["codigo_conta"].astype("string").str.strip()
    return agregado


def _selecionar_recorte(
    recorte: pd.DataFrame,
    filhos_por_pai: dict[str, set[str]],
    pai_por_filho: dict[str, str],
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    agregado = _agregar_recorte(recorte)
    valores = dict(zip(agregado["codigo_conta"].astype(str), agregado["valor_recorte"].astype(float)))
    frequencias = dict(zip(agregado["codigo_conta"].astype(str), agregado["registros_origem"].astype(int)))
    codigos = set(valores)

    selecionados_total: set[str] = set()
    regra_total: dict[str, str] = {}
    conciliado: dict[str, bool] = {}
    diferenca: dict[str, float] = {}
    filhos_comparados: dict[str, list[str]] = {}

    raizes = sorted(codigo for codigo in codigos if pai_por_filho.get(codigo) not in codigos)

    def resolver_totalizacao(codigo: str) -> None:
        filhos_diretos = sorted(filhos_por_pai.get(codigo, set()) & codigos)
        if not filhos_diretos:
            selecionados_total.add(codigo)
            regra_total[codigo] = "folha_observada"
            return
        valor_pai = valores[codigo]
        soma_filhos = sum(valores[filho] for filho in filhos_diretos)
        delta = valor_pai - soma_filhos
        confere = abs(delta) <= _tolerancia(valor_pai, soma_filhos)
        conciliado[codigo] = confere
        diferenca[codigo] = delta
        filhos_comparados[codigo] = filhos_diretos
        if confere:
            selecionados_total.add(codigo)
            regra_total[codigo] = "conta_pai_conciliada"
            return
        regra_total[codigo] = "descendentes_por_divergencia"
        for filho in filhos_diretos:
            resolver_totalizacao(filho)

    for raiz in raizes:
        resolver_totalizacao(raiz)

    # Decomposicao usa folhas observadas em toda a arvore, inclusive quando ha nos
    # conceituais intermediarios nao observados.
    selecionados_decomposicao = {
        codigo for codigo in codigos if not (_descendentes(codigo, filhos_por_pai) & codigos)
    }

    linhas_base: list[dict[str, Any]] = []
    for codigo in sorted(codigos):
        descendentes = _descendentes(codigo, filhos_por_pai) & codigos
        linhas_base.append(
            {
                "codigo_conta": codigo,
                "valor_recorte": valores[codigo],
                "registros_origem": frequencias[codigo],
                "possui_descendente_no_recorte": bool(descendentes),
                "quantidade_descendentes_no_recorte": len(descendentes),
            }
        )
    base = pd.DataFrame(linhas_base)

    totalizacao = base.copy()
    totalizacao["modo_selecao"] = "totalizacao"
    totalizacao["selecionado_para_agregacao"] = totalizacao["codigo_conta"].isin(selecionados_total)
    totalizacao["regra_selecao"] = totalizacao["codigo_conta"].map(regra_total).fillna(
        "suprimida_por_ancestral_conciliado"
    )

    decomposicao = base.copy()
    decomposicao["modo_selecao"] = "decomposicao"
    decomposicao["selecionado_para_agregacao"] = decomposicao["codigo_conta"].isin(
        selecionados_decomposicao
    )
    decomposicao["regra_selecao"] = decomposicao["selecionado_para_agregacao"].map(
        {True: "folha_observada_decomposicao", False: "suprimida_por_descendente_observado"}
    )

    conciliacao = pd.DataFrame(
        [
            {
                "codigo_pai": codigo,
                "valor_pai": valores[codigo],
                "filhos_diretos_observados": " | ".join(filhos_comparados[codigo]),
                "soma_filhos_diretos": valores[codigo] - diferenca[codigo],
                "diferenca_pai_menos_filhos": diferenca[codigo],
                "conciliado_com_filhos_diretos": conciliado[codigo],
            }
            for codigo in sorted(conciliado)
        ]
    )
    return totalizacao, decomposicao, conciliacao


def selecionar_agregacao_hierarquica(
    pasta_qualificacao: Path,
    pasta_hierarquia: Path,
    pasta_saida: Path,
) -> ResultadoSelecaoHierarquica:
    """Gera selecoes de totalizacao e decomposicao e trilha de conciliacao."""
    pasta_saida.mkdir(parents=True, exist_ok=True)
    relacoes = pd.read_parquet(pasta_hierarquia / "relacoes_pai_filho.parquet")

    totais: list[pd.DataFrame] = []
    decomposicoes: list[pd.DataFrame] = []
    conciliacoes: list[pd.DataFrame] = []
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
        total_bloco: list[pd.DataFrame] = []
        decomposicao_bloco: list[pd.DataFrame] = []
        conciliacao_bloco: list[pd.DataFrame] = []

        for chaves, recorte in quadro.groupby(CHAVES_RECORTE, dropna=False, sort=False):
            totalizacao, decomposicao, conciliacao = _selecionar_recorte(
                recorte, filhos_por_pai, pai_por_filho
            )
            for tabela in [totalizacao, decomposicao, conciliacao]:
                for coluna, valor in zip(CHAVES_RECORTE, chaves):
                    tabela[coluna] = valor
            total_bloco.append(totalizacao)
            decomposicao_bloco.append(decomposicao)
            if not conciliacao.empty:
                conciliacao_bloco.append(conciliacao)

        saida_total = pd.concat(total_bloco, ignore_index=True) if total_bloco else pd.DataFrame()
        saida_decomp = (
            pd.concat(decomposicao_bloco, ignore_index=True) if decomposicao_bloco else pd.DataFrame()
        )
        saida_conc = (
            pd.concat(conciliacao_bloco, ignore_index=True) if conciliacao_bloco else pd.DataFrame()
        )
        totais.append(saida_total)
        decomposicoes.append(saida_decomp)
        conciliacoes.append(saida_conc)

        divergencias = (
            int((~saida_conc["conciliado_com_filhos_diretos"]).sum())
            if not saida_conc.empty
            else 0
        )
        resumos.append(
            ResultadoSelecaoBloco(
                bloco=bloco,
                registros_avaliados=int(len(saida_total)),
                selecionados_totalizacao=int(saida_total["selecionado_para_agregacao"].sum()),
                selecionados_decomposicao=int(saida_decomp["selecionado_para_agregacao"].sum()),
                recortes=(
                    int(saida_total[CHAVES_RECORTE].drop_duplicates().shape[0])
                    if not saida_total.empty
                    else 0
                ),
                pais_conciliados=(
                    int(saida_conc["conciliado_com_filhos_diretos"].sum())
                    if not saida_conc.empty
                    else 0
                ),
                divergencias_conciliacao=divergencias,
            )
        )

    total_final = pd.concat(totais, ignore_index=True) if totais else pd.DataFrame()
    decomp_final = pd.concat(decomposicoes, ignore_index=True) if decomposicoes else pd.DataFrame()
    conc_final = pd.concat(conciliacoes, ignore_index=True) if conciliacoes else pd.DataFrame()

    arquivo_total = pasta_saida / "selecao_totalizacao.parquet"
    arquivo_decomp = pasta_saida / "selecao_decomposicao.parquet"
    arquivo_conc = pasta_saida / "conciliacao_hierarquica.parquet"
    arquivo_legado = pasta_saida / "selecao_agregacao_hierarquica.parquet"
    arquivo_xlsx = pasta_saida / "selecao_hierarquica.xlsx"
    arquivo_json = pasta_saida / "resultado_selecao_hierarquica.json"

    total_final.to_parquet(arquivo_total, index=False)
    total_final.to_parquet(arquivo_legado, index=False)
    decomp_final.to_parquet(arquivo_decomp, index=False)
    conc_final.to_parquet(arquivo_conc, index=False)
    with pd.ExcelWriter(arquivo_xlsx, engine="openpyxl") as escritor:
        total_final.to_excel(escritor, sheet_name="Totalizacao", index=False)
        decomp_final.to_excel(escritor, sheet_name="Decomposicao", index=False)
        conc_final.to_excel(escritor, sheet_name="Conciliacao", index=False)
        pd.DataFrame([asdict(item) for item in resumos]).to_excel(
            escritor, sheet_name="Resumo", index=False
        )

    resultado = ResultadoSelecaoHierarquica(
        pasta_qualificacao=str(pasta_qualificacao),
        pasta_hierarquia=str(pasta_hierarquia),
        pasta_saida=str(pasta_saida),
        blocos=resumos,
        total_registros_avaliados=sum(item.registros_avaliados for item in resumos),
        total_selecionados_totalizacao=sum(item.selecionados_totalizacao for item in resumos),
        total_selecionados_decomposicao=sum(item.selecionados_decomposicao for item in resumos),
        total_divergencias_conciliacao=sum(item.divergencias_conciliacao for item in resumos),
        arquivo_totalizacao_parquet=str(arquivo_total),
        arquivo_decomposicao_parquet=str(arquivo_decomp),
        arquivo_conciliacao_parquet=str(arquivo_conc),
        arquivo_selecao_xlsx=str(arquivo_xlsx),
        arquivo_resumo_json=str(arquivo_json),
        status="aprovado" if not total_final.empty else "reprovado",
    )
    pd.Series(resultado.como_dicionario()).to_json(arquivo_json, force_ascii=False, indent=2)
    return resultado
