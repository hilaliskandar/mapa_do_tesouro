from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from pipeline.sources.siconfi import SiconfiClient, read_raw_dca, write_raw_dca


def annex_slug(annex: str | None) -> str:
    if annex is None:
        return "all"
    return (
        annex.lower()
        .replace("dca-anexo ", "")
        .replace(" ", "-")
        .replace("/", "-")
    )


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
    only_codes: set[str] | None = None,
    min_interval: float = 1.05,
) -> dict:
    codes = load_codes(geojson)
    if only_codes is not None and limit_codes is not None:
        raise ValueError("only_codes and limit_codes are mutually exclusive.")
    if only_codes is not None:
        requested = {str(code).strip() for code in only_codes if str(code).strip()}
        available = {code for code, _ in codes}
        unknown = sorted(requested - available)
        if unknown:
            raise ValueError(f"Unknown municipality codes: {unknown}")
        codes = [(code, name) for code, name in codes if code in requested]
    elif limit_codes is not None:
        codes = codes[:limit_codes]

    client = SiconfiClient(min_interval=min_interval)
    completed = 0
    reused = 0
    failed: list[dict] = []

    for year in sorted(set(int(year) for year in years)):
        for code, name in codes:
            target = output / annex_slug(annex) / str(year) / f"{code}.json.gz"
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
    manifest_text = json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    (output / "manifest.json").write_text(
        manifest_text,
        encoding="utf-8",
    )
    years_key = (
        str(manifest["years"][0])
        if len(manifest["years"]) == 1
        else f'{manifest["years"][0]}-{manifest["years"][-1]}'
    )
    manifest_dir = output / "manifests"
    manifest_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = manifest_dir / (
        f'{annex_slug(annex)}-{years_key}.json'
    )
    manifest_path.write_text(manifest_text, encoding="utf-8")
    manifest["manifest_path"] = str(manifest_path)
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
    parser.add_argument("--only-codes", nargs="+")
    parser.add_argument("--min-interval", type=float, default=1.05)
    args = parser.parse_args()

    manifest = acquire(
        args.geojson,
        args.years,
        args.output,
        annex=args.annex,
        limit_codes=args.limit_codes,
        only_codes=set(args.only_codes) if args.only_codes else None,
        min_interval=args.min_interval,
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
