import json

from pipeline.qa.rgf02_state import build_qa


def test_build_rgf02_state_qa(tmp_path):
    acquisition = {
        "year": 2025,
        "municipalities_requested": 2,
        "observed_municipalities": 1,
        "long_rows": 3,
        "distinct_account_codes": 2,
        "failed": [],
        "long_csv_sha256": "long",
        "raw_tree_sha256": "raw",
    }
    normalized = {
        "rows": 2,
        "conflicts": [],
        "coverage": {
            "rgf02_divida_consolidada": 1,
            "rgf02_rcl_bruta": 2,
        },
        "output_sha256": "norm",
    }
    acquisition_path = tmp_path / "acquisition.json"
    normalized_path = tmp_path / "normalized.json"
    csv_path = tmp_path / "rgf02.csv"
    output = tmp_path / "qa.md"

    acquisition_path.write_text(json.dumps(acquisition), encoding="utf-8")
    normalized_path.write_text(json.dumps(normalized), encoding="utf-8")
    csv_path.write_text(
        "cod_ibge,ano,rgf02_divida_consolidada,rgf02_rcl_bruta\n"
        "3500105,2025,10,20\n"
        "3500204,2025,,30\n",
        encoding="utf-8",
    )

    result = build_qa(acquisition_path, normalized_path, csv_path, output)

    assert result["missing_by_field"]["rgf02_divida_consolidada"] == ["3500204"]
    assert result["missing_by_field"]["rgf02_rcl_bruta"] == []
    text = output.read_text(encoding="utf-8")
    assert "50.00%" in text
    assert "100.00%" in text
