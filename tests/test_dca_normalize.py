from pipeline.normalize.dca import normalize_bundle


MAPPING = {
    "variables": {
        "receita": {
            "annex": "DCA-Anexo I-C",
            "column": "Receitas Brutas Realizadas",
            "rotulo": "Padrão",
            "cod_conta": "RO1.0",
        },
        "urbanismo": {
            "annex": "DCA-Anexo I-E",
            "column": "Despesas Liquidadas",
            "rotulo": "Total Geral da Despesa por Função",
            "cod_conta": "TotalDespesas",
            "conta_regex": r"^15\s+-\s+",
        },
        "populacao": {"special": "population_consensus"},
    }
}


def payload(annex, items):
    return {
        "source": "SICONFI",
        "endpoint": "dca",
        "year": 2025,
        "entity_id": "3501608",
        "annex": annex,
        "items": items,
    }


def test_normalizer_selects_one_exact_row_and_function_total():
    result = normalize_bundle(
        {
            "DCA-Anexo I-C": payload(
                "DCA-Anexo I-C",
                [
                    {
                        "coluna": "Receitas Brutas Realizadas",
                        "rotulo": "Padrão",
                        "cod_conta": "RO1.0",
                        "conta": "Receitas Correntes",
                        "valor": 100.0,
                        "populacao": 200,
                    }
                ],
            ),
            "DCA-Anexo I-E": payload(
                "DCA-Anexo I-E",
                [
                    {
                        "coluna": "Despesas Liquidadas",
                        "rotulo": "Total Geral da Despesa por Função",
                        "cod_conta": "TotalDespesas",
                        "conta": "15 - Urbanismo",
                        "valor": 20.0,
                        "populacao": 200,
                    },
                    {
                        "coluna": "Despesas Liquidadas",
                        "rotulo": "Total Geral da Despesa por Função",
                        "cod_conta": "TotalDespesas",
                        "conta": "15.452 - Serviços Urbanos",
                        "valor": 18.0,
                        "populacao": 200,
                    },
                ],
            ),
        },
        mapping=MAPPING,
    )

    assert result["variables"]["receita"]["status"] == "observado"
    assert result["variables"]["receita"]["value"] == 100.0
    assert result["variables"]["urbanismo"]["status"] == "observado"
    assert result["variables"]["urbanismo"]["value"] == 20.0
    assert result["variables"]["populacao"]["value"] == 200.0
    assert result["issues"] == []


def test_normalizer_never_converts_missing_row_to_zero():
    result = normalize_bundle(
        {
            "DCA-Anexo I-C": payload(
                "DCA-Anexo I-C",
                [{"populacao": 200}],
            ),
            "DCA-Anexo I-E": payload(
                "DCA-Anexo I-E",
                [{"populacao": 200}],
            ),
        },
        mapping=MAPPING,
    )
    assert result["variables"]["receita"] == {
        "status": "ausente",
        "value": None,
        "source": {
            "annex": "DCA-Anexo I-C",
            "column": "Receitas Brutas Realizadas",
            "cod_conta": "RO1.0",
            "conta_regex": None,
        },
    }
    assert result["variables"]["urbanismo"]["status"] == "ausente"
    assert result["variables"]["urbanismo"]["value"] is None


def test_normalizer_flags_duplicate_exact_matches_for_review():
    duplicate = {
        "coluna": "Receitas Brutas Realizadas",
        "rotulo": "Padrão",
        "cod_conta": "RO1.0",
        "conta": "Receitas Correntes",
        "valor": 100.0,
        "populacao": 200,
    }
    result = normalize_bundle(
        {
            "DCA-Anexo I-C": payload(
                "DCA-Anexo I-C",
                [duplicate, dict(duplicate)],
            ),
            "DCA-Anexo I-E": payload("DCA-Anexo I-E", [{"populacao": 200}]),
        },
        mapping=MAPPING,
    )
    assert result["variables"]["receita"]["status"] == "em_revisao"
    assert result["variables"]["receita"]["value"] is None
    assert any(issue["type"] == "ambiguous_match" for issue in result["issues"])


def test_population_conflict_is_review_not_average():
    result = normalize_bundle(
        {
            "DCA-Anexo I-C": payload(
                "DCA-Anexo I-C",
                [{"populacao": 200}],
            ),
            "DCA-Anexo I-E": payload(
                "DCA-Anexo I-E",
                [{"populacao": 201}],
            ),
        },
        mapping=MAPPING,
    )
    assert result["variables"]["populacao"]["status"] == "em_revisao"
    assert result["variables"]["populacao"]["value"] is None
    assert any(issue["type"] == "population_conflict" for issue in result["issues"])
