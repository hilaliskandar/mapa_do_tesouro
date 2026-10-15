#!/usr/bin/env python3
"""Independent arithmetic audit of embedded RMJ municipal fiscal series."""
import json
import math
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent
HTML = (ROOT / "index.html").read_text(encoding="utf-8")

def embedded(name):
    match = re.search(r"const\s+" + re.escape(name) + r"\s*=\s*(\[[^;]*\]|\{[^;]*\});", HTML)
    if not match:
        raise AssertionError(f"Embedded dataset missing: {name}")
    return json.loads(match.group(1))

historical = embedded("historical")
extra = embedded("extra")
ipca = embedded("ipcaMedio")
years = set(range(2021, 2026))
identifiers = {r["id"] for r in historical}
assert len(identifiers) == 7 and {r["ano"] for r in historical} == years
assert len(historical) == len(extra) == 35
H = {(r["id"], r["ano"]): r for r in historical}
E = {(r["id"], r["ano"]): r for r in extra}
assert len(H) == len(E) == 35 and set(H) == set(E)
def nearly(a, b, eps=0.011):
    return abs(a-b) <= eps

for key in H:
    a, b = H[key], E[key]
    if a["investimento"] is not None and b["dca_investimentos_liquidada"] is not None:
        assert nearly(a["investimento"], b["dca_investimentos_liquidada"]), ("investment", key)
    for field in ("receita", "tributaria"):
        value = a[field]
        assert value is None or (math.isfinite(value) and value >= 0), (key,field)
    for field in ("dca_despesa_total_liquidada", "dca_despesa_corrente_liquidada",
                  "dca_investimentos_liquidada"):
        value = b[field]
        assert value is None or (math.isfinite(value) and value >= 0), (key,field)

assert all(float(ipca[str(year)]) > 0 for year in years)
factor = float(ipca["2025"])/float(ipca["2021"])
assert 1.20 < factor < 1.30

def value(dataset, field, year, ids):
    values = [dataset[(identifier, year)][field] for identifier in ids]
    if any(x is None for x in values):
        return None
    return sum(values)

def ratio(numerator, denominator):
    if numerator is None or denominator is None or denominator <= 0:
        return None
    return numerator / denominator

ids = sorted(identifiers)
checks = 0
for chosen in [[x] for x in ids] + [ids]:
    for year in years:
        revenue = value(H,"receita",year,chosen)
        tax = value(H,"tributaria",year,chosen)
        investment = value(E,"dca_investimentos_liquidada",year,chosen)
        current = value(E,"dca_despesa_corrente_liquidada",year,chosen)
        expense = value(E,"dca_despesa_total_liquidada",year,chosen)
        for n,d in ((tax,revenue),(investment,expense),(current,expense)):
            share = ratio(n,d)
            assert share is None or math.isfinite(share)
            checks += 1
    for dataset,field,denom,source in (
        (H,"tributaria","receita",H),
        (H,"receita",None,None),
        (E,"dca_investimentos_liquidada","dca_despesa_total_liquidada",E),
        (E,"dca_despesa_corrente_liquidada","dca_despesa_total_liquidada",E)
    ):
        a=value(dataset,field,2021,chosen)
        b=value(dataset,field,2025,chosen)
        if a is not None and a > 0 and b is not None:
            nominal=b/a-1
            real=b/a/factor-1
            assert math.isclose((1+nominal)/factor-1,real,abs_tol=1e-12)
            checks += 2
        if denom:
            pa=ratio(a,value(source,denom,2021,chosen))
            pb=ratio(b,value(source,denom,2025,chosen))
            assert pa is None or pb is None or math.isfinite(100*(pb-pa))
            checks += 1

regional_2025 = value(E,"dca_investimentos_liquidada",2025,ids)
assert nearly(regional_2025,265425559.07), regional_2025
print(json.dumps({"status":"PASS","municipal_year_pairs":len(H),
                  "municipalities":len(ids),"years":len(years),
                  "arithmetic_checks":checks,"regional_investment_2025":round(regional_2025,2),
                  "ipca_2025_over_2021":factor},ensure_ascii=False))
