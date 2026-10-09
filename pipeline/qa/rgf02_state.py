from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def build_qa(
    acquisition_manifest: Path,
    normalized_manifest: Path,
    normalized_csv: Path,
    output: Path,
) -> dict:
    acquisition = json.loads(acquisition_manifest.read_text(encoding="utf-8"))
    normalized = json.loads(normalized_manifest.read_text(encoding="utf-8"))

    total = int(acquisition["municipalities_requested"])
    coverage = normalized["coverage"]
    missing_by_field = {field: [] for field in coverage}

    with normalized_csv.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            code = row["cod_ibge"]
            for field in coverage:
                if row.get(field, "") == "":
                    missing_by_field[field].append(code)

    lines = [
        f"# QA — RGF Anexo 02 SP645 — {acquisition['year']}",
        "",
        f"- municípios solicitados: {total};",
        f"- municípios com itens observados: {acquisition['observed_municipalities']};",
        f"- linhas longas: {acquisition['long_rows']};",
        f"- códigos de conta distintos: {acquisition['distinct_account_codes']};",
        f"- falhas de aquisição: {len(acquisition['failed'])};",
        f"- linhas normalizadas: {normalized['rows']};",
        f"- conflitos de normalização: {len(normalized['conflicts'])};",
        f"- SHA-256 longo: `{acquisition['long_csv_sha256']}`;",
        f"- SHA-256 árvore bruta: `{acquisition['raw_tree_sha256']}`;",
        f"- SHA-256 normalizado: `{normalized['output_sha256']}`.",
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
            "A taxonomia oficial do Anexo 02 é preservada. Ausência permanece vazia;",
            "nenhum componente de dívida é inferido, somado ou substituído por CAPAG.",
            "",
        ]
    )

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")

    return {
        "year": acquisition["year"],
        "municipalities": total,
        "observed_municipalities": acquisition["observed_municipalities"],
        "failed": len(acquisition["failed"]),
        "conflicts": len(normalized["conflicts"]),
        "coverage": coverage,
        "missing_by_field": missing_by_field,
        "output": str(output),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build reproducible RGF02 statewide QA.")
    parser.add_argument("--acquisition-manifest", type=Path, required=True)
    parser.add_argument("--normalized-manifest", type=Path, required=True)
    parser.add_argument("--normalized-csv", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    result = build_qa(
        args.acquisition_manifest,
        args.normalized_manifest,
        args.normalized_csv,
        args.output,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
