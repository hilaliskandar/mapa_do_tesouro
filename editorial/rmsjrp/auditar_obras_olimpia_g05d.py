#!/usr/bin/env python3
"""Capture and audit Olímpia public-works JSON as a current listing, NOT annual expenditure."""
from __future__ import annotations
import csv, datetime, hashlib, html, json, os, re, sys
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

ROOT=Path("build/rmsjrp-g05d-olimpia"); ROOT.mkdir(parents=True,exist_ok=True)
BASE="https://www.olimpia.sp.gov.br/portal/dados-abertos/obras/"
ENDPOINTS={2024:BASE+"2024",2025:BASE+"2025"}
def fetch(year,url):
    errors=[]
    for attempt in range(2):
        try:
            req=Request(url,headers={"User-Agent":"Mozilla/5.0 (compatible; RMSJRP-fiscal-research/1.0)","Accept":"application/json"})
            with urlopen(req,timeout=35) as response:
                data=response.read(15_000_000)
                status=response.status; content_type=response.headers.get("Content-Type","")
            assert status==200, f"HTTP {status}"
            if not data: raise ValueError("empty response")
            return data,content_type,errors
        except Exception as exc:
            errors.append(f"{type(exc).__name__}: {str(exc)[:220]}")
    return None,"",errors
def datepart(x):
    s=str(x or "")
    m=re.match(r"^(\d{4})-\d{2}-\d{2}",s)
    return int(m.group(1)) if m else None
def fmt(x):
    if isinstance(x,(dict,list)):return json.dumps(x,ensure_ascii=False,separators=(",",":"))
    return html.unescape(str(x)) if x is not None else ""
captured=[]; rows=[]; statuses=[]
for year,url in ENDPOINTS.items():
    data,content_type,errors=fetch(year,url)
    if data is None:
        statuses.append({"ano_endpoint":year,"status":"fetch_failed","url":url,"errors":errors})
        continue
    path=ROOT/f"OBRAS_OLIMPIA_{year}_RAW.json"
    path.write_bytes(data)
    sha=hashlib.sha256(data).hexdigest()
    try: parsed=json.loads(data.decode("utf-8-sig"))
    except Exception as e:
        statuses.append({"ano_endpoint":year,"status":"invalid_json","sha256":sha,"errors":[str(e)]})
        continue
    records=parsed.get("dados") if isinstance(parsed,dict) else None
    if not isinstance(records,list):
        statuses.append({"ano_endpoint":year,"status":"unexpected_schema","sha256":sha,"keys":list(parsed) if isinstance(parsed,dict) else []})
        continue
    fields=set()
    earlier=0; later_update=0; num_titles=0
    for idx,item in enumerate(records,1):
        if not isinstance(item,dict):continue
        fields.update(item.keys())
        start=datepart(item.get("dataExecucaoInicio"))
        update=datepart(item.get("dataAtualizacao"))
        earlier+=bool(start is not None and start<year)
        later_update+=bool(update is not None and update>year)
        title=fmt(item.get("titulo"))
        num_titles+=bool(title)
        rows.append({"ano_endpoint":year,"indice_registro":idx,"titulo":title,
                     "inicio_execucao":fmt(item.get("dataExecucaoInicio")),
                     "fim_execucao":fmt(item.get("dataExecucaoFim")),
                     "atualizacao":fmt(item.get("dataAtualizacao")),
                     "situacao":fmt(item.get("situacao")),"categoria":fmt(item.get("categoria")),
                     "valor_informado_sem_estagio":fmt(item.get("valor")),
                     "descricao":fmt(item.get("descricao")),
                     "campos_adicionais":fmt({k:v for k,v in item.items() if k not in {
                        "titulo","dataExecucaoInicio","dataExecucaoFim","dataAtualizacao","situacao","categoria","valor","descricao"}})})
    statuses.append({"ano_endpoint":year,"status":"parsed","url":url,"sha256":sha,"bytes":len(data),
                     "content_type":content_type,"registros":len(records),
                     "com_titulo":num_titles,"inicio_anterior_ao_endpoint":earlier,
                     "atualizacao_posterior_ao_endpoint":later_update,
                     "campos":sorted(fields),"errors":errors})
    captured.append(year)
if rows:
    path=ROOT/"OBRAS_OLIMPIA_2024_2025_INVENTARIO.csv"
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter=";")
        w.writeheader();w.writerows(rows)
    inventory={"path":path.name,"sha256":hashlib.sha256(path.read_bytes()).hexdigest(),"records":len(rows)}
else: inventory=None
qa={"gate":"G05-D","checked_at_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "status":"pass" if len(captured)==2 else ("partial" if captured else "blocked"),
    "anos_recuperados":captured,"fontes":statuses,"inventario":inventory,
    "limites":["endpoint year is not fiscal liquidation year",
              "listed project value is not annual liquidated expenditure",
              "no financial matching by title alone",
              "no zero imputation of missing values"]}
(ROOT/"QA_OBRAS_OLIMPIA.json").write_text(json.dumps(qa,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"status":qa["status"],"anos_recuperados":captured,
                  "contagens":{z["ano_endpoint"]:z.get("registros") for z in statuses},
                  "atualizacoes_posteriores":{z["ano_endpoint"]:z.get("atualizacao_posterior_ao_endpoint") for z in statuses},
                  "inventario":inventory},ensure_ascii=False))
# Publish evidence even if one endpoint is blocked. Fail if no useful data exists.
if not captured:sys.exit(2)
