"""Statewide 2026 delivery inventory; preserve raw public metadata, never infer fiscal zero."""
import argparse,csv,hashlib,json,time
from collections import Counter
from datetime import datetime,timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request,urlopen
p=argparse.ArgumentParser()
p.add_argument("--output",type=Path,required=True)
p.add_argument("--offset",type=int,default=0)
p.add_argument("--limit",type=int,default=645)
a=p.parse_args()
with Path("governance/DIM_SP645_IBGE_RA_RG_RM_AU_CONSOLIDADA_2026_11_14.csv").open(encoding="utf-8-sig") as f:
    roster=list(csv.DictReader(f,delimiter=";"))
assert len(roster)==645 and len({r["codigo_ibge"] for r in roster})==645
# RMRP first, remaining municipalities in stable IBGE order.
roster.sort(key=lambda r:(r["rm_au_nome"]!="Região Metropolitana de Ribeirão Preto",r["codigo_ibge"]))
assert sum(r["rm_au_nome"]=="Região Metropolitana de Ribeirão Preto" for r in roster)==34
assert 0<=a.offset<645 and 1<=a.limit<=645
selected=roster[a.offset:a.offset+a.limit]
a.output.mkdir(parents=True,exist_ok=True)
rawdir=a.output/"raw";rawdir.mkdir(exist_ok=True)
base="https://apidatalake.tesouro.gov.br/ords/siconfi/tt/extrato_entregas"
results=[]
for r in selected:
    code=r["codigo_ibge"]
    item={"codigo_ibge":code,"municipio":r["municipio"],"checked_at":datetime.now(timezone.utc).isoformat()}
    try:
        req=Request(base+"?"+urlencode({"id_ente":code,"an_referencia":2026}),headers={"Accept":"application/json","User-Agent":"mapa-do-tesouro-SP645-delivery-inventory/1"})
        with urlopen(req,timeout=25) as response:
            raw=response.read(4_000_001)
            assert response.status==200
        assert len(raw)<=4_000_000
        obj=json.loads(raw.decode("utf-8-sig"))
        (rawdir/(code+".json")).write_bytes(raw)
        item["sha256"]=hashlib.sha256(raw).hexdigest()
        assert isinstance(obj["items"],list) and not obj.get("hasMore")
        item["status"]="responded" if obj["items"] else "empty_not_zero"
        item["deliveries"]=obj["items"]
    except Exception as exc:
        item["status"]="unavailable"
        item["error"]=f"{type(exc).__name__}: {str(exc)[:250]}"
    results.append(item)
    time.sleep(1.1)
    if len(results)%25==0: print("DELIVERY_PROGRESS",len(results),flush=True)
summary={"year":2026,"offset":a.offset,"requested":len(selected),"roster_count":645,"status_counts":dict(Counter(r["status"] for r in results)),"delivery_types":dict(Counter(str(d.get("entregavel")) for r in results for d in r.get("deliveries",[]))),"publication_authorized":False,"limitations":"Raw status codes retained; no conclusion about compliance or missing fiscal values."}
(a.output/"inventory.json").write_text(json.dumps({"summary":summary,"municipalities":results},ensure_ascii=False,indent=2),encoding="utf-8")
print("SICONFI_2026_DELIVERY_INVENTORY",json.dumps(summary,ensure_ascii=False))
