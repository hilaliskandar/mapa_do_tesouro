from __future__ import annotations

import argparse
import csv
import hashlib
import json
from decimal import Decimal, InvalidOperation
from pathlib import Path


KEY_COLUMNS = ("cod_ibge", "ano")
NON_VALUE_COLUMNS = {"cod_ibge", "ano", "qa_issue_count"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _read_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError(f"CSV has no header: {path}")
        rows = list(reader)
    return list(reader.fieldnames), rows


def _key(row: dict[str, str]) -> tuple[str, str]:
    return tuple(str(row.get(column, "")).strip() for column in KEY_COLUMNS)  # type: ignore[return-value]


def _is_blank(value: object) -> bool:
    return value is None or str(value).strip() == ""


def _equal_value(left: str, right: str) -> bool:
    if left == right:
        return True
    try:
        return Decimal(left) == Decimal(right)
    except (InvalidOperation, ValueError):
        return False


def merge_fill_only(
    base_csv: Path,
    delta_csv: Path,
    output_csv: Path,
    report_path: Path,
    *,
    fail_on_conflict: bool = True,
) -> dict:
    base_header, base_rows = _read_rows(base_csv)
    delta_header, delta_rows = _read_rows(delta_csv)

    if base_header != delta_header:
        raise ValueError(
            "Base and delta schemas differ. "
            f"base={base_header!r} delta={delta_header!r}"
        )

    base_index: dict[tuple[str, str], dict[str, str]] = {}
    for row in base_rows:
        key = _key(row)
        if key in base_index:
            raise ValueError(f"Duplicate base key: {key}")
        base_index[key] = row

    delta_index: dict[tuple[str, str], dict[str, str]] = {}
    for row in delta_rows:
        key = _key(row)
        if key in delta_index:
            raise ValueError(f"Duplicate delta key: {key}")
        delta_index[key] = row

    unknown_keys = sorted(set(delta_index) - set(base_index))
    if unknown_keys:
        raise ValueError(
            "Delta contains keys not present in the base universe: "
            f"{unknown_keys[:20]}"
        )

    value_columns = [
        column for column in base_header if column not in NON_VALUE_COLUMNS
    ]
    filled_by_variable = {column: 0 for column in value_columns}
    filled_cells: list[dict] = []
    conflicts: list[dict] = []

    for key, delta_row in delta_index.items():
        base_row = base_index[key]
        for column in value_columns:
            base_value = str(base_row.get(column, "") or "").strip()
            delta_value = str(delta_row.get(column, "") or "").strip()

            if _is_blank(base_value) and not _is_blank(delta_value):
                base_row[column] = delta_value
                filled_by_variable[column] += 1
                filled_cells.append(
                    {
                        "cod_ibge": key[0],
                        "ano": key[1],
                        "variable": column,
                        "value": delta_value,
                    }
                )
                continue

            if (
                not _is_blank(base_value)
                and not _is_blank(delta_value)
                and not _equal_value(base_value, delta_value)
            ):
                conflicts.append(
                    {
                        "cod_ibge": key[0],
                        "ano": key[1],
                        "variable": column,
                        "base_value": base_value,
                        "delta_value": delta_value,
                        "resolution": "base_preserved",
                    }
                )

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=base_header)
        writer.writeheader()
        writer.writerows(base_rows)

    report = {
        "policy": "fill_only",
        "base_csv": str(base_csv),
        "delta_csv": str(delta_csv),
        "base_sha256": sha256(base_csv),
        "delta_sha256": sha256(delta_csv),
        "output_sha256": sha256(output_csv),
        "base_rows": len(base_rows),
        "delta_rows": len(delta_rows),
        "delta_codes": sorted({key[0] for key in delta_index}),
        "filled_cell_count": len(filled_cells),
        "filled_by_variable": {
            column: count
            for column, count in filled_by_variable.items()
            if count
        },
        "conflict_count": len(conflicts),
        "conflicts": conflicts,
        "filled_cells": filled_cells,
        "rules": [
            "blank base + observed delta => fill",
            "observed base + blank delta => preserve base",
            "equal observed values => preserve base",
            "different observed values => preserve base and report conflict",
            "delta cannot introduce a new municipality-year key",
        ],
    }

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    if conflicts and fail_on_conflict:
        raise RuntimeError(
            f"Delta merge found {len(conflicts)} conflicts. "
            f"See {report_path}."
        )
    return report


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Merge a normalized DCA delta into a normalized local snapshot "
            "without overwriting observed base values."
        )
    )
    parser.add_argument("--base-csv", type=Path, required=True)
    parser.add_argument("--delta-csv", type=Path, required=True)
    parser.add_argument("--output-csv", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument(
        "--allow-conflicts",
        action="store_true",
        help="Keep base values and return success even when conflicts are reported.",
    )
    args = parser.parse_args()

    result = merge_fill_only(
        args.base_csv,
        args.delta_csv,
        args.output_csv,
        args.report,
        fail_on_conflict=not args.allow_conflicts,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
