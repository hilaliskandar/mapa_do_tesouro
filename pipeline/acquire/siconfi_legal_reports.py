from __future__ import annotations

import argparse
import gzip
import json
from pathlib import Path

from pipeline.sources.siconfi import FetchResult, SiconfiClient


def slug(value: str) -> str:
    return value.lower().replace(" ", "-").replace("/", "-")


def write_raw(
    path: Path,
    *,
    endpoint: str,
    year: int,
    entity_id: str,
    params: dict,
    result: FetchResult,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "source": "SICONFI",
        "endpoint": endpoint,
        "year": int(year),
        "entity_id": str(entity_id),
        "parameters": params,
        "status": "observado" if result.items else "ausente",
        "pages": result.pages,
        "requests": result.request_count,
        "items": result.items,
    }
    with gzip.open(path, "wt", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, separators=(",", ":"))


def read_raw(path: Path) -> dict:
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        return json.load(handle)


def valid_raw(path: Path, *, endpoint: str, year: int, entity_id: str) -> bool:
    try:
        payload = read_raw(path)
    except Exception:
        return False
    return (
        payload.get("endpoint") == endpoint
        and int(payload.get("year")) == int(year)
        and str(payload.get("entity_id")) == str(entity_id)
        and payload.get("status") in {"observado", "ausente"}
        and isinstance(payload.get("items"), list)
    )


def acquire_legal_reports(
    *,
    endpoint: str,
    entity_id: str,
    years: list[int],
    annexes: list[str],
    output: Path,
    min_interval: float = 1.05,
    period: int,
    report_type: str,
    sphere: str = "M",
    periodicity: str = "Q",
    branch: str = "E",
) -> dict:
    if endpoint not in {"rreo", "rgf"}:
        raise ValueError(f"Unsupported legal-report endpoint: {endpoint}")

    client = SiconfiClient(min_interval=min_interval)
    completed_now = 0
    reused = 0
    failed = []
    request_count = 0
    artifacts = []

    for year in years:
        for annex in annexes:
            path = (
                output
                / endpoint
                / slug(annex)
                / str(int(year))
                / f"{entity_id}.json.gz"
            )
            if valid_raw(
                path,
                endpoint=endpoint,
                year=int(year),
                entity_id=str(entity_id),
            ):
                reused += 1
                artifacts.append(str(path))
                continue

            try:
                if endpoint == "rreo":
                    result = client.fetch_rreo(
                        year=int(year),
                        period=int(period),
                        entity_id=entity_id,
                        annex=annex,
                        report_type=report_type,
                        sphere=sphere,
                    )
                    params = {
                        "nr_periodo": int(period),
                        "co_tipo_demonstrativo": report_type,
                        "no_anexo": annex,
                        "co_esfera": sphere,
                    }
                else:
                    result = client.fetch_rgf(
                        year=int(year),
                        periodicity=periodicity,
                        period=int(period),
                        entity_id=entity_id,
                        annex=annex,
                        report_type=report_type,
                        sphere=sphere,
                        branch=branch,
                    )
                    params = {
                        "in_periodicidade": periodicity,
                        "nr_periodo": int(period),
                        "co_tipo_demonstrativo": report_type,
                        "no_anexo": annex,
                        "co_esfera": sphere,
                        "co_poder": branch,
                    }

                request_count += result.request_count
                write_raw(
                    path,
                    endpoint=endpoint,
                    year=int(year),
                    entity_id=str(entity_id),
                    params=params,
                    result=result,
                )
                completed_now += 1
                artifacts.append(str(path))
            except Exception as exc:
                failed.append(
                    {
                        "year": int(year),
                        "annex": annex,
                        "error": f"{type(exc).__name__}: {exc}",
                    }
                )

    manifest = {
        "source": "SICONFI",
        "endpoint": endpoint,
        "entity_id": str(entity_id),
        "years": [int(year) for year in years],
        "annexes": list(annexes),
        "completed_now": completed_now,
        "reused": reused,
        "request_count": request_count,
        "failed": failed,
        "artifacts": artifacts,
    }
    manifest_path = output / "manifests" / f"{endpoint}-{entity_id}.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    manifest["manifest_path"] = str(manifest_path)
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Acquire selected SICONFI RREO or RGF reports."
    )
    parser.add_argument("--endpoint", choices=["rreo", "rgf"], required=True)
    parser.add_argument("--entity-id", required=True)
    parser.add_argument("--years", nargs="+", type=int, required=True)
    parser.add_argument("--annexes", nargs="+", required=True)
    parser.add_argument("--periodicity", default="Q")
    parser.add_argument("--period", type=int, required=True)
    parser.add_argument("--report-type")
    parser.add_argument("--sphere", default="M")
    parser.add_argument("--branch", default="E")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--min-interval", type=float, default=1.05)
    args = parser.parse_args()

    report_type = args.report_type or args.endpoint.upper()
    result = acquire_legal_reports(
        endpoint=args.endpoint,
        entity_id=args.entity_id,
        years=args.years,
        annexes=args.annexes,
        output=args.output,
        min_interval=args.min_interval,
        period=args.period,
        report_type=report_type,
        sphere=args.sphere,
        periodicity=args.periodicity,
        branch=args.branch,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))

    if result["failed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
