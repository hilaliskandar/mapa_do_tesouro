from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

import openpyxl


SUPPLEMENT_FIELDS = {
    "rgf_caixa_bruta_nao_vinculada":
        "2025DisponibilidadeDeCaixaBrutaDISPONIBILIDADE DE CAIXA BRUTA (a)TOTAL DOS RECURSOS NÃO VINCULADOS (I)",
    "rgf_demais_obrigacoes_nao_vinculadas":
        "2025DemaisObrigacoesFinanceirasDemais Obrigações Financeiras (e)TOTAL DOS RECURSOS NÃO VINCULADOS (I)",
    "rgf_rp_nao_liquidados_anteriores_nao_vinculados":
        "2025RestosAPagarEmpenhadosENaoLiquidadosDeExerciciosAnterioresRestos a Pagar Empenhados e Não Liquidados de Exercícios Anteriores (d)TOTAL DOS RECURSOS NÃO VINCULADOS (I)",
    "rgf_rp_liquidados_anteriores_nao_vinculados":
        "2025RestosAPagarLiquidadosENaoPagosDeExerciciosAnterioresDe Exercícios Anteriores (b)TOTAL DOS RECURSOS NÃO VINCULADOS (I)",
    "rgf_rp_liquidados_exercicio_nao_vinculados":
        "2025RestosAPagarLiquidadosENaoPagosDoExercicioDo Exercício (c)TOTAL DOS RECURSOS NÃO VINCULADOS (I)",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_capag_supplement(path: Path) -> dict[str, dict[str, object]]:
    workbook = openpyxl.load_workbook(path, read_only=True, data_only=True)
    sheet = workbook["Datalake"]
    rows = sheet.iter_rows(values_only=True)
    header = list(next(rows))
    indexes = {
        field: header.index(source_header)
        for field, source_header in SUPPLEMENT_FIELDS.items()
    }

    result: dict[str, dict[str, object]] = {}
    for row in rows:
        code = str(row[0] or "").split(".")[0]
        if len(code) == 7 and code.startswith("35"):
            result[code] = {field: row[index] for field, index in indexes.items()}
    return result


def compose_fill_only(
    base_csv: Path,
    capag_xlsx: Path,
    output_csv: Path,
    manifest_path: Path,
    *,
    tolerance: float = 0.01,
) -> dict:
    supplement = load_capag_supplement(capag_xlsx)

    with base_csv.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        fieldnames = list(reader.fieldnames or [])

    filled = {field: 0 for field in SUPPLEMENT_FIELDS}
    overlap = {field: 0 for field in SUPPLEMENT_FIELDS}
    conflicts: list[dict] = []

    for row in rows:
        code = row["cod_ibge"]
        source = supplement.get(code, {})
        for field in SUPPLEMENT_FIELDS:
            base_value = row.get(field, "")
            source_value = source.get(field)

            if base_value != "" and source_value not in (None, ""):
                overlap[field] += 1
                if abs(float(base_value) - float(source_value)) > tolerance:
                    conflicts.append(
                        {
                            "cod_ibge": code,
                            "field": field,
                            "base": float(base_value),
                            "supplement": float(source_value),
                        }
                    )
            elif base_value == "" and source_value not in (None, ""):
                row[field] = str(float(source_value))
                filled[field] += 1

    if conflicts:
        raise ValueError(f"Fill-only conflicts found: {conflicts[:20]}")

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    coverage = {
        field: sum(1 for row in rows if row.get(field, "") != "")
        for field in fieldnames
        if field.startswith("rgf_")
    }

    manifest = {
        "rows": len(rows),
        "base_sha256": sha256(base_csv),
        "supplement_sha256": sha256(capag_xlsx),
        "output_sha256": sha256(output_csv),
        "filled_by_field": filled,
        "overlap_by_field": overlap,
        "conflicts": conflicts,
        "coverage": coverage,
        "tolerance": tolerance,
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Compose RGF 2025 with CAPAG local supplement.")
    parser.add_argument("--base-csv", type=Path, required=True)
    parser.add_argument("--capag-xlsx", type=Path, required=True)
    parser.add_argument("--output-csv", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--tolerance", type=float, default=0.01)
    args = parser.parse_args()

    result = compose_fill_only(
        args.base_csv,
        args.capag_xlsx,
        args.output_csv,
        args.manifest,
        tolerance=args.tolerance,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
