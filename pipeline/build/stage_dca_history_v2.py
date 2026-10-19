"""Validate and stage a DCA history sidecar in a v2 candidate site tree.

This module does not update v2/manifest.json or any existing observation.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path

CONTRACT = "dca-history-v2-candidate"
EXPECTED_SOURCE_SHA = "67a94313e0f0557bc23f48c78a1396fd02ae10ad7923ea2ac2e5c9f2726f65d5"
YEARS = list(range(2013, 2026))


def _json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"Expected JSON object: {path}")
    return value


def _write(path: Path, item: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(item, sort_keys=True, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8")


def stage(history: Path, v2: Path, *, expected_municipalities: int = 645) -> dict:
    """Validate a whole candidate snapshot before writing anything to the target."""
    manifest = _json(history / "manifest.json")
    if manifest.get("contract") != CONTRACT:
        raise ValueError("Unexpected DCA history contract")
    if manifest.get("source_sha256") != EXPECTED_SOURCE_SHA:
        raise ValueError("DCA history has unexpected canonical source hash")
    if manifest.get("publication_qa") != "not_evaluated":
        raise ValueError("Unexpected publication readiness")
    if manifest.get("years") != YEARS or manifest.get("variable_count") != 26:
        raise ValueError("Unexpected DCA historical variables or years")
    if manifest.get("municipality_count") != expected_municipalities:
        raise ValueError("Unexpected DCA municipality count")
    if manifest.get("municipality_year_count") != expected_municipalities * len(YEARS):
        raise ValueError("Unexpected municipality-year count")
    counts = manifest.get("coverage")
    if not isinstance(counts, dict) or len(counts) != 26:
        raise ValueError("Invalid coverage metadata")
    for field, data in counts.items():
        if not isinstance(data, dict) or set(data) != {"observado", "ausente"}:
            raise ValueError(f"Unexpected coverage state for {field}")
        if (not all(type(v) is int and v >= 0 for v in data.values())
                or sum(data.values()) != expected_municipalities * len(YEARS)):
            raise ValueError(f"Invalid coverage counts for {field}")
    items = sorted((history / "municipalities").glob("*.json"))
    if len(items) != expected_municipalities:
        raise ValueError("Missing or extra municipality files")
    expected_vars = set(counts)
    actual = {key: {"observado": 0, "ausente": 0} for key in expected_vars}
    seen = set()
    hashes = {}
    for item in items:
        record = _json(item)
        code = record.get("codigo_ibge")
        if (not isinstance(code, str) or len(code) != 7 or not code.isascii()
                or not code.isdigit() or code != item.stem or code in seen):
            raise ValueError("Invalid or duplicate municipality file")
        seen.add(code)
        payload = record.get("years")
        if not isinstance(payload, dict) or set(payload) != {str(y) for y in YEARS}:
            raise ValueError(f"Year coverage mismatch for {code}")
        for year, values in payload.items():
            if not isinstance(values, dict) or set(values) != expected_vars:
                raise ValueError(f"Variable mismatch for {code}/{year}")
            for variable, cell in values.items():
                status = cell.get("status") if isinstance(cell, dict) else None
                if status == "ausente":
                    if cell != {"status": "ausente", "value": None}:
                        raise ValueError("Invalid absent cell")
                elif status == "observado":
                    from decimal import Decimal, InvalidOperation
                    if set(cell) != {"status", "value_decimal"}:
                        raise ValueError("Invalid observed cell")
                    try:
                        number = Decimal(cell["value_decimal"])
                    except (InvalidOperation, TypeError) as exc:
                        raise ValueError("Invalid decimal representation") from exc
                    if not number.is_finite():
                        raise ValueError("Nonfinite observed number")
                else:
                    raise ValueError("Unknown observation status")
                actual[variable][status] += 1
        hashes[code] = hashlib.sha256(item.read_bytes()).hexdigest()
    if actual != counts:
        raise ValueError("Coverage mismatch versus municipality files")
    dest = v2 / "history" / "dca"
    catalog = v2 / "catalog" / "historical_sources.json"
    if dest.exists() or catalog.exists():
        raise FileExistsError("Refusing to overwrite existing historical endpoint")
    # All input validation is complete before site mutation.
    shutil.copytree(history, dest)
    discovery = {
        "contract": "api-v2-historical-discovery-candidate",
        "publication_authorized": False,
        "sources": [{
            "id": "finbra_dca_sp645_2013_2025",
            "manifest": "/data/api/v2/history/dca/manifest.json",
            "municipality": "/data/api/v2/history/dca/municipalities/{codigo_ibge}.json",
            "source_sha256": manifest["source_sha256"],
            "years": YEARS,
            "municipality_count": expected_municipalities,
            "variable_count": 26,
            "notes": "Supplementary historical data; no automatic merge with core v2 observations.",
        }],
    }
    _write(catalog, discovery)
    return {"municipalities": len(seen), "years": YEARS,
            "cells_verified": expected_municipalities * len(YEARS) * 26,
            "municipality_file_sha256": hashes, "discovery_path": str(catalog)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("history", type=Path)
    parser.add_argument("v2_output", type=Path)
    args = parser.parse_args()
    result = stage(args.history, args.v2_output)
    print(json.dumps({"municipalities": result["municipalities"],
                      "cells_verified": result["cells_verified"],
                      "discovery_path": result["discovery_path"]}))


if __name__ == "__main__":
    main()
