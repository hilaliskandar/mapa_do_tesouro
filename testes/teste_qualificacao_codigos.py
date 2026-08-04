from pathlib import Path

import pandas as pd

from processamentos.qualificar_codigos import qualificar_codigos


def teste_qualificacao_separa_pendencias_e_funcao(tmp_path: Path) -> None:
    origem = tmp_path / "normalizacao"
    saida = tmp_path / "qualificacao"
    origem.mkdir()

    base = pd.DataFrame(
        {
            "bloco": ["receitas", "receitas", "receitas"],
            "aba_origem": ["Receitas"] * 3,
            "codigo_ibge": ["3500000"] * 3,
            "municipio": ["Municipio A"] * 3,
            "ano": [2024] * 3,
            "estagio": ["Realizadas"] * 3,
            "codigo_conta": ["1.1.1.2.50", pd.NA, pd.NA],
            "descricao_conta": ["IPTU", "Total das Receitas", "Descricao sem codigo"],
            "rotulo_conta_original": [
                "Realizadas | 1.1.1.2.50 - IPTU",
                "Total das Receitas",
                "Descricao sem codigo",
            ],
            "origem_metadados": ["dicionario", "dicionario", "dicionario"],
            "valor": [100.0, 300.0, 50.0],
            "valor_original": [100.0, 300.0, 50.0],
        }
    )
    base.to_parquet(origem / "receitas_longo.parquet", index=False)
    base.assign(bloco="despesas", aba_origem="Despesas").to_parquet(
        origem / "despesas_longo.parquet", index=False
    )
    funcao = base.assign(
        bloco="despesa_por_funcao",
        aba_origem="Despesa por função",
        codigo_conta=["15.451", pd.NA, pd.NA],
        descricao_conta=["Infraestrutura Urbana", "Total da Funcao", "Descricao sem codigo"],
        rotulo_conta_original=[
            "Empenhadas | 15.451 - Infraestrutura Urbana",
            "Total da Funcao",
            "Descricao sem codigo",
        ],
    )
    funcao.to_parquet(origem / "despesa_por_funcao_longo.parquet", index=False)

    resultado = qualificar_codigos(origem, saida)

    assert resultado.status == "revisao_necessaria"
    assert resultado.total_registros_pendentes == 3
    assert (saida / "pendencias_codigos_conta.xlsx").exists()
    quadro_funcao = pd.read_parquet(saida / "despesa_por_funcao_qualificado.parquet")
    assert quadro_funcao.loc[0, "codigo_funcao"] == "15"
    assert quadro_funcao.loc[0, "codigo_subfuncao"] == "451"
    assert quadro_funcao.loc[1, "tipo_registro"] == "total_ou_subtotal"
    assert not bool(quadro_funcao.loc[1, "pendencia_revisao"])
