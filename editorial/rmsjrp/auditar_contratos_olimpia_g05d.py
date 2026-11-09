#!/usr/bin/env python3
"""Audit official Olimpia contract register. Never treat contract amounts as fiscal liquidations."""
from __future__ import annotations
import collections,csv,datetime,hashlib,json,re,sys
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.error import HTTPError
ROOT=Path("build/rmsjrp-g05d-contratos");ROOT.mkdir(parents=True,exist_ok=True)
URL="https://dadosabertos.olimpia.sp.gov.br/dataset/3bf027f3-fb97-45e4-8748-0e6368dd9cac/resource/353160d1-2ba7-4605-a8ee-af48b52ed36c/download/contratos.json"
req=Request(URL,headers={"Accept":"application/json","User-Agent":"Mozilla/5.0"})
with urlopen(req,timeout=100) as response:
  assert response.status==200
  raw=response.read(12_000_000)
assert raw and len(raw)<12_000_000
(ROOT/"CONTRATOS_OLIMPIA_OFICIAL_RAW.json").write_bytes(raw)
sha=hashlib.sha256(raw).hexdigest()
obj=json.loads(raw.decode("utf-8-sig"))
assert isinstance(obj,list),type(obj)
assert len(obj)>0
keys=set().union(*(set(x) for x in obj if isinstance(x,dict)))
rows=[]
for i,r in enumerate(obj,1):
  assert isinstance(r,dict),i
  nr=str(r.get("numeroContrato") or "").strip()
  proc=str(r.get("numeroProcesso") or "").strip()
  date=str(r.get("dataAssinatura") or "")
  year=int(date[:4]) if re.match(r"^\d{4}-",date) else None
  rows.append({"indice":i,"ano_assinatura":str(year or ""),"numero_contrato":nr,"numero_processo":proc,
    "contratada":str(r.get("nomeContratada") or ""),"assinatura":date,
    "inicio_vigencia":str(r.get("dataInicioVigencia") or ""),
    "fim_vigencia":str(r.get("dataFimVigencia") or ""),
    "valor_contrato_na_fonte":str(r.get("valorContrato") if r.get("valorContrato") is not None else ""),
    "tipo_licitacao":str(r.get("tipoLicitacao") or ""),"tipo":str(r.get("tipo") or ""),
    "situacao":str(r.get("situacao") or "")})
assert len(rows)==len(obj)
with (ROOT/"CONTRATOS_OLIMPIA_INVENTARIO.csv").open("w",encoding="utf-8",newline="") as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter=";");w.writeheader();w.writerows(rows)
yearcounts=collections.Counter(x["ano_assinatura"] for x in rows)
keys_2024=[r for r in rows if r["ano_assinatura"]=="2024"]
keys_2025=[r for r in rows if r["ano_assinatura"]=="2025"]
by_num=collections.Counter((r["ano_assinatura"],r["numero_contrato"]) for r in rows)
duplicate_numbers=sum(n>1 for (y,k),n in by_num.items() if k)
# Explicitly distinguish source joinability, not fuzzy title matching.
semantic_fields=[k for k in keys if re.search(r"objeto|descri|obra|empenho|medic|acao|programa|liquid",k,re.I)]
qa={"status":"pass","captured_at_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "url":URL,"sha256_raw":sha,"bytes_raw":len(raw),
    "records":len(rows),"fields":sorted(keys),
    "records_assinados_2024":len(keys_2024),"records_assinados_2025":len(keys_2025),
    "by_signature_year":dict(sorted(yearcounts.items())),
    "duplicate_number_within_year":duplicate_numbers,"semantic_join_fields":semantic_fields,
    "works_register_joinability":"not_verified_no_contract_number_in_works_inventory",
    "limitations":["Contracts register does not establish fiscal liquidation",
      "No contract-to-work identity from amount or similar project title",
      "Year of signature is not year of liquidation",
      "Contract number is not globally unique absent year and entity"]}
inv=ROOT/"CONTRATOS_OLIMPIA_INVENTARIO.csv"
qa["inventory_sha256"]=hashlib.sha256(inv.read_bytes()).hexdigest()
(ROOT/"QA_G05D_CONTRATOS_OLIMPIA.json").write_text(json.dumps(qa,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"status":"pass","records":len(rows),"signed_2024":len(keys_2024),
    "signed_2025":len(keys_2025),"fields":sorted(keys),"semantic_fields":semantic_fields,
    "sha256":sha,"inventory_sha256":qa["inventory_sha256"]},ensure_ascii=False))
