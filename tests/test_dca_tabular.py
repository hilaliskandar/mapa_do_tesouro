import csv
import json

from openpyxl import Workbook

from pipeline.normalize.dca_tabular import (
    read_tabular_annex,
    normalize_tabular_files,
)


HEADER = [
    "Instituição",
    "Cod.IBGE",
    "UF",
    "População",
    "Coluna",
    "Conta",
    "Identificador da Conta",
    "Valor",
]


def _write_csv(path, annex, rows):
    with path.open("w", encoding="cp1252", newline="") as handle:
        handle.write("Exercício: 2025\n")
        handle.write("Escopo: Municípios do Estado - SP\n")
        title = {
            "I-C": "Receitas Orçamentárias",
            "I-D": "Despesas Orçamentárias",
            "I-E": "Despesas por Função",
        }[annex]
        handle.write(f"Tabela: {title} (Anexo {annex})\n")
        writer = csv.writer(handle, delimiter=";")
        writer.writerow(HEADER)
        writer.writerows(rows)


def _row(code, column, account, identifier, value, population=1000):
    return [
        f"Prefeitura {code}",
        code,
        "SP",
        population,
        column,
        account,
        identifier,
        value,
    ]


def test_read_xlsx_tabular_export(tmp_path):
    path = tmp_path / "i-c.xlsx"
    workbook = Workbook()
    ws = workbook.active
    ws.append(["Exercício: 2024"])
    ws.append(["Escopo: Municípios do Estado - SP"])
    ws.append(["Tabela: Receitas Orçamentárias (Anexo I-C)"])
    ws.append(HEADER)
    ws.append(
        _row(
            3500001,
            "Receitas Brutas Realizadas",
            "1.0.0.0.00.0.0 - Receitas Correntes",
            "siconfi-cor_RO1.0.0.0.00.0.0",
            123.45,
        )
    )
    workbook.save(path)

    result = read_tabular_annex(path)
    assert result["year"] == 2024
    assert result["annex"] == "DCA-Anexo I-C"
    assert result["codes"] == ["3500001"]
    item = result["by_code"]["3500001"][0]
    assert item["cod_conta"] == "RO1.0.0.0.00.0.0"
    assert item["rotulo"] == "Padrão"
    assert item["valor"] == 123.45


def test_normalize_tabular_csv_with_explicit_universe(tmp_path):
    i_c = tmp_path / "i-c.csv"
    i_d = tmp_path / "i-d.csv"
    i_e = tmp_path / "i-e.csv"

    _write_csv(
        i_c,
        "I-C",
        [
            _row(
                "3500001",
                "Receitas Brutas Realizadas",
                "1.0.0.0.00.0.0 - Receitas Correntes",
                "siconfi-cor_RO1.0.0.0.00.0.0",
                "100,50",
            ),
            _row(
                "3500001",
                "Receitas Brutas Realizadas",
                "1.1.0.0.00.0.0 - Impostos",
                "siconfi-cor_RO1.1.0.0.00.0.0",
                "20,25",
            ),
        ],
    )
    _write_csv(
        i_d,
        "I-D",
        [
            _row(
                "3500001",
                "Despesas Liquidadas",
                "Total Geral da Despesa",
                "siconfi-cor_TotalDespesas",
                "80,00",
            ),
            _row(
                "3500001",
                "Despesas Liquidadas",
                "3.0.00.00.00 - Despesas Correntes",
                "siconfi-cor_DO3.0.00.00.00.00",
                "70,00",
            ),
        ],
    )
    _write_csv(
        i_e,
        "I-E",
        [
            _row(
                "3500001",
                "Despesas Liquidadas",
                "10 - Saúde",
                "siconfi-cor_TotalDespesas",
                "10,00",
            ),
            _row(
                "3500001",
                "Despesas Liquidadas",
                "12 - Educação",
                "siconfi-cor_TotalDespesas",
                "15,00",
            ),
        ],
    )

    geojson = tmp_path / "sp.geojson"
    geojson.write_text(
        json.dumps(
            {
                "features": [
                    {"properties": {"id": "3500001", "name": "A"}},
                    {"properties": {"id": "3500002", "name": "B"}},
                ]
            }
        ),
        encoding="utf-8",
    )
    output = tmp_path / "normalized.csv"
    report_path = tmp_path / "report.json"

    report = normalize_tabular_files(
        [i_c, i_d, i_e],
        output,
        universe_geojson=geojson,
        report_path=report_path,
    )

    with output.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    assert len(rows) == 2
    first = rows[0]
    assert first["cod_ibge"] == "3500001"
    assert float(first["dca_receita_corrente_bruta"]) == 100.5
    assert float(first["dca_despesa_total_liquidada"]) == 80.0
    assert float(first["dca_func_saude_liquidada"]) == 10.0
    assert float(first["dca_func_educacao_liquidada"]) == 15.0

    second = rows[1]
    assert second["cod_ibge"] == "3500002"
    assert second["dca_receita_corrente_bruta"] == ""

    assert report["expected_municipalities"] == 2
    assert report["municipalities_present_all_annexes"] == 1
    assert report["coverage"]["dca_receita_corrente_bruta"]["observed"] == 1
    assert report["annexes"]["DCA-Anexo I-C"]["missing_codes"] == ["3500002"]
