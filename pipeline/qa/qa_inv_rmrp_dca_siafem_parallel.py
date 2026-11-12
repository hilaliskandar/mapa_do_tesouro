#!/usr/bin/env python3
"""Verifica matriz paralela RMRP DCA/SIAFEM sem operações contábeis cruzadas.

Compara o CSV versionado com fontes autênticas e tipagem exata em centavos.
Ausentes e anos fora do período da DCA são categorias, jamais zero.
"""
from __future__ import annotations

import argparse
import csv
from decimal import Decimal, InvalidOperation
from pathlib import Path

CORE = (
    "codigo_ibge", "municipio", "sub_regiao", "ano",
    "dca_investimentos_liquidados_centavos", "dca_investimentos_liquidados_status",
    "dca_transferencias_capital_centavos", "dca_transferencias_capital_status",
    "siafem_estadual_investimento_liberado_estornado_centavos",
    "siafem_quantidade_pagamentos", "regra_nao_aditividade", "fonte_dca",
    "fonte_siafem"
)


def read(path: Path, separator: str):
    with path.open(encoding="utf-8-sig", newline="") as fp:
        return list(csv.DictReader(fp, delimiter=separator))


def cents(s: str):
    if not s.strip():
        return None
    try:
        raw = Decimal(s) * 100
    except InvalidOperation as e:
        raise ValueError(f"DCA invalido: {s!r}") from e
    if raw != raw.to_integral_value():
        raise ValueError(f"Mais de dois decimais na DCA: {s!r}")
    return int(raw)


def expected_status(value, year: int):
    if year == 2026:
        return "DCA_ANO_NAO_DISPONIVEL"
    if value is None:
        return "AUSENTE_NAO_ZERO"
    if value == 0:
        return "ZERO_EXPLICITO"
    return "OBSERVADO"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dca", type=Path, required=True)
    p.add_argument("--roster", type=Path, required=True)
    p.add_argument("--siafem", type=Path, required=True)
    p.add_argument("--matrix", type=Path, required=True)
    a = p.parse_args()

    roster = {x["codigo_ibge"]: x for x in read(a.roster, ";")}
    if len(roster) != 34:
        raise ValueError("Universo RMRP incorreto")
    dca = {(r["cod_ibge"], int(r["ano"])): r for r in read(a.dca, ",")
           if r["cod_ibge"] in roster and int(r["ano"]) >= 2020}
    siafem = {(r["codigo_ibge"], int(r["ano"])): r for r in read(a.siafem, ";")}
    matrix = read(a.matrix, ";")
    if len(dca) != 204 or len(siafem) != 238 or len(matrix) != 238:
        raise ValueError("Quantidades divergentes das fontes")
    if list(matrix[0]) != list(CORE):
        raise ValueError("Ordem ou contrato de colunas divergente")
    seen = set()
    count_missing = 0
    for line in matrix:
        code, year = line["codigo_ibge"], int(line["ano"])
        key = code, year
        if key in seen or key not in siafem:
            raise ValueError(f"Chave duplicada ou desconhecida: {key}")
        seen.add(key)
        city, official = roster[code], siafem[key]
        if line["municipio"] != city["municipio"] or line["sub_regiao"] != city["sub_regiao"]:
            raise ValueError(f"Territorializacao divergente: {key}")
        if line["siafem_estadual_investimento_liberado_estornado_centavos"] != official["valor_liberado_estornado_exato_centavos"]:
            raise ValueError(f"Valor SIAFEM divergente: {key}")
        if line["siafem_quantidade_pagamentos"] != official["quantidade_pagamentos"]:
            raise ValueError(f"Quantidade SIAFEM divergente: {key}")
        if line["regra_nao_aditividade"] != "DCA_DESPESA_LIQUIDADA_E_SIAFEM_LIBERACAO_NAO_ADITIVAS":
            raise ValueError("Ausencia de controle de nao aditividade")
        raw = dca.get(key)
        for source, prefix in (
            ("dca_investimentos_liquidada", "dca_investimentos_liquidados"),
            ("dca_transferencias_capital", "dca_transferencias_capital"),
        ):
            value = cents(raw[source]) if raw is not None else None
            status = expected_status(value, year)
            raw_target = line[f"{prefix}_centavos"]
            observed = int(raw_target) if raw_target.strip() else None
            if status != line[f"{prefix}_status"] or observed != value:
                raise ValueError(f"DCA divergente: {key}, {prefix}")
            if status == "AUSENTE_NAO_ZERO":
                count_missing += 1
        if year == 2026 and (line["fonte_dca"] or raw is not None):
            raise ValueError("DCA 2026 nao deveria estar preenchida")
        if year <= 2025 and not line["fonte_dca"]:
            raise ValueError("Linha DCA historica sem fonte")
    if seen != set(siafem) or count_missing != 3:
        raise ValueError("Cobertura ou ausencia DCA divergente")
    print(f"QA_PARALLEL_PASS rows=238 matched_2020_2025=204 missing_dca_capital=3")


if __name__ == "__main__":
    main()
