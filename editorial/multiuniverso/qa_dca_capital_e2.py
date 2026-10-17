"""Audit three DCA capital accounts between official 2025 CSV and E2 JSON.
Read-only. For unavailable source rows, demand the E2 to remain non-observed;
do not infer a declared zero.
"""
import argparse
import csv
import json
import math
from pathlib import Path
from urllib.request import urlopen

ACCOUNTS = ("dca_inversoes_financeiras_liquidada", "dca_operacoes_credito", "dca_alienacao_bens")


def audit(csv_path: Path, municipality_json_dir: Path, output: Path) -> dict:
    with csv_path.open(encoding="utf-8-sig", newline="") as handle:
        official = {row["cod_ibge"]: row for row in csv.DictReader(handle)}
    reports = []
    missing_file = []
    for path in sorted(municipality_json_dir.glob("*.json")):
        code = path.stem
        if code not in official:
            continue
        obj = json.loads(path.read_text(encoding="utf-8"))
        for account in ACCOUNTS:
            source = official[code].get(account, "")
            variables = obj.get("variables") or {}
            if account not in variables:
                reports.append({"codigo_ibge": code, "variable": account,
                                "category": "variable_not_exposed", "source": source,
                                "api_status": None, "api_value": None})
                continue
            latest = (variables.get(account) or {}).get("latest") or {}
            status, value = latest.get("status"), latest.get("value")
            if source == "":
                ok = status != "observado" and value is None
                category = "missing_preserved" if ok else "missing_promoted"
            else:
                valid = status == "observado" and isinstance(value, (int, float)) and not isinstance(value, bool)
                ok = valid and math.isclose(float(source), float(value), abs_tol=0.01, rel_tol=1e-10)
                category = "observed_equal" if ok else "observed_mismatch"
            reports.append({"codigo_ibge": code, "variable": account, "category": category,
                            "source": source, "api_status": status, "api_value": value})
    if not reports:
        raise ValueError("No overlap between E2 municipality JSON files and official CSV.")
    summary = {"accounts": ACCOUNTS, "comparison_count": len(reports),
               "by_category": {key: sum(r["category"] == key for r in reports)
                               for key in ("observed_equal", "observed_mismatch", "missing_preserved", "missing_promoted", "variable_not_exposed")},
               "mismatches": [r for r in reports if r["category"] in ("observed_mismatch", "missing_promoted", "variable_not_exposed")],
               "limitations": "Checks only available municipality JSON files. Requires complete E2 coverage independently."}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({"summary": summary, "records": reports}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if summary["mismatches"]:
        raise ValueError(f"Capital DCA E2 mismatches: {len(summary['mismatches'])}")
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", type=Path, required=True)
    parser.add_argument("--municipality-json-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(audit(args.csv, args.municipality_json_dir, args.output), ensure_ascii=False, indent=2))
