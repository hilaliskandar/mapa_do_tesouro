#!/usr/bin/env python3
"""Confere a matriz de decomposição TCESP e seu vínculo editorial."""
import csv
from collections import defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parent
CSV=ROOT/"dados/rmj_decomposicao_programas_acoes_2023_2025.csv"
HTML=ROOT/"index.html"
with CSV.open(encoding="utf-8-sig",newline="") as f:
    rows=list(csv.DictReader(f,delimiter=";"))
assert len(rows)==1169,len(rows)
totals=defaultdict(int)
for r in rows:
    initial=int(r["liquidado_inicial_centavos"])
    final=int(r["liquidado_final_centavos"])
    delta=int(r["variacao_centavos"])
    assert final-initial==delta,r
    assert r["nivel"] in ("programa","acao")
    assert int(r["ano_final"])-int(r["ano_inicial"])==1
    key=(r["municipio"],r["ano_inicial"],r["ano_final"],r["nivel"])
    totals[key]+=delta
assert len(totals)==28,len(totals)
for municipio in sorted({k[0] for k in totals}):
    for period in (("2023","2024"),("2024","2025")):
        assert totals[municipio,*period,"programa"]==totals[municipio,*period,"acao"],(municipio,period)
html=HTML.read_text(encoding="utf-8")
assert html.count('<section id="explorador-investimentos">')==1
assert 'dados/rmj_decomposicao_programas_acoes_2023_2025.csv' in html
assert 'id="ex-tbody"' in html and 'id="ex-cidade"' in html
assert 'Explore todas as variações por programa e ação' in html
assert '<script>' in html and html.count('<script>')==1
print("OK: 1169 registros; 28 decomposições; 14 reconciliações cruzadas; HTML vinculado")
