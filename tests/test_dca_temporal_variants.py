from pipeline.normalize.dca import normalize_bundle, resolve_rule_for_year


def test_temporal_rule_resolution_uses_historical_code_only_in_range():
    rule = {
        "annex": "DCA-Anexo I-C",
        "column": "Receitas Brutas Realizadas",
        "cod_conta": "RO1.1.1.2.50.0.0",
        "variants": [
            {
                "from_year": 2018,
                "to_year": 2021,
                "cod_conta": "RO1.1.1.8.01.1.0",
            }
        ],
    }
    assert resolve_rule_for_year(rule, 2021)["cod_conta"] == "RO1.1.1.8.01.1.0"
    assert resolve_rule_for_year(rule, 2022)["cod_conta"] == "RO1.1.1.2.50.0.0"
    assert resolve_rule_for_year(rule, 2017)["cod_conta"] == "RO1.1.1.2.50.0.0"


def test_normalize_bundle_applies_temporal_variant():
    mapping = {
        "variables": {
            "iptu": {
                "annex": "DCA-Anexo I-C",
                "column": "Receitas Brutas Realizadas",
                "rotulo": "Padrão",
                "cod_conta": "RO1.1.1.2.50.0.0",
                "variants": [
                    {
                        "from_year": 2018,
                        "to_year": 2021,
                        "cod_conta": "RO1.1.1.8.01.1.0",
                    }
                ],
            }
        }
    }
    payloads = {
        "DCA-Anexo I-C": {
            "entity_id": "3500001",
            "year": 2021,
            "items": [
                {
                    "coluna": "Receitas Brutas Realizadas",
                    "rotulo": "Padrão",
                    "cod_conta": "RO1.1.1.8.01.1.0",
                    "conta": "IPTU",
                    "valor": 123.45,
                }
            ],
        }
    }
    result = normalize_bundle(payloads, mapping=mapping)
    assert result["variables"]["iptu"]["status"] == "observado"
    assert result["variables"]["iptu"]["value"] == 123.45
    assert result["variables"]["iptu"]["source"]["cod_conta"] == "RO1.1.1.8.01.1.0"
