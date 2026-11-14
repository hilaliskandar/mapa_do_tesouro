#!/usr/bin/env python3
"""QA territorial SP645: exact membership, RG -> RA and RM/AU dimension.

Candidate data from EL2026 is NOT a normative RA/RG homologation.
"""
from __future__ import annotations
import csv,json,hashlib,sys
from collections import defaultdict,Counter
from pathlib import Path

CANDIDATE=Path("governance/INV_SP645_CROSSWALK_RA_RG_RM_AU_EL2026_CANDIDATO_2026_11_14.csv")
RMRP=Path("governance/INV_RMRP_34_MUNICIPIOS_PILOTO_IBGE_VERIFICADO_2026_11_11.csv")
OUTPUT=Path("governance/INV_SP645_QA_TERRITORIAL_EL2026_2026_11_14.json")

def read_csv(p):
    with p.open(encoding="utf-8-sig",newline="") as f:
        return list(csv.DictReader(f,delimiter=";"))

def main():
    records=read_csv(CANDIDATE)
    rmrp=read_csv(RMRP)
    valid={r["codigo_ibge"] for r in records}
    assert len(records)==645 and len(valid)==645
    assert all(len(ib)==7 and ib.startswith("35") and ib.isdigit() for ib in valid)
    assert len({r["codigo_tse"] for r in records})==645
    assert all(r["ra_codigo_seade"] and r["rg_codigo_seade"] for r in records)
    assert all(r["ra_rg_status"]=="RA_RG_SEADE_2021_PROXY_NAO_HOMOLOGADO" for r in records)
    ras=defaultdict(set);rgs=defaultdict(set);rgs_parent=defaultdict(set);met=defaultdict(set)
    for r in records:
        ras[r["ra_codigo_seade"]].add(r["codigo_ibge"])
        rgs[r["rg_codigo_seade"]].add(r["codigo_ibge"])
        rgs_parent[r["rg_codigo_seade"]].add(r["ra_codigo_seade"])
        typ,code=r["rm_au_tipo"],r["rm_au_codigo"]
        if typ or code:
            assert typ in ("RM","AU") and code and r["rm_au_nome"]
            met[(typ,code,r["rm_au_nome"])].add(r["codigo_ibge"])
        else:
            assert r["rm_au_situacao"]=="FORA_RM_AU_2025"
    assert len(ras)==16 and sum(map(len,ras.values()))==645
    assert len(rgs)==43 and sum(map(len,rgs.values()))==645
    assert all(len(parents)==1 for parents in rgs_parent.values())
    assert len(met)==10 and sum(map(len,met.values()))==255
    assert len(set().union(*met.values()))==255
    assert sum(k[0]=="RM" for k in met)==9 and sum(k[0]=="AU" for k in met)==1
    expected={r["codigo_ibge"] for r in rmrp}
    actual=next(v for k,v in met.items() if k[2]=="Região Metropolitana de Ribeirão Preto")
    assert len(expected)==34 and expected==actual
    region_intersections=[]
    for (typ,code,name),members in sorted(met.items()):
        parent_ra={r["ra_codigo_seade"] for r in records if r["codigo_ibge"] in members}
        parent_rg={r["rg_codigo_seade"] for r in records if r["codigo_ibge"] in members}
        region_intersections.append({"tipo":typ,"codigo":code,"nome":name,"municipios":len(members),
             "ra_abrangidas":len(parent_ra),"rg_abrangidas":len(parent_rg)})
    report={
        "status":"PASS_CADASTRAL_WITH_RA_RG_NON_HOMOLOGATED",
        "candidate_sha256":hashlib.sha256(CANDIDATE.read_bytes()).hexdigest(),
        "candidate_rows":645,"ibge7_distinct":645,
        "administrative_regions":len(ras),"government_regions":len(rgs),
        "rg_spanning_multiple_ra":sum(len(s)!=1 for s in rgs_parent.values()),
        "metro_regions":sum(k[0]=="RM" for k in met),"urban_agglomerations":sum(k[0]=="AU" for k in met),
        "municipalities_in_rm_au":255,"municipalities_outside_rm_au":390,
        "municipalities_in_rmrp":len(actual),"rmrp_roster_difference":0,
        "metro_ra_rg_intersections":region_intersections,
        "source_status":"EL2026 RA/RG 2021 inferred via voting location points: DIAGNOSTICO_NAO_HOMOLOGADO; RM/AU 2025 user-supplied workbook; update/legality to verify",
        "limitations":["No topological audit of Seade boundaries has been performed in this QA",
          "RA/RG membership is a proxy until corroborated with official municipal regionalization",
          "Aggregations by RA and RM/AU must never be added together",
          "Do not assign project location from municipality of proponent",
          "Source version 2025/2021, not proof of current 2026 normative composition",
          "No financial amounts were calculated or modified"]}
    OUTPUT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:report[k] for k in ("status","candidate_rows","administrative_regions","government_regions","rg_spanning_multiple_ra","metro_regions","urban_agglomerations","municipalities_in_rm_au","municipalities_outside_rm_au","municipalities_in_rmrp","rmrp_roster_difference")},ensure_ascii=False))
if __name__=="__main__":main()
