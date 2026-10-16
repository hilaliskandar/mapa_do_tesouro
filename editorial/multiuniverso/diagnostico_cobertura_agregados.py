#!/usr/bin/env python3
"""Diagnostico auditavel da cobertura: usa os 280 JSONs do pacote aprovado."""
import argparse,collections,json,math
from pathlib import Path
from graficos_agregados import GROUPS,observed,reconcile

def classify(variables,total_id,components):
    keys=[total_id]+[key for key,_ in components]
    absent=[k for k in keys if k not in variables]
    if absent:return "variavel_fora_catalogo",absent
    values={k:observed(variables[k]) for k in keys}
    missing=[k for k in keys if values[k] is None]
    if missing:return "sem_observacao_valida",missing
    if len({v[1] for v in values.values()})!=1:return "exercicio_incompativel",[]
    total=values[total_id][0]
    if total<=0 or any(values[k][0]<0 for k,_ in components):return "montante_invalido",[]
    summed=math.fsum(values[k][0] for k,_ in components)
    if not math.isclose(total,summed,rel_tol=1e-9,abs_tol=0.01):return "divergencia_soma",[]
    return "aprovado",[]

def audit(root):
    docs=sorted((root/"data/api/v1/publication/universes").glob("*/municipalities/*.json"))
    if len(docs)!=280:raise ValueError(f"Quantidade inesperada de JSONs: {len(docs)}")
    counts={ident:collections.Counter() for ident,_,_ in GROUPS}
    missing={ident:collections.Counter() for ident,_,_ in GROUPS}
    breakdown={};without=[]
    for p in docs:
        d=json.loads(p.read_text(encoding="utf-8"))
        code=p.stem;uid=p.parent.parent.name
        vars=d.get("variables") or {}
        accepted,_=reconcile(d)
        approved={x[0] for x in accepted}
        if not approved:without.append({"universo":uid,"codigo_ibge":code,"municipio":d.get("municipality",{}).get("nome")})
        row=breakdown.setdefault(uid,{"fichas":0,"com_alguma":0,"agregados":{id:collections.Counter() for id,_,_ in GROUPS}})
        row["fichas"]+=1;row["com_alguma"]+=bool(approved)
        for ident,_,components in GROUPS:
            status,details=classify(vars,ident,components)
            assert (status=="aprovado")== (ident in approved),(p,ident,status)
            counts[ident][status]+=1;row["agregados"][ident][status]+=1
            missing[ident].update(details)
    return {"total_fichas":len(docs),"sem_decomposicao":without,
       "motivos":{k:dict(v) for k,v in counts.items()},
       "componentes_sem_observacao":{k:dict(v) for k,v in missing.items()},
       "por_universo":{k:{"fichas":v["fichas"],"com_alguma":v["com_alguma"],"agregados":{a:dict(b) for a,b in v["agregados"].items()}} for k,v in breakdown.items()}}
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--root",type=Path,required=True);p.add_argument("--out",type=Path,required=True)
    a=p.parse_args();report=audit(a.root);a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"total_fichas":report["total_fichas"],"sem_decomposicao":report["sem_decomposicao"],"motivos":report["motivos"],"componentes_sem_observacao":report["componentes_sem_observacao"]},ensure_ascii=False))
