from pathlib import Path

import pandas as pd

from processamentos.agregar_conceitos_semanticos import agregar_conceitos_semanticos


def teste_agrega_por_finalidade_sem_dupla_contagem(tmp_path: Path) -> None:
    mapa = tmp_path / "mapa"
    selecao = tmp_path / "selecao"
    saida = tmp_path / "agregados"
    mapa.mkdir()
    selecao.mkdir()

    registros = pd.DataFrame(
        {
            "id_registro_semantico": [1, 2, 3, 4],
            "bloco": ["receitas", "receitas", "despesas", "despesas"],
            "codigo_ibge": ["3500000"] * 4,
            "municipio": ["Municipio A"] * 4,
            "ano": [2024] * 4,
            "estagio": ["realizada", "realizada", "liquidada", "liquidada"],
            "natureza_operacao": ["orcamentaria"] * 4,
            "codigo_conta": ["1.0", "1.1", "4.0", "4.4"],
            "descricao_conta": [
                "Receitas Correntes",
                "IPTU",
                "Despesas de Capital",
                "Investimentos",
            ],
            "valor": [100.0, 30.0, 80.0, 50.0],
            "id_semantico": [
                "REV_CORRENTES_TOTAL",
                "REV_TRIB_IPTU_PRINCIPAL",
                "DESP_CAPITAL_TOTAL",
                "DESP_INVESTIMENTOS",
            ],
            "grupo_semantico": [
                "receita_categoria",
                "receita_tributaria",
                "despesa_categoria",
                "despesa_natureza",
            ],
            "nivel_semantico": ["categoria", "conta_especifica", "categoria", "grupo"],
            "finalidade_semantica": ["totalizacao", "indicador", "totalizacao", "composicao"],
            "confianca_mapeamento": ["alta"] * 4,
            "status_mapeamento": ["mapeado"] * 4,
        }
    )
    registros.to_parquet(mapa / "registros_qualificados_semanticos.parquet", index=False)

    totalizacao = pd.DataFrame(
        {
            "bloco": ["receitas", "despesas"],
            "codigo_ibge": ["3500000"] * 2,
            "municipio": ["Municipio A"] * 2,
            "ano": [2024] * 2,
            "estagio": ["realizada", "liquidada"],
            "natureza_operacao": ["orcamentaria"] * 2,
            "codigo_conta": ["1.0", "4.0"],
        }
    )
    decomposicao = pd.DataFrame(
        {
            "bloco": ["receitas", "despesas"],
            "codigo_ibge": ["3500000"] * 2,
            "municipio": ["Municipio A"] * 2,
            "ano": [2024] * 2,
            "estagio": ["realizada", "liquidada"],
            "natureza_operacao": ["orcamentaria"] * 2,
            "codigo_conta": ["1.1", "4.4"],
        }
    )
    totalizacao.to_parquet(selecao / "selecao_totalizacao.parquet", index=False)
    decomposicao.to_parquet(selecao / "selecao_decomposicao.parquet", index=False)

    resultado = agregar_conceitos_semanticos(mapa, selecao, saida)

    assert resultado.status == "aprovado"
    assert resultado.agregados_gerados == 4
    assert resultado.conceitos_distintos == 4
    assert (saida / "agregados_semanticos.xlsx").exists()
    assert (saida / "linhagem_agregados_semanticos.parquet").exists()

    agregados = pd.read_parquet(saida / "agregados_semanticos.parquet")
    valores = dict(zip(agregados["id_semantico"], agregados["valor_nominal"]))
    assert valores["REV_CORRENTES_TOTAL"] == 100.0
    assert valores["REV_TRIB_IPTU_PRINCIPAL"] == 30.0
    assert valores["DESP_CAPITAL_TOTAL"] == 80.0
    assert valores["DESP_INVESTIMENTOS"] == 50.0

    painel = pd.read_parquet(saida / "painel_semantico_municipio_ano.parquet")
    assert "REV_TRIB_IPTU_PRINCIPAL" in painel.columns
    assert "DESP_INVESTIMENTOS" in painel.columns
