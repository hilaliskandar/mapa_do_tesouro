import csv
import json

import pytest

from pipeline.normalize.dca_delta_merge import merge_fill_only


HEADER = [
    "cod_ibge",
    "ano",
    "receita",
    "despesa",
    "qa_issue_count",
]


def _write(path, rows):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=HEADER)
        writer.writeheader()
        writer.writerows(rows)


def test_fill_only_merges_missing_cells_and_preserves_existing(tmp_path):
    base = tmp_path / "base.csv"
    delta = tmp_path / "delta.csv"
    out = tmp_path / "out.csv"
    report = tmp_path / "report.json"

    _write(
        base,
        [
            {
                "cod_ibge": "3500105",
                "ano": "2022",
                "receita": "",
                "despesa": "50",
                "qa_issue_count": "0",
            },
            {
                "cod_ibge": "3500204",
                "ano": "2022",
                "receita": "100",
                "despesa": "60",
                "qa_issue_count": "0",
            },
        ],
    )
    _write(
        delta,
        [
            {
                "cod_ibge": "3500105",
                "ano": "2022",
                "receita": "75",
                "despesa": "50.0",
                "qa_issue_count": "0",
            }
        ],
    )

    result = merge_fill_only(base, delta, out, report)
    assert result["filled_cell_count"] == 1
    assert result["conflict_count"] == 0
    assert result["filled_by_variable"] == {"receita": 1}

    with out.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert rows[0]["receita"] == "75"
    assert rows[0]["despesa"] == "50"


def test_fill_only_reports_conflict_and_keeps_base(tmp_path):
    base = tmp_path / "base.csv"
    delta = tmp_path / "delta.csv"
    out = tmp_path / "out.csv"
    report = tmp_path / "report.json"

    _write(
        base,
        [{
            "cod_ibge": "3500105",
            "ano": "2022",
            "receita": "100",
            "despesa": "50",
            "qa_issue_count": "0",
        }],
    )
    _write(
        delta,
        [{
            "cod_ibge": "3500105",
            "ano": "2022",
            "receita": "101",
            "despesa": "50",
            "qa_issue_count": "0",
        }],
    )

    with pytest.raises(RuntimeError):
        merge_fill_only(base, delta, out, report)

    payload = json.loads(report.read_text(encoding="utf-8"))
    assert payload["conflict_count"] == 1
    assert payload["conflicts"][0]["resolution"] == "base_preserved"

    with out.open(encoding="utf-8", newline="") as handle:
        row = next(csv.DictReader(handle))
    assert row["receita"] == "100"


def test_fill_only_rejects_delta_outside_base_universe(tmp_path):
    base = tmp_path / "base.csv"
    delta = tmp_path / "delta.csv"
    out = tmp_path / "out.csv"
    report = tmp_path / "report.json"

    _write(
        base,
        [{
            "cod_ibge": "3500105",
            "ano": "2022",
            "receita": "",
            "despesa": "",
            "qa_issue_count": "0",
        }],
    )
    _write(
        delta,
        [{
            "cod_ibge": "3500204",
            "ano": "2022",
            "receita": "1",
            "despesa": "2",
            "qa_issue_count": "0",
        }],
    )

    with pytest.raises(ValueError):
        merge_fill_only(base, delta, out, report)
