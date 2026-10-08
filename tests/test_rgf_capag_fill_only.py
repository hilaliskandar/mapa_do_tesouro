import csv

import openpyxl

from pipeline.normalize.rgf_capag_fill_only import compose_fill_only


def test_rgf_capag_fill_only(tmp_path):
    base = tmp_path / "base.csv"
    base.write_text(
        "cod_ibge,ano,rgf_caixa_bruta_nao_vinculada,rgf_demais_obrigacoes_nao_vinculadas\n"
        "3500105,2025,10,\n"
        "3500204,2025,,\n",
        encoding="utf-8",
    )

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Datalake"
    sheet.append(
        [
            "ID_ENTE",
            "2025DisponibilidadeDeCaixaBrutaDISPONIBILIDADE DE CAIXA BRUTA (a)TOTAL DOS RECURSOS NÃO VINCULADOS (I)",
            "2025DemaisObrigacoesFinanceirasDemais Obrigações Financeiras (e)TOTAL DOS RECURSOS NÃO VINCULADOS (I)",
            "2025RestosAPagarEmpenhadosENaoLiquidadosDeExerciciosAnterioresRestos a Pagar Empenhados e Não Liquidados de Exercícios Anteriores (d)TOTAL DOS RECURSOS NÃO VINCULADOS (I)",
            "2025RestosAPagarLiquidadosENaoPagosDeExerciciosAnterioresDe Exercícios Anteriores (b)TOTAL DOS RECURSOS NÃO VINCULADOS (I)",
            "2025RestosAPagarLiquidadosENaoPagosDoExercicioDo Exercício (c)TOTAL DOS RECURSOS NÃO VINCULADOS (I)",
        ]
    )
    sheet.append([3500105, 10, 5, None, None, None])
    sheet.append([3500204, 20, None, None, None, None])
    xlsx = tmp_path / "capag.xlsx"
    workbook.save(xlsx)

    output = tmp_path / "out.csv"
    manifest = tmp_path / "manifest.json"
    result = compose_fill_only(base, xlsx, output, manifest)

    rows = list(csv.DictReader(output.open(encoding="utf-8")))
    assert result["filled_by_field"]["rgf_caixa_bruta_nao_vinculada"] == 1
    assert result["filled_by_field"]["rgf_demais_obrigacoes_nao_vinculadas"] == 1
    assert result["conflicts"] == []
    assert rows[0]["rgf_caixa_bruta_nao_vinculada"] == "10"
    assert rows[0]["rgf_demais_obrigacoes_nao_vinculadas"] == "5.0"
    assert rows[1]["rgf_caixa_bruta_nao_vinculada"] == "20.0"
