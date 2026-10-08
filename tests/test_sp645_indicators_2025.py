import openpyxl

from pipeline.transform.sp645_indicators_2025 import calculate_row, calculate_workbook


def test_calculate_row_preserves_strict_territorial_absence():
    row = {
        "dca_receita_corrente_bruta": 1000,
        "dca_receita_tributaria_bruta": 200,
        "dca_iptu_principal": 50,
        "dca_itbi_principal": 20,
        "dca_iss_principal": 100,
        "dca_fpm_cota_mensal": 100,
        "dca_icms_cota_parte": 100,
        "dca_ipva_cota_parte": 50,
        "dca_investimentos_liquidada": 100,
        "dca_despesa_total_liquidada": 900,
        "populacao_dca": 100,
        "dca_func_urbanismo_liquidada": 10,
        "dca_func_habitacao_liquidada": None,
        "dca_func_saneamento_liquidada": 5,
        "dca_func_gestao_ambiental_liquidada": 5,
        "dca_func_transporte_liquidada": 5,
        "rgf_dtp_percentual_rcl": 40,
        "rgf02_dc_percentual_rcl": 10,
        "rgf02_dcl_percentual_rcl": 5,
        "rgf_caixa_liquida_apos_rpnp": 50,
        "rreo_rcl_oficial": 1000,
        "indicador_1": 0.1,
        "indicador_2": 0.9,
        "indicador_3": 0.2,
    }
    result = calculate_row(row)
    assert result["iptu_pc"] == 0.5
    assert result["dtp_pct_rcl"] == 40
    assert result["despesa_territorial_pct_despesa"] is None
    assert result["urbanismo_pct_territorial"] is None


def test_calculate_workbook_645_rows(tmp_path):
    source = tmp_path / "source.xlsx"
    book = openpyxl.Workbook()
    sheet = book.active
    sheet.title = "Base multifuentes"
    fields = [
        "cod_ibge", "municipio", "ano",
        "dca_receita_corrente_bruta", "dca_receita_tributaria_bruta",
        "dca_iptu_principal", "dca_itbi_principal", "dca_iss_principal",
        "dca_fpm_cota_mensal", "dca_icms_cota_parte", "dca_ipva_cota_parte",
        "dca_investimentos_liquidada", "dca_despesa_total_liquidada",
        "populacao_dca", "dca_func_urbanismo_liquidada",
        "dca_func_habitacao_liquidada", "dca_func_saneamento_liquidada",
        "dca_func_gestao_ambiental_liquidada", "dca_func_transporte_liquidada",
        "rgf_dtp_percentual_rcl", "rgf02_dc_percentual_rcl",
        "rgf02_dcl_percentual_rcl", "rgf_caixa_liquida_apos_rpnp",
        "rreo_rcl_oficial", "indicador_1", "indicador_2", "indicador_3"
    ]
    sheet.append(fields)
    for index in range(645):
        values = {
            "cod_ibge": f"{3500000 + index:07d}",
            "municipio": f"M{index}",
            "ano": 2025,
        }
        values.update({field: 1 for field in fields if field not in values})
        sheet.append([values[field] for field in fields])
    book.save(source)

    output = tmp_path / "indicators.xlsx"
    manifest = tmp_path / "manifest.json"
    result = calculate_workbook(source, output, manifest)
    assert result["rows"] == 645
    assert result["coverage"]["dtp_pct_rcl"] == 645
    assert result["coverage"]["despesa_territorial_pct_despesa"] == 645
