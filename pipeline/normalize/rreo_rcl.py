from __future__ import annotations

import csv
from pathlib import Path

from pipeline.acquire.siconfi_legal_reports import read_raw, slug

ANNEX = "RREO-Anexo 03"
ACCOUNT_CODE = "RREO3ReceitaCorrenteLiquida"
COLUMN = "TOTAL (ÚLTIMOS 12 MESES)"


def normalize_payload(payload: dict) -> dict:
    items = payload.get("items", [])
    matches = [
        item
        for item in items
        if item.get("cod_conta") == ACCOUNT_CODE
        and item.get("coluna") == COLUMN
    ]

    issues: list[dict] = []
    if len(matches) == 1:
        item = matches[0]
        value = item.get("valor")
        rcl_status = "observado" if value is not None else "ausente"
        rcl_value = float(value) if value is not None else None
    elif len(matches) == 0:
        rcl_status = "ausente"
        rcl_value = None
    else:
        rcl_status = "em_revisao"
        rcl_value = None
        issues.append(
            {
                "type": "ambiguous_rcl_match",
                "match_count": len(matches),
            }
        )

    populations = {
        int(item["populacao"])
        for item in items
        if item.get("populacao") is not None
    }
    if len(populations) == 1:
        population = float(next(iter(populations)))
    elif not populations:
        population = None
    else:
        population = None
        issues.append(
            {
                "type": "population_conflict",
                "values": sorted(populations),
            }
        )

    return {
        "cod_ibge": str(payload.get("entity_id") or ""),
        "ano": int(payload["year"]),
        "rreo_rcl_total_12m": rcl_value,
        "populacao_rreo": population,
        "rcl_status": rcl_status,
        "issues": issues,
    }


def normalize_tree(raw_root: Path, output_csv: Path) -> dict:
    annex_root = raw_root / slug(ANNEX)
    paths = sorted(annex_root.glob("*/*.json.gz")) if annex_root.exists() else []

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    issue_count = 0
    observed_count = 0
    with output_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "cod_ibge",
                "ano",
                "rreo_rcl_total_12m",
                "populacao_rreo",
                "qa_issue_count",
            ],
        )
        writer.writeheader()

        for path in paths:
            normalized = normalize_payload(read_raw(path))
            issue_count += len(normalized["issues"])
            if normalized["rcl_status"] == "observado":
                observed_count += 1
            writer.writerow(
                {
                    "cod_ibge": normalized["cod_ibge"],
                    "ano": normalized["ano"],
                    "rreo_rcl_total_12m": (
                        normalized["rreo_rcl_total_12m"]
                        if normalized["rcl_status"] == "observado"
                        else ""
                    ),
                    "populacao_rreo": (
                        normalized["populacao_rreo"]
                        if normalized["populacao_rreo"] is not None
                        else ""
                    ),
                    "qa_issue_count": len(normalized["issues"]),
                }
            )

    return {
        "rows": len(paths),
        "observed_rcl_rows": observed_count,
        "issues": issue_count,
        "output": str(output_csv),
    }
