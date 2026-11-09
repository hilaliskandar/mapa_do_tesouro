#!/usr/bin/env python3
"""Discover *existing* instrument/financial execution API routes and their parameter contracts.
Does not assert records were paid or signed. Canonical schema evidence only.
"""
import csv,datetime,hashlib,json,re
from pathlib import Path
from urllib.request import Request,urlopen
R=Path("build/rmsjrp-g06f3-discovery");R.mkdir(parents=True,exist_ok=True)
BASE="https://api-publica.transferegov.gestao.gov.br"
modules=("parcerias","discricionarias","especiais","fundoafundo")
rows=[];results=[]
for m in modules:
  endpoint=f"{BASE}/{m}/openapi.json"
  try:
    with urlopen(Request(endpoint,headers={"Accept":"application/json","User-Agent":"RMSJRP-G06F3/1.0"}),timeout=40) as h:
      raw=h.read(6_000_000)
    spec=json.loads(raw)
    sha=hashlib.sha256(raw).hexdigest()
    (R/f"OPENAPI_{m}.json").write_bytes(raw)
    for route,methods in spec["paths"].items():
      if not isinstance(methods,dict) or not isinstance(methods.get("get"),dict):continue
      op=methods["get"]
      params=[]
      for p in (methods.get("parameters") or [])+(op.get("parameters") or []):
        if not isinstance(p,dict):continue
        if "$ref" in p:p=spec.get("components",{}).get("parameters",{}).get(p["$ref"].split("/")[-1],p)
        params.append({"name":p.get("name"),"required":p.get("required",False),"location":p.get("in"),
                       "type":(p.get("schema") or {}).get("type")})
      alltext=" ".join([route,op.get("summary") or "",op.get("description") or ""])
      if re.search(r"instrument|conv[eê]n|empenh|pagam|liquid|desembols|financeir|celebra|execu|repasse|beneficiar|propost",alltext,re.I):
        rows.append({"module":m,"path":route,"operation_id":op.get("operationId",""),
           "summary":(op.get("summary") or "")[:250],
           "description":(op.get("description") or "")[:400],
           "parameters_json":json.dumps(params,ensure_ascii=False,separators=(",",":")),
           "response_schema_ref":str((op.get("responses",{}).get("200",{}).get("content",{}).get("application/json",{}).get("schema",{}).get("$ref",""))),
           "source_url":endpoint,"source_sha256":sha,
           "route_class":"financial_candidate" if re.search("pagam|desembols|empenh|financeir|liquid",alltext,re.I) else "instrument_candidate"})
    results.append({"module":m,"status":"ok","n_paths":len(spec["paths"]),"sha256":sha})
  except Exception as e:results.append({"module":m,"status":"error","error":type(e).__name__+": "+str(e)[:200]})
if rows:
  with (R/"G06F3_ROTAS_INSTRUMENTOS_FINANCEIRO.csv").open("w",newline="",encoding="utf8") as h:
    w=csv.DictWriter(h,fieldnames=list(rows[0]),delimiter=";");w.writeheader();w.writerows(rows)
qa={"time_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"modules":results,"routes":len(rows),
"financial_candidates":sum(x["route_class"]=="financial_candidate" for x in rows),
"routes_preview":[{"module":r["module"],"path":r["path"],"parameters":json.loads(r["parameters_json"])} for r in rows[:100]],
"limitations":["Route existence is not data completeness","Neither celebration nor payments verified by route availability",
"Rollout of instruments and financial modules may be incomplete in November 2026"]}
(R/"QA_G06F3_ROUTES.json").write_text(json.dumps(qa,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
print("RESULT_JSON="+json.dumps({"modules":results,"routes":len(rows),"financial":qa["financial_candidates"],
"candidates":qa["routes_preview"][:50]},ensure_ascii=False),flush=True)
if not rows:raise SystemExit(2)
