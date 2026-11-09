#!/usr/bin/env python3
"""G06F3 pilot: documented join proposal -> partnership -> federal commitment.
No payment joins without an explicit key. No causal claims.
"""
import csv,json,hashlib,time,datetime
from pathlib import Path
from urllib.request import urlopen,Request
from urllib.parse import urlencode
R=Path("build/rmsjrp-g06f3-pilot");R.mkdir(parents=True,exist_ok=True)
BASE="https://api-publica.transferegov.gestao.gov.br/parcerias"
PILOT=[
 ("São José do Rio Preto","3549805","75094"),
 ("Olímpia","3533908","13999"),
 ("Olímpia","3533908","14002"),
 ("Mirassol","3530300","76321"),
 ("José Bonifácio","3525706","92185")
]
def fetch(route,params):
    url=BASE+route+"?"+urlencode(params)
    err=None
    for attempt in range(2):
        try:
            with urlopen(Request(url,headers={"Accept":"application/json","User-Agent":"RMSJRP-G06F3-audit/1.0"}),timeout=35) as resp:
                assert resp.status==200
                raw=resp.read(2_000_000)
            return json.loads(raw.decode("utf-8-sig")),url,hashlib.sha256(raw).hexdigest(),None
        except Exception as e:err=f"{type(e).__name__}: {str(e)[:200]}";time.sleep(1.5)
    return None,url,"",err
def unpack(v):
    if isinstance(v,list):return v
    if isinstance(v,dict):
        for k in ("data","items","results","records","content","dados"):
            if isinstance(v.get(k),list):return v[k]
    return []
rows=[];empenhos=[]
for city,ibge,pid in PILOT:
    proposal,pu,ps,pe=fetch("/proposta",{"id_proposta":pid,"pagina":1,"tamanho_da_pagina":50})
    listp=unpack(proposal)
    valid=[x for x in listp if isinstance(x,dict) and str(x.get("id_proposta"))==pid and str(x.get("cd_ibge_recebedor"))==ibge]
    partnership,ru,rs,re=fetch("/parceria",{"id_proposta":pid,"pagina":1,"tamanho_da_pagina":50})
    related=[x for x in unpack(partnership) if isinstance(x,dict) and str(x.get("id_proposta"))==pid]
    record={"municipio":city,"cod_ibge":ibge,"id_proposta":pid,
        "proposta_identidade_confirmada":str(bool(valid)).lower(),
        "situacao_proposta":str(valid[0].get("situacao_proposta",""))[:120] if valid else "",
        "parceria_registros":len(related),"consulta_proposta":pu,"consulta_parceria":ru,
        "sha_resposta_proposta":ps,"sha_resposta_parceria":rs,
        "erro_proposta":pe or "","erro_parceria":re or "",
        "status_cadeia":"sem_parceria_retorno" if not related else "parceria_retorno",
        "id_parcerias":"|".join(str(z.get("id_parceria","")) for z in related[:10]),
        "data_assinatura":"|".join(str(z.get("dh_assinatura","")) for z in related[:10]),
        "data_publicacao":"|".join(str(z.get("publicacao_dt_publicacao","")) for z in related[:10]),
        "situacao_parceria":"|".join(str(z.get("in_situacao_parceria","")) for z in related[:10]),
        "prova_celebracao":"metadado_nao_documento_assinado" if related else "nao_localizada",
        "pagamento_federal":"nao_verificado","liquidacao_municipal":"nao_verificada",
        "efeito_lc200":"nao_estimado"}
    for p in related[:10]:
        parid=str(p.get("id_parceria",""))
        if not parid:continue
        commitment,cu,cs,ce=fetch("/empenho-parceria",{"id_parceria":parid,"pagina":1,"tamanho_da_pagina":50})
        for x in unpack(commitment):
            if not isinstance(x,dict) or str(x.get("id_parceria",""))!=parid:continue
            empenhos.append({"municipio":city,"cod_ibge":ibge,"id_proposta":pid,"id_parceria":parid,
              "id_empenho_parceria":str(x.get("id_empenho_parceria","")),
              "numero_empenho":str(x.get("nr_empenho",x.get("numero_empenho","")))[:100],
              "ano_empenho":str(x.get("aa_empenho","")),"data_emissao":str(x.get("data_emissao","")),
              "valor_empenho_nao_pagamento":str(x.get("valor_empenho",""))[:100],
              "situacao_siafi":str(x.get("in_situacao_siafi",""))[:120],
              "url":cu,"sha_resposta":cs,"estagio":"empenho_registro_nao_pagamento"})
        record["status_cadeia"]="parceria_e_empenho_registro" if any(x["id_parceria"]==parid for x in empenhos) else record["status_cadeia"]
    rows.append(record)
def csvout(name,rr):
    if not rr:return None
    p=R/name
    with p.open("w",encoding="utf-8",newline="") as h:
        w=csv.DictWriter(h,fieldnames=list(rr[0]),delimiter=";");w.writeheader();w.writerows(rr)
    return {"file":name,"sha256":hashlib.sha256(p.read_bytes()).hexdigest(),"rows":len(rr)}
files=[csvout("G06F3_CADEIA_PILOTO.csv",rows),csvout("G06F3_EMPENHOS_PILOTO.csv",empenhos)]
qa={"status":"pass" if all(x["proposta_identidade_confirmada"]=="true" for x in rows) else "partial",
    "timestamp_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "propostas_consultadas":len(rows),"propostas_com_identidade_confirmada":sum(x["proposta_identidade_confirmada"]=="true" for x in rows),
    "propostas_com_parceria":sum(x["parceria_registros"]>0 for x in rows),
    "empenhos_registros":len(empenhos),
    "files":[x for x in files if x],
    "limits":["Published partnership metadata is not signed instrument image","Federal commitment record is not payment",
       "Payment order route lacks direct partnership ID filter, no speculative join",
       "No municipal revenue or local liquidation joined","No LC200 effect estimated"]}
(R/"QA_G06F3_PILOTO.json").write_text(json.dumps(qa,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
print("FINAL_QA="+json.dumps({"qa":qa,"records":[{k:v for k,v in r.items() if k in ("municipio","id_proposta","situacao_proposta","parceria_registros","id_parcerias","data_assinatura","status_cadeia","erro_parceria")} for r in rows]},ensure_ascii=False),flush=True)
