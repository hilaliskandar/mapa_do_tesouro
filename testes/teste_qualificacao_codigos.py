from pathlib import Path

import pandas as pd

from processamentos.qualificar_codigos import qualificar_codigos


def _base_receitas() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "bloco": ["receitas"] * 5,
            "aba_origem": ["Receitas"] * 5,
            "codigo_ibge": ["3500000"] * 5,
            "municipio": ["Municipio A"] * 5,
            "ano": [2024] * 5,
            "estagio": ["Realizadas"] * 5,
            "codigo_conta": ["1.1.1.2.50", pd.NA, pd.NA, pd.NA, pd.NA],
            "descricao_conta": [
                "IPTU",
                "Total das Receitas",
                "Descricao sem codigo",
                "1.7.2.8.01.1.0 Cota-Parte do ICMS",
                "7.2.1.5.01.0.0 Contribuicao patronal intraorcamentaria",
            ],
            "rotulo_conta_original": [
                "Realizadas | 1.1.1.2.50 - IPTU",
                "Total das Receitas",
                "Descricao sem codigo",
                "Realizadas | 1.7.2.8.01.1.0 Cota-Parte do ICMS",
                "Realizadas | 7.2.1.5.01.0.0 Contribuicao patronal intraorcamentaria",
            ],
            "origem_metadados": ["dicionario"] * 5,
            "valor": [100.0, 300.0, 50.0, 200.0, 80.0],
            "valor_original": [100.0, 300.0, 50.0, 200.0, 80.0],
        }
    )


def teste_qualificacao_separa_pendencias_e_funcao(tmp_path: Path) -> None:
    origem = tmp_path / "normalizacao"
    saida = tmp_path / "qualificacao"
    origem.mkdir()

    receitas = _base_receitas()
    receitas.to_parquet(origem / "receitas_longo.parquet", index=False)

    despesas = receitas.assign(
        bloco="despesas",
        aba_origem="Despesas",
        codigo_conta=["3.3.90.30.00", pd.NA, pd.NA, "3.3.91.39.00", pd.NA],
        descricao_conta=[
            "Material de Consumo",
            "Total das Despesas",
            "Descricao sem codigo",
            "Outros Servicos de Terceiros",
            "Descricao sem codigo 2",
        ],
        rotulo_conta_original=[
            "Empenhadas | 3.3.90.30.00 - Material de Consumo",
            "Total das Despesas",
            "Descricao sem codigo",
            "Empenhadas | 3.3.91.39.00 - Outros Servicos de Terceiros",
            "Descricao sem codigo 2",
        ],
    )
    despesas.to_parquet(origem / "despesas_longo.parquet", index=False)

    funcao = receitas.assign(
        bloco="despesa_por_funcao",
        aba_origem="Despesa por funcao",
        codigo_conta=["15.451", pd.NA, pd.NA, pd.NA, pd.NA],
        descricao_conta=[
            "Infraestrutura Urbana",
            "Total da Funcao",
            "Descricao sem codigo",
            "FU12 - Demais Subfuncoes",
            "26.782 Transporte Rodoviario",
        ],
        rotulo_conta_original=[
            "Empenhadas | 15.451 - Infraestrutura Urbana",
            "Total da Funcao",
            "Descricao sem codigo",
            "Empenhadas | FU12 - Demais Subfuncoes",
            "Empenhadas | 26.782 Transporte Rodoviario",
        ],
    )
    funcao.to_parquet(origem / "despesa_por_funcao_longo.parquet", index=False)

    resultado = qualificar_codigos(origem, saida)

    assert resultado.status == "revisao_necessaria"
    assert (saida / "pendencias_codigos_conta.xlsx").exists()

    quadro_receitas = pd.read_parquet(saida / "receitas_qualificado.parquet")
    assert quadro_receitas.loc[3, "codigo_conta"] == "1.7.2.8.01.1.0"
    assert quadro_receitas.loc[3, "origem_codigo_qualificado"] == "extraido_do_texto"
    assert quadro_receitas.loc[4, "natureza_operacao"] == "intraorcamentaria"

    quadro_despesas = pd.read_parquet(saida / "despesas_qualificado.parquet")
    assert quadro_despesas.loc[3, "natureza_operacao"] == "intraorcamentaria"

    quadro_funcao = pd.read_parquet(saida / "despesa_por_funcao_qualificado.parquet")
    assert quadro_funcao.loc[0, "codigo_funcao"] == "15"
    assert quadro_funcao.loc[0, "codigo_subfuncao"] == "451"
    assert quadro_funcao.loc[1, "tipo_registro"] == "total_ou_subtotal"
    assert not bool(quadro_funcao.loc[1, "pendencia_revisao"])
    assert quadro_funcao.loc[3, "codigo_funcao"] == "12"
    assert pd.isna(quadro_funcao.loc[3, "codigo_subfuncao"])
    assert quadro_funcao.loc[3, "tipo_registro"] == "agregado_funcional_residual"
    assert not bool(quadro_funcao.loc[3, "pendencia_revisao"])
    assert quadro_funcao.loc[4, "codigo_conta"] == "26.782"
    assert quadro_funcao.loc[4, "codigo_funcao"] == "26"
    assert quadro_funcao.loc[4, "codigo_subfuncao"] == "782"
