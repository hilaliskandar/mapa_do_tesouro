"""Build a separate, read-only DCA historical payload from the canonical CSV.

Do not recompute accounts, overwrite v2 endpoints, or infer missing cells as zero.
Run: python -m pipeline.build.export_dca_historical_v2 SOURCE.csv OUTPUT_DIR
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

START_YEAR = 2013
END_YEAR = 2025
MUNICIPALITIES = 645
KEYS = {"cod_ibge", "ano", "qa_issue_count"}
EXPECTED_VARIABLES = (
    "dca_receita_corrente_bruta", "dca_receita_tributaria_bruta",
    "dca_iptu_principal", "dca_itbi_principal", "dca_iss_principal",
    "dca_fpm_cota_mensal", "dca_icms_cota_parte", "dca_ipva_cota_parte",
    "dca_operacoes_credito", "dca_alienacao_bens",
    "dca_transferencias_capital", "dca_despesa_total_liquidada",
    "dca_despesa_corrente_liquidada", "dca_pessoal_encargos_liquidada",
    "dca_juros_encargos_liquidada", "dca_investimentos_liquidada",
    "dca_inversoes_financeiras_liquidada", "dca_amortizacao_divida_liquidada",
    "dca_func_saude_liquidada", "dca_func_educacao_liquidada",
    "dca_func_urbanismo_liquidada", "dca_func_habitacao_liquidada",
    "dca_func_saneamento_liquidada", "dca_func_gestao_ambiental_liquidada",
    "dca_func_transporte_liquidada", "populacao_dca",
)


def _write(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, sort_keys=True,
                               separators=(",", ":")) + "\n", encoding="utf-8")


def export_history(source: Path, output: Path, *, expected_sha256: str | None = None,
                   expected_municipalities: int = MUNICIPALITIES) -> dict:
    raw_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    if expected_sha256 and raw_hash != expected_sha256:
        raise ValueError("Canonical CSV SHA-256 mismatch; refusing to export")
    data = {}
    years = set()
    municipalities = set()
    counts = {name: {"observado": 0, "ausente": 0} for name in EXPECTED_VARIABLES}
    with source.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("CSV header missing")
        if len(reader.fieldnames) != len(set(reader.fieldnames)):
            raise ValueError("Duplicate CSV columns")
        actual = set(reader.fieldnames)
        required = KEYS | set(EXPECTED_VARIABLES)
        if actual != required:
            raise ValueError(f"CSV schema mismatch: missing={sorted(required-actual)}, extra={sorted(actual-required)}")
        for row in reader:
            code = row["cod_ibge"].strip()
            if not (len(code) == 7 and code.isascii() and code.isdigit()):
                raise ValueError(f"Invalid municipality code: {code!r}")
            year = int(row["ano"])
            if not START_YEAR <= year <= END_YEAR:
                raise ValueError(f"Unexpected year: {year}")
            if row["qa_issue_count"].strip() != "0":
                raise ValueError(f"Unresolved QA issues for {code}/{year}")
            key = (code, year)
            if key in data:
                raise ValueError(f"Duplicate municipality-year: {code}/{year}")
            values = {}
            for variable in EXPECTED_VARIABLES:
                cell = row[variable].strip()
                if not cell:
                    values[variable] = {"status": "ausente", "value": None}
                    counts[variable]["ausente"] += 1
                else:
                    # Pass numeric text through unchanged: no rounding, formulas or transformations.
                    # Consumers may parse for display only after a separate QA gate.
                    from decimal import Decimal, InvalidOperation
                    try:
                        number = Decimal(cell)
                    except InvalidOperation as error:
                        raise ValueError(f"Invalid numeric cell {variable} for {code}/{year}") from error
                    if not number.is_finite():
                        raise ValueError("Non-finite fiscal value")
                    values[variable] = {"status": "observado", "value_decimal": cell}
                    counts[variable]["observado"] += 1
            data[key] = values
            municipalities.add(code)
            years.add(year)
    if years != set(range(START_YEAR, END_YEAR + 1)):
        raise ValueError("Incomplete year domain")
    if len(municipalities) != expected_municipalities:
        raise ValueError("Incomplete municipality universe")
    if len(data) != len(years) * expected_municipalities:
        raise ValueError("Incomplete municipality-year grid")
    # Write only after every input check passes.
    for code in sorted(municipalities):
        observations = {str(year): data[(code, year)] for year in sorted(years)}
        _write(output / "municipalities" / f"{code}.json",
               {"codigo_ibge": code, "years": observations})
    manifest = {
        "contract": "dca-history-v2-candidate",
        "source_sha256": raw_hash,
        "source_kind": "canonical_finbra_dca_csv",
        "municipality_count": len(municipalities),
        "years": sorted(years),
        "variable_count": len(EXPECTED_VARIABLES),
        "municipality_year_count": len(data),
        "coverage": counts,
        "value_policy": "original_decimal_text; blank_is_absent_not_zero",
        "publication_qa": "not_evaluated",
    }
    _write(output / "manifest.json", manifest)
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--expected-sha256")
    args = parser.parse_args()
    print(json.dumps(export_history(args.source, args.output,
                                    expected_sha256=args.expected_sha256),
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
