#!/usr/bin/env python3
"""G06F: inspect current official Transferegov openapi; no blind joins or estimated effects."""
from __future__ import annotations
import csv,hashlib,json,re,sys,time
from datetime import datetime,timezone
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.error import HTTPError,URLError
ROOT=Path("build/rmsjrp-g06f");ROOT.mkdir(parents=True,exist_ok=True)
BASE="https://api-publica.transferegov.gestao.gov.br"
MODULES=("especiais","parcerias","discricionarias","fundoafundo")
PILOTS=[("3549805","São José do Rio Preto"),("3533908","Olímpia"),("3530300","Mirassol"),("3525706","José Bonifácio"),("3500204","Adolfo")]
CATALOG=Path("editorial/rmsjrp/MUNICIPIOS_SUBREGIOES_2025.csv")
with CATALOG.open(encoding="utf-8",newline="") as f: cities=list(csv.DictReader(f,delimiter=";"))
assert len(cities)==37 and len(set(x["cod_ibge"] for x in cities))==37
assert all(any(c["cod_ibge"]==code for c in cities) for code,_ in PILOTS)
def fetch(url,limit=7_000_000):
    req=Request(url,headers={"User-Agent":"RMSJRP-evidence-QA/1.0","Accept":"application/json"})
    with urlopen(req,timeout=45) as resp:
        assert resp.status==200
        typ=resp.headers.get("Content-Type","")
        data=resp.read(limit+1)
    if len(data)>limit:raise ValueError("size_limit")
    return data,typ
results=[];paths=[];pilot=[]
for mod in MODULES:
    d={"module":mod,"observed_at_utc":datetime.now(timezone.utc).isoformat(),"openapi_url":f"{BASE}/{mod}/openapi.json"}
    try:
        b,typ=fetch(d["openapi_url"])
        spec=json.loads(b)
        assert isinstance(spec,dict) and isinstance(spec.get("paths"),dict)
        d.update({"status":"openapi_verified","sha256":hashlib.sha256(b).hexdigest(),
                  "n_paths":len(spec["paths"]),"title":spec.get("info",{}).get("title",""),
                  "server_urls":[s.get("url") for s in spec.get("servers",[]) if isinstance(s,dict)]})
        for name,v in spec["paths"].items():
            if not isinstance(v,dict):continue
            for verb,op in v.items():
                if verb.lower()!="get" or not isinstance(op,dict):continue
                params=[]
                for p in op.get("parameters",[]):
                    if not isinstance(p,dict):continue
                    if "$ref" in p:
                        key=p["$ref"].split("/")[-1]
                        p=spec.get("components",{}).get("parameters",{}).get(key,p)
                    params.append({"name":p.get("name",""),"in":p.get("in",""),"required":p.get("required",False),
                                  "type":p.get("schema",{}).get("type","") if isinstance(p.get("schema"),dict) else ""})
                relevant=bool(re.search(r"municip|beneficiar|instrument|conv|propost|emend|pagament|programa|transfer|planos-acao",name,re.I))
                geographic=[p for p in params if re.search(r"municip|ibge|local|uf|codigo|c[oó]digo|nome",p["name"],re.I)]
                paths.append({"modulo":mod,"rota":name,"verbo":"GET","relevante":str(relevant).lower(),
                              "filtros_geograficos":" | ".join(p["name"] for p in geographic),
                              "parametros_json":json.dumps(params,ensure_ascii=False,separators=(",",":")),
                              "situacao":"rota_documentada_na_openapi"})
        d["n_get"]=sum(1 for p in paths if p["modulo"]==mod)
        (ROOT/f"OPENAPI_{mod.upper()}.json").write_bytes(b)
    except Exception as e:
        d.update({"status":"fetch_failed","error":f"{type(e).__name__}: {str(e)[:300]}"})
    results.append(d)
# No pilot calls until paths are inspected: filters and identifiers must first be grounded.
out=ROOT/"ROTAS_OFICIAIS_G06F.csv"
if paths:
    with out.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(paths[0]),delimiter=";")
        w.writeheader();w.writerows(paths)
summary={"status":"pass" if any(r["status"]=="openapi_verified" for r in results) else "blocked",
"scope":"discover verified official OpenAPI paths, before data retrieval",
"checked_at_utc":datetime.now(timezone.utc).isoformat(),
"municipios_universo":len(cities),"municipios_piloto":PILOTS,
"modules":results,"n_routes":len(paths),
"documented_geo_filter_routes":[{"modulo":x["modulo"],"rota":x["rota"],"parametros":x["filtros_geograficos"]}
 for x in paths if x["relevante"]=="true" and x["filtros_geograficos"]][:50],
"limitations":["A documented endpoint is not proof of existing instruments in any municipality",
"No federal empenho/payment or local liquidation derived",
"Discretionary/legal API rollout is staged; unavailable endpoints remain unknown",
"Do not equate proposals, plans or agreements with paid transfers",
"No causal attribution to LC 200/2023"],
"files_sha256":{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.glob("*.json")}}
(ROOT/"QA_G06F_API_DESCOBERTA.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"status":summary["status"],"modules":[{"module":x["module"],"status":x["status"],"n_paths":x.get("n_paths"),"error":x.get("error")} for x in results],"n_routes":len(paths),"geo_routes":summary["documented_geo_filter_routes"][:15]},ensure_ascii=False))
# absence of all APIs is a blocked research checkpoint, not an empty result set.
if summary["status"]=="blocked":sys.exit(2)
