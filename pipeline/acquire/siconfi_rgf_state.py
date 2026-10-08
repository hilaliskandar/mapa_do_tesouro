from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from pipeline.acquire.siconfi_dca import load_codes
from pipeline.acquire.siconfi_legal_reports import slug, valid_raw, write_raw, read_raw
from pipeline.normalize.rgf_legal import ANNEX_01, ANNEX_05, normalize_annex01, normalize_annex05
from pipeline.sources.siconfi import SiconfiClient

PERIODICITY = "Q"
PERIOD = 3
REPORT_TYPE = "RGF"
SPHERE = "M"
BRANCH = "E"


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
    start_index: int = 0,
    expected_municipalities: int | None = 645,
) -> dict:
    codes = load_codes(geojson)
    if expected_municipalities is not None and len(codes) != expected_municipalities:
        raise ValueError(
            f"Unexpected municipality count: {len(codes)} != {expected_municipalities}"
        )
    if start_index < 0 or start_index > len(codes):
        raise ValueError(f"Invalid start_index: {start_index}")
    tail = codes[start_index:]
    selected = tail[:limit_codes] if limit_codes is not None else tail
    client = SiconfiClient(min_interval=min_interval)

    completed_now = 0
    reused = 0
    request_count = 0
    failed: list[dict] = []

    for code, name in selected:
        for annex in (ANNEX_01, ANNEX_05):
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

    fieldnames = [
        "cod_ibge",
        "ano",
        "rgf_despesa_total_pessoal",
        "rgf_rcl_denominador_legal",
        "rgf_dtp_percentual_rcl",
        "rgf_caixa_bruta_nao_vinculada",
        "rgf_rp_liquidados_anteriores_nao_vinculados",
        "rgf_rp_liquidados_exercicio_nao_vinculados",
        "rgf_rp_nao_liquidados_anteriores_nao_vinculados",
        "rgf_demais_obrigacoes_nao_vinculadas",
        "rgf_caixa_liquida_antes_rpnp",
        "rgf_rp_nao_liquidados_exercicio_nao_vinculados",
        "rgf_caixa_liquida_apos_rpnp",
        "qa_issue_count",
    ]

    normalized_csv.parent.mkdir(parents=True, exist_ok=True)
    coverage = {field: 0 for field in fieldnames if field.startswith("rgf_")}
    issue_count = 0
    rows = 0

    with normalized_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for code, _name in selected:
            a1_path = output / slug(ANNEX_01) / str(int(year)) / f"{code}.json.gz"
            a5_path = output / slug(ANNEX_05) / str(int(year)) / f"{code}.json.gz"
            if not a1_path.exists() or not a5_path.exists():
                continue

            a1 = normalize_annex01(read_raw(a1_path))
            a5 = normalize_annex05(read_raw(a5_path))
            row = {
                "cod_ibge": code,
                "ano": int(year),
                **{key: a1[key] for key in a1 if key.startswith("rgf_")},
                **{key: a5[key] for key in a5 if key.startswith("rgf_")},
            }
            row["qa_issue_count"] = a1["qa_issue_count"] + a5["qa_issue_count"]
            issue_count += row["qa_issue_count"]
            for field in coverage:
                if row.get(field) is not None:
                    coverage[field] += 1
            writer.writerow({key: "" if row.get(key) is None else row.get(key) for key in fieldnames})
            rows += 1

    manifest = {
        "source": "SICONFI",
        "dataset": "RGF",
        "scope": "SP_645" if expected_municipalities == 645 else "custom",
        "year": int(year),
        "periodicity": PERIODICITY,
        "period": PERIOD,
        "annexes": [ANNEX_01, ANNEX_05],
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "municipalities_in_geojson": len(codes),
        "municipalities_requested": len(selected),
        "start_index": int(start_index),
        "expected_raw_files": len(selected) * 2,
        "completed_now": completed_now,
        "reused": reused,
        "request_count": request_count,
        "failed": failed,
        "normalization": {
            "rows": rows,
            "issues": issue_count,
            "coverage": coverage,
            "output": str(normalized_csv),
        },
        "normalized_sha256": sha256(normalized_csv),
        "raw_tree_sha256": raw_tree_sha256(output),
        "minimum_interval_seconds": float(min_interval),
    }

    manifest_path = output / "manifests" / f"rgf-01-05-{int(year)}.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    manifest["manifest_path"] = str(manifest_path)
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Acquire SP RGF Annexes 01 and 05.")
    parser.add_argument("--geojson", type=Path, required=True)
    parser.add_argument("--year", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--normalized-csv", type=Path, required=True)
    parser.add_argument("--min-interval", type=float, default=1.05)
    parser.add_argument("--limit-codes", type=int)
    parser.add_argument("--start-index", type=int, default=0)
    parser.add_argument("--expected-municipalities", type=int, default=645)
    args = parser.parse_args()

    result = acquire_state_year(
        args.geojson,
        args.year,
        args.output,
        args.normalized_csv,
        min_interval=args.min_interval,
        limit_codes=args.limit_codes,
        start_index=args.start_index,
        expected_municipalities=args.expected_municipalities,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["failed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
