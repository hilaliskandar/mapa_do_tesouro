#!/usr/bin/env python3
"""FED00: stage STN monthly national file as SP645 item records, preserving raw amounts.

This is an audited *candidate*, not a financial reconciliation or a production import.
All municipality codes are from an STN-to-SQLite identity crosswalk with prior QA.
Do not sum decendial amounts, merge different transfer classes, or infer receipts.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

SOURCE_SHA = "097638cec48145ac0f509d526be49d40929d177ef3a2ae3b7f77c0acd990cf24"
CROSSWALK_SHA = "20c80f6464de30f899430327db569fd7a52610c14bfc88678b769638572f036c"
RESOURCE_ID = "63b5f470-135f-4431-9158-ca8b7a43f61b"
COLUMN_MAP = {"municipio": "Município", "uf": "UF", "ano": "ANO", "mes": "Mês",
              "one": "1º Decêndio", "two": "2º Decêndio", "three": "3º Decêndio",
              "item": "Item transferência", "transferencia": "Transferência"}
OUTPUT_FIELDS = [
    "codigo_ibge", "municipio_stn", "ano", "mes", "transferencia",
    "item_transferencia", "decendio_1_raw", "decendio_2_raw", "decendio_3_raw",
    "source_extra_raw", "source_resource_id", "source_sha256", "data_status",
]

def hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def stage(source: Path, crosswalk: Path, output: Path) -> dict:
    src_hash, cross_hash = hash_file(source), hash_file(crosswalk)
    if src_hash != SOURCE_SHA or cross_hash != CROSSWALK_SHA:
        raise ValueError("Unapproved input hash: stop, do not silently replace historical source")
    with crosswalk.open(encoding="utf-8-sig", newline="") as f:
        matched = list(csv.DictReader(f, delimiter=";"))
    if len(matched) != 645:
        raise ValueError("Crosswalk is not 645 rows")
    names = {x["municipio_stn"].strip(): x["codigo_ibge"].strip() for x in matched}
    if len(names) != 645 or len(set(names.values())) != 645:
        raise ValueError("Municipal IDs or names are not one-to-one")
    if any(not (len(c) == 7 and c.isdigit() and c.startswith("35")) for c in names.values()):
        raise ValueError("Invalid IBGE codes")
    rows = []
    country_rows = 0
    period_counts = Counter()
    sp_transfer_counts = Counter()
    duplicates = []
    seen = set()
    formats = Counter()
    extra_nonempty = 0
    with source.open(encoding="cp1252", newline="") as f:
        reader = csv.DictReader(f, delimiter=";")
        hdr = set(reader.fieldnames or ())
        if not set(COLUMN_MAP.values()).issubset(hdr):
            raise ValueError("STN original columns differ from approved historical layout")
        extra_col = [x for x in (reader.fieldnames or ()) if not x]
        for entry in reader:
            country_rows += 1
            uf = entry["UF"].strip().upper()
            year, month = entry["ANO"].strip(), entry["Mês"].strip()
            period_counts[(year, month)] += 1
            if uf != "SP":
                continue
            name = entry["Município"].strip()
            if name not in names:
                raise ValueError("STN municipality absent from checked crosswalk: " + name)
            code = names[name]
            transferencia, item = entry["Transferência"].strip(), entry["Item transferência"].strip()
            grain = (code, year, month, transferencia, item)
            if grain in seen:
                duplicates.append(grain)
                continue
            seen.add(grain)
            raw = [entry[x].strip() for x in ("1º Decêndio", "2º Decêndio", "3º Decêndio")]
            for cell in raw:
                if re.fullmatch(r"-?[0-9]+", cell):
                    formats["integer"] += 1
                elif re.fullmatch(r"-?[0-9]+\.[0-9]{1,2}", cell):
                    formats["dot_decimal"] += 1
                else:
                    formats["invalid"] += 1
            extra = entry.get("", "") or ""
            if extra.strip():
                extra_nonempty += 1
            rows.append({
                "codigo_ibge": code, "municipio_stn": name, "ano": year, "mes": month,
                "transferencia": transferencia, "item_transferencia": item,
                "decendio_1_raw": raw[0], "decendio_2_raw": raw[1],
                "decendio_3_raw": raw[2], "source_extra_raw": extra,
                "source_resource_id": RESOURCE_ID, "source_sha256": SOURCE_SHA,
                "data_status": "candidate_unreconciled_financial_unit",
            })
            sp_transfer_counts[transferencia] += 1
    if (country_rows != 126807 or len(rows) != 13889 or len(set(r["codigo_ibge"] for r in rows)) != 645
        or len(seen) != 13889 or period_counts != {("2026", "09"): 126807}
        or duplicates or formats.get("invalid", 0) or extra_nonempty):
        raise ValueError("STN 2026/09 staging QA failed: counts, grain, decimals or source extra field")
    rows.sort(key=lambda r: (r["codigo_ibge"], r["transferencia"], r["item_transferencia"]))
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=OUTPUT_FIELDS, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)
    return {
        "status": "qa_pass_staging_only",
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_resource_id": RESOURCE_ID, "source_sha256": src_hash,
        "crosswalk_sha256": cross_hash, "national_source_rows": country_rows,
        "sp_rows": len(rows), "municipalities": 645, "sp_unique_grain": len(seen),
        "period": "2026/09", "sp_transfer_counts": dict(sorted(sp_transfer_counts.items())),
        "decendial_string_formats": dict(sorted(formats.items())),
        "extra_source_field_nonempty": extra_nonempty,
        "output_csv": str(output), "output_sha256": hash_file(output),
        "output_bytes": output.stat().st_size,
        "restrictions": [
            "No accounting totals or cents are computed and no missing amounts are silently made zero",
            "The original source values are preserved as text; the unit and source deductions require homologation",
            "The code mapping passed SQLite identity QA, but names remain source-specific",
            "No SQLite inserts or updates, no site changes, no transfer payment causality inferred",
        ],
    }

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--source", type=Path, required=True)
    p.add_argument("--crosswalk", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--qa", type=Path, required=True)
    args = p.parse_args()
    try:
        result = stage(args.source, args.crosswalk, args.output)
    except Exception as e:
        result = {"status": "failed_or_changed_source",
                  "error": f"{type(e).__name__}: {str(e)[:350]}"}
    args.qa.parent.mkdir(parents=True, exist_ok=True)
    args.qa.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: result.get(k) for k in
                      ("status", "sp_rows", "municipalities", "output_sha256", "error")}, ensure_ascii=False))
    if result["status"] != "qa_pass_staging_only":
        raise SystemExit(2)

if __name__ == "__main__":
    main()
