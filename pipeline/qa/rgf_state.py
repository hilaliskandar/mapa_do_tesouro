from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def build_qa(manifest_path: Path, normalized_csv: Path, output: Path) -> dict:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    total = int(manifest["municipalities_requested"])
    coverage = manifest["normalization"]["coverage"]

    missing_by_field: dict[str, list[str]] = {field: [] for field in coverage}
    with normalized_csv.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            code = row["cod_ibge"]
            for field in coverage:
                if row.get(field, "") == "":
                    missing_by_field[field].append(code)

    lines = [
        f"# QA — RGF SP645 — {manifest['year']}",
        "",
        f"- municípios solicitados: {total};",
        f"- linhas normalizadas: {manifest['normalization']['rows']};",
        f"- issues: {manifest['normalization']['issues']};",
        f"- falhas de aquisição: {len(manifest['failed'])};",
        f"- SHA-256 normalizado: `{manifest['normalized_sha256']}`;",
        f"- SHA-256 árvore bruta: `{manifest['raw_tree_sha256']}`.",
        "",
        "## Cobertura por variável",
        "",
        "| Variável | Observados | Ausentes | Cobertura |",
        "|---|---:|---:|---:|",
    ]

    for field in sorted(coverage):
        observed = int(coverage[field])
        missing = total - observed
        pct = 100.0 * observed / total if total else 0.0
        lines.append(f"| `{field}` | {observed} | {missing} | {pct:.2f}% |")

    lines.extend(["", "## Ausências por variável", ""])
    for field in sorted(missing_by_field):
        codes = missing_by_field[field]
        if codes:
            lines.append(f"- `{field}`: {len(codes)} — " + ", ".join(codes))
        else:
            lines.append(f"- `{field}`: 0.")

    lines.extend(
        [
            "",
            "## Regra",
            "",
            "Ausência permanece ausência. Nenhum valor é criado por soma de sublinhas,",
            "por substituição de outro demonstrativo ou por inferência de zero.",
            "",
        ]
    )

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")

    return {
        "year": manifest["year"],
        "municipalities": total,
        "issues": manifest["normalization"]["issues"],
        "failed": len(manifest["failed"]),
        "coverage": coverage,
        "missing_by_field": missing_by_field,
        "output": str(output),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build reproducible RGF statewide QA.")
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--normalized-csv", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    result = build_qa(args.manifest, args.normalized_csv, args.output)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
