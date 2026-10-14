"""Independently reconcile stored derived ratios against stored source accounts."""
import argparse
import json
import math
import sqlite3
from collections import Counter
from pathlib import Path

from pipeline.transform.calculate_annual import RATIOS


def audit(database: Path, output: Path) -> dict:
    con = sqlite3.connect(database)
    try:
        identifiers = set(RATIOS)
        dependencies = {value for pair in RATIOS.values() for value in pair}
        wanted = tuple(sorted(identifiers | dependencies))
        marks = ",".join("?" for _ in wanted)
        rows = con.execute(
            f"""SELECT codigo_ibge,ano,variavel_id,status,valor_num
                FROM observacao WHERE variavel_id IN ({marks})""", wanted
        ).fetchall()
    finally:
        con.close()
    by_key = {}
    keys = set()
    for code, year, variable, status, value in rows:
        by_key[(str(code), int(year), variable)] = (status, value)
        keys.add((str(code), int(year)))
    counts = {identifier: Counter() for identifier in RATIOS}
    failures = []
    for code, year in sorted(keys):
        for identifier, (numerator, denominator) in RATIOS.items():
            ns, nv = by_key.get((code, year, numerator), ("ausente", None))
            ds, dv = by_key.get((code, year, denominator), ("ausente", None))
            actual_status, actual = by_key.get((code, year, identifier), ("sem_registro", None))
            if ns == ds == "nao_aplicavel":
                expected_status, expected = "nao_aplicavel", None
            elif ns != "observado" or ds != "observado" or nv is None or dv is None or float(dv) == 0:
                expected_status, expected = "ausente", None
            else:
                expected_status, expected = "observado", float(nv) / float(dv)
            if actual_status != expected_status:
                if actual_status == "sem_registro" and expected_status == "ausente":
                    counts[identifier]["sem_registro_missing"] += 1
                    continue
                failures.append([code, year, identifier, "status", actual_status, expected_status])
                continue
            if expected_status != "observado":
                counts[identifier][expected_status] += 1
            elif actual is None or not math.isfinite(float(actual)) or not math.isclose(
                float(actual), expected, rel_tol=1e-9, abs_tol=1e-10
            ):
                failures.append([code, year, identifier, "value", actual, expected])
            else:
                counts[identifier]["numeric_parity"] += 1
                counts[identifier][f"year_{year}"] += 1
    report = {
        "basis": "SQLite observation values; ratio=numerator/denominator; no multiplication by 100",
        "scope": "all ratio variables in pipeline.transform.calculate_annual.RATIOS",
        "by_variable": {key: dict(value) for key, value in counts.items()},
        "failure_count": len(failures),
        "failure_examples": failures[:30],
        "years": sorted({year for _, year in keys}),
        "municipality_year_keys": len(keys),
        "not_certified": ["original-source correctness", "source accounting comparability",
                          "display multiplier", "official RGF ratios outside RATIOS"],
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if failures:
        raise ValueError(f"Derived-ratio parity failed: {len(failures)}; {failures[:5]}")
    return report


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--database", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    args = p.parse_args()
    result = audit(args.database, args.output)
    print(json.dumps({"failure_count": result["failure_count"],
                      "variables": len(result["by_variable"])}, indent=2))
