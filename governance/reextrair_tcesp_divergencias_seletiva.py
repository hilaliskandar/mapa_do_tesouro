#!/usr/bin/env python3
"""Independent, read-only selective reconstruction from official TCESP statewide ZIP.

Reads every CSV record but retains evidence exclusively for nominated municipality/year
pairs. No dependency on the original investment aggregation code.
"""
import argparse
import csv
import decimal
import hashlib
import io
import json
import pathlib
import urllib.request
import zipfile
from collections import Counter, defaultdict

TARGETS = {
    2023: {"3548807", "3545209", "3502804"},
    2024: {"3554102", "3522158", "3533254", "3548906", "3534708", "3520301"},
    2025: {"3517901"},
}
D = decimal.Decimal

def centavos(text):
    value = D(str(text).strip().replace(".", "").replace(",", ".")) * 100
    if not value.is_finite() or value != value.to_integral_value():
        raise ValueError("not exact integer cents")
    return int(value)

def execute(year, dest, source=None):
    dest.mkdir(parents=True, exist_ok=True)
    url = source or f"https://transparencia.tce.sp.gov.br/sites/default/files/conjunto-dados/despesas-{year}.zip"
    archive_path = dest / "fonte_tcesp.zip"
    digest = hashlib.sha256()
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (independent TCESP audit)", "Accept-Encoding": "identity"})
    with urllib.request.urlopen(req, timeout=240) as resp, archive_path.open("wb") as target:
        while block := resp.read(4 * 1024 * 1024):
            target.write(block)
            digest.update(block)
    totals = Counter()
    months = defaultdict(set)
    stages = Counter()
    records = Counter()
    diagnostic = Counter()
    sample = defaultdict(list)
    rows_seen = 0
    selected = 0
    if not zipfile.is_zipfile(archive_path):
        signature = archive_path.open("rb").read(64)
        failure = {"status": "blocked_source_not_zip", "year": year, "url": url,
                   "sha256": digest.hexdigest(), "bytes": archive_path.stat().st_size,
                   "prefix_hex": signature[:16].hex()}
        (dest / "source_access_diagnostic.json").write_text(json.dumps(failure, indent=2) + "\\n")
        print(json.dumps(failure), flush=True)
        raise RuntimeError("Official source did not return ZIP; no financial comparison made")
    with zipfile.ZipFile(archive_path) as z:
        if z.testzip() is not None:
            raise ValueError("ZIP CRC error")
        members = [x for x in z.namelist() if x.lower().endswith(".csv")]
        if len(members) != 1:
            raise ValueError("Unexpected CSV member count")
        with z.open(members[0]) as source_stream:
            reader = csv.DictReader(io.TextIOWrapper(source_stream, encoding="latin-1", newline=""), delimiter=";")
            required = {"codigo_municipio_ibge", "ano_exercicio", "mes_referencia", "ds_elemento", "tp_despesa", "vl_despesa"}
            if not required.issubset(reader.fieldnames or []):
                raise ValueError("Missing source columns")
            for row in reader:
                rows_seen += 1
                city = row["codigo_municipio_ibge"].strip()
                if city not in TARGETS[year]:
                    continue
                if row["ano_exercicio"].strip() != str(year):
                    diagnostic["wrong_year"] += 1
                    continue
                records[city] += 1
                month = row["mes_referencia"].strip()
                if not month.isdigit() or not 1 <= int(month) <= 12:
                    diagnostic["invalid_month"] += 1
                    continue
                months[city].add(month)
                code = row["ds_elemento"].strip().split(" - ", 1)[0]
                if not code.startswith("44"):
                    continue
                try:
                    cents = centavos(row["vl_despesa"])
                except (ValueError, decimal.InvalidOperation):
                    diagnostic["invalid_money"] += 1
                    continue
                selected += 1
                stage = row["tp_despesa"].strip().casefold()
                stages[(city, stage)] += 1
                totals[(city, stage)] += cents
                if len(sample[city]) < 3:
                    sample[city].append({"mes": month, "elemento": code, "estagio": stage, "centavos": cents})
    result = {
        "status": "pass" if not diagnostic and set(records) == TARGETS[year] else "needs_review",
        "year": year, "source_url": url, "source_sha256": digest.hexdigest(),
        "source_bytes": archive_path.stat().st_size, "rows_scanned": rows_seen,
        "selected_group44_rows": selected,
        "record_counts": dict(records),
        "stages": [{"codigo_ibge": c, "stage": s, "rows": n} for (c, s), n in sorted(stages.items())],
        "totals": [{"codigo_ibge": c, "stage": s, "centavos": n} for (c, s), n in sorted(totals.items())],
        "month_presence": {k: sorted(v) for k, v in sorted(months.items())},
        "issues": dict(diagnostic), "sample": dict(sample)
    }
    (dest / "seletiva_qa.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "sample"}, ensure_ascii=False))
    return result

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--year", type=int, required=True, choices=sorted(TARGETS))
    p.add_argument("--output", type=pathlib.Path, required=True)
    p.add_argument("--url", default=None)
    args = p.parse_args()
    result = execute(args.year, args.output, args.url)
    if result["status"] != "pass":
        raise SystemExit(2)
