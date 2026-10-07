from pathlib import Path

import openpyxl

from pipeline.ingest.prepare_sp645_revenue_pilot import prepare_sp645_revenue_pilot


def test_prepare_sp645_revenue_pilot_contract(tmp_path: Path):
    source = tmp_path / "source.xlsx"
    output = tmp_path / "pilot.xlsx"

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Base_Analitica"
    ws.append([
        "cod_ibge", "municipio", "ano_finbra",
        "receitas_correntes", "receita_tributaria_total",
        "iptu", "itbi", "iss", "despesa_total_empenhada",
    ])
    for code, name in (("3500001", "A"), ("3500002", "B")):
        for year in (2020, 2021, 2022, 2023):
            ws.append([code, name, year, 100, 50, 10, 20, 30, 999])
    wb.save(source)

    result = prepare_sp645_revenue_pilot(
        source, output, expected_municipalities=2
    )
    assert result["rows"] == 8
    assert result["municipalities"] == 2
    assert result["variables"] == 5

    out = openpyxl.load_workbook(output, read_only=True, data_only=True)
    try:
        headers = [cell.value for cell in out["Base multifuentes"][1]]
        assert headers == [
            "cod_ibge", "municipio", "ano",
            "sp645_receitas_correntes",
            "sp645_receita_tributaria_total",
            "sp645_iptu", "sp645_itbi", "sp645_iss",
        ]
        assert "despesa_total_empenhada" not in headers
    finally:
        out.close()
