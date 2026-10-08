import csv
import openpyxl

from pipeline.build.sp645_multisource_2025 import build_multisource_2025


def write_csv(path, fieldnames, rows):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def test_build_multisource_2025(tmp_path, monkeypatch):
    codes = [f"35{i:05d}" for i in range(645)]

    dca = tmp_path / "dca.csv"
    write_csv(dca, ["cod_ibge", "ano", "dca_iptu_principal"], [
        {"cod_ibge": c, "ano": 2025, "dca_iptu_principal": i}
        for i, c in enumerate(codes)
    ])
    rreo = tmp_path / "rreo.csv"
    write_csv(rreo, ["cod_ibge", "ano", "rreo_rcl_total_12m"], [
        {"cod_ibge": c, "ano": 2025, "rreo_rcl_total_12m": 10}
        for c in codes
    ])
    rgf = tmp_path / "rgf.csv"
    write_csv(rgf, ["cod_ibge", "ano", "rgf_despesa_total_pessoal"], [
        {"cod_ibge": c, "ano": 2025, "rgf_despesa_total_pessoal": 20}
        for c in codes
    ])
    rgf02 = tmp_path / "rgf02.csv"
    write_csv(rgf02, ["cod_ibge", "ano", "rgf02_divida_consolidada"], [
        {"cod_ibge": c, "ano": 2025, "rgf02_divida_consolidada": 30}
        for c in codes
    ])
    capag = tmp_path / "capag.csv"
    write_csv(capag, ["codigo_ibge", "municipio", "capag"], [
        {"codigo_ibge": c, "municipio": f"M{i}", "capag": "A"}
        for i, c in enumerate(codes)
    ])

    output = tmp_path / "base.xlsx"
    manifest = tmp_path / "manifest.json"
    result = build_multisource_2025(dca, rreo, rgf, rgf02, capag, output, manifest)

    assert result["rows"] == 645
    assert result["coverage"]["rreo_rcl_oficial"] == 645
    wb = openpyxl.load_workbook(output, read_only=True, data_only=True)
    ws = wb["Base multifuentes"]
    assert ws.max_row == 646
    wb.close()
