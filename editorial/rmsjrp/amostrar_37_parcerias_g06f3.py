#!/usr/bin/env python3
"""G06F3: one historical approved Partnership proposal per municipality (37); documentary linkage pilot.
No estimation of totals, transfers, payment or LC200 impacts.
"""
import csv,json,os,hashlib,datetime,time
from pathlib import Path
from urllib.request import urlopen,Request
from urllib.parse import urlencode
from collections import defaultdict
from deployment.download_r2_source import download_r2_object
ROOT=Path("build/rmsjrp-g06f3-cohort");ROOT.mkdir(parents=True,exist_ok=True)
PREFIX="rmsjrp/g06/2026_11_09/instrumentos_api_f2/"
def download(name):
    target=ROOT/name
    download_r2_object(account_id=os.environ["CLOUDFLARE_ACCOUNT_ID"],
       api_token=os.environ["CLOUDFLARE_API_TOKEN"],bucket=os.environ["CLOUDFLARE_R2_BUCKET"],
       object_key=PREFIX+name,output=target)
    return target
qa=json.loads(download("QA_G06F2.json").read_text(encoding="utf8"))
assert qa["status"]=="pass" and qa["qa_pass"]==74 and qa["registros_propostas_canonicas_com_geo"]==9338
expected=next(a["sha256"] for a in qa["artifacts"] if a["name"]=="G06F2_PROPOSTAS_CANONICAS.csv")
source=download("G06F2_PROPOSTAS_CANONICAS.csv")
assert hashlib.sha256(source.read_bytes()).hexdigest()==expected
with source.open(encoding="utf8",newline="") as f: allrows=list(csv.DictReader(f,delimiter=";"))
pp=[x for x in allrows if x["modulo"]=="parcerias"]
assert len(pp)==508
bycity=defaultdict(list)
for p in pp:
    if p["id_proposta"]:bycity[p["codigo_ibge"]].append(p)
assert len(bycity)==37
# pre-registered sampling: oldest approved 2025 first, then earliest available.
def selection_key(x):
    status=x["situacao_original"].casefold()
    return (0 if "aprovad" in status else 1, x["ano_proposta"] or "9999", int(x["id_proposta"]) if x["id_proposta"].isdigit() else 999999999)
cohort=[sorted(group,key=selection_key)[0] for code,group in sorted(bycity.items())]
BASE="https://api-publica.transferegov.gestao.gov.br/parcerias"
def fetch(path,params):
    url=BASE+path+"?"+urlencode(params);err=""
    for retry in range(2):
        try:
            with urlopen(Request(url,headers={"Accept":"application/json","User-Agent":"RMSJRP-G06F3/1.0"}),timeout=40) as r:
                assert r.status==200
                data=r.read(3_000_000)
            if len(data)>=3_000_000:raise ValueError("response_too_large")
            return json.loads(data),hashlib.sha256(data).hexdigest(),url,""
        except Exception as e:err=type(e).__name__+": "+str(e)[:150];time.sleep(1+retry)
    return None,"",url,err
def lst(o):
    if isinstance(o,list):return o
    if isinstance(o,dict):
        for key in ("items","data","content","records","results","dados"):
            if isinstance(o.get(key),list):return o[key]
    return []
records=[];commitments=[]
for p in cohort:
    pid=p["id_proposta"];mod="parcerias"
    obj,sha,url,err=fetch("/parceria",{"id_proposta":pid,"pagina":1,"tamanho_da_pagina":50})
    related=[x for x in lst(obj) if isinstance(x,dict) and str(x.get("id_proposta"))==pid]
    rec={"codigo_ibge":p["codigo_ibge"],"municipio":p["municipio"],
        "id_proposta":pid,"ano_proposta":p["ano_proposta"],"situacao_original":p["situacao_original"],
        "criterio_amostragem":"primeira_aprovada_ano_antigo_por_municipio",
        "qtd_parcerias_correspondentes":len(related),"id_parcerias":"|".join(str(x.get("id_parceria","")) for x in related),
        "data_assinatura":"|".join(str(x.get("dh_assinatura") or "") for x in related),
        "publicacao_data":"|".join(str(x.get("publicacao_dt_publicacao") or "") for x in related),
        "url_documento_publicado":"|".join(str(x.get("publicacao_ds_url_documento_publicado") or "")[:220] for x in related),
        "estado_registro":"erro_acesso" if err else "parceria_registro" if related else "sem_parceria_retornada",
        "documento_assinado_lido":"nao","pagamento_federal_comprovado":"nao",
        "fonte_url":url,"sha_resposta":sha,"erro":err}
    for item in related:
        parid=str(item.get("id_parceria") or "")
        if not parid:continue
        o,h,u,e=fetch("/empenho-parceria",{"id_parceria":parid,"pagina":1,"tamanho_da_pagina":50})
        for x in lst(o):
            if not isinstance(x,dict) or str(x.get("id_parceria"))!=parid:continue
            commitments.append({"codigo_ibge":p["codigo_ibge"],"municipio":p["municipio"],
               "id_proposta":pid,"id_parceria":parid,
               "id_empenho_parceria":str(x.get("id_empenho_parceria") or ""),
               "numero_empenho":str(x.get("nr_empenho",x.get("numero_empenho","")))[:80],
               "ano_empenho":str(x.get("aa_empenho") or ""),
               "valor_empenho_nao_pagamento":str(x.get("valor_empenho") or ""),
               "url":u,"sha":h,"status":"registro_empenho_nao_pagamento"})
    records.append(rec)
    print(json.dumps({"codigo":p["codigo_ibge"],"proposta":pid,"parcerias":len(related),"assinada_metadado":sum(bool(x.get("dh_assinatura")) for x in related),"empenhos":sum(x["id_proposta"]==pid for x in commitments),"erro":err},ensure_ascii=False),flush=True)
def export(name,rs):
    if not rs:return None
    path=ROOT/name
    with path.open("w",encoding="utf8",newline="") as h:
        w=csv.DictWriter(h,fieldnames=list(rs[0]),delimiter=";");w.writeheader();w.writerows(rs)
    return {"file":name,"rows":len(rs),"sha256":hashlib.sha256(path.read_bytes()).hexdigest()}
outputs=[export("G06F3_AMOSTRA_37_CADEIAS.csv",records),export("G06F3_EMPENHOS_37.csv",commitments)]
qaout={"status":"pass" if len(records)==37 and all(not x["erro"] for x in records) else "partial",
    "collected_at_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "selection_rule":"One earliest approved proposal from Parcerias per municipality; not representative of 9338 proposals",
    "municipalities":len(records),"parcerias_registradas":sum(x["qtd_parcerias_correspondentes"] for x in records),
    "com_metadado_assinatura":sum(bool(x["data_assinatura"]) for x in records),
    "com_metadado_publicacao":sum(bool(x["publicacao_data"]) for x in records),
    "registros_empenhos":len(commitments),
    "access_failures":sum(bool(x["erro"]) for x in records),
    "f2_source_sha256":expected,"files":[x for x in outputs if x],
    "limitations":["No random representative sample; do not generalize a 37-observation signing rate",
    "Date of signature is metadata, not an independently verified signed contract",
    "Commitments are not bank payments or liquidated municipal expenses",
    "No LC 200 causal effects estimated"]}
(ROOT/"QA_G06F3_AMOSTRA37.json").write_text(json.dumps(qaout,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
print("FINAL_QA="+json.dumps(qaout,ensure_ascii=False),flush=True)
