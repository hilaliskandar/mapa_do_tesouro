from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from pipeline.acquire.siconfi_dca import load_codes
from pipeline.acquire.siconfi_legal_reports import (
    slug,
    valid_raw,
    write_raw,
)
from pipeline.normalize.rreo_rcl import ANNEX, normalize_tree
from pipeline.sources.siconfi import SiconfiClient

PERIOD = 6
REPORT_TYPE = "RREO"
SPHERE = "M"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def raw_tree_sha256(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(root.glob("**/*.json.gz")):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(bytes.fromhex(sha256(path)))
    return digest.hexdigest()


def acquire_state_year(
    geojson: Path,
    year: int,
    output: Path,
    normalized_csv: Path,
    *,
    min_interval: float = 1.05,
    limit_codes: int | None = None,
    expected_municipalities: int | None = 645,
) -> dict:
    codes = load_codes(geojson)
    if expected_municipalities is not None and len(codes) != expected_municipalities:
        raise ValueError(
            f"Unexpected municipality count: {len(codes)} != {expected_municipalities}"
        )

    selected = codes[:limit_codes] if limit_codes is not None else codes
    client = SiconfiClient(min_interval=min_interval)
    completed_now = 0
    reused = 0
    failed = []
    requests = 0

    params = {
        "nr_periodo": PERIOD,
        "co_tipo_demonstrativo": REPORT_TYPE,
        "no_anexo": ANNEX,
        "co_esfera": SPHERE,
    }

    for code, name in selected:
        path = output / slug(ANNEX) / str(int(year)) / f"{code}.json.gz"
        if valid_raw(path, endpoint="rreo", year=year, entity_id=code):
            reused += 1
            continue

        try:
            result = client.fetch_rreo(
                year=year,
                period=PERIOD,
                entity_id=code,
                annex=ANNEX,
                report_type=REPORT_TYPE,
                sphere=SPHERE,
            )
            requests += result.request_count
            write_raw(
                path,
                endpoint="rreo",
                year=year,
                entity_id=code,
                params=params,
                result=result,
            )
            completed_now += 1
        except Exception as exc:
            failed.append(
                {
                    "code": code,
                    "name": name,
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )

    normalization = normalize_tree(output, normalized_csv)
    if normalization["rows"] != len(selected):
        raise RuntimeError(
            f"Normalized rows mismatch: {normalization['rows']} != {len(selected)}"
        )

    manifest = {
        "source": "SICONFI",
        "dataset": "RREO",
        "scope": "SP_645" if expected_municipalities == 645 else "custom",
        "year": int(year),
        "period": PERIOD,
        "annex": ANNEX,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "municipalities_in_geojson": len(codes),
        "municipalities_requested": len(selected),
        "completed_now": completed_now,
        "reused": reused,
        "request_count": requests,
        "failed": failed,
        "normalization": normalization,
        "normalized_sha256": sha256(normalized_csv),
        "raw_tree_sha256": raw_tree_sha256(output),
        "minimum_interval_seconds": float(min_interval),
    }

    manifest_path = output / "manifests" / f"rreo-rcl-{int(year)}.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    manifest["manifest_path"] = str(manifest_path)
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Acquire RREO Annex 03 annual RCL for Sao Paulo municipalities."
    )
    parser.add_argument("--geojson", type=Path, required=True)
    parser.add_argument("--year", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--normalized-csv", type=Path, required=True)
    parser.add_argument("--min-interval", type=float, default=1.05)
    parser.add_argument("--limit-codes", type=int)
    parser.add_argument("--expected-municipalities", type=int, default=645)
    args = parser.parse_args()

    result = acquire_state_year(
        args.geojson,
        args.year,
        args.output,
        args.normalized_csv,
        min_interval=args.min_interval,
        limit_codes=args.limit_codes,
        expected_municipalities=args.expected_municipalities,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
