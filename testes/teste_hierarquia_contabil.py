from pathlib import Path

import pandas as pd

from processamentos.construir_hierarquia_contabil import construir_hierarquia_contabil


def _quadro(bloco: str, codigos: list[object]) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "bloco": [bloco] * len(codigos),
            "codigo_conta": codigos,
            "descricao_conta": [f"Conta {i}" for i in range(len(codigos))],
            "tipo_registro": ["conta_sintetica", "conta_sintetica", "conta_terminal", "subtotal_estrutural"],
            "natureza_operacao": ["orcamentaria"] * len(codigos),
            "codigo_funcao": [pd.NA] * len(codigos),
            "codigo_subfuncao": [pd.NA] * len(codigos),
            "ano": [2023, 2023, 2024, 2024],
            "codigo_ibge": ["3500000", "3500000", "3500000", "3500000"],
            "valor": [100.0, 60.0, 40.0, 200.0],
        }
    )


def teste_constroi_catalogo_e_relacoes(tmp_path: Path) -> None:
    origem = tmp_path / "qualificacao"
    saida = tmp_path / "hierarquia"
    origem.mkdir()

    receitas = _quadro("receitas", ["1", "1.1", "1.1.1", pd.NA])
    despesas = _quadro("despesas", ["3", "3.3", "3.3.90", pd.NA])
    funcoes = _quadro("despesa_por_funcao", ["15", "15.451", "15.451.1", pd.NA])
    funcoes["codigo_funcao"] = ["15", "15", "15", pd.NA]
    funcoes["codigo_subfuncao"] = [pd.NA, "451", "451", pd.NA]

    receitas.to_parquet(origem / "receitas_qualificado.parquet", index=False)
    despesas.to_parquet(origem / "despesas_qualificado.parquet", index=False)
    funcoes.to_parquet(origem / "despesa_por_funcao_qualificado.parquet", index=False)

    resultado = construir_hierarquia_contabil(origem, saida)

    assert resultado.status == "aprovado"
    assert resultado.total_codigos_distintos == 9
    assert resultado.total_relacoes_pai_filho == 6
    assert (saida / "catalogo_contabil.parquet").exists()
    assert (saida / "catalogo_contabil.xlsx").exists()
    assert (saida / "relacoes_pai_filho.parquet").exists()
    assert (saida / "resultado_hierarquia.json").exists()

    catalogo = pd.read_parquet(saida / "catalogo_contabil.parquet")
    conta = catalogo[(catalogo["bloco"] == "receitas") & (catalogo["codigo_conta"] == "1.1")].iloc[0]
    assert conta["codigo_pai"] == "1"
    assert bool(conta["possui_filhos"])
    assert conta["classificacao_hierarquica"] == "sintetica"

    folha = catalogo[(catalogo["bloco"] == "receitas") & (catalogo["codigo_conta"] == "1.1.1")].iloc[0]
    assert bool(folha["conta_terminal_calculada"])
    assert folha["classificacao_hierarquica"] == "terminal"
