from pathlib import Path

import pandas as pd

from processamentos.calcular_indicadores import calcular_indicadores


def teste_indicador_ignora_estagios_e_naturezas_nao_aplicaveis(tmp_path: Path) -> None:
    pasta_agregacoes = tmp_path / "agregacoes"
    pasta_saida = tmp_path / "indicadores"
    pasta_agregacoes.mkdir()

    linhas = []
    for estagio, natureza, total, tributaria in [
        ("Receitas Brutas Realizadas", "orcamentaria", 1000.0, 200.0),
        ("Outras Deducoes da Receita", "orcamentaria", 100.0, 50.0),
        ("Receitas Brutas Realizadas", "intraorcamentaria", 300.0, 120.0),
    ]:
        for conceito, valor, grupo, finalidade in [
            ("REV_CORRENTES_TOTAL", total, "receita_categoria", "totalizacao"),
            ("REV_TRIBUTARIA_TOTAL", tributaria, "receita_origem", "composicao"),
        ]:
            linhas.append(
                {
                    "bloco": "receitas",
                    "codigo_ibge": "3500000",
                    "municipio": "Municipio A",
                    "ano": 2024,
                    "estagio": estagio,
                    "natureza_operacao": natureza,
                    "grupo_semantico": grupo,
                    "id_semantico": conceito,
                    "nivel_semantico": "categoria",
                    "finalidade_semantica": finalidade,
                    "valor_nominal": valor,
                }
            )
    pd.DataFrame(linhas).to_parquet(
        pasta_agregacoes / "agregados_semanticos.parquet", index=False
    )

    catalogo = tmp_path / "catalogo.yaml"
    catalogo.write_text(
        """
versao: teste
indicadores:
  - id_indicador: AUTONOMIA
    nome: Autonomia
    grupo: autonomia
    operacao: razao
    numerador: [REV_TRIBUTARIA_TOTAL]
    denominador: [REV_CORRENTES_TOTAL]
    multiplicador: 100
    unidade: percentual
    estagios_validos: [Receitas Brutas Realizadas]
    naturezas_validas: [orcamentaria]
""".strip(),
        encoding="utf-8",
    )

    resultado = calcular_indicadores(pasta_agregacoes, catalogo, pasta_saida)
    indicadores = pd.read_parquet(pasta_saida / "indicadores.parquet")
    cobertura = pd.read_parquet(pasta_saida / "cobertura_indicadores.parquet")

    assert resultado.observacoes_aplicaveis == 1
    assert resultado.observacoes_calculadas == 1
    assert len(indicadores) == 1
    assert indicadores.iloc[0]["valor_indicador"] == 20.0
    assert cobertura.iloc[0]["observacoes_aplicaveis"] == 1
    assert cobertura.iloc[0]["cobertura"] == 1.0
