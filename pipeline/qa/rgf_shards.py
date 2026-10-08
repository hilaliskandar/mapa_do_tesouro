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


def combine_shards(input_root: Path, output_csv: Path, expected_rows: int = 645) -> dict:
    paths = sorted(input_root.glob("**/rgf_01_05_*_*.csv"))
    if not paths:
        raise ValueError("No RGF shard CSVs found.")

    rows_by_key: dict[tuple[str, str], dict] = {}
    fieldnames: list[str] | None = None
    duplicates: list[tuple[str, str]] = []

    for path in paths:
        with path.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            if fieldnames is None:
                fieldnames = list(reader.fieldnames or [])
            elif list(reader.fieldnames or []) != fieldnames:
                raise ValueError(f"Shard schema mismatch: {path}")
            for row in reader:
                key = (row["cod_ibge"], row["ano"])
                if key in rows_by_key:
                    duplicates.append(key)
                    continue
                rows_by_key[key] = row

    if duplicates:
        raise ValueError(f"Duplicate municipality-year keys: {duplicates[:20]}")
    if len(rows_by_key) != expected_rows:
        raise ValueError(
            f"Combined row count mismatch: {len(rows_by_key)} != {expected_rows}"
        )
    if fieldnames is None:
        raise ValueError("Missing shard schema.")

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for key in sorted(rows_by_key):
            writer.writerow(rows_by_key[key])

    coverage = {
        field: sum(1 for row in rows_by_key.values() if row.get(field, "") != "")
        for field in fieldnames
        if field.startswith("rgf_")
    }
    issues = sum(
        int(row.get("qa_issue_count") or 0)
        for row in rows_by_key.values()
    )
    return {
        "shard_files": len(paths),
        "rows": len(rows_by_key),
        "issues": issues,
        "coverage": coverage,
        "sha256": sha256(output_csv),
        "output": str(output_csv),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Combine RGF statewide shard CSVs.")
    parser.add_argument("--input-root", type=Path, required=True)
    parser.add_argument("--output-csv", type=Path, required=True)
    parser.add_argument("--expected-rows", type=int, default=645)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()

    result = combine_shards(args.input_root, args.output_csv, args.expected_rows)
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
