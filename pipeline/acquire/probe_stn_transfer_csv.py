#!/usr/bin/env python3
"""FED00: bounded one-resource STN transfer CSV pilot. Never touches canonical DB/R2.

Downloads one explicitly selected CKAN resource by *resource ID*, verifies metadata,
inspects CSV header/row count, and records SHA256 and source evidence. Does not
assume that a resource's title or filename proves month of competence.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import io
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

API = "https://www.tesourotransparente.gov.br/ckan/api/3/action/package_show?id=transferencias-constitucionais-para-municipios"
RESOURCE_ID_DEFAULT = "63b5f470-135f-4431-9158-ca8b7a43f61b"
MAX_CSV_BYTES = 20_000_000
MAX_CATALOG_BYTES = 2_000_000
UA = "mapa-do-tesouro-FED00-STN-read-only/1.0"

def fetch(url: str, limit: int) -> bytes:
    req = Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urlopen(req, timeout=65) as response:
        if response.status != 200:
            raise RuntimeError(f"HTTP_{response.status}")
        blob = response.read(limit + 1)
    if len(blob) > limit:
        raise RuntimeError(f"bounded_download_exceeded_{limit}")
    return blob

def decode_text(blob: bytes) -> tuple[str, str]:
    for encoding in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            text = blob.decode(encoding)
            if not text.lstrip().lower().startswith(("<!doctype html", "<html")):
                return text, encoding
        except UnicodeDecodeError:
            continue
    raise RuntimeError("not_a_decodable_csv_or_html_response")

def inspect_csv(text: str) -> dict:
    f = io.StringIO(text, newline="")
    first = f.readline()
    if not first.strip():
        raise RuntimeError("empty_csv_header")
    delimiter = max((";", ",", "\t", "|"), key=first.count)
    if first.count(delimiter) == 0:
        raise RuntimeError("delimiter_not_recognized")
    f.seek(0)
    reader = csv.reader(f, delimiter=delimiter)
    header = next(reader)
    if len(header) < 3 or len(set(header)) != len(header):
        raise RuntimeError("unexpected_csv_header")
    count = 0
    width_mismatches = 0
    for row in reader:
        if not row:
            continue
        count += 1
        if len(row) != len(header):
            width_mismatches += 1
    if not count:
        raise RuntimeError("csv_without_records")
    return {"delimiter": delimiter, "column_names": header,
            "row_count_national_not_sp": count, "column_count": len(header),
            "row_width_mismatches": width_mismatches}

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--resource-id", default=RESOURCE_ID_DEFAULT)
    parser.add_argument("--output", default="build/fed00_stn_csv/QA_FED00_STN_CSV.json")
    args = parser.parse_args()
    report = {"checked_at_utc": datetime.now(timezone.utc).isoformat(),
              "resource_id": args.resource_id, "catalog_url": API,
              "status": "not_started",
              "restrictions": ["National dataset not filtered to SP645",
                               "No municipalities are inferred from source file name",
                               "No change to canonical SQLite R2 or production"]}
    try:
        catalog_raw = fetch(API, MAX_CATALOG_BYTES)
        catalog = json.loads(catalog_raw.decode("utf-8-sig"))
        if catalog.get("success") is not True:
            raise RuntimeError("CKAN_catalog_failed")
        items = [x for x in catalog["result"]["resources"] if x.get("id") == args.resource_id]
        if len(items) != 1:
            raise RuntimeError(f"resource_not_unique_{len(items)}")
        resource = items[0]
        url = str(resource.get("url", ""))
        parsed = urlparse(url)
        if parsed.scheme != "https" or parsed.hostname != "www.tesourotransparente.gov.br":
            raise RuntimeError("unexpected_resource_host")
        blob = fetch(url, MAX_CSV_BYTES)
        content, encoding = decode_text(blob)
        stats = inspect_csv(content)
        report.update({"status": "qa_pass" if stats["row_width_mismatches"] == 0 else "partial",
                       "catalog_sha256": hashlib.sha256(catalog_raw).hexdigest(),
                       "catalog_modified": catalog["result"].get("metadata_modified"),
                       "resource_name": resource.get("name"),
                       "resource_url": url, "resource_created": resource.get("created"),
                       "resource_last_modified": resource.get("last_modified"),
                       "resource_size_declared": resource.get("size"),
                       "download_sha256": hashlib.sha256(blob).hexdigest(),
                       "download_bytes": len(blob), "encoding": encoding,
                       "csv_evidence": stats,
                       "caution": "File header and content month must be checked before assigning fiscal competence"})
    except Exception as exc:
        report.update({"status": "failed_or_unavailable",
                       "error": f"{type(exc).__name__}: {str(exc)[:350]}"})
    dst = Path(args.output)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"],
                      "resource_id": args.resource_id,
                      "rows": report.get("csv_evidence", {}).get("row_count_national_not_sp"),
                      "error": report.get("error")}, ensure_ascii=False))
    if report["status"] != "qa_pass":
        raise SystemExit(2)

if __name__ == "__main__":
    main()
