import csv
import json

import pytest

from pipeline.build.export_dca_historical_v2 import EXPECTED_VARIABLES, export_history


def fixture(tmp_path, *, duplicate=False, blank=True):
    source = tmp_path / "canonical.csv"
    fields = ["cod_ibge", "ano", *EXPECTED_VARIABLES, "qa_issue_count"]
    with source.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for year in range(2013, 2026):
            for code in ("3500001", "3500002"):
                row = {"cod_ibge": code, "ano": year, "qa_issue_count": "0"}
                row.update({key: "0" for key in EXPECTED_VARIABLES})
                if blank and year == 2013 and code == "3500001":
                    row["dca_itbi_principal"] = ""
                writer.writerow(row)
                if duplicate and year == 2025 and code == "3500002":
                    writer.writerow(row)
    return source


def test_full_grid_preserves_zero_and_absence(tmp_path):
    source = fixture(tmp_path)
    target = tmp_path / "history"
    manifest = export_history(source, target, expected_municipalities=2)
    assert manifest["municipality_year_count"] == 26
    assert manifest["variable_count"] == 26
    payload = json.loads((target / "municipalities" / "3500001.json").read_text())
    assert payload["years"]["2013"]["dca_itbi_principal"]["status"] == "ausente"
    zero = payload["years"]["2013"]["dca_iptu_principal"]
    assert zero == {"status": "observado", "value_decimal": "0"}


def test_duplicate_rejected_without_writing(tmp_path):
    source = fixture(tmp_path, duplicate=True)
    target = tmp_path / "history"
    with pytest.raises(ValueError, match="Duplicate municipality-year"):
        export_history(source, target, expected_municipalities=2)
    assert not target.exists()


def test_wrong_source_hash_rejected(tmp_path):
    source = fixture(tmp_path)
    with pytest.raises(ValueError, match="SHA-256 mismatch"):
        export_history(source, tmp_path / "history", expected_sha256="0" * 64,
                       expected_municipalities=2)
