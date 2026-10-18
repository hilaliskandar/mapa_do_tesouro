#!/usr/bin/env python3
"""Auditoria cruzada de observacoes municipais vs medianas publicadas na API."""
import argparse,json,math,pathlib,statistics
from build_boletins import BASE, EXCLUDE, fetch, normalize_universes

def close(x,y):
    return math.isclose(float(x),float(y),rel_tol=1e-9,abs_tol=0.011)

def run(base,out):
    idx,_=fetch(base+"/publication/universes.json")
    report=[]
    for item in normalize_universes(idx):
        uid=item["publication_id"]
        if uid in EXCLUDE:continue
        ctx,_=fetch(f"{base}/publication/universes/{uid}/context.json")
        mun=[]
        for member in ctx["members"]:
            code=str(member["codigo_ibge"])
            obj,_=fetch(f"{base}/publication/universes/{uid}/municipalities/{code}.json")
            mun.append(obj)
        failures=[]
        audited=0
        for key,entry in ctx["variables"].items():
            latest=entry.get("latest") or {}
            n=latest.get("numeric") or {}
            if n.get("median") is None:continue
            values=[]
            for m in mun:
                detail=m.get("variables",{}).get(key,{})
                row=detail.get("latest") or {}
                val=row.get("value")
                if row.get("status")=="observado" and isinstance(val,(float,int)) and not isinstance(val,bool):
                    values.append(float(val))
            if len(values)!=latest.get("observed"):
                failures.append(f"{key}: observados {len(values)} vs {latest.get('observed')}")
                continue
            if not values:
                failures.append(f"{key}: mediana presente sem observacoes")
                continue
            median=statistics.median(values)
            if not close(median,n["median"]):
                failures.append(f"{key}: mediana diverge, {median} vs {n['median']}")
            if n.get("sum") is not None and not close(sum(values),n["sum"]):
                failures.append(f"{key}: soma diverge")
            audited+=1
        report.append({"universo":uid,"municipios":len(mun),"indicadores_auditados":audited,"divergencias":failures})
    (out/"qa_paridade_municipal.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    bad=[(r["universo"],r["divergencias"]) for r in report if r["divergencias"]]
    if bad:raise ValueError(f"Paridade municipal divergente: {bad[:5]}")
    print(f"Paridade API aprovada: {sum(r['indicadores_auditados'] for r in report)} combinacoes universo/indicador")
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--base",default=BASE);p.add_argument("--out",default="build/editorial-universes")
    a=p.parse_args();run(a.base.rstrip("/"),pathlib.Path(a.out))
