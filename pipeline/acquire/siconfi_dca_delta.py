from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from pipeline.acquire.siconfi_dca import acquire, annex_slug, load_codes
from pipeline.acquire.siconfi_dca_state import ANNEXES
from pipeline.normalize.dca import normalize_tree
from pipeline.sources.siconfi import read_raw_dca


ANNEX_BY_KEY = {
    "i_c": "DCA-Anexo I-C",
    "i_d": "DCA-Anexo I-D",
    "i_e": "DCA-Anexo I-E",
}


def parse_codes(value: str) -> list[str]:
    text = str(value or "")
    codes = re.findall(r"(?<!\d)\d{7}(?!\d)", text)
    unique = []
    seen = set()
    for code in codes:
        if code not in seen:
            seen.add(code)
            unique.append(code)
    if not unique:
        raise ValueError(
            "At least one 7-digit IBGE municipality code is required."
        )
    return unique


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalize_plan(plan: dict) -> dict[str, list[str]]:
    normalized: dict[str, list[str]] = {}
    for raw_annex, raw_codes in plan.items():
        annex = ANNEX_BY_KEY.get(raw_annex, raw_annex)
        if annex not in ANNEXES:
            raise ValueError(f"Unsupported DCA annex in delta plan: {raw_annex!r}")
        codes = []
        seen = set()
        for raw in raw_codes or []:
            code = str(raw).strip()
            if not re.fullmatch(r"\d{7}", code):
                raise ValueError(f"Invalid IBGE municipality code: {code!r}")
            if code not in seen:
                seen.add(code)
                codes.append(code)
        if codes:
            normalized[annex] = codes
    if not normalized:
        raise ValueError("Delta plan contains no municipality-annex pairs.")
    return normalized


def acquire_delta_plan(
    geojson: Path,
    year: int,
    plan: dict,
    output: Path,
    normalized_csv: Path,
    *,
    min_interval: float = 1.05,
    max_codes: int = 100,
) -> dict:
    annex_plan = normalize_plan(plan)
    available = dict(load_codes(geojson))
    selected = sorted(
        {
            code
            for codes in annex_plan.values()
            for code in codes
        }
    )
    if len(selected) > max_codes:
        raise ValueError(
            f"Delta request is too large: {len(selected)} > {max_codes}. "
            "Use a historical snapshot or split the delta."
        )

    unknown = sorted(set(selected) - set(available))
    if unknown:
        raise ValueError(f"Unknown municipality codes: {unknown}")

    manifests = {}
    source_items = {}
    empty_source_pairs = []

    for annex, codes in annex_plan.items():
        manifests[annex] = acquire(
            geojson,
            [int(year)],
            output,
            annex=annex,
            only_codes=set(codes),
            min_interval=min_interval,
        )
        source_items[annex] = {}
        for code in codes:
            path = (
                output
                / annex_slug(annex)
                / str(int(year))
                / f"{code}.json.gz"
            )
            payload = read_raw_dca(path)
            item_count = len(payload.get("items", []))
            source_items[annex][code] = item_count
            if item_count == 0:
                empty_source_pairs.append(
                    {"annex": annex, "code": code}
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
    requested_pairs = sum(len(codes) for codes in annex_plan.values())

    manifest = {
        "source": "SICONFI",
        "dataset": "DCA",
        "scope": "SP_645_DELTA",
        "year": int(year),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "municipalities_requested": len(selected),
        "municipality_annex_pairs_requested": requested_pairs,
        "codes": selected,
        "municipalities": [
            {"code": code, "name": available[code]}
            for code in selected
        ],
        "annex_plan": annex_plan,
        "annex_results": {
            annex: {
                "codes": annex_plan[annex],
                "completed_now": value["completed_now"],
                "reused": value["reused"],
                "request_count": value["request_count"],
                "failed_count": len(value["failed"]),
                "manifest_path": value["manifest_path"],
                "source_item_counts": source_items[annex],
            }
            for annex, value in manifests.items()
        },
        "failed": failed,
        "empty_source_pairs": empty_source_pairs,
        "empty_source_pair_count": len(empty_source_pairs),
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
    return acquire_delta_plan(
        geojson,
        year,
        {annex: list(codes) for annex in ANNEXES},
        output,
        normalized_csv,
        min_interval=min_interval,
        max_codes=max_codes,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Acquire a targeted DCA delta for explicit SP municipality-annex pairs."
        )
    )
    parser.add_argument("--geojson", type=Path, required=True)
    parser.add_argument("--year", type=int, required=True)
    parser.add_argument("--codes")
    parser.add_argument("--plan", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--normalized-csv", type=Path, required=True)
    parser.add_argument("--min-interval", type=float, default=1.05)
    parser.add_argument("--max-codes", type=int, default=100)
    args = parser.parse_args()

    if bool(args.codes) == bool(args.plan):
        raise SystemExit("Use exactly one of --codes or --plan.")

    if args.plan:
        plan = json.loads(args.plan.read_text(encoding="utf-8"))
        result = acquire_delta_plan(
            args.geojson,
            args.year,
            plan,
            args.output,
            args.normalized_csv,
            min_interval=args.min_interval,
            max_codes=args.max_codes,
        )
    else:
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
