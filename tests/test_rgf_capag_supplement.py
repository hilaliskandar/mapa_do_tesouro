import csv

from openpyxl import Workbook

from pipeline.normalize.rgf_capag_supplement import build_supplement


def test_rgf_capag_supplement_is_fill_only(tmp_path):
    rgf = tmp_path / "rgf.csv"
    rgf.write_text(
        "cod_ibge,ano,rgf_caixa_bruta_nao_vinculada,"
        "rgf_demais_obrigacoes_nao_vinculadas,"
        "rgf_rp_nao_liquidados_anteriores_nao_vinculados,"
        "rgf_rp_liquidados_anteriores_nao_vinculados,"
        "rgf_rp_liquidados_exercicio_nao_vinculados\n"
        "3500105,2025,,10,,,\n"
        "3500204,2025,20,,,,\n",
        encoding="utf-8",
    )

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Datalake"
    from pipeline.normalize.rgf_capag_supplement import FIELD_HEADERS

    headers = ["ID_ENTE", *FIELD_HEADERS.values()]
    sheet.append(headers)
    sheet.append([None] * len(headers))
    sheet.append([3500105, 15, 10, 2, 3, 4])
    sheet.append([3500204, 20, 5, None, None, None])
    capag = tmp_path / "capag.xlsx"
    workbook.save(capag)

    output = tmp_path / "supplement.csv"
    manifest = tmp_path / "manifest.json"
    result = build_supplement(rgf, capag, output, manifest)

    assert result["filled_cells"] == 5
    assert result["conflicts"] == 0

    rows = list(csv.DictReader(output.open(encoding="utf-8")))
    assert rows[0]["rgf_caixa_bruta_nao_vinculada"] == "15.0"
    assert rows[0]["rgf_demais_obrigacoes_nao_vinculadas"] == ""
    assert rows[1]["rgf_caixa_bruta_nao_vinculada"] == ""
