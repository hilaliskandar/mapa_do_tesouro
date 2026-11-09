#!/usr/bin/env python3
"""FED02: SICONFI extrato_entregas of 2026 for three pilot municipalities.

Read-only, <=1 request/sec. No missing declarations are interpreted as zero,
and an absent RREO entry is not necessarily a late filing.
"""
from __future__ import annotations
import argparse,hashlib,json,time
from datetime import datetime,timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request,urlopen

BASE="https://apidatalake.tesouro.gov.br/ords/siconfi/tt/extrato_entregas"
MUNICIPIOS={"3543402":"Ribeirão Preto","3549805":"São José do Rio Preto","3533908":"Olímpia"}
TARGET="Relatório Resumido de Execução Orçamentária"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",type=Path,required=True)
    args=ap.parse_args()
    qa={"checked_at_utc":datetime.now(timezone.utc).isoformat(),"api_url":BASE,
        "reference_year":2026,"status":"failed_or_unavailable","cities":[]}
    try:
        for code,name in MUNICIPIOS.items():
            url=BASE+"?"+urlencode({"id_ente":code,"an_referencia":2026})
            req=Request(url,headers={"User-Agent":"mapa-do-tesouro-FED02-extrato/1.0","Accept":"application/json"})
            with urlopen(req,timeout=35) as response:
                if response.status!=200:raise RuntimeError("unexpected_http_status")
                raw=response.read(2_000_001)
            if len(raw)>2_000_000:raise ValueError("response_size_exceeded")
            data=json.loads(raw.decode("utf-8-sig"))
            if data.get("hasMore"):raise ValueError("pagination_requires_explicit_handling")
            deliveries=[
                {"period":r["periodo"],"periodicity":r["periodicidade"],
                 "status":r["status_relatorio"],"declared_at":r["data_status"],
                 "institution":r["instituicao"]}
                for r in data.get("items",[])
                if r.get("entregavel")==TARGET
                and str(r.get("instituicao","")).startswith("Prefeitura")
            ]
            qa["cities"].append({"codigo_ibge":code,"municipio":name,
                "response_sha256":hashlib.sha256(raw).hexdigest(),
                "all_delivery_rows":len(data["items"]),"rreo_rows":deliveries,
                "last_rreo_period":max((x["period"] for x in deliveries),default=None),
                "fifth_bimester_in_extrato":any(x["period"]==5 and x["periodicity"]=="B" for x in deliveries)})
            time.sleep(1.1)
        if len(qa["cities"])!=3:raise ValueError("missing_city")
        qa["status"]="qa_pass_delivery_metadata_only"
        qa["restrictions"]=[
            "A missing RREO for fifth bimester at query time is not a fiscal zero",
            "A missing RREO is not an assertion of delay without deadline verification",
            "Do not compare September 2026 STN directly with RREO ending in August",
            "Source status codes HO/RE require official glossary before normative conclusions",
            "No data written to canonical SQLite or fiscal variables"
        ]
    except Exception as exc:
        qa["status"]="failed_or_unavailable"
        qa["error"]=f"{type(exc).__name__}: {str(exc)[:300]}"
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(qa,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":qa["status"],"cities":len(qa["cities"]),"error":qa.get("error")},ensure_ascii=False))
    if qa["status"]!="qa_pass_delivery_metadata_only":raise SystemExit(2)
if __name__=="__main__":main()
