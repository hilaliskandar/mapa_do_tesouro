#!/usr/bin/env python3
"""Reconcile TCESP raw nature against dynamic program/action descriptions. Aggregate only."""
import collections
import csv
import hashlib
import io
import json
import os
import re
import sys
import unicodedata
import urllib.request
import zipfile
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path

TARGETS = [("ribeirao-preto", 2024), ("ribeirao-preto", 2025),
           ("sertaozinho", 2025), ("guatapara", 2023)]
KEYWORDS = ("precator", "amortiz", "divida", "operac", "judicia")
def clean(s):
    return "".join(c for c in unicodedata.normalize("NFKD", str(s).lower())
                   if not unicodedata.combining(c))
def cents(s):
    return int((Decimal(str(s or "0").replace(".", "").replace(",", ".")) * 100)
               .quantize(Decimal("1"), rounding=ROUND_HALF_UP))
def run(slug, year, out):
    url = f"https://transparencia.tce.sp.gov.br/sites/default/files/csv/despesas-{slug}-{year}.zip"
    with urllib.request.urlopen(urllib.request.Request(
         url, headers={"User-Agent":"Mozilla/5.0"}), timeout=200) as response:
        data = response.read()
    source_hash = hashlib.sha256(data).hexdigest()
    nature = collections.defaultdict(lambda: {"rows":0, "cents":0})
    candidates = collections.defaultdict(lambda: {"rows":0, "cents":0, "elements":{}})
    program_keys = set()
    full = 0
    matched = 0
    invalid = 0
    total_rows = 0
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        files = [n for n in z.namelist() if not n.endswith("/")]
        if len(files) != 1: raise ValueError("Expected one TCESP CSV")
        with z.open(files[0]) as f:
            reader = csv.DictReader(io.TextIOWrapper(f, encoding="latin-1", newline=""), delimiter=";")
            for row in reader:
                total_rows += 1
                tp = (row.get("tp_despesa") or "").strip().lower()
                element = (row.get("ds_elemento") or "").strip()
                code = element.split(" - ", 1)[0].strip()
                if tp != "valor liquidado" or not code.startswith("44"):
                    continue
                try: value = cents(row.get("vl_despesa"))
                except (InvalidOperation, ValueError):
                    invalid += 1
                    continue
                full += value
                name = row.get("ds_acao") or ""
                prog = row.get("ds_programa") or ""
                key = (str(row.get("cd_programa") or "").strip(),
                       str(row.get("cd_acao") or "").strip(),
                       prog.strip(), name.strip())
                program_keys.add(key)
                desc = clean(name + " " + prog)
                if not any(k in desc for k in KEYWORDS):
                    continue
                matched += 1
                nature[element]["rows"] += 1
                nature[element]["cents"] += value
                c = candidates[key]
                c["rows"] += 1
                c["cents"] += value
                c["elements"][element] = c["elements"].get(element, 0) + value
    if invalid: raise ValueError(f"{invalid} malformed 44-liquidado values")
    rows = [{"program_code":k[0], "action_code":k[1],
             "program_name":k[2], "action_name":k[3],
             "rows":v["rows"], "cents":v["cents"], "nature_elements":v["elements"]}
            for k,v in candidates.items()]
    rows.sort(key=lambda x:(-abs(x["cents"]),x["program_code"],x["action_code"]))
    summary = {"slug":slug, "year":year, "url":url, "zip_sha256":source_hash,
               "source_rows":total_rows, "investment_44_liquidado_cents":full,
               "distinct_program_actions":len(program_keys),
               "keyword_matched_rows":matched,
               "keyword_matched_cents":sum(v["cents"] for v in candidates.values()),
               "keyword_matched_actions":len(candidates),
               "nature_by_element":dict(sorted(nature.items())),
               "candidate_actions":rows,
               "keywords":KEYWORDS, "note":"Keyword search is investigative, not classification; sums are aggregate, no individual expenses."}
    assert summary["keyword_matched_cents"] == sum(v["cents"] for v in nature.values())
    dest = out / f"{slug}_{year}_nature_audit.json"
    dest.write_text(json.dumps(summary, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    return {k:summary[k] for k in ("slug","year","zip_sha256","investment_44_liquidado_cents","keyword_matched_rows","keyword_matched_actions","keyword_matched_cents")}
def main():
    out = Path(sys.argv[1] if len(sys.argv)>1 else "build/rmrp-tcesp-nature")
    out.mkdir(parents=True, exist_ok=True)
    records = [run(slug,year,out) for slug,year in TARGETS]
    (out/"SUMMARY.json").write_text(json.dumps(records,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(records,ensure_ascii=False))
if __name__ == "__main__": main()
