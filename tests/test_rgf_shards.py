import csv

from pipeline.qa.rgf_shards import combine_shards, write_qa


def test_combine_rgf_shards(tmp_path):
    header = [
        "cod_ibge",
        "ano",
        "rgf_despesa_total_pessoal",
        "rgf_caixa_liquida_apos_rpnp",
        "qa_issue_count",
    ]
    for idx, rows in enumerate(
        [
            [["3500105", "2025", "10", "5", "0"]],
            [["3500204", "2025", "20", "", "0"]],
        ]
    ):
        path = tmp_path / f"part-{idx}" / f"rgf_01_05_2025_{idx}.csv"
        path.parent.mkdir(parents=True)
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(header)
            writer.writerows(rows)

    output = tmp_path / "combined.csv"
    result = combine_shards(tmp_path, output, expected_rows=2)

    assert result["shard_files"] == 2
    assert result["rows"] == 2
    assert result["issues"] == 0
    assert result["coverage"]["rgf_despesa_total_pessoal"] == 2
    assert result["coverage"]["rgf_caixa_liquida_apos_rpnp"] == 1



def test_write_rgf_shard_qa(tmp_path):
    output = tmp_path / "qa.md"
    write_qa(
        {
            "shard_files": 5,
            "rows": 645,
            "issues": 0,
            "coverage": {
                "rgf_despesa_total_pessoal": 640,
                "rgf_caixa_liquida_apos_rpnp": 600,
            },
            "sha256": "abc",
        },
        output,
        year=2025,
    )
    text = output.read_text(encoding="utf-8")
    assert "RGF SP645 shardado — 2025" in text
    assert "99.22%" in text
    assert "93.02%" in text
