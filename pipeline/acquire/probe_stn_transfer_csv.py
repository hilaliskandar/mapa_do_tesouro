#!/usr/bin/env python3
"""FED00: bounded one-resource STN transfer CSV pilot. Never touches canonical DB/R2.

Downloads one explicitly selected CKAN resource by *resource ID*, verifies metadata,
inspects CSV header/row count, and records SHA256 and source evidence. Does not
assume that a resource's title or filename proves month of competence.
"""
from __future__ import annotations
import argparse
from collections import Counter
import csv
import hashlib
import io
import json
import re
import time
import unicodedata
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

API = "https://www.tesourotransparente.gov.br/ckan/api/3/action/package_show?id=transferencias-constitucionais-para-municipios"
RESOURCE_ID_DEFAULT = "63b5f470-135f-4431-9158-ca8b7a43f61b"
IBGE_API = "https://servicodados.ibge.gov.br/api/v1/localidades/estados/35/municipios"
MAX_IBGE_BYTES = 2_000_000
MAX_CSV_BYTES = 20_000_000
MAX_CATALOG_BYTES = 2_000_000
UA = "mapa-do-tesouro-FED00-STN-read-only/1.0"

def fetch(url: str, limit: int) -> bytes:
    last_error = None
    for attempt in range(1, 4):
        try:
            req = Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
            with urlopen(req, timeout=35) as response:
                if response.status != 200:
                    raise RuntimeError(f"HTTP_{response.status}")
                blob = response.read(limit + 1)
            if len(blob) > limit:
                raise RuntimeError(f"bounded_download_exceeded_{limit}")
            return blob
        except Exception as exc:
            last_error = exc
            if attempt == 3 or "bounded_download_exceeded" in str(exc):
                break
            time.sleep(attempt * 2)
    raise RuntimeError(f"download_failed_after_3_attempts: {type(last_error).__name__}: {str(last_error)[:170]}")

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
    uf_counts: Counter[str] = Counter()
    sp_municipalities: set[str] = set()
    period_counts: Counter[str] = Counter()
    sp_period_counts: Counter[str] = Counter()
    transfer_type_counts: Counter[str] = Counter()
    missing_uf = 0
    for row in reader:
        if not row:
            continue
        count += 1
        if len(row) != len(header):
            width_mismatches += 1
            continue
        obj = dict(zip(header, row))
        uf = obj.get("UF", "").strip().upper()
        municipio = obj.get("Município", "").strip()
        ano = obj.get("ANO", "").strip()
        mes = obj.get("Mês", "").strip()
        uf_counts[uf] += 1
        period_counts[f"{ano}/{mes}"] += 1
        if not uf:
            missing_uf += 1
        if uf == "SP":
            sp_municipalities.add(municipio)
            sp_period_counts[f"{ano}/{mes}"] += 1
            transfer_type_counts[obj.get("Transferência", "").strip()] += 1
    if not count:
        raise RuntimeError("csv_without_records")
    return {"delimiter": delimiter, "column_names": header,
            "row_count_national_not_sp": count, "column_count": len(header),
            "row_width_mismatches": width_mismatches,
            "uf_counts": dict(sorted(uf_counts.items())),
            "sp_rows": uf_counts["SP"],
            "sp_distinct_municipality_names": len(sp_municipalities),
            "sp_municipality_names_sample": sorted(sp_municipalities)[:12],
            "sp_municipality_names": sorted(sp_municipalities),
            "all_period_counts": dict(sorted(period_counts.items())),
            "sp_period_counts": dict(sorted(sp_period_counts.items())),
            "sp_transfer_types": dict(sorted(transfer_type_counts.items())),
            "missing_uf_rows": missing_uf,
            "ibge_join_status": "pending_official_ibge_name_uf_crosswalk",
            "warning": "municipality labels are not official IBGE codes; counts are names, not validated municipal entities"}

def normalize_name(value: str) -> str:
    value = unicodedata.normalize("NFKD", value.casefold())
    value = "".join(c for c in value if not unicodedata.combining(c))
    return " ".join(re.sub(r"[^a-z0-9]+", " ", value).split())

def check_sp_ibge(stn_names: list[str], output: Path) -> dict:
    raw = fetch(IBGE_API, MAX_IBGE_BYTES)
    ibge = json.loads(raw.decode("utf-8-sig"))
    if not isinstance(ibge, list):
        raise RuntimeError("unexpected_ibge_response")
    by_key: dict[str, list[dict]] = defaultdict(list)
    for item in ibge:
        if not isinstance(item, dict):
            continue
        code, name = str(item.get("id", "")), str(item.get("nome", ""))
        if len(code) == 7 and code.startswith("35") and name:
            by_key[normalize_name(name)].append({"codigo_ibge": code, "nome_ibge": name})
    pairs = []
    unmatched = []
    ambiguous = []
    for stn in sorted(set(stn_names)):
        options = by_key.get(normalize_name(stn), [])
        if len(options) == 1:
            pairs.append({"municipio_stn": stn, "municipio_ibge": options[0]["nome_ibge"],
                          "codigo_ibge": options[0]["codigo_ibge"], "match_method": "name_uf_sp_normalized_exact"})
        elif not options:
            unmatched.append(stn)
        else:
            ambiguous.append({"municipio_stn": stn, "candidates": options})
    dst = output.parent / "STN_IBGE_SP_MATCH.csv"
    if len(pairs) == 645 and len({p["codigo_ibge"] for p in pairs}) == 645 and len(ibge) == 645:
        with dst.open("w", encoding="utf-8", newline="") as out:
            writer = csv.DictWriter(out, fieldnames=("municipio_stn", "municipio_ibge", "codigo_ibge", "match_method"), delimiter=";")
            writer.writeheader()
            writer.writerows(pairs)
        crosswalk_sha = hashlib.sha256(dst.read_bytes()).hexdigest()
        status = "qa_pass"
    else:
        crosswalk_sha = None
        status = "requires_review"
    return {"status": status, "ibge_api_url": IBGE_API, "ibge_response_sha256": hashlib.sha256(raw).hexdigest(),
            "ibge_municipalities": len(ibge), "stn_distinct_names": len(set(stn_names)),
            "matched": len(pairs), "matched_unique_ibge_codes": len({p["codigo_ibge"] for p in pairs}),
            "unmatched_names": unmatched, "ambiguous_matches": ambiguous,
            "crosswalk_file": str(dst) if crosswalk_sha else None,
            "crosswalk_sha256": crosswalk_sha,
            "caution": "Exact normalized names are checked against current IBGE names; historical renamings require separate versioned rules"}

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--resource-id", default=RESOURCE_ID_DEFAULT)
    parser.add_argument("--output", default="build/fed00_stn_csv/QA_FED00_STN_CSV.json")
    args = parser.parse_args()
    report = {"checked_at_utc": datetime.now(timezone.utc).isoformat(),
              "resource_id": args.resource_id, "catalog_url": API,
              "status": "not_started", "stage": "catalog",
              "restrictions": ["National dataset not filtered to SP645",
                               "No municipalities are inferred from source file name",
                               "No change to canonical SQLite R2 or production"]}
    try:
        catalog_raw = fetch(API, MAX_CATALOG_BYTES)
        report["stage"] = "catalog_fetched"
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
        report["stage"] = "csv_download"
        blob = fetch(url, MAX_CSV_BYTES)
        report["stage"] = "csv_fetched"
        content, encoding = decode_text(blob)
        stats = inspect_csv(content)
        report["stage"] = "csv_inspected"
        report.update({"status": "partial", "catalog_sha256": hashlib.sha256(catalog_raw).hexdigest(),
                       "catalog_modified": catalog["result"].get("metadata_modified"),
                       "resource_name": resource.get("name"),
                       "resource_url": url, "resource_created": resource.get("created"),
                       "resource_last_modified": resource.get("last_modified"),
                       "resource_size_declared": resource.get("size"),
                       "download_sha256": hashlib.sha256(blob).hexdigest(),
                       "download_bytes": len(blob), "encoding": encoding,
                       "csv_evidence": stats,
                       "caution": "File header and content month must be checked before assigning fiscal competence"})
        report["stage"] = "ibge_api_crosswalk"
        try:
            crosswalk = check_sp_ibge(stats["sp_municipality_names"], Path(args.output))
            report["ibge_crosswalk_qa"] = crosswalk
            if stats["row_width_mismatches"] == 0 and stats["missing_uf_rows"] == 0 and stats["sp_rows"] > 0 and crosswalk["status"] == "qa_pass":
                report["status"] = "qa_pass"
                report["stage"] = "completed"
            else:
                report["status"] = "partial"
                report["stage"] = "ibge_requires_review"
        except Exception as exc:
            report["status"] = "partial"
            report["stage"] = "ibge_api_failed"
            report["ibge_error"] = f"{type(exc).__name__}: {str(exc)[:350]}"
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
