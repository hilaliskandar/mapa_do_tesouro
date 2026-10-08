import csv
import json

from openpyxl import Workbook

from pipeline.normalize.dca_revenue_supplement import (
    normalize_revenue_supplement,
)


HEADER = [
    "Ano",
    "Instituição",
    "Cod.IBGE",
    "UF",
    "População",
    "Coluna",
    "Conta",
    "Identificador da Conta",
    "Valor",
]


def _row(code, account, identifier, value, population=1000):
    return [
        2022,
        f"Prefeitura {code}",
        int(code),
        "SP",
        population,
        "Receitas Brutas Realizadas",
        account,
        identifier,
        value,
    ]


def test_normalize_revenue_supplement_outputs_full_schema(tmp_path):
    workbook = Workbook()
    ws = workbook.active
    ws.title = "2022-finbra"
    ws.append(HEADER)
    ws.append(
        _row(
            "3517802",
            "1.0.0.0.00.0.0 - Receitas Correntes",
            "siconfi-cor_RO1.0.0.0.00.0.0",
            100.0,
        )
    )
    ws.append(
        _row(
            "3517802",
            "1.1.0.0.00.0.0 - Impostos, Taxas e Contribuições",
            "siconfi-cor_RO1.1.0.0.00.0.0",
            20.0,
        )
    )
    ws.append(
        _row(
            "3517802",
            "1.1.1.2.50.0.0 - IPTU",
            "siconfi-cor_RO1.1.1.2.50.0.0",
            5.0,
        )
    )
    path = tmp_path / "receitas.xlsx"
    workbook.save(path)

    output = tmp_path / "delta.csv"
    report = tmp_path / "report.json"
    result = normalize_revenue_supplement(
        path,
        2022,
        ["3517802"],
        output,
        report,
    )

    with output.open(encoding="utf-8", newline="") as handle:
        row = next(csv.DictReader(handle))

    assert row["cod_ibge"] == "3517802"
    assert row["ano"] == "2022"
    assert float(row["dca_receita_corrente_bruta"]) == 100.0
    assert float(row["dca_receita_tributaria_bruta"]) == 20.0
    assert float(row["dca_iptu_principal"]) == 5.0
    assert row["dca_despesa_total_liquidada"] == ""
    assert float(row["populacao_dca"]) == 1000.0
    assert result["rows"] == 1
    assert result["issues"] == 0

    payload = json.loads(report.read_text(encoding="utf-8"))
    assert payload["policy"] == "local_fill_only_supplement"
    assert payload["worksheet"] == "2022-finbra"


def test_revenue_supplement_rejects_missing_requested_code(tmp_path):
    workbook = Workbook()
    ws = workbook.active
    ws.title = "2022-finbra"
    ws.append(HEADER)
    ws.append(
        _row(
            "3517802",
            "1.0.0.0.00.0.0 - Receitas Correntes",
            "siconfi-cor_RO1.0.0.0.00.0.0",
            100.0,
        )
    )
    path = tmp_path / "receitas.xlsx"
    workbook.save(path)

    try:
        normalize_revenue_supplement(
            path,
            2022,
            ["3500000"],
            tmp_path / "delta.csv",
            tmp_path / "report.json",
        )
    except ValueError as exc:
        assert "not found" in str(exc)
    else:
        raise AssertionError("Expected missing-code validation")
