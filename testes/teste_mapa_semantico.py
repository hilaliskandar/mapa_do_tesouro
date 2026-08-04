from pathlib import Path

import pandas as pd

from processamentos.construir_mapa_semantico import construir_mapa_semantico


def teste_constroi_mapa_semantico_e_preserva_pendencias(tmp_path: Path) -> None:
    pasta_selecao = tmp_path / "selecao"
    pasta_hierarquia = tmp_path / "hierarquia"
    pasta_saida = tmp_path / "mapa"
    pasta_selecao.mkdir()
    pasta_hierarquia.mkdir()

    selecao = pd.DataFrame(
        {
            "bloco": ["receitas", "despesas", "receitas"],
            "codigo_ibge": ["3500000", "3500000", "3500000"],
            "municipio": ["Municipio A"] * 3,
            "ano": [2024, 2024, 2024],
            "estagio": ["Receitas Realizadas", "Despesas Liquidadas", "Receitas Realizadas"],
            "natureza_operacao": ["orcamentaria"] * 3,
            "codigo_conta": ["1.1.1.2.50.0.1", "4.4.90.51.00", "9.9.9.9.99.9.9"],
            "valor_recorte": [100.0, 50.0, 10.0],
            "registros_origem": [1, 1, 1],
            "possui_descendente_no_recorte": [False, False, False],
            "quantidade_descendentes_no_recorte": [0, 0, 0],
            "selecionado_para_agregacao": [True, True, True],
            "regra_selecao": ["folha_observada"] * 3,
            "conciliacao_aplicavel": [False] * 3,
            "conciliado_com_filhos_diretos": [False] * 3,
            "diferenca_pai_menos_filhos": [0.0] * 3,
        }
    )
    selecao.to_parquet(pasta_selecao / "selecao_agregacao_hierarquica.parquet", index=False)

    catalogo = pd.DataFrame(
        {
            "bloco": ["receitas", "despesas", "receitas"],
            "codigo_conta": ["1.1.1.2.50.0.1", "4.4.90.51.00", "9.9.9.9.99.9.9"],
            "descricao_conta": [
                "Imposto sobre a Propriedade Predial e Territorial Urbana - Principal",
                "Obras e Instalacoes",
                "Conta desconhecida",
            ],
            "origem_no": ["observado"] * 3,
            "codigo_observado": [True] * 3,
        }
    )
    catalogo.to_parquet(pasta_hierarquia / "catalogo_contabil.parquet", index=False)

    regras = tmp_path / "regras.yaml"
    regras.write_text(
        """
versao: teste
regras:
  - id_semantico: REV_TRIB_IPTU_PRINCIPAL
    grupo_semantico: receita_tributaria
    bloco: receitas
    prioridade: 100
    confianca: alta
    descricao_contem_algum: [iptu, propriedade predial e territorial urbana]
    descricao_nao_contem: [multa, juros, divida ativa]
  - id_semantico: DESP_INVESTIMENTOS
    grupo_semantico: despesa_natureza
    bloco: despesas
    prioridade: 100
    confianca: alta
    codigo_regex: '^4\\.4(?:\\.|$)'
""".strip(),
        encoding="utf-8",
    )

    resultado = construir_mapa_semantico(
        pasta_selecao, pasta_hierarquia, regras, pasta_saida
    )

    assert resultado.status == "aprovado"
    assert resultado.total_registros_selecionados == 3
    assert resultado.total_registros_mapeados == 2
    assert resultado.total_registros_nao_mapeados == 1
    assert resultado.total_ambiguidades == 0

    registros = pd.read_parquet(pasta_saida / "registros_selecionados_semanticos.parquet")
    iptu = registros[registros["codigo_conta"] == "1.1.1.2.50.0.1"].iloc[0]
    assert iptu["id_semantico"] == "REV_TRIB_IPTU_PRINCIPAL"

    investimento = registros[registros["codigo_conta"] == "4.4.90.51.00"].iloc[0]
    assert investimento["id_semantico"] == "DESP_INVESTIMENTOS"

    desconhecida = registros[registros["codigo_conta"] == "9.9.9.9.99.9.9"].iloc[0]
    assert desconhecida["status_mapeamento"] == "nao_mapeado"
    assert (pasta_saida / "pendencias_mapa_semantico.xlsx").exists()
