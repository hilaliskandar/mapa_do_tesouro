from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def combine(input_root: Path, output_csv: Path, summary: Path) -> dict:
    paths = sorted(input_root.glob("**/rgf_history_*.csv"))
    if not paths:
        raise ValueError("No historical RGF shard CSVs found.")

    rows = {}
    fieldnames = None
    for path in paths:
        with path.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            current_fields = list(reader.fieldnames or [])
            if fieldnames is None:
                fieldnames = current_fields
            elif current_fields != fieldnames:
                raise ValueError(f"Schema mismatch: {path}")
            for row in reader:
                key = (row["cod_ibge"], row["ano"])
                if key in rows:
                    raise ValueError(f"Duplicate key: {key}")
                rows[key] = row

    if len(rows) != 1290:
        raise ValueError(f"Expected 1290 municipality-year rows, got {len(rows)}")

    coverage = {}
    for year in ("2023", "2024"):
        subset = [row for (code, y), row in rows.items() if y == year]
        if len(subset) != 645:
            raise ValueError(f"Expected 645 rows in {year}, got {len(subset)}")
        coverage[year] = {
            field: sum(row.get(field, "") != "" for row in subset)
            for field in fieldnames
            if field.startswith("rgf")
        }

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for key in sorted(rows, key=lambda item: (item[1], item[0])):
            writer.writerow(rows[key])

    result = {
        "rows": len(rows),
        "years": [2023, 2024],
        "shard_files": len(paths),
        "coverage": coverage,
        "sha256": sha256(output_csv),
    }
    summary.parent.mkdir(parents=True, exist_ok=True)
    summary.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Combine Gate E RGF historical shards.")
    parser.add_argument("--input-root", type=Path, required=True)
    parser.add_argument("--output-csv", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()
    print(
        json.dumps(
            combine(args.input_root, args.output_csv, args.summary),
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
