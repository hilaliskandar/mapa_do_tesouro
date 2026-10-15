#!/usr/bin/env python3
"""Reconcile fiscal entries embedded in RMJ HTML against canonical DCA CSV.

Usage: python3 editorial/rmj/audit_against_dca_csv.py PATH_TO_DCA_CSV
The CSV is an external input and must not be committed to the repository.
"""
import csv
import json
import pathlib
import re
import sys

BASE = pathlib.Path(__file__).resolve().parent
HTML = (BASE / "index.html").read_text(encoding="utf-8")
EPS = 0.011
FIELDS = {
    "historical": {
        "receita": "dca_receita_corrente_bruta",
        "tributaria": "dca_receita_tributaria_bruta",
        "investimento": "dca_investimentos_liquidada",
    },
}
def dataset(name):
    match = re.search(r"const\s+" + re.escape(name) + r"\s*=\s*(\[[^;]*\]);", HTML)
    if not match:
        raise ValueError("Embedded data not found: " + name)
    return json.loads(match.group(1))

def number(value):
    return None if value is None or value == "" else float(value)

def main(source):
    historical, extra = dataset("historical"), dataset("extra")
    fields = dict(FIELDS)
    fields["extra"] = {
        key: key for key in extra[0] if key.startswith("dca_")
    }
    with open(source, newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        wanted = {(r["id"], str(r["ano"])) for rows in (historical,extra) for r in rows}
        reference = {}
        for row in reader:
            key = (str(row["cod_ibge"]), str(row["ano"]))
            if key in wanted:
                if key in reference:
                    raise ValueError("Duplicate source pair " + str(key))
                reference[key] = row
    failures = []
    count = 0
    for name, rows in (("historical",historical),("extra",extra)):
        seen = set()
        for entry in rows:
            pair = (entry["id"], str(entry["ano"]))
            if pair in seen:
                failures.append(f"Duplicate HTML pair in {name}: {pair}")
            seen.add(pair)
            original = reference.get(pair)
            for html_name, source_name in fields[name].items():
                count += 1
                left = number(entry.get(html_name))
                right = number(original.get(source_name)) if original is not None else None
                if left is None and right is None and original is not None:
                    continue
                if left is None or right is None or abs(left-right) > EPS:
                    failures.append(f"{name} {pair} {html_name}: html={left}, csv={right}")
    summary = {
        "status": "PASS" if not failures else "FAIL",
        "source_rows_matched": len(reference),
        "html_municipality_years": len(set((x["id"], x["ano"]) for x in historical)),
        "fields_compared": sum(len(mapping) for mapping in fields.values()),
        "values_compared": count,
        "divergences": len(failures),
        "sample_failures": failures[:20],
    }
    print(json.dumps(summary, ensure_ascii=False))
    if failures:
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Pass the path to the canonical DCA CSV")
    main(sys.argv[1])
