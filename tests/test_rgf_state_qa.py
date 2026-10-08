import json

from pipeline.qa.rgf_state import build_qa


def test_build_rgf_state_qa(tmp_path):
    manifest = {
        "year": 2025,
        "municipalities_requested": 2,
        "failed": [],
        "normalization": {
            "rows": 2,
            "issues": 0,
            "coverage": {
                "rgf_despesa_total_pessoal": 2,
                "rgf_caixa_liquida_apos_rpnp": 1,
            },
        },
        "normalized_sha256": "abc",
        "raw_tree_sha256": "def",
    }
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    csv_path = tmp_path / "rgf.csv"
    csv_path.write_text(
        "cod_ibge,ano,rgf_despesa_total_pessoal,rgf_caixa_liquida_apos_rpnp\n"
        "3500105,2025,10,5\n"
        "3500204,2025,20,\n",
        encoding="utf-8",
    )
    output = tmp_path / "qa.md"

    result = build_qa(manifest_path, csv_path, output)

    assert result["missing_by_field"]["rgf_despesa_total_pessoal"] == []
    assert result["missing_by_field"]["rgf_caixa_liquida_apos_rpnp"] == ["3500204"]
    text = output.read_text(encoding="utf-8")
    assert "100.00%" in text
    assert "50.00%" in text
