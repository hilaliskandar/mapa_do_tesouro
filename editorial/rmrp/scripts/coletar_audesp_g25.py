#!/usr/bin/env python3
"""Coleta isolada, somente leitura, de arquivos públicos Audesp para QA RMRP.
Não publica resultados fiscais; saída é artefato bruto e triagem de candidatos.
"""
import csv
import hashlib
import io
import json
import os
import re
import ssl
import sys
import urllib.error
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path

TARGETS={"3540200":"Pontal","3505609":"Barrinha","3534302":"Orlandia"}
BASE="https://www.transparencia.tce.sp.gov.br/sites/default/files/conjunto-dados"
FILES={"rcl_mensal":"rcl_completo.zip","analises_lrf":"resultado_analises_audesp.zip"}
OUT=Path(sys.argv[1] if len(sys.argv)>1 else "build/rmrp/audesp-g25")
OUT.mkdir(parents=True,exist_ok=True)
REPORT={"timestamp_utc":datetime.now(timezone.utc).isoformat(),"sources":{},"municipalities":TARGETS,"method":"independent source inspection; no legal homologation"}

def download(name):
    dest=OUT/name
    url=f"{BASE}/{name}"
    headers={"User-Agent":"RMRP-auditoria-documental/1.0 (public data reproducibility)","Accept":"application/zip,application/octet-stream,*/*"}
    try:
        req=urllib.request.Request(url,headers=headers)
        with urllib.request.urlopen(req,timeout=35,context=ssl.create_default_context()) as response:
            data=response.read(15_000_000+1)
            status=getattr(response,"status",200)
            mime=response.headers.get("Content-Type","")
        if len(data)>15_000_000:raise RuntimeError("File exceeds safety limit 15 MB")
        if not data.startswith(b"PK"):raise RuntimeError("Response does not have a ZIP magic header")
        dest.write_bytes(data)
        return dest,{"url":url,"http_status":status,"content_type":mime,"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest(),"state":"downloaded"}
    except Exception as e:
        return None,{"url":url,"state":"failed","error":type(e).__name__+": "+str(e)[:400]}

def candidate_rows(text,delimiter):
    reader=csv.DictReader(io.StringIO(text),delimiter=delimiter)
    head=reader.fieldnames or []
    hits=[]
    count=0
    for row in reader:
        count+=1
        plain=" ".join(str(x or "") for x in row.values()).lower()
        if any(code in plain or city.lower() in plain for code,city in TARGETS.items()):
            if re.search(r"(?:^|[^0-9])2025(?:[^0-9]|$)",plain):
                hits.append(row)
                if len(hits)>=2000:break
    return head,hits,count

for kind,name in FILES.items():
    dest,meta=download(name)
    REPORT["sources"][kind]=meta
    if dest is None:continue
    audit=[]
    try:
        with zipfile.ZipFile(dest) as z:
            bad=z.testzip()
            if bad:raise RuntimeError("Damaged ZIP member: "+bad)
            for info in z.infolist():
                item={"name":info.filename,"uncompressed_size":info.file_size}
                if info.file_size>40_000_000:
                    item["state"]="skipped_oversize"
                elif not info.filename.lower().endswith((".csv",".txt")):
                    item["state"]="skipped_non_csv"
                else:
                    raw=z.read(info)
                    decoded=None
                    for encoding in ("utf-8-sig","cp1252","latin1"):
                        try:decoded=raw.decode(encoding);item["encoding"]=encoding;break
                        except UnicodeDecodeError:pass
                    if decoded is None:item["state"]="cannot_decode"
                    else:
                        first=decoded[:6000]
                        delimiter=max((";",",",chr(9)),key=lambda v:first.count(v))
                        head,rows,n=candidate_rows(decoded,delimiter)
                        item.update({"delimiter":repr(delimiter),"columns":head,"rows_scanned":n,"candidate_rows":len(rows)})
                        if rows:
                            output=OUT/(kind+"_"+str(len(audit))+"_candidates_2025.csv")
                            with output.open("w",encoding="utf-8-sig",newline="") as f:
                                writer=csv.DictWriter(f,fieldnames=head,delimiter=";",extrasaction="ignore")
                                writer.writeheader();writer.writerows(rows)
                            item["candidate_file"]=output.name
                        item["state"]="inspected"
                audit.append(item)
        meta["members"]=audit
    except Exception as e:
        meta["parse_error"]=type(e).__name__+": "+str(e)[:400]
(OUT/"qa_manifest.json").write_text(json.dumps(REPORT,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps({k:{"state":v["state"],"bytes":v.get("bytes"),"members":[{"name":i["name"],"rows":i.get("rows_scanned"),"candidates":i.get("candidate_rows")} for i in v.get("members",[])],"error":v.get("error")} for k,v in REPORT["sources"].items()},ensure_ascii=False,indent=2))
