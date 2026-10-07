from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_dca_mapping_uses_only_budgetary_revenue_and_liquidated_expenses():
    mapping = yaml.safe_load(
        (ROOT / "data" / "mappings" / "dca_canonical_v1.yml").read_text(
            encoding="utf-8"
        )
    )
    variables = mapping["variables"]

    for variable_id, rule in variables.items():
        if rule.get("special"):
            continue
        annex = rule["annex"]
        if annex == "DCA-Anexo I-C":
            assert rule["column"] == "Receitas Brutas Realizadas"
            assert str(rule["cod_conta"]).startswith("RO")
            assert not str(rule["cod_conta"]).startswith("RI")
        elif annex in {"DCA-Anexo I-D", "DCA-Anexo I-E"}:
            assert rule["column"] == "Despesas Liquidadas"

    assert variables["dca_func_urbanismo_liquidada"]["conta_regex"].startswith("^15")
    assert variables["dca_func_habitacao_liquidada"]["conta_regex"].startswith("^16")
    assert variables["dca_func_saneamento_liquidada"]["conta_regex"].startswith("^17")
    assert variables["dca_func_gestao_ambiental_liquidada"]["conta_regex"].startswith("^18")
    assert variables["dca_func_transporte_liquidada"]["conta_regex"].startswith("^26")
