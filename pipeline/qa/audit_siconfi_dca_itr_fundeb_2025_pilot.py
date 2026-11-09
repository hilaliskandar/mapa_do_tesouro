#!/usr/bin/env python3
"""Audit official DCA 2025 analytic ITR/Fundeb accounts in eight SP municipalities.

Avoid duplicating DCA municipal revenues when staging STN transfers.
Report original DCA accounting columns separately; distinguish missing lines
from explicit zero and absence of entire delivery. Never sum gross/deductions,
never update canonical SQLite, R2 sources or frontend.
"""
from __future__ import annotations
import argparse,csv,hashlib,json,time
from collections import defaultdict
from datetime import datetime,timezone
from decimal import Decimal
from pathlib import Path
from pipeline.sources.siconfi import SiconfiClient

MUNICIPALITIES={
"3543402":"Ribeirão Preto",
"3550308":"São Paulo",
"3544004":"Rio das Pedras",
"3551207":"Sarutaiá",
"3549805":"São José do Rio Preto",
"3533908":"Olímpia",
"3518800":"Guarulhos",
"3505708":"Barueri",
}
ACCOUNTS={
"ITR":"RO1.7.1.1.52.0.0",
"FUNDEB_COMPLEMENTACAO":"RO1.7.1.5.00.0.0",
"FUNDEB_RECEBIDO":"RO1.7.5.1.00.0.0",
"FPM_MENSAL":"RO1.7.1.1.51.1.0",
}
COLS=("Receitas Brutas Realizadas","Deduções - FUNDEB","Outras Deduções da Receita")
FIELDS=["codigo_ibge","municipio","anexo","ano","conceito",
"cod_conta","coluna","valor_literal_api","estado","linha_dca_detectada",
"fonte_url","source_response_sha256"]

def main():
 p=argparse.ArgumentParser()
 p.add_argument("--matrix",type=Path,required=True)
 p.add_argument("--qa",type=Path,required=True)
 a=p.parse_args()
 client=SiconfiClient(min_interval=1.1,timeout=65)
 qa={"collected_at_utc":datetime.now(timezone.utc).isoformat(),
 "status":"failed_or_unavailable","source":"SICONFI DCA Anexo I-C/2025",
 "exclusion":"No STN or historical comparison, no fiscal summation",
 "municipalities":list(MUNICIPALITIES)}
 rows=[];stats=defaultdict(dict)
 try:
  for code,name in MUNICIPALITIES.items():
   data=client.fetch_dca(year=2025,entity_id=code,annex="DCA-Anexo I-C")
   entries=[x for x in data.items if str(x.get("cod_ibge"))==code
            and x.get("anexo")=="DCA-Anexo I-C"
            and x.get("rotulo")=="Padrão"]
   if not entries:raise ValueError("DCA annex unavailable for "+code)
   canonical=json.dumps(entries,ensure_ascii=False,sort_keys=True,default=str).encode("utf-8")
   response_hash=hashlib.sha256(canonical).hexdigest()
   qa.setdefault("per_municipality",{})[code]={
     "name":name,"source_rows":len(entries),"pages":data.pages,
     "response_subset_sha256":response_hash}
   for concept,account in ACCOUNTS.items():
    for column in COLS:
     matches=[x for x in entries if x.get("cod_conta")==account
              and x.get("coluna")==column]
     if len(matches)>1:raise ValueError("Duplicate DCA analytic account and column "+code+" "+account+" "+column)
     if matches:
      x=matches[0]
      value=x.get("valor")
      status="zero_explicito" if value is not None and Decimal(str(value))==0 else (
       "observado" if value is not None else "valor_nulo_em_linha")
      literal="" if value is None else str(value)
     else:status="linha_ausente";literal=""
     rows.append({
       "codigo_ibge":code,"municipio":name,"anexo":"DCA-Anexo I-C",
       "ano":"2025","conceito":concept,"cod_conta":account,"coluna":column,
       "valor_literal_api":literal,"estado":status,
       "linha_dca_detectada":"sim" if matches else "nao",
       "fonte_url":"https://apidatalake.tesouro.gov.br/ords/siconfi/tt/dca",
       "source_response_sha256":response_hash})
     stats[concept][column]=stats[concept].get(column,0)+(1 if matches else 0)
  a.matrix.parent.mkdir(parents=True,exist_ok=True)
  with a.matrix.open("w",encoding="utf-8",newline="") as f:
   w=csv.DictWriter(f,fieldnames=FIELDS,delimiter=";")
   w.writeheader();w.writerows(rows)
  qa.update({"status":"qa_pass_pilot_accounts_only","matrix_sha256":hashlib.sha256(a.matrix.read_bytes()).hexdigest(),
   "matrix_rows":len(rows),"municipalities_with_anexo":len(qa["per_municipality"]),
   "account_columns_with_rows":stats,"requests":client.request_count,
   "limitations":["2025 DCA only; no conclusion about 2013-2024 coverage",
   "Absent account or deduction row is not an explicit fiscal zero",
   "Receitas Brutas Realizadas and Deducoes are separate; no gross/net totals inferred",
   "Broader parent accounts may include child accounts; aggregation is prohibited",
   "No DCA-STN value equality asserted; fiscal account IDs are names, not homologated transfer conversions",
   "No writes to production SQLite or public portal"]})
 except Exception as e:
  qa.update({"status":"failed_or_unavailable","error":type(e).__name__+": "+str(e)[:400]})
 a.qa.parent.mkdir(parents=True,exist_ok=True)
 a.qa.write_text(json.dumps(qa,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print(json.dumps({"status":qa["status"],"rows":qa.get("matrix_rows"),
 "municipios":qa.get("municipalities_with_anexo"),"error":qa.get("error")},ensure_ascii=False))
 if qa["status"]!="qa_pass_pilot_accounts_only":raise SystemExit(2)
if __name__=="__main__":main()
