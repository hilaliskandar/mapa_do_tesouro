import csv

from pipeline.qa.rgf_history_patch_a01 import patch_history


def test_patch_history_replaces_only_2023_a01(tmp_path):
    fields = [
        "cod_ibge",
        "ano",
        "rgf_despesa_total_pessoal",
        "rgf_rcl_denominador_legal",
        "rgf_dtp_percentual_rcl",
        "rgf02_dc_percentual_rcl",
        "qa_issue_count",
    ]
    history = tmp_path / "history.csv"
    with history.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for year in ("2023", "2024"):
            for idx in range(645):
                code = f"{3500000 + idx:07d}"
                writer.writerow(
                    {
                        "cod_ibge": code,
                        "ano": year,
                        "rgf_despesa_total_pessoal": "" if year == "2023" else "20",
                        "rgf_rcl_denominador_legal": "" if year == "2023" else "40",
                        "rgf_dtp_percentual_rcl": "" if year == "2023" else "50",
                        "rgf02_dc_percentual_rcl": "60",
                        "qa_issue_count": "0",
                    }
                )

    a01 = tmp_path / "a01.csv"
    with a01.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "cod_ibge",
                "ano",
                "rgf_despesa_total_pessoal",
                "rgf_rcl_denominador_legal",
                "rgf_dtp_percentual_rcl",
                "qa_issue_count",
            ],
        )
        writer.writeheader()
        for idx in range(645):
            code = f"{3500000 + idx:07d}"
            writer.writerow(
                {
                    "cod_ibge": code,
                    "ano": "2023",
                    "rgf_despesa_total_pessoal": "10",
                    "rgf_rcl_denominador_legal": "20",
                    "rgf_dtp_percentual_rcl": "50",
                    "qa_issue_count": "0",
                }
            )

    output = tmp_path / "out.csv"
    summary = tmp_path / "summary.json"
    result = patch_history(history, a01, output, summary)

    assert result["rows"] == 1290
    assert result["patched_2023_rows"] == 645
    assert result["coverage"]["2023"]["rgf_despesa_total_pessoal"] == 645
    assert result["coverage"]["2024"]["rgf_despesa_total_pessoal"] == 645
    assert result["coverage"]["2023"]["rgf02_dc_percentual_rcl"] == 645
