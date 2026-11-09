#!/usr/bin/env python3
"""G06F pilot: constrained, source-verified official federal-transfer API searches.
No extrapolation, no monetary aggregates, no attribution to LC 200/2023.
"""
from __future__ import annotations
import csv,hashlib,json,re,time
from datetime import datetime,timezone
from pathlib import Path
from urllib.parse import urlencode,urljoin
from urllib.request import Request,urlopen
ROOT=Path("build/rmsjrp-g06f-piloto");ROOT.mkdir(parents=True,exist_ok=True)
API="https://api-publica.transferegov.gestao.gov.br"
cities_path=Path("editorial/rmsjrp/MUNICIPIOS_SUBREGIOES_2025.csv")
with cities_path.open(encoding="utf-8",newline="") as f:
    allcities={r["cod_ibge"]:r for r in csv.DictReader(f,delimiter=";")}
PILOTS=["3549805","3533908","3530300","3525706","3500204"]
assert len(allcities)==37 and all(x in allcities for x in PILOTS)
QUERY=[
 ("parcerias","/proposta","cd_ibge_recebedor","code"),
 ("discricionarias","/propostas","cod_munic_ibge","code"),
 ("fundoafundo","/planos-acao","codigo_ibge_municipio_ente_recebedor_plano_acao","code"),
 ("especiais","/beneficiarios-especiais","nome_beneficiario","name"),
]
def fetch(url,timeout=18,max_size=750000):
    req=Request(url,headers={"User-Agent":"RMSJRP-G06F-public-research/1.0",
      "Accept":"application/json"})
    with urlopen(req,timeout=timeout) as r:
        assert r.status==200
        b=r.read(max_size+1)
    if len(b)>max_size:raise ValueError("oversized_payload")
    return json.loads(b.decode("utf-8-sig")),b
def data_records(obj):
    if isinstance(obj,list):return obj,"list"
    if isinstance(obj,dict):
        for k in ("data","items","results","records","content","dados"):
            if isinstance(obj.get(k),list):return obj[k],k
        # Single record is not proof of a listable hit; keep a diagnostic.
    return [],"unknown_shape"
def safe_string(x):
    if isinstance(x,(str,int,float)):return str(x)
    return ""
def test_municipality_match(row,city):
    name=city["municipio"].casefold()
    code=city["cod_ibge"]
    identifiers=[];names=[]
    for k,v in row.items():
        if isinstance(v,(dict,list)):continue
        val=safe_string(v)
        if re.search(r"ibge|munic",k,re.I):
            if val==code or val==code[:6]:identifiers.append(k)
            if name in val.casefold():names.append(k)
    return identifiers,names
sources={};results=[];examples=[]
for module,path,param,kind in QUERY:
    url=f"{API}/{module}/openapi.json"
    try:
        spec,b=fetch(url,timeout=30,max_size=7500000)
        p=spec["paths"][path]["get"]
        available={x.get("name"):x for x in p.get("parameters",[]) if isinstance(x,dict)}
        assert param in available,(module,path,"filter_not_in_schema")
        servers=spec.get("servers") or []
        root=servers[0].get("url","") if servers else ""
        if root.startswith("/"):root=API+root
        if not root.startswith("http"):root=API+"/"+module
        url_root=root.rstrip("/")
        sources[module]={"sha256":hashlib.sha256(b).hexdigest(),"url_base":url_root,
             "path":path,"parameter":param,"status":"openapi_validated"}
    except Exception as e:
        sources[module]={"status":"openapi_invalid_or_blocked","error":type(e).__name__+":"+str(e)[:180]}
        continue
    for cid in PILOTS:
        city=allcities[cid];value=city["municipio"] if kind=="name" else cid
        candidate=f"{url_root}{path}"
        # Only the municipality filter; no guessing whether 'limit' is valid.
        query=urlencode({param:value})
        url=candidate+"?"+query
        row={"modulo":module,"rota":path,"municipio":city["municipio"],"cod_ibge":cid,
           "filtro":param,"valor_filtro":value,"url_consulta":url,
           "consulta_status":"","forma_resposta":"","total_retornado_primeira_resposta":"",
           "evidencia_localizacao":"","exemplos_ids":"","observacao":""}
        try:
            obj,b=fetch(url)
            records,shape=data_records(obj)
            row["consulta_status"]="http_200"
            row["forma_resposta"]=shape
            row["total_retornado_primeira_resposta"]=str(len(records))
            verified=[]
            sample=[]
            for item in records[:10]:
                if not isinstance(item,dict):continue
                codes,names=test_municipality_match(item,city)
                if codes or names:
                    verified.append("codigo" if codes else "nome")
                    id_fields={k:safe_string(v)[:100] for k,v in item.items() if re.search(r"^(id_|id$|nr_|num_|cod_|codigo_|situacao_proposta$|ano_proposta$|dt_proposta$)",k,re.I) and not isinstance(v,(list,dict))}
                    sample.append({"identificadores":dict(list(id_fields.items())[:8]),
                      "campo_confirmacao":codes+names,"chaves":list(item)[:60]})
            row["evidencia_localizacao"]=" | ".join(sorted(set(verified))) if verified else "nenhuma_correspondencia_verificada"
            row["exemplos_ids"]=json.dumps([s["identificadores"] for s in sample[:2]],ensure_ascii=False,separators=(",",":"))
            row["observacao"]="Amostra limitada; itens não confirmados não são instrumentos validados"
            if sample:
                examples.append({"modulo":module,"municipio":city["municipio"],"cod_ibge":cid,
                                 "url":url,"records_with_geo_evidence":len(sample),"samples":sample[:2]})
        except Exception as e:
            row["consulta_status"]="erro_ou_bloqueio"
            row["observacao"]=type(e).__name__+":"+str(e)[:250]
        results.append(row)
        time.sleep(.15)
assert len(results)>=5,"no queries attempted"
csvpath=ROOT/"G06F_PILOTO_ENDPOINTS.csv"
with csvpath.open("w",encoding="utf-8",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(results[0]),delimiter=";")
    w.writeheader();w.writerows(results)
qa={"status":"pass" if any(r["consulta_status"]=="http_200" for r in results) else "blocked",
    "observed_at_utc":datetime.now(timezone.utc).isoformat(),
    "municipios_piloto":PILOTS,"consultas":len(results),
    "consultas_http_200":sum(r["consulta_status"]=="http_200" for r in results),
    "com_registro_e_validacao_geo":sum(r["evidencia_localizacao"] not in ("","nenhuma_correspondencia_verificada") for r in results),
    "fontes":sources,"examples_verified_geo":examples[:20],
    "csv_sha256":hashlib.sha256(csvpath.read_bytes()).hexdigest(),
    "limitations":["A first-page response is not exhaustive coverage or proof of zero elsewhere",
    "Municipality matched by an explicit field only; false name matches require follow-up",
    "Proposals/plans/beneficiaries are not necessarily executed agreements",
    "No paid amount, received transfer or liquidated municipal investment certified",
    "No effect of LC 200/2023 measured"]}
(ROOT/"QA_G06F_PILOTO.json").write_text(json.dumps(qa,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"status":qa["status"],"consultas":qa["consultas"],"http_200":qa["consultas_http_200"],
"com_registro_e_validacao_geo":qa["com_registro_e_validacao_geo"],
"sample":examples[:4],"errors":[{"module":r["modulo"],"city":r["municipio"],"error":r["observacao"]} for r in results if r["consulta_status"]!="http_200"][:8]},ensure_ascii=False))
