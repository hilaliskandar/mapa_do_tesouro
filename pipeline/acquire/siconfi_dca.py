from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from pipeline.sources.siconfi import SiconfiClient, read_raw_dca, write_raw_dca


def load_codes(geojson: Path) -> list[tuple[str, str]]:
    payload = json.loads(geojson.read_text(encoding="utf-8"))
    codes = sorted(
        (
            str(feature["properties"]["id"]),
            str(feature["properties"].get("name") or ""),
        )
        for feature in payload["features"]
    )
    if len({code for code, _ in codes}) != len(codes):
        raise ValueError("Duplicate municipality codes in GeoJSON.")
    return codes


def acquire(
    geojson: Path,
    years: list[int],
    output: Path,
    *,
    annex: str | None = None,
    limit_codes: int | None = None,
    min_interval: float = 1.05,
) -> dict:
    codes = load_codes(geojson)
    if limit_codes is not None:
        codes = codes[:limit_codes]

    client = SiconfiClient(min_interval=min_interval)
    completed = 0
    reused = 0
    failed: list[dict] = []

    for year in sorted(set(int(year) for year in years)):
        for code, name in codes:
            target = output / str(year) / f"{code}.json.gz"
            if target.exists():
                try:
                    payload = read_raw_dca(target)
                    if (
                        str(payload.get("entity_id")) == code
                        and int(payload.get("year")) == year
                        and isinstance(payload.get("items"), list)
                    ):
                        reused += 1
                        continue
                except Exception:
                    pass

            try:
                result = client.fetch_dca(
                    year=year,
                    entity_id=code,
                    annex=annex,
                )
                write_raw_dca(
                    target,
                    year=year,
                    entity_id=code,
                    result=result,
                    annex=annex,
                )
                completed += 1
            except Exception as exc:
                failed.append(
                    {
                        "year": year,
                        "entity_id": code,
                        "municipality": name,
                        "error": f"{type(exc).__name__}: {exc}",
                    }
                )

    manifest = {
        "source": "SICONFI",
        "endpoint": "dca",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "annex": annex,
        "years": sorted(set(int(year) for year in years)),
        "municipalities_requested": len(codes),
        "completed_now": completed,
        "reused": reused,
        "failed": failed,
        "request_count": client.request_count,
        "minimum_interval_seconds": min_interval,
    }
    output.mkdir(parents=True, exist_ok=True)
    (output / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Acquire raw DCA records from the official SICONFI API."
    )
    parser.add_argument("--geojson", type=Path, required=True)
    parser.add_argument("--years", nargs="+", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--annex")
    parser.add_argument("--limit-codes", type=int)
    parser.add_argument("--min-interval", type=float, default=1.05)
    args = parser.parse_args()

    manifest = acquire(
        args.geojson,
        args.years,
        args.output,
        annex=args.annex,
        limit_codes=args.limit_codes,
        min_interval=args.min_interval,
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
