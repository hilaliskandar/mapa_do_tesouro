import csv

import openpyxl

from pipeline.build.sp645_typology_input import build_typology_input


def test_build_sp645_typology_input(tmp_path):
    codes = ["3500001", "3500002"]

    dca = tmp_path / "dca.csv"
    with dca.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "cod_ibge",
                "ano",
                "receita_tributaria_pct_receita_corrente",
                "investimento_pct_receita_corrente",
                "despesa_territorial_pct_despesa",
            ],
        )
        writer.writeheader()
        for code in codes:
            for year in range(2021, 2026):
                writer.writerow(
                    {
                        "cod_ibge": code,
                        "ano": year,
                        "receita_tributaria_pct_receita_corrente": 10,
                        "investimento_pct_receita_corrente": 5,
                        "despesa_territorial_pct_despesa": "" if year < 2024 else 8,
                    }
                )

    history = tmp_path / "history.csv"
    with history.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "cod_ibge",
                "ano",
                "rgf_dtp_percentual_rcl",
                "rgf02_dc_percentual_rcl",
                "rgf02_dcl_percentual_rcl",
            ],
        )
        writer.writeheader()
        for code in codes:
            for year in (2023, 2024):
                writer.writerow(
                    {
                        "cod_ibge": code,
                        "ano": year,
                        "rgf_dtp_percentual_rcl": 40,
                        "rgf02_dc_percentual_rcl": 20,
                        "rgf02_dcl_percentual_rcl": 10,
                    }
                )

    gate_d = tmp_path / "gate_d.xlsx"
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Indicadores"
    ws.append(
        [
            "cod_ibge",
            "municipio",
            "ano",
            "dtp_pct_rcl",
            "dc_pct_rcl",
            "dcl_pct_rcl",
            "caixa_pos_rpnp_pct_rcl",
        ]
    )
    for idx, code in enumerate(codes):
        ws.append([code, f"M{idx}", 2025, 41, 21, 11, 7])
    wb.save(gate_d)

    output = tmp_path / "typology.xlsx"
    manifest = tmp_path / "manifest.json"

    result = build_typology_input(
        dca,
        history,
        gate_d,
        output,
        manifest,
        expected_municipalities=2,
    )

    assert result["rows"] == 10
    assert result["municipalities"] == 2
    assert result["municipalities_with_at_least_3_years"]["dtp_pct_rcl"] == 2
    assert result["municipalities_with_at_least_3_years"]["dc_pct_rcl"] == 2
    assert result["municipalities_with_at_least_3_years"]["caixa_pos_rpnp_pct_rcl"] == 0
