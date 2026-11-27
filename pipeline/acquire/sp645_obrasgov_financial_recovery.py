"""Recover frozen missing project IDs, reusing verified inventory and pilot."""
import argparse,collections,concurrent.futures,hashlib,json,tarfile,subprocess,sys
from pathlib import Path
from pipeline.acquire.collect_rmrp_obrasgov_planned_values import fetch_one
p=argparse.ArgumentParser();p.add_argument("--inventory",type=Path,required=True);p.add_argument("--offset",type=int,required=True);p.add_argument("--limit",type=int,default=100);p.add_argument("--out",type=Path,required=True);a=p.parse_args()
with tarfile.open(a.inventory) as tf:
    def read(name):
        matches=[m for m in tf.getmembers() if m.isfile() and Path(m.name).name==name]
        assert len(matches)==1
        return json.load(tf.extractfile(matches[0]))
    inv=read("inventory.json");pilot=read("values.json")
assert len(inv["projects"])==4224 and len(inv["pending_ids"])==4006
assert len(pilot)==100 and all(r["estado"]=="ok" for r in pilot)
done={r["id_projeto_investimento"] for r in pilot}
assert done==set(inv["pending_ids"][:100])
pending=[k for k in inv["pending_ids"] if k not in done]
assert len(pending)==3906 and len(set(pending))==3906
selected=pending[a.offset:a.offset+a.limit]
assert selected
a.out.mkdir(parents=True,exist_ok=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    rows=list(pool.map(fetch_one,selected))
assert [r["id_projeto_investimento"] for r in rows]==selected
for r in rows:r["codigo_ibge_proponente"]=inv["projects"][r["id_projeto_investimento"]]
(a.out/"values.json").write_text(json.dumps(rows,ensure_ascii=False))
qa={"offset":a.offset,"requested":len(selected),"status":dict(collections.Counter(r["estado"] for r in rows)),"with_planned_values":sum(bool(r.get("investimentos_previstos")) for r in rows),"publication_authorized":False}
(a.out/"qa.json").write_text(json.dumps(qa,indent=2))
print("OBRAS_RECOVERY_BATCH",json.dumps(qa),flush=True)
