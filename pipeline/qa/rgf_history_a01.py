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
    paths = sorted(input_root.glob("**/rgf_a01_2023_*.csv"))
    if not paths:
        raise ValueError("No 2023 RGF A01 shard CSVs found.")

    rows = {}
    fieldnames = None
    for path in paths:
        with path.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            current = list(reader.fieldnames or [])
            if fieldnames is None:
                fieldnames = current
            elif current != fieldnames:
                raise ValueError(f"Schema mismatch: {path}")
            for row in reader:
                key = row["cod_ibge"]
                if key in rows:
                    raise ValueError(f"Duplicate code: {key}")
                rows[key] = row

    if len(rows) != 645:
        raise ValueError(f"Expected 645 municipalities, got {len(rows)}")

    coverage = {
        field: sum(row.get(field, "") != "" for row in rows.values())
        for field in fieldnames
        if field.startswith("rgf_")
    }
    issues = sum(int(row.get("qa_issue_count") or 0) for row in rows.values())

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for code in sorted(rows):
            writer.writerow(rows[code])

    result = {
        "year": 2023,
        "rows": len(rows),
        "shard_files": len(paths),
        "coverage": coverage,
        "issues": issues,
        "sha256": sha256(output_csv),
    }
    summary.parent.mkdir(parents=True, exist_ok=True)
    summary.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Combine corrected 2023 RGF A01 shards.")
    parser.add_argument("--input-root", type=Path, required=True)
    parser.add_argument("--output-csv", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(combine(args.input_root, args.output_csv, args.summary), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
