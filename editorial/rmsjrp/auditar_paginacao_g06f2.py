#!/usr/bin/env python3
"""G06F2: inspect official pagination and evidence-grade status taxonomy.
No monetary transfers or paid amounts inferred from proposal endpoints.
"""
from __future__ import annotations
import json,csv,re,hashlib
from urllib.request import Request,urlopen
from urllib.parse import urlencode
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path("build/rmsjrp-g06f2");ROOT.mkdir(parents=True,exist_ok=True)
BASE="https://api-publica.transferegov.gestao.gov.br"
CANDIDATES=[
 ("parcerias","/proposta","cd_ibge_recebedor","3549805"),
 ("discricionarias","/propostas","cod_munic_ibge","3549805"),
 ("parcerias","/proposta","cd_ibge_recebedor","3500204"),
 ("discricionarias","/propostas","cod_munic_ibge","3500204")]
def req(url):
    r=Request(url,headers={"Accept":"application/json","User-Agent":"RMSJRP-G06F2/1.0"})
    with urlopen(r,timeout=35) as f:
        data=f.read(2000000)
        assert f.status==200
    return json.loads(data.decode("utf-8-sig"))
def records(obj):
    if isinstance(obj,list):return obj,"list"
    if isinstance(obj,dict):
        for k in ("items","data","results","records","content","dados"):
            if isinstance(obj.get(k),list):return obj[k],k
    return [],"unknown"
schemas=[];samples=[]
for module,path,param,ibge in CANDIDATES:
    if not any(s["module"]==module and s["path"]==path for s in schemas):
        spec=req(f"{BASE}/{module}/openapi.json")
        op=spec["paths"][path]["get"]
        fields=[]
        for p in op.get("parameters",[]):
            if "$ref" in p:
                p=spec.get("components",{}).get("parameters",{}).get(p["$ref"].split("/")[-1],p)
            fields.append({"name":p.get("name"),"in":p.get("in"),"required":p.get("required",False),
               "type":(p.get("schema") or {}).get("type"),
               "description":str(p.get("description") or "")[:300]})
        response=op.get("responses",{})
        schemas.append({"module":module,"path":path,"params":fields,
           "status_code_schemas":{status:list((r.get("content") or {}).keys()) for status,r in response.items() if isinstance(r,dict)},
           "pagination_fields":[x for x in fields if re.search(r"page|pagina|limit|size|offset|skip|take|per_page",x["name"] or "",re.I)]})
    url=f"{BASE}/{module}{path}?"+urlencode({param:ibge})
    try:
        obj=req(url)
        rr,shape=records(obj)
        ids=[]
        for entry in rr:
            if not isinstance(entry,dict):continue
            ident=entry.get("id_proposta",entry.get("id",entry.get("numero_proposta","")))
            if ident is not None:ids.append(str(ident))
        resp_meta={k:str(v)[:250] for k,v in obj.items() if k not in ("data","items","results","records","content","dados")} if isinstance(obj,dict) else {}
        samples.append({"module":module,"ibge":ibge,"url":url,"status":"http_200",
            "shape":shape,"count_first_response":len(rr),"unique_ids_first_response":len(set(ids)),
            "first_ids":ids[:5],"last_ids":ids[-5:],
            "response_meta":resp_meta,
            "status_labels_sample":list(sorted(set(str(x.get("situacao_proposta",x.get("situacao",""))) for x in rr if isinstance(x,dict))))[:25]})
    except Exception as e:
        samples.append({"module":module,"ibge":ibge,"url":url,"status":"blocked",
            "error":type(e).__name__+":"+str(e)[:200]})
qa={"checked_utc":datetime.now(timezone.utc).isoformat(),"sources":schemas,"test_queries":samples,
"status":"pass" if sum(z["status"]=="http_200" for z in samples)>=2 else "partial",
"caveats":["No pagination operation performed without schema proof",
 "First response may be incomplete and contains proposals of various status",
 "No inference about executed amounts or impact LC200",
 "No claims of coverage for non-pilot municipalities"]}
(ROOT/"QA_G06F2_PAGINACAO.json").write_text(json.dumps(qa,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"status":qa["status"],"schema":[{"mod":s["module"],"params":s["params"],"pagination":s["pagination_fields"]} for s in schemas],
"sample":[{"mod":s["module"],"ibge":s["ibge"],"status":s["status"],"count":s.get("count_first_response"),
"unique":s.get("unique_ids_first_response"),"first":s.get("first_ids"),"last":s.get("last_ids"),
"meta":s.get("response_meta"),"error":s.get("error")} for s in samples]},ensure_ascii=False))
