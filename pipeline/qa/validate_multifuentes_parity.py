from __future__ import annotations

import argparse
import math
import sqlite3
from pathlib import Path

import openpyxl
import yaml

from pipeline.ingest.import_multifuentes import normalize_ibge

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MAPPING = ROOT / "data" / "mappings" / "base_multifuentes_v0_4.yml"


def same_numeric(left: float, right: float, tolerance: float = 1e-9) -> bool:
    return math.isclose(float(left), float(right), rel_tol=tolerance, abs_tol=tolerance)


def validate_parity(
    workbook: Path,
    database: Path,
    mapping_path: Path = DEFAULT_MAPPING,
) -> dict:
    mapping = yaml.safe_load(mapping_path.read_text(encoding="utf-8"))
    source = mapping["source"]

    wb = openpyxl.load_workbook(workbook, read_only=True, data_only=True)
    ws = wb[source["sheet"]]
    row_iterator = ws.iter_rows(values_only=True)
    headers = [str(x) if x is not None else "" for x in next(row_iterator)]
    columns = {name: i for i, name in enumerate(headers)}

    con = sqlite3.connect(database)
    con.row_factory = sqlite3.Row

    checked = 0
    differences = []
    try:
        for row in row_iterator:
            code = normalize_ibge(row[columns[mapping["keys"]["codigo_ibge"]]])
            year = int(row[columns[mapping["keys"]["ano"]]])

            for variable_id, spec in mapping["variables"].items():
                raw = row[columns[spec["column"]]]
                start = int(spec["availability_start"])
                end = int(spec["availability_end"])

                record = con.execute(
                    """
                    SELECT valor_num, valor_texto, status
                    FROM observacao
                    WHERE codigo_ibge=? AND ano=? AND variavel_id=?
                    """,
                    (code, year, variable_id),
                ).fetchone()
                checked += 1

                if record is None:
                    differences.append((code, year, variable_id, "registro_ausente"))
                    continue

                if year < start or year > end:
                    expected_status = "nao_aplicavel"
                elif raw is None or (isinstance(raw, str) and not raw.strip()):
                    expected_status = "ausente"
                else:
                    expected_status = "observado"

                if record["status"] != expected_status:
                    differences.append(
                        (
                            code,
                            year,
                            variable_id,
                            f"status:{record['status']}!={expected_status}",
                        )
                    )
                    continue

                if expected_status != "observado":
                    continue

                if spec["value_type"] == "numeric":
                    if record["valor_num"] is None or not same_numeric(record["valor_num"], raw):
                        differences.append(
                            (code, year, variable_id, "valor_numerico_divergente")
                        )
                else:
                    if record["valor_texto"] != str(raw):
                        differences.append(
                            (code, year, variable_id, "valor_texto_divergente")
                        )
    finally:
        con.close()
        wb.close()

    return {
        "checked": checked,
        "differences": len(differences),
        "examples": differences[:20],
        "status": "PASS" if not differences else "FAIL",
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compara o SQLite importado com a base multifuentes de origem."
    )
    parser.add_argument("workbook", type=Path)
    parser.add_argument("database", type=Path)
    parser.add_argument("--mapping", type=Path, default=DEFAULT_MAPPING)
    args = parser.parse_args()

    result = validate_parity(args.workbook, args.database, args.mapping)
    for key, value in result.items():
        print(f"{key}={value}")
    if result["differences"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
