from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "data" / "catalogs"


def load(path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def test_v7_documentation_counts_and_unique_ids():
    indicators = load(CATALOG / "indicators_documentation_v7.yml")
    accounts = []
    for path in sorted(CATALOG.glob("accounts_documentation_v7_*.yml")):
        accounts.extend(load(path))

    assert len(indicators) == 25
    assert len(accounts) == 50
    assert len({x["id"] for x in indicators}) == 25
    assert len({x["id"] for x in accounts}) == 50


def test_every_indicator_has_explanatory_contract():
    indicators = load(CATALOG / "indicators_documentation_v7.yml")
    required = {
        "id", "label", "unit", "formula", "source", "period",
        "read", "limits", "inputs", "na_rule", "source_url",
    }
    for item in indicators:
        assert required.issubset(item)
        for key in required:
            assert item[key] not in (None, "")


def test_every_account_has_explanatory_contract():
    accounts = []
    for path in sorted(CATALOG.glob("accounts_documentation_v7_*.yml")):
        accounts.extend(load(path))

    required = {
        "id", "label", "group", "unit", "source", "read",
        "period", "kind", "formula", "inputs", "na_rule", "source_url",
    }
    for item in accounts:
        assert required.issubset(item)
        for key in required:
            assert item[key] not in (None, "")


def test_methodology_sections_are_publishable():
    payload = load(CATALOG / "methodology_sections_v7.yml")
    sections = payload["sections"]
    expected = {
        "ausencia",
        "valores_monetarios",
        "contas_agregacoes",
        "crosswalk",
        "indicadores_legais",
        "capag",
        "rankings_pares",
        "cobertura",
        "governanca",
    }
    assert expected == {x["secao_id"] for x in sections}
    assert all(x["corpo_markdown"].strip() for x in sections)


def test_documentation_manifest_matches_catalogs():
    manifest = load(CATALOG / "panel_v7_documentation_manifest.yml")
    indicators = load(CATALOG / "indicators_documentation_v7.yml")
    accounts = []
    for path in sorted(CATALOG.glob("accounts_documentation_v7_*.yml")):
        accounts.extend(load(path))

    assert manifest["counts"]["indicators"] == len(indicators)
    assert manifest["counts"]["accounts_and_aggregations"] == len(accounts)
