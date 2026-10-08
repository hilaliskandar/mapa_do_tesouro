from pipeline.normalize.rgf_legal import normalize_annex01, normalize_annex05


def test_annex01_exact_legal_fields():
    payload = {
        "entity_id": "3501608",
        "year": 2025,
        "items": [
            {
                "cod_conta": "DespesaComPessoalTotal",
                "conta": "DESPESA TOTAL COM PESSOAL - DTP (VI) = (IIIa + IIIb)",
                "coluna": "Valor",
                "valor": 533730391.12,
            },
            {
                "cod_conta": "ReceitaCorrenteLiquidaAjustada",
                "conta": "= RECEITA CORRENTE LÍQUIDA AJUSTADA PARA CÁLCULO DOS LIMITES DA DESPESA COM PESSOAL (V)",
                "coluna": "Valor",
                "valor": 1454899326.74,
            },
            {
                "cod_conta": "DespesaComPessoalTotal",
                "conta": "DESPESA TOTAL COM PESSOAL - DTP (VI) = (IIIa + IIIb)",
                "coluna": "% sobre a RCL Ajustada",
                "valor": 36.69,
            },
        ],
    }
    row = normalize_annex01(payload)
    assert row["rgf_despesa_total_pessoal"] == 533730391.12
    assert row["rgf_rcl_denominador_legal"] == 1454899326.74
    assert row["rgf_dtp_percentual_rcl"] == 36.69
    assert row["qa_issue_count"] == 0


def test_annex05_uses_non_linked_total_and_preserves_absence():
    payload = {
        "entity_id": "3501608",
        "year": 2025,
        "items": [
            {
                "cod_conta": "DisponibilidadeDeCaixaBruta",
                "conta": "TOTAL DOS RECURSOS NÃO VINCULADOS (I)",
                "coluna": "DISPONIBILIDADE DE CAIXA BRUTA (a)",
                "valor": 129054745.41,
            },
            {
                "cod_conta": "DisponibilidadeDeCaixaBruta",
                "conta": "TOTAL (IV) = (I + II + III)",
                "coluna": "DISPONIBILIDADE DE CAIXA BRUTA (a)",
                "valor": 217343388.04,
            },
        ],
    }
    row = normalize_annex05(payload)
    assert row["rgf_caixa_bruta_nao_vinculada"] == 129054745.41
    assert row["rgf_demais_obrigacoes_nao_vinculadas"] is None
    assert row["qa_issue_count"] == 0
