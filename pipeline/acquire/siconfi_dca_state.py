from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from pipeline.acquire.siconfi_dca import acquire, load_codes
from pipeline.normalize.dca import normalize_tree

ANNEXES = (
    "DCA-Anexo I-C",
    "DCA-Anexo I-D",
    "DCA-Anexo I-E",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def raw_tree_sha256(root: Path) -> str:
    digest = hashlib.sha256()
    files = sorted(root.glob("**/*.json.gz"))
    for path in files:
        relative = path.relative_to(root).as_posix().encode("utf-8")
        digest.update(relative)
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

    annex_manifests = {}
    for annex in ANNEXES:
        annex_manifests[annex] = acquire(
            geojson,
            [int(year)],
            output,
            annex=annex,
            limit_codes=limit_codes,
            min_interval=min_interval,
        )

    normalization = normalize_tree(output, normalized_csv)

    requested = (
        min(len(codes), int(limit_codes))
        if limit_codes is not None
        else len(codes)
    )
    expected_rows = requested
    if normalization["rows"] != expected_rows:
        raise RuntimeError(
            f"Normalized rows mismatch: {normalization['rows']} != {expected_rows}"
        )

    failed = [
        {
            "annex": annex,
            **failure,
        }
        for annex, manifest in annex_manifests.items()
        for failure in manifest["failed"]
    ]

    manifest = {
        "source": "SICONFI",
        "dataset": "DCA",
        "scope": "SP_645" if expected_municipalities == 645 else "custom",
        "year": int(year),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "municipalities_in_geojson": len(codes),
        "municipalities_requested": requested,
        "annexes": list(ANNEXES),
        "annex_results": {
            annex: {
                "completed_now": value["completed_now"],
                "reused": value["reused"],
                "request_count": value["request_count"],
                "failed_count": len(value["failed"]),
                "manifest_path": value["manifest_path"],
            }
            for annex, value in annex_manifests.items()
        },
        "failed": failed,
        "normalization": normalization,
        "normalized_sha256": sha256(normalized_csv),
        "raw_tree_sha256": raw_tree_sha256(output),
        "minimum_interval_seconds": float(min_interval),
    }

    manifest_path = output / "manifests" / f"state-{int(year)}.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    manifest["manifest_path"] = str(manifest_path)
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Acquire and normalize one full DCA year for the 645 municipalities "
            "of Sao Paulo."
        )
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
