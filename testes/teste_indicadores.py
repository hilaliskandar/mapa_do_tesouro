from pathlib import Path

import pandas as pd

from processamentos.calcular_indicadores import calcular_indicadores


def teste_calcula_razoes_sem_transformar_ausencia_em_zero(tmp_path: Path) -> None:
    pasta_agregacoes = tmp_path / "agregacoes"
    pasta_saida = tmp_path / "indicadores"
    pasta_agregacoes.mkdir()

    base = pd.DataFrame(
        [
            {
                "bloco": "receitas",
                "codigo_ibge": "3500000",
                "municipio": "Municipio A",
                "ano": 2024,
                "estagio": "realizada",
                "natureza_operacao": "orcamentaria",
                "grupo_semantico": "receita_categoria",
                "id_semantico": "REV_CORRENTES_TOTAL",
                "nivel_semantico": "categoria",
                "finalidade_semantica": "totalizacao",
                "valor_nominal": 1000.0,
            },
            {
                "bloco": "receitas",
                "codigo_ibge": "3500000",
                "municipio": "Municipio A",
                "ano": 2024,
                "estagio": "realizada",
                "natureza_operacao": "orcamentaria",
                "grupo_semantico": "receita_origem",
                "id_semantico": "REV_TRIBUTARIA_TOTAL",
                "nivel_semantico": "origem",
                "finalidade_semantica": "composicao",
                "valor_nominal": 250.0,
            },
            {
                "bloco": "receitas",
                "codigo_ibge": "3500000",
                "municipio": "Municipio A",
                "ano": 2024,
                "estagio": "realizada",
                "natureza_operacao": "orcamentaria",
                "grupo_semantico": "receita_tributaria_especifica",
                "id_semantico": "REV_TRIB_IPTU_PRINCIPAL",
                "nivel_semantico": "conta_especifica",
                "finalidade_semantica": "indicador",
                "valor_nominal": 50.0,
            },
        ]
    )
    base.to_parquet(pasta_agregacoes / "agregados_semanticos.parquet", index=False)

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
  - id_indicador: IPTU
    nome: IPTU na tributaria
    grupo: composicao
    operacao: razao
    numerador: [REV_TRIB_IPTU_PRINCIPAL]
    denominador: [REV_TRIBUTARIA_TOTAL]
    multiplicador: 100
    unidade: percentual
  - id_indicador: FPM
    nome: FPM nas correntes
    grupo: dependencia
    operacao: razao
    numerador: [REV_TRANSF_FPM]
    denominador: [REV_CORRENTES_TOTAL]
    multiplicador: 100
    unidade: percentual
""".strip(),
        encoding="utf-8",
    )

    resultado = calcular_indicadores(pasta_agregacoes, catalogo, pasta_saida)

    assert resultado.status == "aprovado_com_alertas"
    assert resultado.indicadores_definidos == 3
    assert resultado.indicadores_calculados == 2

    indicadores = pd.read_parquet(pasta_saida / "indicadores.parquet")
    autonomia = indicadores.loc[indicadores["id_indicador"] == "AUTONOMIA"].iloc[0]
    iptu = indicadores.loc[indicadores["id_indicador"] == "IPTU"].iloc[0]
    fpm = indicadores.loc[indicadores["id_indicador"] == "FPM"].iloc[0]

    assert autonomia["valor_indicador"] == 25.0
    assert iptu["valor_indicador"] == 20.0
    assert fpm["status_calculo"] == "dados_insuficientes"
    assert pd.isna(fpm["valor_indicador"])


def teste_rejeita_catalogo_com_identificador_duplicado(tmp_path: Path) -> None:
    pasta_agregacoes = tmp_path / "agregacoes"
    pasta_saida = tmp_path / "saida"
    pasta_agregacoes.mkdir()
    pd.DataFrame(
        [
            {
                "bloco": "receitas",
                "codigo_ibge": "1",
                "municipio": "A",
                "ano": 2024,
                "estagio": "realizada",
                "natureza_operacao": "orcamentaria",
                "grupo_semantico": "g",
                "id_semantico": "X",
                "nivel_semantico": "n",
                "finalidade_semantica": "composicao",
                "valor_nominal": 1.0,
            }
        ]
    ).to_parquet(pasta_agregacoes / "agregados_semanticos.parquet", index=False)

    catalogo = tmp_path / "duplicado.yaml"
    catalogo.write_text(
        """
versao: teste
indicadores:
  - {id_indicador: I1, nome: Um, operacao: soma, numerador: [X], unidade: reais}
  - {id_indicador: I1, nome: Dois, operacao: soma, numerador: [X], unidade: reais}
""".strip(),
        encoding="utf-8",
    )

    try:
        calcular_indicadores(pasta_agregacoes, catalogo, pasta_saida)
    except ValueError as erro:
        assert "duplicado" in str(erro).lower()
    else:
        raise AssertionError("Catalogo duplicado deveria ser rejeitado")
