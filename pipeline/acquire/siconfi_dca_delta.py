from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from pipeline.acquire.siconfi_dca import acquire, load_codes
from pipeline.acquire.siconfi_dca_state import ANNEXES
from pipeline.normalize.dca import normalize_tree


def parse_codes(value: str) -> list[str]:
    codes = [
        token.strip()
        for token in re.split(r"[,;\s]+", value or "")
        if token.strip()
    ]
    unique = []
    seen = set()
    for code in codes:
        if not re.fullmatch(r"\d{7}", code):
            raise ValueError(f"Invalid IBGE municipality code: {code!r}")
        if code not in seen:
            seen.add(code)
            unique.append(code)
    if not unique:
        raise ValueError("At least one municipality code is required.")
    return unique


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def acquire_delta_year(
    geojson: Path,
    year: int,
    codes: list[str],
    output: Path,
    normalized_csv: Path,
    *,
    min_interval: float = 1.05,
    max_codes: int = 100,
) -> dict:
    if len(codes) > max_codes:
        raise ValueError(
            f"Delta request is too large: {len(codes)} > {max_codes}. "
            "Use a historical snapshot or split the delta."
        )

    available = dict(load_codes(geojson))
    unknown = sorted(set(codes) - set(available))
    if unknown:
        raise ValueError(f"Unknown municipality codes: {unknown}")

    selected = sorted(set(codes))
    manifests = {}
    for annex in ANNEXES:
        manifests[annex] = acquire(
            geojson,
            [int(year)],
            output,
            annex=annex,
            only_codes=set(selected),
            min_interval=min_interval,
        )

    normalization = normalize_tree(output, normalized_csv)
    if normalization["rows"] != len(selected):
        raise RuntimeError(
            f"Normalized rows mismatch: {normalization['rows']} != {len(selected)}"
        )

    failed = [
        {"annex": annex, **failure}
        for annex, manifest in manifests.items()
        for failure in manifest["failed"]
    ]

    manifest = {
        "source": "SICONFI",
        "dataset": "DCA",
        "scope": "SP_645_DELTA",
        "year": int(year),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "municipalities_requested": len(selected),
        "codes": selected,
        "municipalities": [
            {"code": code, "name": available[code]}
            for code in selected
        ],
        "annexes": list(ANNEXES),
        "annex_results": {
            annex: {
                "completed_now": value["completed_now"],
                "reused": value["reused"],
                "request_count": value["request_count"],
                "failed_count": len(value["failed"]),
                "manifest_path": value["manifest_path"],
            }
            for annex, value in manifests.items()
        },
        "failed": failed,
        "normalization": normalization,
        "normalized_sha256": sha256(normalized_csv),
        "minimum_interval_seconds": float(min_interval),
    }

    manifest_path = output / "manifests" / f"delta-{int(year)}.json"
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
            "Acquire a targeted DCA delta for an explicit list of SP municipality codes."
        )
    )
    parser.add_argument("--geojson", type=Path, required=True)
    parser.add_argument("--year", type=int, required=True)
    parser.add_argument("--codes", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--normalized-csv", type=Path, required=True)
    parser.add_argument("--min-interval", type=float, default=1.05)
    parser.add_argument("--max-codes", type=int, default=100)
    args = parser.parse_args()

    result = acquire_delta_year(
        args.geojson,
        args.year,
        parse_codes(args.codes),
        args.output,
        args.normalized_csv,
        min_interval=args.min_interval,
        max_codes=args.max_codes,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
