from pathlib import Path

import pandas as pd

from processamentos.construir_mapa_semantico import (
    _carregar_regras,
    _regra_corresponde,
    construir_mapa_semantico,
)


def _gravar_qualificados(pasta: Path) -> None:
    comum = {
        "codigo_ibge": ["3500000"],
        "municipio": ["Municipio A"],
        "ano": [2024],
        "estagio": ["realizada"],
        "natureza_operacao": ["orcamentaria"],
        "valor": [100.0],
        "tipo_registro": ["conta_terminal"],
    }
    pd.DataFrame({**comum, "bloco": ["receitas"], "codigo_conta": ["1.1.1.2.50.0.1"]}).to_parquet(
        pasta / "receitas_qualificado.parquet", index=False
    )
    pd.DataFrame({**comum, "bloco": ["despesas"], "codigo_conta": ["4.4.90.51.00"]}).to_parquet(
        pasta / "despesas_qualificado.parquet", index=False
    )
    pd.DataFrame(
        {**comum, "bloco": ["despesa_por_funcao"], "codigo_conta": ["10.301"]}
    ).to_parquet(pasta / "despesa_por_funcao_qualificado.parquet", index=False)


def teste_constroi_mapa_semantico_sobre_qualificados(tmp_path: Path) -> None:
    pasta_qualificacao = tmp_path / "qualificacao"
    pasta_hierarquia = tmp_path / "hierarquia"
    pasta_saida = tmp_path / "mapa"
    pasta_qualificacao.mkdir()
    pasta_hierarquia.mkdir()
    _gravar_qualificados(pasta_qualificacao)

    catalogo = pd.DataFrame(
        {
            "bloco": ["receitas", "despesas", "despesa_por_funcao"],
            "codigo_conta": ["1.1.1.2.50.0.1", "4.4.90.51.00", "10.301"],
            "descricao_conta": [
                "Imposto sobre a Propriedade Predial e Territorial Urbana - Principal",
                "Obras e Instalacoes",
                "Atencao Basica",
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
parametros:
  blocos_obrigatorios: [receitas, despesas, despesa_por_funcao]
regras:
  - id_semantico: REV_TRIB_IPTU_PRINCIPAL
    grupo_semantico: receita_tributaria
    bloco: receitas
    descricao_contem_algum: [iptu, propriedade predial e territorial urbana]
  - id_semantico: DESP_INVESTIMENTOS
    grupo_semantico: despesa_natureza
    bloco: despesas
    codigo_regex: '^4\\.4(?:\\.|$)'
  - id_semantico: FUNCAO_SAUDE
    grupo_semantico: despesa_funcional
    bloco: despesa_por_funcao
    codigo_regex: '^10(?:\\.|$)'
""".strip(),
        encoding="utf-8",
    )

    resultado = construir_mapa_semantico(
        pasta_qualificacao, pasta_hierarquia, regras, pasta_saida
    )

    assert resultado.status == "aprovado"
    assert resultado.total_registros_avaliados == 3
    assert resultado.total_registros_mapeados == 3
    assert resultado.total_registros_nao_mapeados == 0

    registros = pd.read_parquet(pasta_saida / "registros_qualificados_semanticos.parquet")
    assert registros.loc[registros["bloco"] == "receitas", "id_semantico"].iloc[0] == "REV_TRIB_IPTU_PRINCIPAL"
    assert registros.loc[registros["bloco"] == "despesas", "id_semantico"].iloc[0] == "DESP_INVESTIMENTOS"
    assert registros.loc[registros["bloco"] == "despesa_por_funcao", "id_semantico"].iloc[0] == "FUNCAO_SAUDE"
    assert (pasta_saida / "pendencias_mapa_semantico.xlsx").exists()


def teste_catalogo_nao_confunde_agregado_tributario_com_taxas() -> None:
    caminho = Path("referencias/catalogos/mapa_semantico_inicial.yaml")
    _, regras, _ = _carregar_regras(caminho)
    regra_taxas = next(regra for regra in regras if regra["id_semantico"] == "REV_TRIB_TAXAS")

    agregado = pd.Series(
        {
            "bloco": "receitas",
            "ano": 2024,
            "codigo_conta": "1.1.0.0.00.0.0",
            "descricao_conta": "Impostos, Taxas e Contribuicoes de Melhoria",
        }
    )
    taxa = pd.Series(
        {
            "bloco": "receitas",
            "ano": 2024,
            "codigo_conta": "1.1.2.0.00.0.0",
            "descricao_conta": "Taxas pelo Exercicio do Poder de Policia",
        }
    )

    assert not _regra_corresponde(agregado, regra_taxas)
    assert _regra_corresponde(taxa, regra_taxas)


def teste_catalogo_mapeia_origem_e_transferencias_prioritarias() -> None:
    caminho = Path("referencias/catalogos/mapa_semantico_inicial.yaml")
    _, regras, _ = _carregar_regras(caminho)
    por_id = {regra["id_semantico"]: regra for regra in regras}

    transferencia_corrente = pd.Series(
        {
            "bloco": "receitas",
            "ano": 2024,
            "codigo_conta": "1.7.2.1.50.0.0",
            "descricao_conta": "Cota-Parte do ICMS",
        }
    )
    operacao_credito = pd.Series(
        {
            "bloco": "receitas",
            "ano": 2024,
            "codigo_conta": "2.1.1.0.00.0.0",
            "descricao_conta": "Operacoes de Credito Internas",
        }
    )

    assert _regra_corresponde(
        transferencia_corrente, por_id["REV_TRANSFERENCIAS_CORRENTES"]
    )
    assert _regra_corresponde(transferencia_corrente, por_id["REV_TRANSF_ICMS"])
    assert _regra_corresponde(operacao_credito, por_id["REV_OPERACOES_CREDITO"])
