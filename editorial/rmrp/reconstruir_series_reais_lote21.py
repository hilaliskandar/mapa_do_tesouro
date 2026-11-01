#!/usr/bin/env python3
"""Reconstroi series reais RMRP a partir de CSVs locais ja arquivados."""
import argparse
import csv
from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

FIELDS = ("dca_receita_corrente_bruta", "dca_receita_tributaria_bruta",
          "dca_despesa_corrente_liquidada", "dca_investimentos_liquidada")
REGIONS = {"1": "Sub-região de Ribeirão Preto", "2": "Sub-região de Jaboticabal",
           "3": "Sub-região de Mococa", "4": "Sub-região de Batatais"}
BASE = Decimal("7695.82")

def read_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def number(s):
    return Decimal(s) if s not in ("", None, "n.d.") else None

def build(dca_path, territory_path, ipca_path, output):
    cities = {r["cod_ibge"]: r for r in read_csv(territory_path)}
    # IPCA mensal normalizado: mes no formato AAAAMM, numero_indice decimal.
    ipca = defaultdict(list)
    for row in read_csv(ipca_path):
        key = row["mes"]
        if len(key) != 6 or not key.isdigit():
            raise ValueError("IPCA: mes deve ser AAAAMM")
        year = int(key[:4])
        if 2013 <= year <= 2025:
            ipca[year].append((key, number(row["numero_indice"])))
    factors = {}
    for y in range(2013, 2026):
        arr = ipca[y]
        if len(arr) != 12 or len(set(k for k, _ in arr)) != 12 or any(v is None or v <= 0 for _, v in arr):
            raise ValueError(f"IPCA incompleto ou duplicado: {y}")
        average = sum((v for _, v in arr), Decimal(0)) / Decimal(12)
        factors[y] = BASE / average
    rows = []
    for r in read_csv(dca_path):
        code, year = r["cod_ibge"], int(r["ano"])
        if code not in cities or not 2013 <= year <= 2025:
            continue
        c = cities[code]
        pop = number(r.get("populacao_dca"))
        x = {"cod_ibge": code, "municipio": c["municipio"],
             "subregiao": REGIONS[c["subregiao"]], "ano": year,
             "populacao_dca": pop, "fator_ipca_media": factors[year]}
        for field in FIELDS:
            nominal = number(r.get(field))
            real = nominal * factors[year] if nominal is not None else None
            x[field + "_nominal"] = nominal
            x[field + "_real_set2026"] = real
            x[field + "_real_pc_set2026"] = real / pop if real is not None and pop is not None and pop > 0 else None
        rows.append(x)
    if len(rows) != 442 or len({(x["cod_ibge"], x["ano"]) for x in rows}) != 442:
        raise ValueError("Recorte RMRP com cardinalidade inesperada: esperado 442 unico municipio-ano")
    output.mkdir(parents=True, exist_ok=True)
    def rounded(v):
        if v is None:
            return ""
        return str(v.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
    for region in REGIONS.values():
        subset = sorted((x for x in rows if x["subregiao"] == region), key=lambda x: (x["cod_ibge"], x["ano"]))
        fn = output / ("rmrp_" + region.replace("Sub-região de ", "").lower().replace("ã", "a").replace("é", "e").replace(" ", "_") + "_real_2013_2025.csv")
        with open(fn, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(subset[0]), delimiter=";")
            writer.writeheader()
            for x in subset:
                writer.writerow({k: rounded(v) if isinstance(v, Decimal) else v for k, v in x.items()})
    # Reconciliar apenas os totais completos: todos os municipios da subregiao com a rubrica e populacao.
    for region in REGIONS.values():
        for y in range(2013, 2026):
            group = [x for x in rows if x["subregiao"] == region and x["ano"] == y]
            for field in FIELDS:
                observed = [x[field + "_real_set2026"] for x in group]
                if len(observed) != len(group) or any(v is None for v in observed):
                    continue
                total = sum(observed, Decimal(0))
                if total < 0:
                    print("AVISO: total negativo", region, y, field)
    print("442 registros; quatro arquivos; base setembro/2026; ausencias preservadas")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dca", type=Path, required=True)
    p.add_argument("--territorio", type=Path, required=True)
    p.add_argument("--ipca-mensal", type=Path, required=True)
    p.add_argument("--saida", type=Path, required=True)
    a = p.parse_args()
    build(a.dca, a.territorio, a.ipca_mensal, a.saida)
if __name__ == "__main__":
    main()
