from pathlib import Path

import pandas as pd

from processamentos.aperfeicoar_mapa_semantico import aperfeicoar_mapa_semantico


def teste_corrige_codigo_historico_e_valida_compatibilidade(tmp_path: Path) -> None:
    pasta = tmp_path / "mapa"
    pasta.mkdir()
    registros = pd.DataFrame(
        {
            "id_registro_semantico": [1, 2, 2, 3, 3],
            "bloco": ["receitas"] * 5,
            "codigo_ibge": ["3500000"] * 5,
            "municipio": ["Municipio A"] * 5,
            "ano": [2017, 2024, 2024, 2024, 2024],
            "estagio": ["realizada"] * 5,
            "natureza_operacao": ["orcamentaria"] * 5,
            "codigo_conta": [
                "2.5.9.0.00.00.00",
                "1.7.2.1.50.0.0",
                "1.7.2.1.50.0.0",
                "1.1.1.2.50.0.1",
                "1.1.1.2.50.0.1",
            ],
            "descricao_conta": [
                "Outras Receitas",
                "Cota-Parte do ICMS",
                "Cota-Parte do ICMS",
                "IPTU Principal",
                "IPTU Principal",
            ],
            "valor": [10.0, 100.0, 100.0, 50.0, 50.0],
            "id_semantico": [
                pd.NA,
                "REV_TRANSFERENCIAS_CORRENTES",
                "REV_TRANSF_ICMS",
                "REV_TRIB_IPTU_PRINCIPAL",
                "REV_TRIB_IPTU_DIVIDA_ATIVA",
            ],
            "grupo_semantico": [
                pd.NA,
                "receita_origem",
                "transferencias_constitucionais",
                "receita_tributaria_componente",
                "receita_tributaria_componente",
            ],
            "nivel_semantico": [pd.NA, "origem", "conta_especifica", "componente", "componente"],
            "finalidade_semantica": [pd.NA, "composicao", "indicador", "indicador", "indicador"],
            "confianca_mapeamento": [pd.NA, "alta", "alta", "alta", "alta"],
            "interpretacao": [pd.NA, "", "", "", ""],
            "prioridade_regra": [pd.NA, 100, 100, 100, 100],
            "status_mapeamento": ["nao_mapeado", "mapeado", "mapeado", "mapeado", "mapeado"],
            "ambiguidade": [False] * 5,
        }
    )
    registros.to_parquet(pasta / "registros_qualificados_semanticos.parquet", index=False)

    resultado = aperfeicoar_mapa_semantico(pasta)

    assert resultado.correcoes_historicas == 1
    assert resultado.registros_nao_mapeados == 0
    assert resultado.combinacoes_compativeis == 1
    assert resultado.incompatibilidades == 1
    assert resultado.status == "reprovado"

    corrigidos = pd.read_parquet(
        pasta / "registros_qualificados_semanticos_aperfeicoados.parquet"
    )
    historico = corrigidos[corrigidos["id_registro_semantico"] == 1].iloc[0]
    assert historico["id_semantico"] == "REV_OUTRAS_RECEITAS_CAPITAL"
    assert historico["origem_ajuste_semantico"] == "regra_historica_2_5_ate_2017"

    compatibilidade = pd.read_parquet(pasta / "matriz_compatibilidade_semantica.parquet")
    assert compatibilidade["compativel"].sum() == 1
    assert (~compatibilidade["compativel"]).sum() == 1
