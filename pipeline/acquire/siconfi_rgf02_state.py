from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode

from pipeline.acquire.siconfi_dca import load_codes
from pipeline.acquire.siconfi_legal_reports import read_raw, slug, valid_raw, write_raw
from pipeline.sources.siconfi import SiconfiClient

ANNEX = "RGF-Anexo 02"
PERIODICITY = "Q"
PERIOD = 3
REPORT_TYPE = "RGF"
SPHERE = "M"
BRANCH = "E"
ENDPOINT_URL = "https://apidatalake.tesouro.gov.br/ords/siconfi/tt/rgf"


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


def source_url(year: int, code: str) -> str:
    return ENDPOINT_URL + "?" + urlencode(
        {
            "an_exercicio": int(year),
            "in_periodicidade": PERIODICITY,
            "nr_periodo": PERIOD,
            "co_tipo_demonstrativo": REPORT_TYPE,
            "no_anexo": ANNEX,
            "co_esfera": SPHERE,
            "co_poder": BRANCH,
            "id_ente": code,
        }
    )


def acquire_state_year(
    geojson: Path,
    year: int,
    output: Path,
    long_csv: Path,
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
    request_count = 0
    failed: list[dict] = []

    for code, name in selected:
        path = output / slug(ANNEX) / str(int(year)) / f"{code}.json.gz"
        if valid_raw(path, endpoint="rgf", year=year, entity_id=code):
            reused += 1
            continue
        try:
            result = client.fetch_rgf(
                year=year,
                periodicity=PERIODICITY,
                period=PERIOD,
                entity_id=code,
                annex=ANNEX,
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
                    "no_anexo": ANNEX,
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
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )

    long_csv.parent.mkdir(parents=True, exist_ok=True)
    municipality_rows = 0
    observed_municipalities = 0
    accounts: set[str] = set()
    with long_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "ano",
                "cod_ibge",
                "municipio",
                "cod_conta",
                "conta",
                "coluna",
                "valor",
                "populacao",
                "fonte_url",
                "fonte",
            ],
        )
        writer.writeheader()
        for code, name in selected:
            path = output / slug(ANNEX) / str(int(year)) / f"{code}.json.gz"
            if not path.exists():
                continue
            payload = read_raw(path)
            items = payload.get("items", [])
            if items:
                observed_municipalities += 1
            for item in items:
                accounts.add(str(item.get("cod_conta") or ""))
                writer.writerow(
                    {
                        "ano": int(year),
                        "cod_ibge": code,
                        "municipio": name,
                        "cod_conta": item.get("cod_conta"),
                        "conta": item.get("conta"),
                        "coluna": item.get("coluna"),
                        "valor": item.get("valor"),
                        "populacao": item.get("populacao"),
                        "fonte_url": source_url(year, code),
                        "fonte": "SICONFI_API",
                    }
                )
                municipality_rows += 1

    manifest = {
        "source": "SICONFI",
        "dataset": "RGF-Anexo 02",
        "scope": "SP_645" if expected_municipalities == 645 else "custom",
        "year": int(year),
        "periodicity": PERIODICITY,
        "period": PERIOD,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "municipalities_in_geojson": len(codes),
        "municipalities_requested": len(selected),
        "observed_municipalities": observed_municipalities,
        "long_rows": municipality_rows,
        "distinct_account_codes": len(accounts),
        "completed_now": completed_now,
        "reused": reused,
        "request_count": request_count,
        "failed": failed,
        "long_csv_sha256": sha256(long_csv),
        "raw_tree_sha256": raw_tree_sha256(output),
        "minimum_interval_seconds": float(min_interval),
    }

    manifest_path = output / "manifests" / f"rgf-02-{int(year)}.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    manifest["manifest_path"] = str(manifest_path)
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Acquire SP RGF Annex 02 preserving official long taxonomy."
    )
    parser.add_argument("--geojson", type=Path, required=True)
    parser.add_argument("--year", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--long-csv", type=Path, required=True)
    parser.add_argument("--min-interval", type=float, default=1.05)
    parser.add_argument("--limit-codes", type=int)
    parser.add_argument("--expected-municipalities", type=int, default=645)
    args = parser.parse_args()

    result = acquire_state_year(
        args.geojson,
        args.year,
        args.output,
        args.long_csv,
        min_interval=args.min_interval,
        limit_codes=args.limit_codes,
        expected_municipalities=args.expected_municipalities,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["failed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
