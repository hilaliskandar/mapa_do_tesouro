from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

import openpyxl


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_csv(path: Path, *, key: str = "cod_ibge") -> tuple[dict[str, dict], list[str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = {}
        for row in reader:
            code = str(row[key]).strip()
            if code in rows:
                raise ValueError(f"Duplicate code in {path}: {code}")
            rows[code] = row
        return rows, list(reader.fieldnames or [])


def build_multisource_2025(
    dca_csv: Path,
    rreo_csv: Path,
    rgf_csv: Path,
    rgf02_csv: Path,
    capag_csv: Path,
    output_xlsx: Path,
    manifest_path: Path,
) -> dict:
    dca, dca_fields = read_csv(dca_csv)
    rreo, rreo_fields = read_csv(rreo_csv)
    rgf, rgf_fields = read_csv(rgf_csv)
    rgf02, rgf02_fields = read_csv(rgf02_csv)
    capag, capag_fields = read_csv(capag_csv, key="codigo_ibge")

    expected = set(dca)
    if len(expected) != 645:
        raise ValueError(f"DCA universe must have 645 codes, got {len(expected)}")

    sources = {
        "dca": dca,
        "rreo": rreo,
        "rgf": rgf,
        "rgf02": rgf02,
        "capag": capag,
    }
    for name, rows in sources.items():
        unknown = sorted(set(rows) - expected)
        if unknown:
            raise ValueError(f"{name} contains codes outside DCA universe: {unknown[:20]}")

    merged_rows = []
    coverage: dict[str, int] = {}

    excluded = {
        "dca": {"cod_ibge", "ano", "qa_issue_count"},
        "rreo": {"cod_ibge", "ano", "qa_issue_count", "populacao_rreo"},
        "rgf": {"cod_ibge", "ano", "qa_issue_count"},
        "rgf02": {"cod_ibge", "ano"},
        "capag": {"codigo_ibge", "uf", "ano_base", "snapshot_posicao", "fonte", "source_file_sha256"},
    }
    renamed = {
        ("rreo", "rreo_rcl_total_12m"): "rreo_rcl_oficial",
    }

    source_fields = {
        "dca": dca_fields,
        "rreo": rreo_fields,
        "rgf": rgf_fields,
        "rgf02": rgf02_fields,
        "capag": capag_fields,
    }

    output_fields = ["cod_ibge", "municipio", "ano"]
    for source_name, fields in source_fields.items():
        for field in fields:
            if field in excluded[source_name]:
                continue
            out_field = renamed.get((source_name, field), field)
            if out_field not in output_fields:
                output_fields.append(out_field)

    for code in sorted(expected):
        row = {
            "cod_ibge": code,
            "municipio": capag.get(code, {}).get("municipio", ""),
            "ano": 2025,
        }
        for source_name, rows in sources.items():
            source_row = rows.get(code, {})
            for field in source_fields[source_name]:
                if field in excluded[source_name]:
                    continue
                out_field = renamed.get((source_name, field), field)
                value = source_row.get(field, "")
                if value not in (None, ""):
                    row[out_field] = value
        merged_rows.append(row)

    for field in output_fields:
        if field in {"cod_ibge", "municipio", "ano"}:
            continue
        coverage[field] = sum(1 for row in merged_rows if row.get(field, "") not in (None, ""))

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Base multifuentes"
    sheet.append(output_fields)
    for row in merged_rows:
        sheet.append([row.get(field, "") for field in output_fields])

    output_xlsx.parent.mkdir(parents=True, exist_ok=True)
    workbook.save(output_xlsx)

    result = {
        "rows": len(merged_rows),
        "municipalities": len(expected),
        "year": 2025,
        "input_sha256": {
            "dca": sha256(dca_csv),
            "rreo": sha256(rreo_csv),
            "rgf": sha256(rgf_csv),
            "rgf02": sha256(rgf02_csv),
            "capag": sha256(capag_csv),
        },
        "output_sha256": sha256(output_xlsx),
        "coverage": coverage,
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Build SP645 multisource workbook for 2025.")
    parser.add_argument("--dca", type=Path, required=True)
    parser.add_argument("--rreo", type=Path, required=True)
    parser.add_argument("--rgf", type=Path, required=True)
    parser.add_argument("--rgf02", type=Path, required=True)
    parser.add_argument("--capag", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    result = build_multisource_2025(
        args.dca, args.rreo, args.rgf, args.rgf02, args.capag, args.output, args.manifest
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
