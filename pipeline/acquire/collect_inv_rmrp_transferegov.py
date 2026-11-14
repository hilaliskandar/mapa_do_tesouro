#!/usr/bin/env python3
"""RMRP: evidence-first Transferegov collection. No canonical database writes."""
import csv, hashlib, json, os, time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

BASE="https://api-publica.transferegov.gestao.gov.br"
ROOT=Path(os.getenv("INV_OUTPUT","build/inv-rmrp-transferegov"))
ROOT.mkdir(parents=True,exist_ok=True)
CATALOG=Path("governance/INV_RMRP_34_MUNICIPIOS_PILOTO_IBGE_VERIFICADO_2026_11_11.csv")
MODULES=[("parcerias","/proposta","cd_ibge_recebedor"),("discricionarias","/propostas","cod_munic_ibge")]
MAX_PAGES=int(os.getenv("INV_MAX_PAGES","250"))
MAX_BYTES=12_000_000
HEADERS={"Accept":"application/json","User-Agent":"mapa-do-tesouro-RMRP-evidence-collector/1.0"}
def request(url):
    last=None
    for attempt in range(4):
        try:
            with urlopen(Request(url,headers=HEADERS),timeout=40) as response:
                if response.status!=200:raise ValueError("unexpected_status")
                body=response.read(MAX_BYTES+1)
                if len(body)>MAX_BYTES:raise ValueError("oversized_response")
                return json.loads(body.decode("utf-8-sig")),body
        except (HTTPError,URLError,TimeoutError) as e:
            last=e
            if isinstance(e,HTTPError) and e.code not in (429,500,502,503,504):break
            time.sleep(min(2**attempt,8))
    raise RuntimeError(str(last))
def as_records(obj):
    if isinstance(obj,list):return obj,"root_array"
    if isinstance(obj,dict):
        for key in ("data","items","results","records","content","dados"):
            if isinstance(obj.get(key),list):return obj[key],key
    raise ValueError("unrecognized_records_shape")
def parameters(spec,path):
    op=spec["paths"][path]["get"]
    params=[]
    for p in op.get("parameters",[]):
        if "$ref" in p:p=spec.get("components",{}).get("parameters",{}).get(p["$ref"].split("/")[-1],p)
        if p.get("in")=="query":params.append(p.get("name"))
    return params
def page_metadata(obj):
    if not isinstance(obj,dict):return {}
    out={}
    for key in ("total","total_items","totalItems","total_registros","totalPages","total_pages","total_paginas","page","pagina","paginaAtual","has_next","hasNext","next"):
        if key in obj:out[key]=obj[key]
    return out
def sha(data):return hashlib.sha256(data).hexdigest()
cities=list(csv.DictReader(CATALOG.open(encoding="utf-8",newline=""),delimiter=";"))
assert len(cities)==34 and len({x["codigo_ibge"] for x in cities})==34
manifest={"created_at":datetime.now(timezone.utc).isoformat(),"scope":"RMRP 34 cities, proposal records only, no payments inferred","modules":[],"consultations":[],"files":[],"limitations":[]}
for mod,path,filter_name in MODULES:
    try:
        spec,raw=request(f"{BASE}/{mod}/openapi.json")
        params=parameters(spec,path)
        if filter_name not in params:raise ValueError("geographic_filter_not_in_openapi")
        page_param=next((x for x in ("pagina","page","numero_pagina","numeroPagina","page_number","pageNumber") if x in params),None)
        size_param=next((x for x in ("tamanho_da_pagina","tamanho_pagina","page_size","size","limit","per_page") if x in params),None)
        file=ROOT/f"openapi_{mod}.json";file.write_bytes(raw)
        manifest["files"].append({"path":str(file),"sha256":sha(raw),"bytes":len(raw)})
        manifest["modules"].append({"module":mod,"status":"openapi_verified","path":path,"parameters":params,"page_parameter":page_param,"size_parameter":size_param,"openapi_sha256":sha(raw)})
    except Exception as e:
        manifest["modules"].append({"module":mod,"status":"blocked","error":repr(e)})
        continue
    for city in cities:
        code=city["codigo_ibge"]; parts=[];seen_payloads=set();status="unverified";error=None
        for index in range(1,MAX_PAGES+1):
            q={filter_name:code}
            if page_param:q[page_param]=index
            if size_param:q[size_param]=100
            url=f"{BASE}/{mod}{path}?"+urlencode(q)
            try:
                obj,raw=request(url);records,shape=as_records(obj)
            except Exception as e:
                status="failed_or_partial";error=repr(e);break
            digest=sha(raw)
            if digest in seen_payloads:
                status="partial_repeated_page";break
            seen_payloads.add(digest)
            # Preserve exact source reply, not just an interpreted subset.
            p=ROOT/mod/code/f"page_{index:04d}.json"
            p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
            manifest["files"].append({"path":str(p),"sha256":digest,"bytes":len(raw)})
            parts.append({"page":index,"records":len(records),"shape":shape,"metadata":page_metadata(obj),"sha256":digest,"url":url})
            if not page_param:
                status="first_page_only_pagination_unavailable";break
            if not records:
                status="complete_empty_terminal_page";break
            meta=page_metadata(obj)
            total_pages=next((meta[k] for k in ("totalPages","total_pages","total_paginas") if isinstance(meta.get(k),int)),None)
            if total_pages is not None and index>=total_pages:
                status="complete_by_reported_total_pages";break
            if meta.get("has_next") is False or meta.get("hasNext") is False:
                status="complete_by_next_flag";break
            if meta.get("next") is None and "next" in meta:
                status="complete_by_next_flag";break
        else:status="partial_max_pages_reached"
        manifest["consultations"].append({"module":mod,"ibge7":code,"municipio":city["municipio"],"status":status,"pages":parts,"error":error,"reported_records":sum(x["records"] for x in parts)})
        print(json.dumps({"module":mod,"ibge7":code,"status":status,"pages":len(parts)},ensure_ascii=False),flush=True)
manifest["statistics"]={"municipalities":len(cities),"planned_queries":len(cities)*len(MODULES),"consultations":len(manifest["consultations"]),"complete":sum(c["status"].startswith("complete_") for c in manifest["consultations"]),"first_page_only":sum(c["status"]=="first_page_only_pagination_unavailable" for c in manifest["consultations"]),"failed_or_partial":sum(c["status"].startswith(("failed","partial")) for c in manifest["consultations"])}
manifest["limitations"]=["No proposal is proof of signed instrument or actual payment","Only explicit termination indicators classify pagination complete","API schema controls each query; modules not published are blocked","Responses are raw and must be classified capital vs operating expenses before fiscal aggregation","No data was imported to canonical SQLite or deployed"]
out=ROOT/"manifest.json";out.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(manifest["statistics"],ensure_ascii=False))
if not manifest["statistics"]["consultations"]:raise SystemExit(2)
