#!/usr/bin/env python3
"""QA offline determinístico dos dados anuais exatos SIAFEM da RMRP.

Nenhuma consulta de rede, nenhum upload de dados pessoais, nenhuma mutação de DB.
Executar: python pipeline/qa/qa_siafem_rmrp_anual_exato.py
"""
from __future__ import annotations
from collections import Counter, defaultdict
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GOV = ROOT / "governance"
ANNUAL = GOV / "INV_RMRP_SIAFEM_34_MUNICIPIOS_2020_2026_ANUAL_EXATO_2026_11_12.csv"
YEAR_CONTRACT = GOV / "INV_RMRP_SIAFEM_889_CONVENIO_ANO_EXATO_2026_11_12.csv"
YEAR_TOTAL = GOV / "INV_RMRP_SIAFEM_2020_2026_RESUMO_ANUAL_EXATO_2026_11_12.csv"
QA = GOV / "INV_RMRP_SIAFEM_2020_2026_ANUAL_EXATO_QA_2026_11_12.json"
LEGACY = [
    GOV / "INV_RMRP_SIAFEM_INVESTIMENTO_2020_LOTE_01_QA_2026_11_12.json",
    GOV / "INV_RMRP_SIAFEM_INVESTIMENTO_2020_LOTE_02_QA_2026_11_12.json",
]
EXPECTED_ANNUAL = {
    2020: (3301604280, 205),
    2021: (2560263607, 113),
    2022: (7248554118, 234),
    2023: (6214677220, 174),
    2024: (5735262211, 150),
    2025: (3593297666, 90),
    2026: (1898443818, 51),
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter=";"))


def brl_cents(text: str) -> int:
    """Número decimal BR monetário exato sem passar por float."""
    from decimal import Decimal
    stripped = text.strip()
    if not stripped:
        raise ValueError("Valor BR monetário vazio")
    number = Decimal(stripped.replace(".", "").replace(",", "."))
    value = number * 100
    if value != value.to_integral_value():
        raise ValueError("Precisão monetária inesperada")
    return int(value)


def main() -> None:
    annual = read_csv(ANNUAL)
    contract = read_csv(YEAR_CONTRACT)
    yr = read_csv(YEAR_TOTAL)
    manifest = json.loads(QA.read_text(encoding="utf-8"))
    assert len(annual) == 238, f"municipio-ano: {len(annual)} != 238"
    assert len(contract) == 889, f"convenio-ano: {len(contract)} != 889"
    assert len(yr) == 7, f"anos: {len(yr)} != 7"
    assert len({r["codigo_ibge"] for r in annual}) == 34
    assert len({(r["codigo_ibge"], r["ano"]) for r in annual}) == 238
    assert len({(r["codigo_ibge"], r["numero_convenio_siafem"], r["ano"]) for r in contract}) == 889
    assert len({(r["codigo_ibge"], r["numero_convenio_siafem"]) for r in contract}) == 752
    assert set(int(r["ano"]) for r in annual) == set(EXPECTED_ANNUAL)
    assert all(len(r["codigo_ibge"]) == 7 and r["codigo_ibge"].isdigit() for r in annual)
    assert all(int(r["valor_liberado_estornado_exato_centavos"]) == int(r["valor_liberado_estornado_exato_centavos"]) for r in annual)
    contract_value = defaultdict(int)
    contract_count = defaultdict(int)
    for r in contract:
        key = (r["codigo_ibge"], r["ano"])
        contract_value[key] += int(r["valor_liberado_estornado_ano_centavos"])
        contract_count[key] += int(r["pagamentos_ano"])
    year_value = Counter()
    year_count = Counter()
    for r in annual:
        key = (r["codigo_ibge"], r["ano"])
        v = int(r["valor_liberado_estornado_exato_centavos"])
        n = int(r["quantidade_pagamentos"])
        assert v == contract_value[key], f"Valor municipio-ano {key}"
        assert n == contract_count[key], f"Contagem municipio-ano {key}"
        year_value[int(r["ano"])] += v
        year_count[int(r["ano"])] += n
    for y, (expected_cents, expected_n) in EXPECTED_ANNUAL.items():
        assert year_value[y] == expected_cents, (y, year_value[y])
        assert year_count[y] == expected_n, (y, year_count[y])
    for r in yr:
        year = int(r["ano"])
        assert year_value[year] == int(r["valor_liberado_estornado_exato_centavos"])
        assert year_count[year] == int(r["quantidade_pagamentos"])
    assert sum(year_value.values()) == 30552102920
    assert sum(year_count.values()) == 1017
    previous = {}
    for path in LEGACY:
        for r in json.loads(path.read_text(encoding="utf-8"))["municipios"]:
            assert r["ibge"] not in previous
            previous[r["ibge"]] = (brl_cents(r["totais"][5]), int(r["totais"][4]))
    assert len(previous) == 34
    aggregated = defaultdict(lambda: [0, 0])
    for r in annual:
        code = r["codigo_ibge"]
        aggregated[code][0] += int(r["valor_liberado_estornado_exato_centavos"])
        aggregated[code][1] += int(r["quantidade_pagamentos"])
    assert all(tuple(aggregated[k]) == previous[k] for k in previous)
    assert manifest["total_exact_centavos"] == 30552102920
    assert manifest["payments"] == 1017
    assert manifest["contract_year_records"] == 889
    assert manifest["query_count"] == 238
    print(json.dumps({
        "status": "PASS", "municipios": 34, "consultas": 238,
        "convenios_unicos": 752, "convenio_ano": 889, "pagamentos": 1017,
        "total_centavos": 30552102920, "diferencas": 0
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
