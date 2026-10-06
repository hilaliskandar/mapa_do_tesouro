from pathlib import Path

import yaml

from pipeline.build.load_catalog import DEFAULT_CATALOGS, read_catalogs

ROOT = Path(__file__).resolve().parents[1]
MAPPING = ROOT / "data" / "mappings" / "base_multifuentes_v0_4.yml"


def test_mapping_references_known_sources_and_variables():
    catalog = read_catalogs(DEFAULT_CATALOGS)
    mapping = yaml.safe_load(MAPPING.read_text(encoding="utf-8"))

    source_ids = {item["fonte_id"] for item in catalog["fontes"]}
    variable_ids = {item["variavel_id"] for item in catalog["variaveis"]}

    assert mapping["source"]["source_id"] in source_ids
    assert set(mapping["variables"]).issubset(variable_ids)

    for spec in mapping["variables"].values():
        assert spec["source_id"] in source_ids
        assert spec["availability_end"] >= spec["availability_start"]
        assert spec["value_type"] in {"numeric", "text"}
        assert float(spec.get("scale", 1.0)) != 0.0


def test_mapping_preserves_expected_initial_universe():
    mapping = yaml.safe_load(MAPPING.read_text(encoding="utf-8"))
    source = mapping["source"]

    assert source["expected_rows"] == 390
    assert source["expected_municipalities"] == 30
    assert source["expected_years"] == {"start": 2013, "end": 2025}


def test_no_duplicate_source_column_for_distinct_direct_variables():
    mapping = yaml.safe_load(MAPPING.read_text(encoding="utf-8"))
    columns = [spec["column"] for spec in mapping["variables"].values()]
    assert len(columns) == len(set(columns))
