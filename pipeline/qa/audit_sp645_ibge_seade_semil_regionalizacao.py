#!/usr/bin/env python3
"""Audit IBGE7 municipal territorial dimensions from direct government records.
No electoral points or election zones in inputs.
"""
from __future__ import annotations
import csv,json,hashlib
from pathlib import Path
from collections import defaultdict, Counter
SRC=Path("governance/DIM_SP645_IBGE_RA_RG_SEMIL_SEADE_2026_11_14.csv")
DIM=Path("governance/DIM_SP645_IBGE_RA_RG_RM_AU_CONSOLIDADA_2026_11_14.csv")
RG_RA=Path("governance/DIM_HIERARQUIA_SEADE_RG_RA_GEOMETRIA_2026_11_14.csv")
RMRP=Path("governance/INV_RMRP_34_MUNICIPIOS_PILOTO_IBGE_VERIFICADO_2026_11_11.csv")
def load(path):
    with path.open(encoding="utf-8-sig",newline="") as handle:return list(csv.DictReader(handle,delimiter=";"))
def main():
    a,b,h,m=map(load,(SRC,DIM,RG_RA,RMRP))
    assert len(a)==len(b)==645
    ids={r["codigo_ibge"] for r in a};assert len(ids)==645 and all(len(i)==7 and i.startswith("35") for i in ids)
    assert ids=={r["codigo_ibge"] for r in b}
    amap={r["codigo_ibge"]:r for r in a}
    parents={r["rg_codigo"]:r["ra_codigo"] for r in h}
    assert len(h)==len(parents)==43
    ra=Counter();rg=Counter();rm=defaultdict(set);rgs=defaultdict(set);missing=[];differences=[]
    for row in b:
        ib=row["codigo_ibge"];ref=amap[ib]
        for key in ("ra_codigo","ra_nome","rg_codigo","rg_nome"):
            assert row[key]==ref[key],(ib,key)
        assert row["ra_rg_referencia"]=="SEADE_SEMIL_CONSULTA_2026_11_14"
        assert row["rm_au_referencia"]=="COMPOSICAO_RM_AU_2025"
        assert parents[row["rg_codigo"]]==row["ra_codigo"]
        ra[row["ra_codigo"]]+=1;rg[row["rg_codigo"]]+=1
        rgs[row["rg_codigo"]].add(row["ra_codigo"])
        if row["rm_au_codigo"]:
            assert row["rm_au_tipo"] in ("RM","AU")
            assert row["rm_au_situacao"]=="RM_AU_2025_COM_VINCULO"
            rm[(row["rm_au_tipo"],row["rm_au_codigo"],row["rm_au_nome"])].add(ib)
        else:
            assert row["rm_au_tipo"]==row["rm_au_nome"]==""
            assert row["rm_au_situacao"]=="FORA_RM_AU_2025"
    assert len(ra)==16 and sum(ra.values())==645
    assert len(rg)==43 and sum(rg.values())==645
    assert all(len(x)==1 for x in rgs.values())
    assert len(rm)==10 and sum(map(len,rm.values()))==255
    assert sum(t=="RM" for t,c,n in rm)==9 and sum(t=="AU" for t,c,n in rm)==1
    assert len(set().union(*rm.values()))==255
    rmrp={r["codigo_ibge"] for r in m};assert len(rmrp)==34
    rm_rp=next(s for (t,c,n),s in rm.items() if n=="Região Metropolitana de Ribeirão Preto")
    assert rm_rp==rmrp
    report={"status":"QA_PASS_MUNICIPAL_IBGE_DIRECT_GOVERNMENT_SOURCE","ibge645":len(ids),
      "ra":len(ra),"rg":len(rg),"rg_with_multiple_ra":0,
      "rm_au":len(rm),"rm":9,"au":1,"municipalities_rm_au":255,
      "municipalities_outside_rm_au":390,"rmrp_roster":34,"rmrp_symmetric_difference":0,
      "source":{"url":"https://mapas.semil.sp.gov.br/server/rest/services/Hosted/Limite_Muncipal_IGC_Seade/FeatureServer/0/query",
        "fields":["cod_ibge","municipio","gid_ra","gid_rg","ra","rg"],
        "retrieval_date":"2026-11-14","source_exceeded_transfer_limit":False},
      "artifacts_sha256":{str(path):hashlib.sha256(path.read_bytes()).hexdigest() for path in (SRC,DIM,RG_RA,RMRP)},
      "note":"Source is municipal records by IBGE7, NOT electoral points. RA/RG source reference date must be verified before interpreting historical validity.",
      "no_financial_data_changed":True}
    print(json.dumps(report,ensure_ascii=False,indent=2))
    Path("/tmp/inv_sp645_regionalizacao_qa.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
if __name__=="__main__":main()
