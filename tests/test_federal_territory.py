"""Testes isolados de chave municipal e semantica de recebedor."""

import pytest

from pipeline.normalize.federal_territory import match_recipient, municipal_summary


SP_CODES = {"3550308", "3543402", "3509502"}


def test_ibge_recebedor_confere_cadastro_sem_inferir_obra():
    row = {"id_proposta": 88300, "cd_ibge_recebedor": 3550308,
           "nm_municipio_recebedor": "SAO PAULO"}
    match = match_recipient(row, municipal_ibge_codes=SP_CODES)
    assert match.municipality_code == "3550308"
    assert match.status == "confirmado_recebedor"
    assert match.role == "ente_recebedor_proposta"
    assert not hasattr(match, "project_location")


@pytest.mark.parametrize("raw", [None, "", "355030", "35503080", True, 3550308.0, "3.550.308", "abc1234"])
def test_ibge_malformado_permanece_em_revisao(raw):
    match = match_recipient({"id_proposta": 1, "cd_ibge_recebedor": raw},
                            municipal_ibge_codes=SP_CODES)
    assert match.status == "em_revisao"
    assert match.municipality_code is None


def test_ibge_valido_mas_fora_do_cadastro_nao_e_recebedor_sp():
    match = match_recipient({"cd_ibge_recebedor": "3304557"},
                            municipal_ibge_codes=SP_CODES)
    assert match.status == "fora_do_universo"
    assert match.municipality_code == "3304557"


def test_nome_cidade_nao_substitui_codigo():
    row = {"nm_municipio_recebedor": "RIBEIRAO PRETO", "sg_uf_recebedor": "SP"}
    match = match_recipient(row, municipal_ibge_codes=SP_CODES)
    assert match.status == "em_revisao"


def test_quantidade_de_propostas_nao_gera_valor_financeiro():
    rows = [
        {"id_proposta": 1, "cd_ibge_recebedor": 3550308},
        {"id_proposta": 2, "cd_ibge_recebedor": 3550308},
        {"id_proposta": 3, "cd_ibge_recebedor": None},
    ]
    result = municipal_summary(rows, municipal_ibge_codes=SP_CODES)
    assert result["record_count"] == 3
    assert result["status_counts"] == {"confirmado_recebedor": 2, "em_revisao": 1}
    assert result["financial_value"] is None


def test_cadastro_deve_ser_fornecido_explicitamente():
    with pytest.raises(ValueError, match="Cadastro"):
        match_recipient({"cd_ibge_recebedor": "3550308"}, municipal_ibge_codes=set())
    with pytest.raises(ValueError, match="Cadastro"):
        match_recipient({"cd_ibge_recebedor": "3550308"}, municipal_ibge_codes={3550308})
