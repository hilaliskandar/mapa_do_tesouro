#!/usr/bin/env python3
"""FED02: audit public SICONFI RREO delivery/line metadata in three sentinel municipalities.

The RREO is bimestral and mostly year-to-date. STN Sep 2026 is a MONTHLY
cash-basis source. This tool does NOT compare their levels before harmonizing
period, source accounting category and delivery status. Read-only and 1 qps.
"""
from __future__ import annotations
import argparse,hashlib,json,time
from datetime import datetime,timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request,urlopen

BASE="https://apidatalake.tesouro.gov.br/ords/siconfi/tt/rreo"
CITIES={"3543402":"Ribeirao Preto","3549805":"Sao Jose do Rio Preto","3533908":"Olimpia"}
ANNEXES=("RREO-Anexo 01","RREO-Anexo 03")
PERIODS=(4,5)
def fetch(params):
    url=BASE+"?"+urlencode(params)
    req=Request(url,headers={"Accept":"application/json","User-Agent":"mapa-do-tesouro-FED02-RREO-probe/1.0"})
    with urlopen(req,timeout=32) as r:
        if r.status!=200:raise RuntimeError("RREO HTTP status "+str(r.status))
        raw=r.read(3_000_001)
    if len(raw)>3_000_000:raise ValueError("RREO source size limit")
    obj=json.loads(raw.decode("utf-8-sig"))
    if not isinstance(obj,dict) or not isinstance(obj.get("items"),list):
        raise ValueError("Unexpected RREO response")
    return obj,hashlib.sha256(raw).hexdigest()
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",required=True,type=Path)
    a=p.parse_args()
    out={"timestamp_utc":datetime.now(timezone.utc).isoformat(),
         "status":"failed_or_unavailable","basis":"RREO bimestral 2026 versus STN monthly 2026/09",
         "source_api":BASE,"requests":[]}
    try:
        for cod,name in CITIES.items():
            for period in PERIODS:
                for ann in ANNEXES:
                    params={"an_exercicio":2026,"nr_periodo":period,
                            "co_tipo_demonstrativo":"RREO","no_anexo":ann,
                            "id_ente":cod}
                    try:
                        obj,sha=fetch(params)
                        items=obj["items"]
                        if obj.get("hasMore"):
                            raise ValueError("RREO pagination not handled by bounded pilot")
                        interesting=[{"cod_conta":str(r.get("cod_conta","")),
                                      "conta":str(r.get("conta","")),
                                      "coluna":str(r.get("coluna",""))}
                                     for r in items
                                     if any(t in (str(r.get("conta",""))+" "+str(r.get("cod_conta",""))).upper()
                                            for t in ("FPM","FUNDEB","ITR"))]
                        # Unique labels only; no fiscal amounts copied or summed.
                        cols=sorted({(r["cod_conta"],r["conta"],r["coluna"]) for r in interesting})
                        entry={"codigo_ibge":cod,"municipio":name,"periodo_bimestral":period,
                               "anexo":ann,"status":"responded_with_rows" if items else "empty_response_not_zero",
                               "count_rows":len(items),"response_sha256":sha,
                               "interesting_labels_count":len(cols),"interesting_labels":[list(x) for x in cols[:50]]}
                    except Exception as e:
                        entry={"codigo_ibge":cod,"municipio":name,"periodo_bimestral":period,
                               "anexo":ann,"status":"unavailable",
                               "error":f"{type(e).__name__}: {str(e)[:200]}"}
                    out["requests"].append(entry)
                    time.sleep(1.1)  # Official API advises no more than 1 request/sec.
        good=sum(x["status"]=="responded_with_rows" for x in out["requests"])
        out["status"]="qa_pass_metadata_only" if good>=6 else "partial"
        out["responses_with_rows"]=good
        out["empty_not_zero"]=sum(x["status"]=="empty_response_not_zero" for x in out["requests"])
        out["unavailable"]=sum(x["status"]=="unavailable" for x in out["requests"])
        out["limitations"]=[
            "No 2026 annual DCA available by presumption; use actual delivery record before any comparison",
            "RREO period 4 corresponds to Jan-Aug while STN source here is Sep",
            "A zero-item response cannot be interpreted as a municipality declaring zero revenue",
            "RREO labels and units need demonstrative-specific reconciliation",
            "No municipal amounts, SQLite or R2 production changes",
        ]
    except Exception as e:
        out["status"]="failed_or_unavailable";out["error"]=str(e)[:300]
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:out.get(k) for k in ("status","responses_with_rows","empty_not_zero","unavailable")},ensure_ascii=False))
    if out["status"]!="qa_pass_metadata_only":raise SystemExit(2)
if __name__=="__main__":main()
