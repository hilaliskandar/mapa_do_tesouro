from pathlib import Path

import pandas as pd

from processamentos.selecionar_agregacao_hierarquica import (
    selecionar_agregacao_hierarquica,
)


def _base(bloco: str, codigos: list[str], valores: list[float]) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "bloco": [bloco] * len(codigos),
            "codigo_conta": codigos,
            "codigo_ibge": ["3500000"] * len(codigos),
            "municipio": ["Municipio Teste"] * len(codigos),
            "ano": [2024] * len(codigos),
            "estagio": ["realizada" if bloco == "receitas" else "liquidada"] * len(codigos),
            "natureza_operacao": ["orcamentaria"] * len(codigos),
            "valor": valores,
        }
    )


def teste_separa_totalizacao_de_decomposicao(tmp_path: Path) -> None:
    qualificacao = tmp_path / "qualificacao"
    hierarquia = tmp_path / "hierarquia"
    saida = tmp_path / "selecao"
    qualificacao.mkdir()
    hierarquia.mkdir()

    receitas = _base(
        "receitas",
        ["1.0.0.0.00.0.0", "1.1.0.0.00.0.0", "1.2.0.0.00.0.0"],
        [100.0, 60.0, 40.0],
    )
    despesas = _base("despesas", ["3", "3.1", "3.3"], [120.0, 50.0, 60.0])
    funcoes = _base("despesa_por_funcao", ["15", "15.451"], [30.0, 30.0])

    receitas.to_parquet(qualificacao / "receitas_qualificado.parquet", index=False)
    despesas.to_parquet(qualificacao / "despesas_qualificado.parquet", index=False)
    funcoes.to_parquet(qualificacao / "despesa_por_funcao_qualificado.parquet", index=False)

    relacoes = pd.DataFrame(
        [
            ["receitas", "1.0.0.0.00.0.0", "1.1.0.0.00.0.0"],
            ["receitas", "1.0.0.0.00.0.0", "1.2.0.0.00.0.0"],
            ["despesas", "3", "3.1"],
            ["despesas", "3", "3.3"],
            ["despesa_por_funcao", "15", "15.451"],
        ],
        columns=["bloco", "codigo_pai", "codigo_filho"],
    )
    relacoes.to_parquet(hierarquia / "relacoes_pai_filho.parquet", index=False)

    resultado = selecionar_agregacao_hierarquica(qualificacao, hierarquia, saida)

    assert resultado.status == "aprovado"
    assert (saida / "selecao_totalizacao.parquet").exists()
    assert (saida / "selecao_decomposicao.parquet").exists()
    assert (saida / "conciliacao_hierarquica.parquet").exists()
    assert (saida / "selecao_hierarquica.xlsx").exists()

    totalizacao = pd.read_parquet(saida / "selecao_totalizacao.parquet")
    decomposicao = pd.read_parquet(saida / "selecao_decomposicao.parquet")

    receita_pai = totalizacao[
        (totalizacao["bloco"] == "receitas")
        & (totalizacao["codigo_conta"] == "1.0.0.0.00.0.0")
    ].iloc[0]
    assert bool(receita_pai["selecionado_para_agregacao"])
    assert receita_pai["regra_selecao"] == "conta_pai_conciliada"

    folhas_receita = decomposicao[
        (decomposicao["bloco"] == "receitas")
        & decomposicao["selecionado_para_agregacao"]
    ]["codigo_conta"].tolist()
    assert folhas_receita == ["1.1.0.0.00.0.0", "1.2.0.0.00.0.0"]

    folhas_despesa = totalizacao[
        (totalizacao["bloco"] == "despesas")
        & totalizacao["selecionado_para_agregacao"]
    ]["codigo_conta"].tolist()
    assert folhas_despesa == ["3.1", "3.3"]
