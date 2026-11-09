#!/usr/bin/env python3
"""FED00: make an immutable, audited local copy of ONE official STN resource.

Only downloads/validates the source; never writes SQLite or uploads to R2.
The accompanying Actions workflow performs R2 upload+readback separately.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

from pipeline.acquire.probe_stn_transfer_csv import (
    API, MAX_CATALOG_BYTES, MAX_CSV_BYTES, RESOURCE_ID_DEFAULT,
    decode_text, fetch, inspect_csv,
)

PINNED_SHA256 = "097638cec48145ac0f509d526be49d40929d177ef3a2ae3b7f77c0acd990cf24"
PINNED_PERIOD = "2026/09"
PINNED_ROWS = 126807
PINNED_SP_ROWS = 13889

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-output", type=Path, required=True)
    parser.add_argument("--report-output", type=Path, required=True)
    parser.add_argument("--resource-id", default=RESOURCE_ID_DEFAULT)
    args = parser.parse_args()
    report: dict = {"collected_at_utc": datetime.now(timezone.utc).isoformat(),
                    "source_api": API, "resource_id": args.resource_id,
                    "status": "not_started", "stage": "catalog",
                    "purpose": "Pinned source preservation, not fiscal homologation"}
    try:
        catalog_bytes = fetch(API, MAX_CATALOG_BYTES)
        catalog = json.loads(catalog_bytes.decode("utf-8-sig"))
        assert catalog["success"] is True
        resources = [x for x in catalog["result"]["resources"] if x.get("id")==args.resource_id]
        if len(resources) != 1:
            raise ValueError("resource_id_missing_or_duplicate")
        resource = resources[0]
        url = str(resource["url"])
        parsed = urlparse(url)
        if parsed.scheme != "https" or parsed.hostname != "www.tesourotransparente.gov.br":
            raise ValueError("unexpected_resource_origin")
        report["stage"] = "download"
        blob = fetch(url, MAX_CSV_BYTES)
        sha = hashlib.sha256(blob).hexdigest()
        report["download_sha256"] = sha
        report["download_bytes"] = len(blob)
        report["resource_url"] = url
        report["resource_name"] = resource.get("name")
        report["resource_catalog_size"] = resource.get("size")
        if sha != PINNED_SHA256:
            raise ValueError("source_hash_changed_quarantine_new_version")
        report["stage"] = "csv_validate"
        text, encoding = decode_text(blob)
        stats = inspect_csv(text)
        report["csv_encoding"] = encoding
        report["source_field_names"] = stats["column_names"]
        report["row_count_national"] = stats["row_count_national_not_sp"]
        report["row_count_sp"] = stats["sp_rows"]
        report["municipal_names_sp"] = stats["sp_distinct_municipality_names"]
        report["national_period_counts"] = stats["all_period_counts"]
        report["sp_period_counts"] = stats["sp_period_counts"]
        report["cell_format_counts_sp"] = stats["sp_monetary_cell_patterns"]
        report["repeated_potential_grain_sp"] = stats["sp_repeated_potential_grain_rows"]
        valid_cells = all(not set(v) - {"plain_integer", "decimal_dot"}
                          for v in stats["sp_monetary_cell_patterns"].values())
        ok = (
            stats["row_count_national_not_sp"] == PINNED_ROWS and
            stats["sp_rows"] == PINNED_SP_ROWS and
            stats["sp_distinct_municipality_names"] == 645 and
            stats["all_period_counts"] == {PINNED_PERIOD: PINNED_ROWS} and
            stats["sp_period_counts"] == {PINNED_PERIOD: PINNED_SP_ROWS} and
            stats["row_width_mismatches"] == 0 and
            stats["missing_uf_rows"] == 0 and
            stats["sp_blank_item_transferencia_rows"] == 0 and
            stats["sp_repeated_potential_grain_rows"] == 0 and
            valid_cells
        )
        if not ok:
            raise ValueError("pinned_stn_source_contract_changed_quarantine")
        args.source_output.parent.mkdir(parents=True, exist_ok=True)
        args.source_output.write_bytes(blob)
        report["status"] = "qa_pass_source_snapshot_only"
        report["stage"] = "verified_local"
        report["limitations"] = [
            "This audit does not prove agreement of STN labels with SICONFI/DCA revenue",
            "Decendial entries cannot yet be summed as municipal receipt values",
            "The file name 202610 is not the competence; source content is 2026/09",
            "A changed official source must be versioned and separately validated, never silently overwritten",
        ]
    except Exception as exc:
        report["status"] = "failed_or_changed_source"
        report["error"] = f"{type(exc).__name__}: {str(exc)[:400]}"
    args.report_output.parent.mkdir(parents=True, exist_ok=True)
    args.report_output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: report.get(k) for k in
                      ("status", "stage", "download_sha256", "row_count_national", "row_count_sp", "error")},
                     ensure_ascii=False))
    if report["status"] != "qa_pass_source_snapshot_only":
        raise SystemExit(2)

if __name__ == "__main__":
    main()
