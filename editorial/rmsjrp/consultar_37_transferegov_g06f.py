#!/usr/bin/env python3
"""G06-F: bounded first-page coverage for 37 RMSJRP municipalities in 2 open official APIs.
No total/count claims beyond first page. No payment, disbursement or LC200 effects inferred.
"""
from __future__ import annotations
import csv,hashlib,json,re,time
from datetime import datetime,timezone
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.parse import urlencode
ROOT=Path("build/rmsjrp-g06f-37");ROOT.mkdir(parents=True,exist_ok=True)
with Path("editorial/rmsjrp/MUNICIPIOS_SUBREGIOES_2025.csv").open(encoding="utf-8",newline="") as f:
    cities=list(csv.DictReader(f,delimiter=";"))
assert len(cities)==37 and len(set(x["cod_ibge"] for x in cities))==37
MODULES=[
 {"mod":"parcerias","path":"/proposta","param":"cd_ibge_recebedor"},
 {"mod":"discricionarias","path":"/propostas","param":"cod_munic_ibge"}
]
BASE="https://api-publica.transferegov.gestao.gov.br"
def fetch(url,limit=1500000):
    request=Request(url,headers={"Accept":"application/json","User-Agent":"RMSJRP-G06F-open-data-audit/1.0"})
    with urlopen(request,timeout=28) as r:
        assert r.status==200
        data=r.read(limit+1)
    if len(data)>limit:raise ValueError("response_over_1_5MB")
    return json.loads(data.decode("utf-8-sig"))
def arr(obj):
    if isinstance(obj,list):return obj,"list"
    if isinstance(obj,dict):
        for k in ("data","items","results","records","content","dados"):
            if isinstance(obj.get(k),list):return obj[k],k
    return [],"unknown"
def matched(row,c):
    code=c["cod_ibge"];name=c["municipio"].casefold().strip()
    evidence=[]
    for k,v in row.items():
        if not re.search("ibge|municip",k,re.I):continue
        if isinstance(v,(str,int)):
            vv=str(v)
            if vv==code or vv==code[:6]:evidence.append("code:"+k)
            elif vv.casefold().strip()==name:evidence.append("name:"+k)
    return evidence
summary=[];candidates=[];metadata=[]
for conf in MODULES:
    mod,path,param=conf["mod"],conf["path"],conf["param"]
    spec=fetch(f"{BASE}/{mod}/openapi.json",7_000_000)
    assert path in spec.get("paths",{})
    params={p.get("name") for p in spec["paths"][path]["get"].get("parameters",[]) if isinstance(p,dict)}
    assert param in params,(mod,path,param)
    metadata.append({"modulo":mod,"rota":path,"filtro":param,
        "openapi_sha256":hashlib.sha256(json.dumps(spec,sort_keys=True,ensure_ascii=False).encode()).hexdigest()})
    for c in cities:
        cid=c["cod_ibge"]
        url=f"{BASE}/{mod}{path}?"+urlencode({param:cid})
        row={"modulo":mod,"municipio":c["municipio"],"cod_ibge":cid,
             "subregiao":c["subregiao_pdui"],"url":url,
             "status":"","primeira_resposta_registros":"","primeira_resposta_confirmados_geo":"",
             "ids_amostra":"","forma_resposta":"","erro":"","completude":"nao_verificada_sem_paginacao"}
        try:
            obj=fetch(url)
            records,shape=arr(obj)
            row["status"]="http_200";row["forma_resposta"]=shape
            row["primeira_resposta_registros"]=len(records)
            seen=set()
            for item in records:
                if not isinstance(item,dict):continue
                ev=matched(item,c)
                if not ev:continue
                proposal_id=str(item.get("id_proposta",item.get("id",item.get("numero_proposta",""))))[:60]
                if proposal_id and proposal_id not in seen:
                    seen.add(proposal_id)
                    if len([x for x in candidates if x["modulo"]==mod and x["cod_ibge"]==cid])<6:
                        candidates.append({"modulo":mod,"cod_ibge":cid,"municipio":c["municipio"],
                          "subregiao":c["subregiao_pdui"],"identificador_proposta":proposal_id,
                          "id_programa":str(item.get("id_programa",""))[:60],
                          "situacao":str(item.get("situacao_proposta",item.get("situacao","")))[:80],
                          "ano_proposta":str(item.get("ano_proposta",item.get("ano","")))[:20],
                          "codigo_territorial_confirmado_por":"|".join(ev),
                          "fonte_url":url,"natureza_evidencia":"proposta_na_primeira_resposta_nao_pagamento"})
            row["primeira_resposta_confirmados_geo"]=len(seen)
            row["ids_amostra"]="|".join(list(seen)[:6])
        except Exception as exc:
            row["status"]="erro_http_ou_formato"
            row["erro"]=type(exc).__name__+":"+str(exc)[:180]
        summary.append(row)
        time.sleep(.10)
assert len(summary)==74
def output(file,rows):
    p=ROOT/file
    if not rows:return None
    with p.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter=";");w.writeheader();w.writerows(rows)
    return {"file":file,"rows":len(rows),"sha256":hashlib.sha256(p.read_bytes()).hexdigest()}
artifacts=[output("G06F_COBERTURA_37x2.csv",summary),output("G06F_PROPOSTAS_CANDIDATAS_AMOSTRA.csv",candidates)]
qa={"status":"pass" if any(s["status"]=="http_200" for s in summary) else "blocked",
 "data_utc":datetime.now(timezone.utc).isoformat(),"municipios":37,"consultas":74,
 "respostas_ok":sum(s["status"]=="http_200" for s in summary),
 "consultas_com_confirmacao_geo":sum(bool(s["primeira_resposta_confirmados_geo"]) and int(s["primeira_resposta_confirmados_geo"])>0 for s in summary),
 "registros_candidatos_amostrados":len(candidates),
 "fontes":metadata,"resultados_por_modulo":[{"modulo":mod,"consultas":37,
   "ok":sum(s["status"]=="http_200" and s["modulo"]==mod for s in summary),
   "com_confirmacao":sum(s["modulo"]==mod and str(s["primeira_resposta_confirmados_geo"]).isdigit() and int(s["primeira_resposta_confirmados_geo"])>0 for s in summary)}
   for mod in ("parcerias","discricionarias")],
 "artefatos":[x for x in artifacts if x],
 "limites":["No pagination verified; counts describe only first response",
          "Only geocoded candidates kept; no inference that other municipalities have zero proposals",
          "Proposals may be drafts/approved; they are not signed instruments or paid transfers",
          "No audited finance amounts or municipal liquidations",
          "No attribution to LC 200"]}
(ROOT/"QA_G06F_COBERTURA.json").write_text(json.dumps(qa,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"status":qa["status"],"consultas":qa["consultas"],"ok":qa["respostas_ok"],
"com_geo":qa["consultas_com_confirmacao_geo"],"amostra":len(candidates),
"modulos":qa["resultados_por_modulo"],"erros":[{"modulo":s["modulo"],"municipio":s["municipio"],"erro":s["erro"]} for s in summary if s["status"]!="http_200"][:8]},ensure_ascii=False))
if qa["status"]=="blocked":raise SystemExit(2)
