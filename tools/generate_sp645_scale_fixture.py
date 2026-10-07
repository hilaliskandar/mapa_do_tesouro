from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path

import openpyxl
import yaml

ROOT = Path(__file__).resolve().parents[1]
BASE_MAPPING = ROOT / "data" / "mappings" / "base_multifuentes_v0_4.yml"


def stable_factor(variable_id: str) -> float:
    digest = hashlib.sha256(variable_id.encode("utf-8")).digest()
    return 0.01 + (int.from_bytes(digest[:2], "big") % 35) / 100.0


def synthetic_value(variable_id: str, code: str, year: int, value_type: str):
    code_num = int(code)
    base = 100_000_000.0 + (code_num % 100_000) * 1_000.0 + (year - 2021) * 2_000_000.0
    rcl = base * 0.92

    if value_type == "text":
        if variable_id == "capag":
            return ("A", "B", "C")[code_num % 3]
        return f"SYNTHETIC-{code[-3:]}"

    explicit = {
        "dca_receita_corrente_bruta": base,
        "dca_receita_tributaria_bruta": base * 0.25,
        "dca_iptu_principal": base * 0.045,
        "dca_itbi_principal": base * 0.018,
        "dca_iss_principal": base * 0.105,
        "dca_fpm_cota_mensal": base * 0.11,
        "dca_icms_cota_parte": base * 0.15,
        "dca_ipva_cota_parte": base * 0.035,
        "dca_investimentos_liquidada": base * (0.055 + (code_num % 7) * 0.004),
        "dca_despesa_total_liquidada": base * 0.93,
        "dca_despesa_corrente_liquidada": base * 0.78,
        "dca_pessoal_encargos_liquidada": base * 0.41,
        "dca_juros_encargos_liquidada": base * 0.012,
        "dca_inversoes_financeiras_liquidada": base * 0.006,
        "dca_amortizacao_divida_liquidada": base * 0.022,
        "dca_operacoes_credito": base * 0.018,
        "dca_alienacao_bens": base * 0.003,
        "dca_transferencias_capital": base * 0.027,
        "dca_func_urbanismo_liquidada": base * (0.035 + (code_num % 5) * 0.002),
        "dca_func_habitacao_liquidada": base * 0.009,
        "dca_func_saneamento_liquidada": base * 0.015,
        "dca_func_gestao_ambiental_liquidada": base * 0.006,
        "dca_func_transporte_liquidada": base * 0.019,
        "dca_func_saude_liquidada": base * 0.205,
        "dca_func_educacao_liquidada": base * 0.245,
        "populacao_dca": 5_000.0 + (code_num % 500_000),
        "rreo_rcl_oficial": rcl,
        "rgf_despesa_total_pessoal": rcl * (0.40 + (code_num % 8) * 0.01),
        "dtp_pct_rcl": 40.0 + (code_num % 8),
        "rgf02_divida_consolidada": rcl * (0.25 + (code_num % 10) * 0.025),
        "rgf02_divida_consolidada_liquida": rcl * (0.18 + (code_num % 8) * 0.02),
        "dc_pct_rcl": 25.0 + (code_num % 10) * 2.5,
        "dcl_pct_rcl": 18.0 + (code_num % 8) * 2.0,
        "rgf_caixa_liquida_apos_rpnp": rcl * (0.02 + (code_num % 6) * 0.01),
        "rgf02_divida_contratual": rcl * 0.22,
        "rgf02_parcelamento_dividas": rcl * 0.025,
        "rgf02_precatorios_vencidos_nao_pagos": rcl * 0.008,
        "rgf02_outras_dividas": rcl * 0.012,
        "rgf02_deducoes_divida_consolidada": rcl * 0.06,
        "rgf02_disponibilidade_caixa": rcl * 0.09,
        "rgf02_demais_haveres_financeiros": rcl * 0.015,
        "rgf02_restos_pagar_processados": rcl * 0.035,
        "indicador_1": 0.65 + (code_num % 20) / 100.0,
        "indicador_2": 0.75 + (code_num % 15) / 100.0,
        "indicador_3": 0.55 + (code_num % 25) / 100.0,
    }
    return explicit.get(variable_id, base * stable_factor(variable_id))


def load_municipalities(geojson_path: Path) -> list[tuple[str, str]]:
    payload = json.loads(geojson_path.read_text(encoding="utf-8"))
    municipalities = sorted(
        (
            str(feature["properties"]["id"]),
            str(feature["properties"]["name"]),
        )
        for feature in payload["features"]
    )
    if len(municipalities) != 645:
        raise ValueError(f"Expected 645 municipalities, got {len(municipalities)}")
    if len({code for code, _ in municipalities}) != 645:
        raise ValueError("Duplicate municipality codes in cartography.")
    return municipalities


def generate(
    geojson_path: Path,
    workbook_path: Path,
    mapping_path: Path,
) -> dict:
    mapping = yaml.safe_load(BASE_MAPPING.read_text(encoding="utf-8"))
    mapping = copy.deepcopy(mapping)
    mapping["universe"] = {
        "id": "SP_645_SYNTHETIC",
        "name": "SP 645 synthetic scale fixture",
        "description": "Fixture sintética determinística para teste de escala; não contém dados oficiais.",
        "type": "teste",
    }
    mapping["source"].update(
        {
            "source_id": "PROJETO_BASE_MULTIFONTES",
            "workbook_name": workbook_path.name,
            "sheet": "Base multifuentes",
            "data_version": "synthetic-sp645-scale-v1",
            "expected_rows": 645 * 5,
            "expected_municipalities": 645,
            "expected_years": {"start": 2021, "end": 2025},
        }
    )

    municipalities = load_municipalities(geojson_path)
    key_columns = [
        mapping["keys"]["codigo_ibge"],
        mapping["keys"]["municipio"],
        mapping["keys"]["ano"],
    ]
    variable_columns = [spec["column"] for spec in mapping["variables"].values()]
    headers = key_columns + variable_columns

    workbook = openpyxl.Workbook(write_only=True)
    worksheet = workbook.create_sheet(mapping["source"]["sheet"])
    worksheet.append(headers)

    for code, name in municipalities:
        for year in range(2021, 2026):
            row = [code, name, year]
            for variable_id, spec in mapping["variables"].items():
                start = int(spec["availability_start"])
                end = int(spec["availability_end"])
                if year < start or year > end:
                    row.append(None)
                else:
                    row.append(
                        synthetic_value(
                            variable_id,
                            code,
                            year,
                            spec["value_type"],
                        )
                    )
            worksheet.append(row)

    workbook_path.parent.mkdir(parents=True, exist_ok=True)
    workbook.save(workbook_path)
    mapping_path.parent.mkdir(parents=True, exist_ok=True)
    mapping_path.write_text(
        yaml.safe_dump(mapping, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    return {
        "municipalities": len(municipalities),
        "years": 5,
        "rows": len(municipalities) * 5,
        "variables": len(mapping["variables"]),
        "universe_id": mapping["universe"]["id"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate deterministic synthetic SP-645 fixture for scale validation."
    )
    parser.add_argument("--geojson", type=Path, required=True)
    parser.add_argument("--workbook", type=Path, required=True)
    parser.add_argument("--mapping", type=Path, required=True)
    args = parser.parse_args()
    result = generate(args.geojson, args.workbook, args.mapping)
    for key, value in result.items():
        print(f"{key}={value}")


if __name__ == "__main__":
    main()
