import csv

import openpyxl

from pipeline.qa.rgf_history_parity import compare_history


def _candidate(path):
    fields = [
        "cod_ibge",
        "ano",
        "rgf_despesa_total_pessoal",
        "rgf_rcl_denominador_legal",
        "rgf_dtp_percentual_rcl",
        "rgf02_divida_consolidada",
        "rgf02_divida_consolidada_liquida",
        "rgf02_dc_percentual_rcl",
        "rgf02_dcl_percentual_rcl",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for year in (2023, 2024):
            writer.writerow(
                {
                    "cod_ibge": "3501608",
                    "ano": year,
                    "rgf_despesa_total_pessoal": 10,
                    "rgf_rcl_denominador_legal": 20,
                    "rgf_dtp_percentual_rcl": 50,
                    "rgf02_divida_consolidada": 30,
                    "rgf02_divida_consolidada_liquida": 25,
                    "rgf02_dc_percentual_rcl": 15,
                    "rgf02_dcl_percentual_rcl": 12.5,
                }
            )


def _a01(path):
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    for year in (2023, 2024):
        ws = wb.create_sheet(f"RGF_{year}")
        ws.append(
            [
                "ano",
                "cod_ibge",
                "municipio",
                "anexo",
                "dtp_legal",
                "rcl_legal_ajustada",
                "dtp_pct_rcl",
            ]
        )
        ws.append([year, "3501608", "Americana", "RGF-Anexo 01", 10, 20, 50])
    wb.save(path)


def _a02(path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "RGF02_LONGA"
    ws.append(
        ["ano", "cod_ibge", "municipio", "cod_conta", "conta", "coluna", "valor"]
    )
    values = {
        "DividaConsolidada": 30,
        "DividaConsolidadaLiquida": 25,
        "PercentualDaDCSobreARCL": 15,
        "PercentualDaDCLSobreARCL": 12.5,
    }
    for year in (2023, 2024):
        for code, value in values.items():
            ws.append(
                [
                    year,
                    "3501608",
                    "Americana",
                    code,
                    code,
                    "Até o 3º Quadrimestre",
                    value,
                ]
            )
    wb.save(path)


def test_history_parity_passes_equal_inputs(tmp_path):
    candidate = tmp_path / "candidate.csv"
    a01 = tmp_path / "a01.xlsx"
    a02 = tmp_path / "a02.xlsx"
    out = tmp_path / "qa.json"
    _candidate(candidate)
    _a01(a01)
    _a02(a02)

    result = compare_history(candidate, a01, a02, out)

    assert result["reference_municipalities"] == 1
    assert result["reference_keys"] == 2
    assert result["comparisons"] == 14
    assert result["mismatch_count"] == 0
    assert result["strict_pass"] is True
