#!/usr/bin/env python3
"""Audit official Olimpia yearly contracts. Contract amounts are not fiscal liquidation."""
from __future__ import annotations
import collections,csv,datetime,hashlib,json,re,sys
from pathlib import Path
from urllib.request import Request,urlopen
ROOT=Path("build/rmsjrp-g05d-contratos");ROOT.mkdir(parents=True,exist_ok=True)
BASE="https://www.olimpia.sp.gov.br/portal/dados-abertos/contratos/"
ATTEMPTS=[];RECORDS=[];SOURCES=[]
for endpoint_year in (2024,2025):
  url=BASE+str(endpoint_year)
  try:
    req=Request(url,headers={"Accept":"application/json","User-Agent":"Mozilla/5.0 (compatible; RMSJRP-fiscal-research/1.0)"})
    with urlopen(req,timeout=70) as response:
      assert response.status==200
      raw=response.read(12_000_000)
    obj=json.loads(raw.decode("utf-8-sig"))
    payload=obj.get("dados") if isinstance(obj,dict) else None
    if not isinstance(payload,list):raise ValueError("unexpected JSON: expected dados list")
    rawpath=ROOT/f"CONTRATOS_OLIMPIA_{endpoint_year}_RAW.json"
    rawpath.write_bytes(raw)
    fields=set()
    for n,r in enumerate(payload,1):
      if not isinstance(r,dict):raise ValueError("non-dict record")
      fields.update(r)
      ass=str(r.get("dataAssinatura") or "")
      year=int(ass[:4]) if re.match(r"^\d{4}-",ass) else None
      RECORDS.append({"ano_endpoint":endpoint_year,"indice":n,
        "ano_assinatura":str(year or ""),"numero_contrato":str(r.get("numeroContrato") or ""),
        "numero_processo":str(r.get("numeroProcesso") or ""),
        "contratada":str(r.get("nomeContratada") or ""),"assinatura":ass,
        "inicio_vigencia":str(r.get("dataInicioVigencia") or ""),
        "fim_vigencia":str(r.get("dataFimVigencia") or ""),
        "valor_contrato_fonte":str(r.get("valorContrato") if r.get("valorContrato") is not None else ""),
        "tipo_licitacao":str(r.get("tipoLicitacao") or ""),"tipo":str(r.get("tipo") or ""),
        "situacao":str(r.get("situacao") or "")})
    SOURCES.append({"endpoint_year":endpoint_year,"status":"pass","url":url,
      "sha256":hashlib.sha256(raw).hexdigest(),"bytes":len(raw),
      "records":len(payload),"fields":sorted(fields),
      "absence_of_object_description":not any(re.search(r"objeto|descri",k,re.I) for k in fields)})
  except Exception as e:
    ATTEMPTS.append({"year":endpoint_year,"url":url,"error":type(e).__name__+": "+str(e)[:300]})
if RECORDS:
  outfile=ROOT/"CONTRATOS_OLIMPIA_2024_2025_INVENTARIO.csv"
  with outfile.open("w",encoding="utf-8",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(RECORDS[0]),delimiter=";")
    w.writeheader();w.writerows(RECORDS)
  sha_inv=hashlib.sha256(outfile.read_bytes()).hexdigest()
else:sha_inv=None
yearcounts=collections.Counter(r["ano_assinatura"] for r in RECORDS)
by_endpoint=collections.Counter(str(r["ano_endpoint"]) for r in RECORDS)
counts_distinct={}
for year in (2024,2025):
  rr=[r for r in RECORDS if r["ano_endpoint"]==year]
  counts_distinct[str(year)]=len(set((r["numero_contrato"],r["numero_processo"],r["contratada"]) for r in rr))
keys_by_endpoint={str(year):set((r["ano_assinatura"],r["numero_contrato"],r["numero_processo"],r["contratada"]) for r in RECORDS if r["ano_endpoint"]==year) for year in (2024,2025)}
overlap=keys_by_endpoint["2024"] & keys_by_endpoint["2025"]
qa={"status":"pass" if len(SOURCES)==2 else ("partial" if SOURCES else "blocked"),
 "captured_at_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
 "sources":SOURCES,"failed_requests":ATTEMPTS,
 "records":len(RECORDS),"by_endpoint_year":dict(by_endpoint),
 "composite_keys_in_both_endpoints":len(overlap),"distinct_composite_keys":len(keys_by_endpoint["2024"] | keys_by_endpoint["2025"]),
 "by_signature_year":dict(yearcounts),"distinct_contract_process_supplier_tuples":counts_distinct,
 "inventory_sha256":sha_inv,
 "limitations":["No object/description key in this register if not in source fields",
    "Contract value != liquidated expense","Year of endpoint != necessarily fiscal year",
    "No matching to works by title without document lookup",
    "No matching to DCA/TCESP program or action without expense reference"]}
(ROOT/"QA_G05D_CONTRATOS_OLIMPIA.json").write_text(json.dumps(qa,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"status":qa["status"],"records":len(RECORDS),"by_endpoint_year":dict(by_endpoint),
 "by_signature_year":dict(yearcounts),"overlap":len(overlap),"distinct":qa["distinct_composite_keys"],"schema":{z["endpoint_year"]:z["fields"] for z in SOURCES},
 "inventory_sha256":sha_inv},ensure_ascii=False))
if not SOURCES:sys.exit(2)
