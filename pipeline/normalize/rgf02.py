from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


COLUMN = "Até o 3º Quadrimestre"

FIELD_CODES = {
    "rgf02_divida_consolidada": "DividaConsolidada",
    "rgf02_divida_consolidada_liquida": "DividaConsolidadaLiquida",
    "rgf02_dc_percentual_rcl": "PercentualDaDCSobreARCL",
    "rgf02_dcl_percentual_rcl": "PercentualDaDCLSobreARCL",
    "rgf02_divida_contratual": "DividaContratual",
    "rgf02_parcelamento_dividas": "RGF2ParcelamentoERenegociacaoDeDividas",
    "rgf02_precatorios_vencidos_nao_pagos": "PrecatoriosPosterioresA05052000VencidosENaoPagos",
    "rgf02_outras_dividas": "OutrasDividas",
    "rgf02_deducoes_divida_consolidada": "DeducoesDaDividaConsolidada",
    "rgf02_disponibilidade_caixa": "RGF2DisponibilidadeDeCaixa",
    "rgf02_demais_haveres_financeiros": "DemaisHaveresFinanceiros",
    "rgf02_restos_pagar_processados": "RestosAPagarProcessadosExcetoPrecatorios",
}

AUDIT_CODES = {
    "rgf02_rcl_bruta": "RGF2ReceitaCorrenteLiquida",
    "rgf02_rcl_ajustada_endividamento":
        "ReceitaCorrenteLiquidaAjustadaParaCalculoDosLimitesDeEndividamento",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalize_long(
    long_csv: Path,
    output_csv: Path,
    manifest_path: Path,
    *,
    universe_geojson: Path | None = None,
    year: int | None = None,
) -> dict:
    codes = {**FIELD_CODES, **AUDIT_CODES}
    reverse = {code: field for field, code in codes.items()}

    by_key: dict[tuple[str, str], dict] = {}
    if universe_geojson is not None:
        if year is None:
            raise ValueError("year is required with universe_geojson.")
        from pipeline.acquire.siconfi_dca import load_codes
        for code, _name in load_codes(universe_geojson):
            by_key[(code, str(int(year)))] = {
                "cod_ibge": code,
                "ano": str(int(year)),
            }

    conflicts: list[dict] = []

    with long_csv.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get("coluna") != COLUMN:
                continue
            field = reverse.get(row.get("cod_conta", ""))
            if field is None:
                continue
            key = (row["cod_ibge"], row["ano"])
            target = by_key.setdefault(
                key,
                {
                    "cod_ibge": row["cod_ibge"],
                    "ano": row["ano"],
                },
            )
            value = row.get("valor", "")
            if field in target and target[field] not in ("", value):
                conflicts.append(
                    {
                        "cod_ibge": row["cod_ibge"],
                        "ano": row["ano"],
                        "field": field,
                        "first": target[field],
                        "second": value,
                    }
                )
            else:
                target[field] = value

    if conflicts:
        raise ValueError(f"RGF02 normalization conflicts: {conflicts[:20]}")

    fieldnames = ["cod_ibge", "ano", *FIELD_CODES, *AUDIT_CODES]
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for key in sorted(by_key):
            writer.writerow(by_key[key])

    coverage = {
        field: sum(1 for row in by_key.values() if row.get(field, "") != "")
        for field in [*FIELD_CODES, *AUDIT_CODES]
    }
    result = {
        "rows": len(by_key),
        "conflicts": conflicts,
        "coverage": coverage,
        "output_sha256": sha256(output_csv),
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return result


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Normalize RGF Annex 02 long data.")
    parser.add_argument("--long-csv", type=Path, required=True)
    parser.add_argument("--output-csv", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--universe-geojson", type=Path)
    parser.add_argument("--year", type=int)
    args = parser.parse_args()

    result = normalize_long(
        args.long_csv,
        args.output_csv,
        args.manifest,
        universe_geojson=args.universe_geojson,
        year=args.year,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
