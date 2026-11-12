#!/usr/bin/env python3
"""Auditoria histórica DCA SP645 x SIAFEM RMRP: cobertura, não conciliação contábil.

DCA: despesa municipal de investimento liquidada e transferências de capital.
SIAFEM: liberação financeira estadual classificada para investimento.
Essas variáveis NÃO são aditivas nem têm equivalência automática.
O script é somente leitura e rejeita snapshots sem SHA256 canônico.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
from decimal import Decimal, InvalidOperation
import hashlib
import json
from pathlib import Path

DCA_SHA256 = "67a94313e0f0557bc23f48c78a1396fd02ae10ad7923ea2ac2e5c9f2726f65d5"
DCA_ROW_COUNT = 8385
DCA_YEARS = range(2013, 2026)
SIAFEM_YEARS = range(2020, 2027)
MONEY_COLUMNS = ("dca_investimentos_liquidada", "dca_transferencias_capital")


def parse_csv(path: Path, delimiter: str) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream, delimiter=delimiter))


def money(raw: str):
    if raw is None or raw.strip() == "":
        return None
    try:
        value = Decimal(raw)
    except InvalidOperation as error:
        raise ValueError(f"Valor DCA inválido: {raw!r}") from error
    cents = value * 100
    if not cents.is_finite() or cents != cents.to_integral_value():
        raise ValueError(f"Precisão DCA inesperada: {raw!r}")
    return int(cents)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dca", required=True, type=Path)
    parser.add_argument("--siafem", required=True, type=Path)
    parser.add_argument("--roster", required=True, type=Path)
    parser.add_argument("--qa", required=True, type=Path)
    args = parser.parse_args()

    digest = hashlib.sha256(args.dca.read_bytes()).hexdigest()
    if digest != DCA_SHA256:
        raise ValueError("Snapshot DCA não coincide com SHA-256 canônico")
    roster = parse_csv(args.roster, ";")
    codes = {r["codigo_ibge"] for r in roster}
    if len(codes) != len(roster) or len(codes) != 34:
        raise ValueError("Cadastro RMRP diverge do universo IBGE7 de 34 municípios")
    names = {r["codigo_ibge"]: r["municipio"] for r in roster}
    subregions = {r["codigo_ibge"]: r["sub_regiao"] for r in roster}

    dca = parse_csv(args.dca, ",")
    if len(dca) != DCA_ROW_COUNT:
        raise ValueError("DCA 2013–2025: quantidade de linhas diferente de 8.385")
    dca_keys = set()
    all_codes = set()
    per_year = Counter()
    match_dca = {}
    for r in dca:
        code = r["cod_ibge"]
        year = int(r["ano"])
        if len(code) != 7 or not code.isdigit() or year not in DCA_YEARS:
            raise ValueError(f"Chave DCA inválida: {code}/{year}")
        key = (code, year)
        if key in dca_keys:
            raise ValueError(f"Duplicação DCA: {key}")
        dca_keys.add(key)
        all_codes.add(code)
        per_year[year] += 1
        if code in codes:
            match_dca[key] = {col: money(r[col]) for col in MONEY_COLUMNS}
    if len(all_codes) != 645 or any(per_year[y] != 645 for y in DCA_YEARS):
        raise ValueError("Snapshot DCA sem cobertura 645×13 completa")
    if len(match_dca) != 34 * 13:
        raise ValueError("RMRP não está inteiramente presente na DCA histórica")

    siafem = parse_csv(args.siafem, ";")
    if len(siafem) != 34 * 7:
        raise ValueError("SIAFEM não possui 238 combinações município×ano")
    siafem_keys = set()
    money_total = 0
    number_total = 0
    per_year_siafem = Counter()
    for r in siafem:
        key = (r["codigo_ibge"], int(r["ano"]))
        if key in siafem_keys or key[0] not in codes or key[1] not in SIAFEM_YEARS:
            raise ValueError(f"Chave SIAFEM inválida ou duplicada: {key}")
        if names[key[0]] != r["municipio"] or subregions[key[0]] != r["sub_regiao"]:
            raise ValueError(f"Mapeamento territorial SIAFEM divergente: {key}")
        siafem_keys.add(key)
        amount = int(r["valor_liberado_estornado_exato_centavos"])
        n = int(r["quantidade_pagamentos"])
        if n < 0:
            raise ValueError("Quantidade negativa de pagamentos")
        money_total += amount
        number_total += n
        per_year_siafem[key[1]] += 1
    if len(siafem_keys) != 238 or any(per_year_siafem[y] != 34 for y in SIAFEM_YEARS):
        raise ValueError("Cobertura anual SIAFEM RMRP divergente")
    if (money_total, number_total) != (30552102920, 1017):
        raise ValueError("Totais SIAFEM não reproduzem QA oficial")

    results = {}
    missing_examples = []
    for year in DCA_YEARS:
        subset = {code: match_dca[(code, year)] for code in codes}
        record = {"municipios_dca": len(subset)}
        for column in MONEY_COLUMNS:
            values = [item[column] for item in subset.values()]
            record[column] = {
                "preenchidos": sum(v is not None for v in values),
                "ausentes": sum(v is None for v in values),
                "zeros_explicitos": sum(v == 0 for v in values),
                "negativos": sum(v is not None and v < 0 for v in values),
                "somatorio_centavos_apenas_preenchidos": sum(v for v in values if v is not None)
            }
            if record[column]["ausentes"]:
                missing_examples.extend(
                    {"codigo_ibge": c, "municipio": names[c],
                     "ano": year, "campo": column}
                    for c, v in subset.items() if v[column] is None
                )
        if year in SIAFEM_YEARS:
            record["municipios_siafem"] = per_year_siafem[year]
            record["chaves_em_ambas"] = sum((c, year) in siafem_keys for c in codes)
        results[str(year)] = record
    overlap = sum((c, y) in siafem_keys and (c, y) in match_dca
                  for c in codes for y in range(2020, 2026))
    if overlap != 34 * 6:
        raise ValueError("Chaves RMRP 2020–2025 não fecham 204/204")
    report = {
        "qa_status": "pass_cobertura_historica_sem_conciliacao_contabil",
        "fonte_dca_sha256": digest,
        "dca_estado": {"anos": 13, "municipios": 645, "linhas": 8385},
        "rmrp": {"municipios": 34, "sub_regioes": len(set(subregions.values())),
                 "linhas_dca": len(match_dca), "linhas_siafem": len(siafem),
                 "intersecao_2020_2025_chaves": overlap,
                 "série_siafem_2026_sem_dca": 34},
        "siafem": {"valor_liberado_estornado_exato_centavos_2020_2026": money_total,
                   "quantidade_pagamentos_2020_2026": number_total},
        "por_ano": results,
        "quantidade_ausencias_dca_campos": len(missing_examples),
        "amostras_ausencias_dca": missing_examples[:40],
        "limites": [
            "DCA investimento municipal liquidado não equivale a liberação estadual SIAFEM",
            "DCA transferências de capital recebidas não equivale a SIAFEM transferência voluntária",
            "Anos 2013–2019 não foram recuperados no SIAFEM deste recorte",
            "2026 DCA ainda indisponível no snapshot 2013–2025",
            "Ausência de valor DCA não é zero; zeros explícitos são contados separadamente",
            "Valores agregados de DCA e SIAFEM não devem ser somados ou subtraídos como mesmo fluxo",
            "Auditoria de cobertura de CSV histórico não comprova importação histórica em SQLite"
        ]
    }
    args.qa.parent.mkdir(parents=True, exist_ok=True)
    args.qa.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"qa": report["qa_status"], "rmrp_dca": len(match_dca),
                      "overlap": overlap, "siafem": money_total,
                      "missing": len(missing_examples)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
