"""Check percent-source-to-SQLite parity, preserving missing and observed zero."""
import argparse
import json
import math
import sqlite3
from collections import Counter
from pathlib import Path

import openpyxl
import yaml

VARIABLES = (
    "receita_tributaria_pct_receita_corrente",
    "investimento_pct_receita_corrente",
    "despesa_territorial_pct_despesa",
    "dtp_pct_rcl", "dc_pct_rcl", "dcl_pct_rcl",
)


def audit(database: Path, workbook: Path, mapping: Path, output: Path) -> dict:
    config = yaml.safe_load(mapping.read_text(encoding="utf-8"))
    specifications = {}
    for identifier in VARIABLES:
        spec = config["variables"][identifier]
        if float(spec.get("scale", 1)) != 0.01:
            raise ValueError(f"Scale no longer 0.01 for {identifier}")
        specifications[identifier] = spec
    con = sqlite3.connect(database)
    try:
        observed = {
            (str(code), int(year), variable): (status, value)
            for code, year, variable, status, value in con.execute(
                """SELECT codigo_ibge,ano,variavel_id,status,valor_num FROM observacao
                   WHERE variavel_id IN (?,?,?,?,?,?)""", VARIABLES
            )
        }
    finally:
        con.close()
    book = openpyxl.load_workbook(workbook, read_only=True, data_only=True)
    results = {v: {"compared": 0, "source_missing": 0, "db_missing": 0,
                    "years": Counter()} for v in VARIABLES}
    mismatches = []
    rows = 0
    try:
        sheet = book[config["source"]["sheet"]]
        iterator = sheet.iter_rows(values_only=True)
        header = list(next(iterator))
        for values in iterator:
            record = dict(zip(header, values))
            code = str(record["cod_ibge"]).strip()
            year = int(record["ano"])
            rows += 1
            for identifier, spec in specifications.items():
                if not spec["availability_start"] <= year <= spec["availability_end"]:
                    continue
                raw = record.get(spec["column"])
                status, stored = observed.get((code, year, identifier), ("sem_registro", None))
                if raw is None or str(raw).strip().casefold() in ("", "n.d.", "na", "n/a"):
                    results[identifier]["source_missing"] += 1
                    if status == "observado" and stored is not None:
                        mismatches.append([code, year, identifier, "unexpected_observation"])
                    continue
                if status != "observado" or stored is None:
                    results[identifier]["db_missing"] += 1
                    mismatches.append([code, year, identifier, "not_observed"])
                    continue
                expected = float(raw) * float(spec["scale"])
                if not math.isfinite(expected) or not math.isfinite(float(stored)):
                    mismatches.append([code, year, identifier, "nonfinite"])
                elif not math.isclose(float(stored), expected, rel_tol=1e-10, abs_tol=1e-10):
                    mismatches.append([code, year, identifier, "value_disagreement"])
                else:
                    results[identifier]["compared"] += 1
                    results[identifier]["years"][year] += 1
    finally:
        book.close()
    if rows != 3225:
        raise ValueError(f"Unexpected source row count: {rows}")
    for v, counts in results.items():
        counts["years"] = dict(sorted(counts["years"].items()))
        if not counts["compared"]:
            mismatches.append([v, "no compared values"])
    report = {
        "scope": "source_workbook_to_stored_numeric_parity",
        "certifies": "imported input values times declared scale; not source semantic correctness",
        "rows": rows,
        "variables": results,
        "mismatch_count": len(mismatches),
        "mismatch_examples": mismatches[:30],
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if mismatches:
        raise ValueError(f"Percentage source parity failed: {len(mismatches)}; {mismatches[:5]}")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--database", type=Path, required=True)
    parser.add_argument("--workbook", type=Path, required=True)
    parser.add_argument("--mapping", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(audit(args.database, args.workbook, args.mapping, args.output),
                     ensure_ascii=False, indent=2))
