#!/usr/bin/env python3
"""Compara fichas E2 ao CSV extraido independentemente do Siconfi DCA."""
import argparse,csv,json,math,pathlib
from build_boletins import BASE,fetch,normalize_universes,EXCLUDE

SENTINELS={"3501608","3509502","3520509","3525904","3556206"}
CHECKS=("dca_receita_corrente_bruta","dca_receita_tributaria_bruta","dca_iptu_principal","dca_itbi_principal","dca_iss_principal","dca_investimentos_liquidada","dca_func_urbanismo_liquidada","dca_func_habitacao_liquidada","dca_func_saneamento_liquidada","dca_func_transporte_liquidada")
def audit(csv_path,base,out):
    with open(csv_path,encoding="utf-8",newline="") as h:
        official={r["cod_ibge"]:r for r in csv.DictReader(h)}
    assert SENTINELS<=set(official),(sorted(SENTINELS-set(official)))
    index,_=fetch(base+"/publication/universes.json")
    comparisons=[]
    mismatches=[]
    seen=set()
    for universe in normalize_universes(index):
        uid=universe["publication_id"]
        if uid in EXCLUDE:continue
        ctx,_=fetch(base+"/publication/universes/"+uid+"/context.json")
        members={str(m["codigo_ibge"]) for m in ctx["members"]}
        for code in sorted(SENTINELS & members):
            seen.add(code)
            obj,_=fetch(base+"/publication/universes/"+uid+"/municipalities/"+code+".json")
            for key in CHECKS:
                raw=official[code].get(key,"")
                detail=(obj.get("variables") or {}).get(key)
                if detail is None or raw=="":continue
                latest=detail.get("latest") or {}
                if latest.get("status")!="observado":continue
                value=latest.get("value")
                if not isinstance(value,(int,float)) or isinstance(value,bool):continue
                valid=math.isclose(float(raw),float(value),rel_tol=1e-10,abs_tol=.01)
                record={"universe":uid,"municipality":code,"variable":key,"official":float(raw),"editorial":float(value),"equal":valid}
                comparisons.append(record)
                if not valid:mismatches.append(record)
    report={"method":"Official Siconfi DCA 2025 independently acquired CSV versus E2 municipality API 2025","municipalities_compared":sorted(seen),"variables":list(CHECKS),"comparisons":len(comparisons),"mismatches":mismatches}
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    assert len(seen)>=3 and len(comparisons)>=25,(len(seen),len(comparisons))
    if mismatches:raise ValueError("DCA E2 divergencias: "+repr(mismatches[:5]))
    print(f"DCA oficial x E2: {len(comparisons)} comparacoes, {len(seen)} municipios, 0 divergencias.")
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--csv",required=True)
    p.add_argument("--base",default=BASE)
    p.add_argument("--out",default="build/qa-dca-e2.json")
    a=p.parse_args();audit(a.csv,a.base.rstrip("/"),pathlib.Path(a.out))
