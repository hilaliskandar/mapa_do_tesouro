#!/usr/bin/env python3
"""Inspect official 2024 Fundeb adjustment XLSX published April 2025.
No fiscal database or production modifications.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen
import openpyxl

SOURCES={
    "vaar_2024_adjustment":"https://www.gov.br/fnde/pt-br/acesso-a-informacao/acoes-e-programas/financiamento/fundeb/2025-1/AjustedaComplementaoVAAR.xlsx/@@download/file",
    "vaat_2024_adjustment":"https://www.gov.br/fnde/pt-br/acesso-a-informacao/acoes-e-programas/financiamento/fundeb/2025-1/AjustedaComplementaoVAAT.xlsx/@@download/file",
}
OUT=Path("build/fed04-fnde-2024")
CODE_SAMPLES=("3550308","3518800","3500105","3501608","3502804")
NAME_SAMPLES=("SAO PAULO","SÃO PAULO","GUARULHOS","ADAMANTINA","AMERICANA","ARACATUBA","ARAÇATUBA")

def inspect(label,url):
    out={"label":label,"url":url,"status":"unavailable"}
    try:
        with urlopen(Request(url,headers={"User-Agent":"Mozilla/5.0 (FED04 QA)"}),timeout=75) as r:
            raw=r.read(15*1024*1024+1);out["final_url"]=r.url;out["content_type"]=r.headers.get("Content-Type")
        out["bytes"]=len(raw)
        out["sha256"]=hashlib.sha256(raw).hexdigest()
        if not raw.startswith(b"PK") or len(raw)>15*1024*1024:
            out["status"]="not_xlsx_or_over_limit";return out
        file=OUT/f"{label}.xlsx";file.write_bytes(raw)
        wb=openpyxl.load_workbook(file,read_only=True,data_only=True)
        try:
            out["worksheets"]=[]
            for ws in wb:
                ws.reset_dimensions();found=[];first=[];n=0
                for line in ws.iter_rows(values_only=True):
                    n+=1
                    vals=[str(x).strip() if x is not None else "" for x in line]
                    cells=[v for v in vals if v]
                    if len(cells)>=3 and len(first)<10:
                        first.append({"row":n,"cells":cells[:16]})
                    if any(k in vals[:8] for k in CODE_SAMPLES) or any(any(nam in v.upper() for nam in NAME_SAMPLES) for v in vals[:7]):
                        if len(found)<60:found.append({"row":n,"cells":vals[:20]})
                out["worksheets"].append({"name":ws.title,"rows_scanned":n,"first_substantive":first,"sample_matches":found})
        finally:wb.close()
        out["status"]="read_success"
    except Exception as e:
        out["status"]="read_failed";out["error"]=f"{type(e).__name__}: {str(e)[:220]}"
    return out

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    result={"origin":"FNDE Portaria MEC/MF 3 of 2025-04-28: 2024 Fundeb annual adjustment","sources":[inspect(k,v) for k,v in SOURCES.items()],"accounting_application":"not_homologated"}
    (OUT/"QA_FED04_FNDE_2024_AJUSTES.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"sources":[{"label":x["label"],"status":x["status"],"sha256":x.get("sha256"),"sheets":x.get("worksheets")} for x in result["sources"]]},ensure_ascii=False))

if __name__=="__main__":main()
