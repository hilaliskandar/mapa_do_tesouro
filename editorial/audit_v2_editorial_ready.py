"""Audit an existing materialized API v2 snapshot for editorial use.

No network, credentials, fiscal calculations or deployment.
Usage: python -m editorial.audit_v2_editorial_ready --site <site-folder> --output <report.json>
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

PERCENTAGE_FIELDS = ("storage_scale", "display_multiplier", "scale_verified")
REQUIRED = ("manifest.json", "catalog/variables.json", "catalog/universes.json",
            "qa/readiness.json")


def audit(site: Path) -> dict:
    root = site / "data" / "api" / "v2"
    missing = [p for p in REQUIRED if not (root / p).is_file()]
    if missing:
        return {"status": "blocked", "reason": "required_files_missing",
                "missing": missing, "snapshot": str(root)}
    try:
        manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
        catalog = json.loads((root / "catalog/variables.json").read_text(encoding="utf-8"))
        universes = json.loads((root / "catalog/universes.json").read_text(encoding="utf-8"))
        readiness = json.loads((root / "qa/readiness.json").read_text(encoding="utf-8"))
    except (ValueError, OSError) as exc:
        return {"status": "blocked", "reason": "invalid_snapshot",
                "error": str(exc)}

    # Accept the two common catalogue envelopes, but never guess indicator metadata.
    if isinstance(catalog, list):
        variables = catalog
    elif isinstance(catalog, dict):
        variables = catalog.get("variables", [])
    else:
        variables = []
    if not isinstance(variables, list):
        variables = []
    indicators = []
    no_cautions = []
    uncertified_percentages = []
    for item in variables:
        if not isinstance(item, dict):
            continue
        key = item.get("variable_id") or item.get("id") or item.get("codigo")
        if not key:
            continue
        indicators.append(str(key))
        if not item.get("cautelas"):
            no_cautions.append(str(key))
        if item.get("unidade") in ("percentual", "%"):
            if (item.get("scale_verified") is not True or
                item.get("storage_scale") in (None, "nao_documentada") or
                item.get("display_multiplier") is None):
                uncertified_percentages.append(str(key))

    return {
        "status": "candidate_only",
        "contract": "api_v2",
        "snapshot": str(root),
        "manifest": manifest,
        "counts": {"variables_recognized": len(indicators),
                   "universe_catalog_size": len(universes) if isinstance(universes, list) else None},
        "checks": {"missing_cautions": sorted(no_cautions),
                   "uncertified_percentages": sorted(uncertified_percentages),
                   "readiness_payload_present": True},
        "raw_readiness": readiness,
        "publication_authorized": False,
        "notes": [
            "Do not infer deployment from private build files.",
            "This inventory does not certify fiscal values or temporal comparability.",
            "Inspect catalog metadata schema before promoting any field."
        ]
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    report = audit(args.site)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False, default=str),
                           encoding="utf-8")
    print(f"{report['status']}: {args.output}")
    return 0 if report["status"] == "candidate_only" else 2


if __name__ == "__main__":
    raise SystemExit(main())
