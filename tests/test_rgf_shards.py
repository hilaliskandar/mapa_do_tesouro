import csv

from pipeline.qa.rgf_shards import combine_shards


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
