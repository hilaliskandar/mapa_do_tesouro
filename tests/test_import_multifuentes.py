from pathlib import Path
import sqlite3

import openpyxl
import yaml

from pipeline.ingest.import_multifuentes import import_multifuentes

ROOT = Path(__file__).resolve().parents[1]


def create_fixture(path: Path, mapping_path: Path) -> None:
    mapping = yaml.safe_load(mapping_path.read_text(encoding="utf-8"))
    headers = list(mapping["keys"].values())
    for spec in mapping["variables"].values():
        if spec["column"] not in headers:
            headers.append(spec["column"])

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = mapping["source"]["sheet"]
    ws.append(headers)

    for year in range(2013, 2026):
        row = {header: None for header in headers}
        row["cod_ibge"] = "3500000"
        row["municipio"] = "Municipio Teste"
        row["ano"] = year
        for variable_id, spec in mapping["variables"].items():
            if spec["availability_start"] <= year <= spec["availability_end"]:
                if spec["value_type"] == "numeric":
                    row[spec["column"]] = float(year)
                else:
                    row[spec["column"]] = "A"
        ws.append([row[h] for h in headers])

    wb.save(path)


def test_importer_preserves_applicability_and_observed_zero(tmp_path):
    mapping_path = ROOT / "data" / "mappings" / "base_multifuentes_v0_4.yml"
    mapping = yaml.safe_load(mapping_path.read_text(encoding="utf-8"))
    mapping["source"]["expected_rows"] = 13
    mapping["source"]["expected_municipalities"] = 1

    local_mapping = tmp_path / "mapping.yml"
    local_mapping.write_text(
        yaml.safe_dump(mapping, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )

    workbook = tmp_path / "fixture.xlsx"
    create_fixture(workbook, local_mapping)

    database = tmp_path / "fixture.sqlite"
    result = import_multifuentes(
        workbook,
        database,
        mapping_path=local_mapping,
        overwrite=False,
        build_timestamp="2026-10-06T00:00:00-03:00",
    )

    assert result["rows"] == 13
    assert result["municipalities"] == 1

    con = sqlite3.connect(database)
    try:
        assert con.execute(
            """
            SELECT status FROM observacao
            WHERE codigo_ibge='3500000'
              AND ano=2013
              AND variavel_id='rreo_rcl_oficial'
            """
        ).fetchone()[0] == "nao_aplicavel"

        assert con.execute(
            """
            SELECT status FROM observacao
            WHERE codigo_ibge='3500000'
              AND ano=2015
              AND variavel_id='rreo_rcl_oficial'
            """
        ).fetchone()[0] == "observado"

        assert con.execute(
            """
            SELECT status FROM observacao
            WHERE codigo_ibge='3500000'
              AND ano=2024
              AND variavel_id='capag'
            """
        ).fetchone()[0] == "nao_aplicavel"

        assert con.execute(
            """
            SELECT status, valor_texto FROM observacao
            WHERE codigo_ibge='3500000'
              AND ano=2025
              AND variavel_id='capag'
            """
        ).fetchone() == ("observado", "A")
    finally:
        con.close()
