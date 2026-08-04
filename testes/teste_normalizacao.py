from pathlib import Path

import pandas as pd

from processamentos.normalizar_finbra import normalizar_arquivo_finbra


def teste_normalizacao_preserva_identificadores_e_valores(tmp_path: Path) -> None:
    entrada = tmp_path / "finbra_teste.xlsx"
    saida = tmp_path / "saida"

    receitas = pd.DataFrame(
        {
            "UF": ["SP", "SP"],
            "Código IBGE": [3500000, 3500001],
            "Município": ["Municipio A", "Municipio B"],
            "Ano": [2024, 2024],
            "Receitas Realizadas | 1.1.1.2.50 - IPTU": [100.0, None],
            "Receitas Realizadas | 1.1.1.3.03 - ISS": [200.0, 300.0],
        }
    )
    cobertura = receitas[["UF", "Código IBGE", "Município", "Ano"]].copy()

    with pd.ExcelWriter(entrada, engine="openpyxl") as escritor:
        cobertura.to_excel(escritor, sheet_name="Cobertura", index=False)
        receitas.to_excel(escritor, sheet_name="Receitas", index=False)
        receitas.to_excel(escritor, sheet_name="Despesas", index=False)
        receitas.to_excel(escritor, sheet_name="Despesa por função", index=False)
        pd.DataFrame({"Campo": ["teste"]}).to_excel(
            escritor, sheet_name="Dicionário", index=False
        )
        pd.DataFrame({"Ano": [2024]}).to_excel(
            escritor, sheet_name="Fontes", index=False
        )
        pd.DataFrame({"Informacao": ["teste"]}).to_excel(
            escritor, sheet_name="Leia-me", index=False
        )

    resultado = normalizar_arquivo_finbra(entrada, saida)

    assert resultado.status == "aprovado"
    assert (saida / "receitas_longo.parquet").exists()
    quadro = pd.read_parquet(saida / "receitas_longo.parquet")
    assert set(["codigo_ibge", "municipio", "ano", "valor"]).issubset(quadro.columns)
    assert len(quadro) == 3
    assert quadro["codigo_ibge"].str.len().eq(7).all()
    assert quadro["valor"].sum() == 600.0
