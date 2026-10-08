from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

A01_FIELDS = [
    "rgf_despesa_total_pessoal",
    "rgf_rcl_denominador_legal",
    "rgf_dtp_percentual_rcl",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def patch_history(
    history_csv: Path,
    a01_csv: Path,
    output_csv: Path,
    summary_path: Path,
) -> dict:
    with history_csv.open(encoding="utf-8", newline="") as handle:
        history_reader = csv.DictReader(handle)
        fieldnames = list(history_reader.fieldnames or [])
        history = {(row["cod_ibge"], row["ano"]): row for row in history_reader}

    if len(history) != 1290:
        raise ValueError(f"Expected 1290 history rows, got {len(history)}")

    with a01_csv.open(encoding="utf-8", newline="") as handle:
        a01_reader = csv.DictReader(handle)
        a01 = {row["cod_ibge"]: row for row in a01_reader}

    if len(a01) != 645:
        raise ValueError(f"Expected 645 corrected A01 rows, got {len(a01)}")

    patched = 0
    for code, row in a01.items():
        key = (code, "2023")
        if key not in history:
            raise ValueError(f"Missing 2023 history row for {code}")
        for field in A01_FIELDS:
            history[key][field] = row.get(field, "")
        history[key]["qa_issue_count"] = str(
            int(history[key].get("qa_issue_count") or 0)
            + int(row.get("qa_issue_count") or 0)
        )
        patched += 1

    coverage = {}
    for year in ("2023", "2024"):
        subset = [row for (code, y), row in history.items() if y == year]
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
        for key in sorted(history, key=lambda item: (item[1], item[0])):
            writer.writerow(history[key])

    result = {
        "rows": len(history),
        "patched_2023_rows": patched,
        "coverage": coverage,
        "sha256": sha256(output_csv),
    }
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Patch Gate E history with corrected 2023 A01.")
    parser.add_argument("--history-csv", type=Path, required=True)
    parser.add_argument("--a01-csv", type=Path, required=True)
    parser.add_argument("--output-csv", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()
    print(
        json.dumps(
            patch_history(
                args.history_csv,
                args.a01_csv,
                args.output_csv,
                args.summary,
            ),
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
