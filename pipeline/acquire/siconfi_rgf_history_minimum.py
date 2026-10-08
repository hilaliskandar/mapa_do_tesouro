from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from pipeline.acquire.siconfi_dca import load_codes
from pipeline.acquire.siconfi_legal_reports import read_raw, slug, valid_raw, write_raw
from pipeline.normalize.rgf_legal import ANNEX_01, normalize_annex01
from pipeline.normalize.rgf02 import COLUMN as RGF02_COLUMN, FIELD_CODES as RGF02_FIELD_CODES
from pipeline.sources.siconfi import SiconfiClient

ANNEX_02 = "RGF-Anexo 02"
PERIODICITY = "Q"
PERIOD = 3
REPORT_TYPE = "RGF"
SPHERE = "M"
BRANCH = "E"

FIELDS = [
    "rgf_despesa_total_pessoal",
    "rgf_rcl_denominador_legal",
    "rgf_dtp_percentual_rcl",
    "rgf02_divida_consolidada",
    "rgf02_divida_consolidada_liquida",
    "rgf02_dc_percentual_rcl",
    "rgf02_dcl_percentual_rcl",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalize_annex02_payload(payload: dict) -> dict:
    reverse = {
        code: field
        for field, code in RGF02_FIELD_CODES.items()
        if field in {
            "rgf02_divida_consolidada",
            "rgf02_divida_consolidada_liquida",
            "rgf02_dc_percentual_rcl",
            "rgf02_dcl_percentual_rcl",
        }
    }
    row = {
        "cod_ibge": str(payload.get("entity_id") or ""),
        "ano": int(payload["year"]),
    }
    issues = []
    for item in payload.get("items", []):
        if item.get("coluna") != RGF02_COLUMN:
            continue
        field = reverse.get(item.get("cod_conta"))
        if field is None:
            continue
        value = item.get("valor")
        if field in row and row[field] not in (None, value):
            issues.append(
                {
                    "type": "ambiguous_match",
                    "variable": field,
                    "first": row[field],
                    "second": value,
                }
            )
        else:
            row[field] = float(value) if value is not None else None
    for field in reverse.values():
        row.setdefault(field, None)
    row["issues"] = issues
    row["qa_issue_count"] = len(issues)
    return row


def acquire_history_shard(
    geojson: Path,
    year: int,
    output: Path,
    normalized_csv: Path,
    *,
    start_index: int = 0,
    limit_codes: int | None = None,
    min_interval: float = 1.05,
    expected_municipalities: int = 645,
) -> dict:
    codes = load_codes(geojson)
    if len(codes) != expected_municipalities:
        raise ValueError(
            f"Unexpected municipality count: {len(codes)} != {expected_municipalities}"
        )
    if start_index < 0 or start_index > len(codes):
        raise ValueError(f"Invalid start_index: {start_index}")
    selected = codes[start_index:]
    if limit_codes is not None:
        selected = selected[:limit_codes]

    client = SiconfiClient(min_interval=min_interval)
    failed = []
    completed_now = reused = request_count = 0

    for code, name in selected:
        for annex in (ANNEX_01, ANNEX_02):
            path = output / slug(annex) / str(int(year)) / f"{code}.json.gz"
            if valid_raw(path, endpoint="rgf", year=year, entity_id=code):
                reused += 1
                continue
            try:
                result = client.fetch_rgf(
                    year=year,
                    periodicity=PERIODICITY,
                    period=PERIOD,
                    entity_id=code,
                    annex=annex,
                    report_type=REPORT_TYPE,
                    sphere=SPHERE,
                    branch=BRANCH,
                )
                request_count += result.request_count
                write_raw(
                    path,
                    endpoint="rgf",
                    year=year,
                    entity_id=code,
                    params={
                        "in_periodicidade": PERIODICITY,
                        "nr_periodo": PERIOD,
                        "co_tipo_demonstrativo": REPORT_TYPE,
                        "no_anexo": annex,
                        "co_esfera": SPHERE,
                        "co_poder": BRANCH,
                    },
                    result=result,
                )
                completed_now += 1
            except Exception as exc:
                failed.append(
                    {
                        "code": code,
                        "name": name,
                        "annex": annex,
                        "error": f"{type(exc).__name__}: {exc}",
                    }
                )

    normalized_csv.parent.mkdir(parents=True, exist_ok=True)
    coverage = {field: 0 for field in FIELDS}
    issue_count = 0
    rows = 0
    fieldnames = ["cod_ibge", "ano", *FIELDS, "qa_issue_count"]

    with normalized_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for code, _name in selected:
            a1 = output / slug(ANNEX_01) / str(int(year)) / f"{code}.json.gz"
            a2 = output / slug(ANNEX_02) / str(int(year)) / f"{code}.json.gz"
            if not a1.exists() or not a2.exists():
                continue
            n1 = normalize_annex01(read_raw(a1))
            n2 = normalize_annex02_payload(read_raw(a2))
            row = {
                "cod_ibge": code,
                "ano": int(year),
                **{field: n1.get(field) for field in FIELDS if field.startswith("rgf_")},
                **{field: n2.get(field) for field in FIELDS if field.startswith("rgf02_")},
            }
            row["qa_issue_count"] = n1["qa_issue_count"] + n2["qa_issue_count"]
            issue_count += row["qa_issue_count"]
            for field in FIELDS:
                if row.get(field) is not None:
                    coverage[field] += 1
            writer.writerow(
                {
                    key: "" if row.get(key) is None else row.get(key)
                    for key in fieldnames
                }
            )
            rows += 1

    result = {
        "year": int(year),
        "start_index": int(start_index),
        "municipalities_requested": len(selected),
        "expected_raw_files": len(selected) * 2,
        "completed_now": completed_now,
        "reused": reused,
        "request_count": request_count,
        "failed": failed,
        "normalization": {
            "rows": rows,
            "issues": issue_count,
            "coverage": coverage,
        },
        "normalized_sha256": sha256(normalized_csv),
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    manifest = output / "manifests" / f"rgf-history-{year}-{start_index}.json"
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Acquire minimal historical RGF A01/A02 state shard."
    )
    parser.add_argument("--geojson", type=Path, required=True)
    parser.add_argument("--year", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--normalized-csv", type=Path, required=True)
    parser.add_argument("--start-index", type=int, default=0)
    parser.add_argument("--limit-codes", type=int)
    parser.add_argument("--min-interval", type=float, default=1.05)
    args = parser.parse_args()
    result = acquire_history_shard(
        args.geojson,
        args.year,
        args.output,
        args.normalized_csv,
        start_index=args.start_index,
        limit_codes=args.limit_codes,
        min_interval=args.min_interval,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["failed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
