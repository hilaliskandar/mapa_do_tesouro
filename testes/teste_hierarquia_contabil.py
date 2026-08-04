from pathlib import Path

import pandas as pd

from processamentos.construir_hierarquia_contabil import construir_hierarquia_contabil


def _quadro(bloco: str, codigos: list[object]) -> pd.DataFrame:
    quantidade = len(codigos)
    return pd.DataFrame(
        {
            "bloco": [bloco] * quantidade,
            "codigo_conta": codigos,
            "descricao_conta": [f"Conta {i}" for i in range(quantidade)],
            "tipo_registro": ["conta_terminal"] * quantidade,
            "natureza_operacao": ["orcamentaria"] * quantidade,
            "codigo_funcao": [pd.NA] * quantidade,
            "codigo_subfuncao": [pd.NA] * quantidade,
            "ano": [2023 + (i % 2) for i in range(quantidade)],
            "codigo_ibge": ["3500000"] * quantidade,
            "valor": [100.0 - i * 10 for i in range(quantidade)],
        }
    )


def teste_constroi_hierarquia_especifica_por_bloco(tmp_path: Path) -> None:
    origem = tmp_path / "qualificacao"
    saida = tmp_path / "hierarquia"
    origem.mkdir()

    receitas = _quadro(
        "receitas",
        [
            "1.0.0.0.00.0.0",
            "1.1.1.2.50.0.0",
            "1.1.1.2.50.0.1",
            pd.NA,
        ],
    )
    despesas = _quadro(
        "despesas",
        ["3", "3.3", "3.3.90.30.00", pd.NA],
    )
    funcoes = _quadro(
        "despesa_por_funcao",
        ["15", "15.451", "26.782", pd.NA],
    )
    funcoes["codigo_funcao"] = ["15", "15", "26", pd.NA]
    funcoes["codigo_subfuncao"] = [pd.NA, "451", "782", pd.NA]

    receitas.to_parquet(origem / "receitas_qualificado.parquet", index=False)
    despesas.to_parquet(origem / "despesas_qualificado.parquet", index=False)
    funcoes.to_parquet(origem / "despesa_por_funcao_qualificado.parquet", index=False)

    resultado = construir_hierarquia_contabil(origem, saida)

    assert resultado.status == "aprovado"
    assert resultado.total_codigos_observados == 9
    assert resultado.total_nos_conceituais_gerados > 0
    assert resultado.total_relacoes_pai_filho > 0
    assert (saida / "catalogo_contabil.parquet").exists()
    assert (saida / "catalogo_contabil.xlsx").exists()
    assert (saida / "relacoes_pai_filho.parquet").exists()
    assert (saida / "resultado_hierarquia.json").exists()

    catalogo = pd.read_parquet(saida / "catalogo_contabil.parquet")

    iptu_base = catalogo[
        (catalogo["bloco"] == "receitas")
        & (catalogo["codigo_conta"] == "1.1.1.2.50.0.0")
    ].iloc[0]
    assert iptu_base["codigo_pai"] == "1.1.1.2.00.0.0"
    assert bool(iptu_base["possui_filhos"])
    assert iptu_base["classificacao_hierarquica"] == "sintetica"

    iptu_principal = catalogo[
        (catalogo["bloco"] == "receitas")
        & (catalogo["codigo_conta"] == "1.1.1.2.50.0.1")
    ].iloc[0]
    assert iptu_principal["codigo_pai"] == "1.1.1.2.50.0.0"
    assert bool(iptu_principal["conta_terminal_calculada"])
    assert bool(iptu_principal["utilizavel_em_agregacao"])

    modalidade = catalogo[
        (catalogo["bloco"] == "despesas")
        & (catalogo["codigo_conta"] == "3.3.90")
    ].iloc[0]
    assert modalidade["origem_no"] == "conceitual_gerado"
    assert modalidade["codigo_pai"] == "3.3"
    assert bool(modalidade["possui_filhos"])

    urbanismo = catalogo[
        (catalogo["bloco"] == "despesa_por_funcao")
        & (catalogo["codigo_conta"] == "15.451")
    ].iloc[0]
    assert urbanismo["codigo_pai"] == "15"
    assert bool(urbanismo["conta_terminal_calculada"])
