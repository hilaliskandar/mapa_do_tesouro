"""Regression checks for the historical DCA availability contract.

These tests inspect metadata only. They never fetch or modify fiscal data.
"""
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
MAPPING = ROOT / "data" / "mappings" / "base_multifuentes_sp645_2025.yml"
BUILDER = ROOT / "pipeline" / "build" / "sp645_private_input.py"


def test_2025_multisource_mapping_not_mislabelled_as_2013_history():
    mapping = yaml.safe_load(MAPPING.read_text(encoding="utf-8"))
    source = mapping["source"]
    assert source["expected_years"] == {"start": 2025, "end": 2025}
    dca_specs = {
        key: spec for key, spec in mapping["variables"].items()
        if spec["source_id"] == "SICONFI_DCA"
    }
    assert dca_specs
    assert all(spec["availability_start"] == 2025 for spec in dca_specs.values())
    assert all(spec["availability_end"] == 2025 for spec in dca_specs)


def test_private_typology_input_must_not_claim_full_dca_history():
    source = BUILDER.read_text(encoding="utf-8")
    assert "if len(hist_rows) != 3225:" in source
    assert "if years != [2021, 2022, 2023, 2024, 2025]:" in source
    assert '"expected_rows": 3225' in source
    assert '"expected_years": {"start": 2021, "end": 2025}' in source
