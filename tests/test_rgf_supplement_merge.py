import csv

from pipeline.normalize.rgf_supplement_merge import merge_fillonly


def test_rgf_fillonly_merge(tmp_path):
    base = tmp_path / "base.csv"
    base.write_text(
        "cod_ibge,ano,a,b\n"
        "3500105,2025,,10\n"
        "3500204,2025,20,\n",
        encoding="utf-8",
    )
    supplement = tmp_path / "supplement.csv"
    supplement.write_text(
        "cod_ibge,ano,a,b,supplement_cell_count\n"
        "3500105,2025,15,,1\n"
        "3500204,2025,,,0\n",
        encoding="utf-8",
    )
    output = tmp_path / "merged.csv"
    manifest = tmp_path / "manifest.json"

    result = merge_fillonly(base, supplement, output, manifest)

    assert result["filled_cells"] == 1
    assert result["coverage_before"]["a"] == 1
    assert result["coverage_after"]["a"] == 2
    rows = list(csv.DictReader(output.open(encoding="utf-8")))
    assert rows[0]["a"] == "15"
    assert rows[0]["b"] == "10"
    assert rows[1]["a"] == "20"
