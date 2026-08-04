from pathlib import Path

import pandas as pd

from processamentos.normalizar_finbra import normalizar_arquivo_finbra


def teste_normalizacao_preserva_contas_e_separa_populacao(tmp_path: Path) -> None:
    entrada = tmp_path / "finbra_teste.xlsx"
    saida = tmp_path / "saida"

    receitas = pd.DataFrame(
        {
            "UF": ["SP", "SP"],
            "Código IBGE": [3500000, 3500001],
            "Município": ["Municipio A", "Municipio B"],
            "Ano": [2024, 2024],
            "População": [1000, 2000],
            "Receitas Realizadas | 1.1.1.2.50 - IPTU": [100.0, None],
            "Receitas Realizadas | 1.1.1.3.03 - ISS": [200.0, 300.0],
        }
    )
    cobertura = receitas[["UF", "Código IBGE", "Município", "Ano", "População"]].copy()
    dicionario = pd.DataFrame(
        {
            "Bloco": ["Receitas", "Receitas"],
            "Estágio contábil": ["Receitas Realizadas", "Receitas Realizadas"],
            "Conta/Subconta original": ["1.1.1.2.50 - IPTU", "1.1.1.3.03 - ISS"],
            "Cabeçalho na matriz": [
                "Receitas Realizadas | 1.1.1.2.50 - IPTU",
                "Receitas Realizadas | 1.1.1.3.03 - ISS",
            ],
            "Aba": ["Receitas", "Receitas"],
            "Coluna": [6, 7],
        }
    )

    with pd.ExcelWriter(entrada, engine="openpyxl") as escritor:
        cobertura.to_excel(escritor, sheet_name="Cobertura", index=False)
        receitas.to_excel(escritor, sheet_name="Receitas", index=False)
        receitas.to_excel(escritor, sheet_name="Despesas", index=False)
        receitas.to_excel(escritor, sheet_name="Despesa por função", index=False)
        dicionario.to_excel(escritor, sheet_name="Dicionário", index=False)
        pd.DataFrame({"Ano": [2024]}).to_excel(escritor, sheet_name="Fontes", index=False)
        pd.DataFrame({"Informacao": ["teste"]}).to_excel(
            escritor, sheet_name="Leia-me", index=False
        )

    resultado = normalizar_arquivo_finbra(entrada, saida)

    assert (saida / "receitas_longo.parquet").exists()
    assert (saida / "dimensao_municipio_ano.parquet").exists()

    quadro = pd.read_parquet(saida / "receitas_longo.parquet")
    dimensao = pd.read_parquet(saida / "dimensao_municipio_ano.parquet")

    assert len(quadro) == 3
    assert quadro["codigo_ibge"].str.len().eq(7).all()
    assert quadro["valor"].sum() == 600.0
    assert quadro["codigo_conta"].notna().all()
    assert quadro["estagio"].eq("Receitas Realizadas").all()
    assert quadro["origem_metadados"].eq("dicionario").all()
    assert not quadro["rotulo_conta_original"].astype(str).str.contains("Popula", case=False).any()

    assert len(dimensao) == 2
    assert dimensao["populacao"].sum() == 3000
    assert resultado.total_registros_contabeis == 9
    assert resultado.inconsistencias_populacao == 0


def teste_regra_contingencia_decompoe_codigo_e_estagio(tmp_path: Path) -> None:
    entrada = tmp_path / "finbra_sem_dicionario.xlsx"
    saida = tmp_path / "saida"
    quadro = pd.DataFrame(
        {
            "Código IBGE": [3500000],
            "Município": ["Municipio A"],
            "Ano": [2024],
            "População": [1000],
            "Despesas Empenhadas | 3.1.90.00.00 - Aplicacoes Diretas": [50.0],
        }
    )
    with pd.ExcelWriter(entrada, engine="openpyxl") as escritor:
        quadro.to_excel(escritor, sheet_name="Receitas", index=False)
        quadro.to_excel(escritor, sheet_name="Despesas", index=False)
        quadro.to_excel(escritor, sheet_name="Despesa por função", index=False)
        pd.DataFrame({"Campo": ["teste"]}).to_excel(
            escritor, sheet_name="Dicionário", index=False
        )

    resultado = normalizar_arquivo_finbra(entrada, saida)
    dados = pd.read_parquet(saida / "despesas_longo.parquet")

    assert resultado.status == "aprovado_com_alertas"
    assert dados.loc[0, "estagio"] == "Despesas Empenhadas"
    assert dados.loc[0, "codigo_conta"] == "3.1.90.00.00"
    assert dados.loc[0, "descricao_conta"] == "Aplicacoes Diretas"
    assert dados.loc[0, "origem_metadados"] == "regra_contingencia"
