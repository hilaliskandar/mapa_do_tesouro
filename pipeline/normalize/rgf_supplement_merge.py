from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path


KEYS = ("cod_ibge", "ano")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _read(path: Path) -> tuple[list[str], dict[tuple[str, str], dict]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        rows = {}
        for row in reader:
            key = (row["cod_ibge"], row["ano"])
            if key in rows:
                raise ValueError(f"Duplicate key in {path}: {key}")
            rows[key] = row
    return fieldnames, rows


def merge_fillonly(
    base_csv: Path,
    supplement_csv: Path,
    output_csv: Path,
    manifest_path: Path,
) -> dict:
    base_fields, base_rows = _read(base_csv)
    supplement_fields, supplement_rows = _read(supplement_csv)

    extra_keys = sorted(set(supplement_rows) - set(base_rows))
    if extra_keys:
        raise ValueError(f"Supplement introduced unknown keys: {extra_keys[:20]}")

    value_fields = [
        field
        for field in supplement_fields
        if field not in {*KEYS, "supplement_cell_count"}
    ]
    missing_fields = [field for field in value_fields if field not in base_fields]
    if missing_fields:
        raise ValueError(f"Supplement fields missing from base: {missing_fields}")

    before = {
        field: sum(1 for row in base_rows.values() if row.get(field, "") != "")
        for field in value_fields
    }
    fills: list[dict] = []
    conflicts: list[dict] = []

    merged_rows = {key: dict(row) for key, row in base_rows.items()}
    for key, supplement in supplement_rows.items():
        target = merged_rows[key]
        for field in value_fields:
            incoming = supplement.get(field, "")
            if incoming in ("", None):
                continue
            current = target.get(field, "")
            if current in ("", None):
                target[field] = incoming
                fills.append(
                    {
                        "cod_ibge": key[0],
                        "ano": key[1],
                        "field": field,
                        "value": incoming,
                        "source": "CAPAG_DATALAKE_FILLONLY",
                    }
                )
            elif abs(float(current) - float(incoming)) > 0.01:
                conflicts.append(
                    {
                        "cod_ibge": key[0],
                        "ano": key[1],
                        "field": field,
                        "base": current,
                        "supplement": incoming,
                    }
                )

    if conflicts:
        raise ValueError(f"Fill-only conflicts: {conflicts[:20]}")

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=base_fields)
        writer.writeheader()
        for key in sorted(merged_rows):
            writer.writerow(merged_rows[key])

    after = {
        field: sum(1 for row in merged_rows.values() if row.get(field, "") != "")
        for field in value_fields
    }
    manifest = {
        "rows": len(merged_rows),
        "filled_cells": len(fills),
        "conflicts": 0,
        "coverage_before": before,
        "coverage_after": after,
        "fills_by_field": {
            field: sum(1 for item in fills if item["field"] == field)
            for field in value_fields
        },
        "filled_cell_details": fills,
        "base_sha256": sha256(base_csv),
        "supplement_sha256": sha256(supplement_csv),
        "output_sha256": sha256(output_csv),
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Apply fill-only RGF supplement.")
    parser.add_argument("--base-csv", type=Path, required=True)
    parser.add_argument("--supplement-csv", type=Path, required=True)
    parser.add_argument("--output-csv", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()

    result = merge_fillonly(
        args.base_csv,
        args.supplement_csv,
        args.output_csv,
        args.manifest,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
