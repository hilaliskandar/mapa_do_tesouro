#!/usr/bin/env python3
"""Inventario exato de decomposicoes realmente exibidas nas 280 fichas HTML."""
import argparse,json,re
from collections import Counter
from pathlib import Path
IDS=("tributos_imobiliarios","transferencias_selecionadas","despesa_territorial","despesas_capital_selecionadas","receitas_capital_selecionadas")
def audit(root):
    files=sorted(root.glob("publicacoes/*/municipios/*.html"))
    if len(files)!=280:raise ValueError(f"Esperadas 280 fichas, encontradas {len(files)}")
    aggregate=Counter();by_universe={}
    for f in files:
        html=f.read_text(encoding="utf-8")
        ids=re.findall(r'data-total="([^"]+)"',html)
        if any(x not in IDS for x in ids) or len(ids)!=len(set(ids)):raise ValueError(f"Marcacao invalida: {f}")
        aggregate.update(ids)
        u=f.parent.parent.name
        row=by_universe.setdefault(u,{"fichas":0,"com_algum_grafico":0,"agregados":dict.fromkeys(IDS,0)})
        row["fichas"]+=1
        row["com_algum_grafico"]+=int(bool(ids))
        for x in ids:row["agregados"][x]+=1
    return {"fichas":len(files),"com_algum_grafico":sum(x["com_algum_grafico"] for x in by_universe.values()),
            "agregados":{k:aggregate[k] for k in IDS},"universos":by_universe}
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--root",type=Path,required=True);p.add_argument("--out",type=Path,required=True)
    a=p.parse_args();out=audit(a.root);a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({"fichas":out["fichas"],"com_algum_grafico":out["com_algum_grafico"],"agregados":out["agregados"]},ensure_ascii=False))
