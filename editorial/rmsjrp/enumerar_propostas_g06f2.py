#!/usr/bin/env python3
"""G06-F2: enumerate actual paginated proposal endpoints for all 37 RMSJRP cities.

A proposal is NOT a signed transfer instrument and never a federal disbursement.
Partial/failed endpoints remain unknown, never zero. Source page hashes retained.
"""
from __future__ import annotations
import csv,hashlib,json,re,sys,time
from collections import Counter,defaultdict
from datetime import datetime,timezone
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.parse import urlencode
ROOT=Path("build/rmsjrp-g06f2-full");ROOT.mkdir(parents=True,exist_ok=True)
BASE="https://api-publica.transferegov.gestao.gov.br"
with Path("editorial/rmsjrp/MUNICIPIOS_SUBREGIOES_2025.csv").open(encoding="utf-8",newline="") as f:
    CITIES=list(csv.DictReader(f,delimiter=";"))
assert len(CITIES)==37 and len({c["cod_ibge"] for c in CITIES})==37
MODULES=[("parcerias","/proposta","cd_ibge_recebedor"),("discricionarias","/propostas","cod_munic_ibge")]
SIZE=50
MAX_PAGES=60
def fetch(url):
    error=None
    for retry in range(3):
        try:
            req=Request(url,headers={"Accept":"application/json","User-Agent":"RMSJRP-G06F2-evidence/1.0"})
            with urlopen(req,timeout=45) as response:
                assert response.status==200
                body=response.read(5_000_001)
            if len(body)>5_000_000:raise ValueError("response_over_5_MB")
            return json.loads(body.decode("utf-8-sig")),hashlib.sha256(body).hexdigest(),len(body)
        except Exception as exc:
            error=f"{type(exc).__name__}: {str(exc)[:180]}"
            time.sleep(1+retry*2)
    raise RuntimeError(error)
def records_and_meta(o):
    if isinstance(o,dict):
        for k in ("data","items","results","records","content","dados"):
            if isinstance(o.get(k),list):
                return o[k],k
    if isinstance(o,list):return o,"list"
    raise ValueError("unrecognized_response_schema")
def geoevidence(o,c,mod):
    key="cd_ibge_recebedor" if mod=="parcerias" else "cod_munic_ibge"
    val=str(o.get(key,"")).strip()
    return "codigo_ibge" if val in (c["cod_ibge"],c["cod_ibge"][:6]) else ""
def get_first(o,keys):
    for k in keys:
        val=o.get(k)
        if val is not None and str(val).strip():
            return str(val).strip()
    return ""
def safe(x,max_len=100):return str(x or "")[:max_len]
def write_csv(name,rows):
    if not rows:return None
    f=ROOT/name
    with f.open("w",encoding="utf-8",newline="") as out:
        w=csv.DictWriter(out,fieldnames=list(rows[0]),delimiter=";")
        w.writeheader();w.writerows(rows)
    return {"file":name,"rows":len(rows),"sha256":hashlib.sha256(f.read_bytes()).hexdigest()}
coverage=[];pages=[];proposals=[];status_counts=Counter()
for module,path,filtername in MODULES:
    spec,_,_=fetch(f"{BASE}/{module}/openapi.json")
    declared={p.get("name") for p in spec["paths"][path]["get"].get("parameters",[]) if isinstance(p,dict)}
    assert {filtername,"pagina","tamanho_da_pagina"}.issubset(declared)
    for city in CITIES:
        base=f"{BASE}/{module}{path}"
        code=city["cod_ibge"]
        seen=set()
        row={"modulo":module,"codigo_ibge":code,"municipio":city["municipio"],
             "subregiao":city["subregiao_pdui"],"pagina_inicial":1,
             "paginas_declaradas":"","paginas_obtidas":0,"itens_declarados":"",
             "itens_obtidos":0,"ids_unicos":0,"sem_id":0,
             "divergencia_paginas":0,"divergencia_total":0,
             "status":"em_execucao","detalhe_falha":"","cobertura":"parcial_nao_homologada"}
        try:
            p=1
            while p<=MAX_PAGES:
                url=base+"?"+urlencode({filtername:code,"pagina":p,"tamanho_da_pagina":SIZE})
                response,sha,size=fetch(url)
                rr,shape=records_and_meta(response)
                if not isinstance(response,dict):raise ValueError("pagination_metadata_missing")
                declared_pages=response.get("total_pages")
                declared_items=response.get("total_items")
                if not isinstance(declared_pages,int) or not isinstance(declared_items,int):
                    raise ValueError("total_pages_or_total_items_missing")
                if p==1:
                    row["paginas_declaradas"]=declared_pages
                    row["itens_declarados"]=declared_items
                    if declared_pages>MAX_PAGES:raise ValueError("total_pages_exceeds_safety_limit")
                if declared_pages!=row["paginas_declaradas"] or declared_items!=row["itens_declarados"]:
                    row["divergencia_paginas"]=1
                    row["detalhe_falha"]="mutable_pagination_metadata"
                if response.get("page_number")!=p:raise ValueError("unexpected_page_number")
                pages.append({"modulo":module,"codigo_ibge":code,"pagina":p,"url":url,
                             "retorno_registros":len(rr),"total_paginas_resposta":declared_pages,
                             "total_itens_resposta":declared_items,"sha256_resposta":sha,"bytes":size})
                row["paginas_obtidas"]+=1
                row["itens_obtidos"]+=len(rr)
                for item in rr:
                    if not isinstance(item,dict):row["sem_id"]+=1;continue
                    geo=geoevidence(item,city,module)
                    if not geo:
                        row["detalhe_falha"]="geografia_nao_confirmada"
                        continue
                    idprop=get_first(item,("id_proposta",))
                    if not idprop:
                        row["sem_id"]+=1;continue
                    key=(module,code,idprop)
                    if key in seen:continue
                    seen.add(key)
                    status=get_first(item,("situacao_proposta","sit_proposta"))
                    year=get_first(item,("ano_proposta","ano_prop"))
                    if status:status_counts[(module,status)]+=1
                    proposals.append({
                        "modulo":module,"codigo_ibge":code,"municipio":city["municipio"],
                        "subregiao":city["subregiao_pdui"],"id_proposta":idprop,
                        "id_programa":get_first(item,("id_programa",)),
                        "ano_proposta":year,
                        "data_proposta":get_first(item,("dt_proposta","dia_proposta")),
                        "situacao_original":safe(status,120),
                        "modalidade":safe(get_first(item,("modalidade",)),100),
                        "orgao_concedente":safe(get_first(item,("desc_orgao","desc_orgao_sup")),140),
                        "possivel_celebracao_metadado":safe(get_first(item,("evento_celebracao",)),120),
                        "data_evento_celebracao":safe(get_first(item,("data_event_celebracao",)),30),
                        "valor_proposto_nao_pago":safe(get_first(item,("nr_vlr_total","vl_global_prop")),40),
                        "valor_repasse_proposto_nao_pago":safe(get_first(item,("vl_repasse_prop",)),40),
                        "chave_geo":geo,"estagio_prova":"proposta_localizada_nao_instrumento_pago",
                        "url_consulta_pagina":url})
                if p>=declared_pages:break
                p+=1
                time.sleep(.1)
            row["ids_unicos"]=len(seen)
            if row["itens_obtidos"]!=row["itens_declarados"]:
                row["divergencia_total"]=1
                row["detalhe_falha"]="count_mismatch"
            if not row["sem_id"] and not row["divergencia_total"] and not row["divergencia_paginas"] and not row["detalhe_falha"]:
                row["status"]="qa_pass"
                row["cobertura"]="completa_conforme_metadados_da_consulta"
            else:
                row["status"]="incompleta"
                row["cobertura"]="nao_homologada"
        except Exception as exc:
            row["status"]="erro_ou_bloqueio"
            row["detalhe_falha"]=f"{type(exc).__name__}: {str(exc)[:220]}"
            row["cobertura"]="nao_homologada"
        coverage.append(row)
        print(json.dumps({"mod":module,"codigo":code,"status":row["status"],
                         "obtidas":row["paginas_obtidas"],"declaradas":row["paginas_declaradas"],
                         "itens":row["itens_obtidos"],"meta_total":row["itens_declarados"]},ensure_ascii=False),flush=True)
assert len(coverage)==74
art=[write_csv("G06F2_COBERTURA_74_CONSULTAS.csv",coverage),
     write_csv("G06F2_AUDITORIA_PAGINAS.csv",pages),
     write_csv("G06F2_PROPOSTAS_CANONICAS.csv",proposals)]
art=[a for a in art if a]
statuses=[{"modulo":mod,"situacao_original":status,"quantidade":n} for (mod,status),n in sorted(status_counts.items())]
if statuses:art.append(write_csv("G06F2_SITUACOES_OBSERVADAS.csv",statuses))
qa={"checked_at_utc":datetime.now(timezone.utc).isoformat(),
    "status":"pass" if all(x["status"]=="qa_pass" for x in coverage) else "partial",
    "consultas":74,"qa_pass":sum(x["status"]=="qa_pass" for x in coverage),
    "incompletas":sum(x["status"]!="qa_pass" for x in coverage),
    "paginas":len(pages),"registros_propostas_canonicas_com_geo":len(proposals),
    "por_modulo":{m:{"consultas":sum(x["modulo"]==m for x in coverage),
                 "qa_pass":sum(x["modulo"]==m and x["status"]=="qa_pass" for x in coverage),
                 "registros":sum(x["modulo"]==m for x in proposals)} for m,_,_ in MODULES},
    "artifacts":art,
    "restrictions":["A complete pagination according to API metadata is not a proof of real-world exhaustive transfers",
     "Proposal IDs are deduped only within module and municipality; no cross-module identity asserted",
     "Proposed values MUST NOT be summed as paid transfers",
     "Celebration metadata does not replace signed instrument or payment",
     "No source of local municipal liquidation; no impact LC200 inferred"]}
(ROOT/"QA_G06F2.json").write_text(json.dumps(qa,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("FINAL_QA="+json.dumps({"status":qa["status"],"qa_pass":qa["qa_pass"],
"pages":qa["paginas"],"records":qa["registros_propostas_canonicas_com_geo"],
"module":qa["por_modulo"],"statuses":statuses[:20]},ensure_ascii=False),flush=True)
# Partial coverage remains a legitimate saved result; do not make assumptions of zero.
