#!/usr/bin/env python3
"""FED02 read-only source layout probe for official FPM and ITR national CSVs.

This is deliberately only a schema/header and source integrity discovery probe:
the files might describe distinct periods and concepts. It does not reconcile
or sum revenues and does not upload source objects to R2.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,re,time
from pathlib import Path
from datetime import datetime,timezone
from urllib.request import urlopen,Request

CATALOG="https://www.tesourotransparente.gov.br/ckan/api/3/action/package_show?id=transferencias-obrigatorias-da-uniao-por-municipio"
RESOURCE_IDS={
"FPM":"d69ff32a-6681-4114-81f0-233bb6b17f58",
"ITR":"f6ad4e51-fc7e-40bb-b35a-3686da7fde2d"
}
MAX_BYTES=35_000_000
UA="mapa-do-tesouro-FED02-pilot/1.0"
def fetch(url,limit):
    req=Request(url,headers={"User-Agent":UA,"Accept":"*/*"})
    with urlopen(req,timeout=70) as response:
        if response.status!=200:raise RuntimeError("http_status_"+str(response.status))
        size=response.headers.get("Content-Length")
        if size and int(size)>limit:raise ValueError("file_too_large")
        chunks=[];n=0;h=hashlib.sha256()
        while True:
            chunk=response.read(262144)
            if not chunk:break
            n+=len(chunk)
            if n>limit:raise ValueError("exceeded_bounded_source_size")
            h.update(chunk);chunks.append(chunk)
    return b"".join(chunks),h.hexdigest()
def inspect(blob):
    last_err=None
    for encoding in ("utf-8-sig","cp1252"):
        try:
            s=blob.decode(encoding)
            break
        except UnicodeDecodeError as e:last_err=e
    else:raise last_err
    first=s[:5000]
    delimiter=max((";",",","\t"),key=lambda d:first.splitlines()[0].count(d))
    reader=csv.reader(io.StringIO(s,newline=""),delimiter=delimiter)
    headers=next(reader)
    examples=[];rows=0;bad_width=0
    for row in reader:
        if not row:continue
        rows+=1
        if len(row)!=len(headers):bad_width+=1
        if len(examples)<3:examples.append(row[:min(15,len(row))])
    return {"encoding":encoding,"delimiter":delimiter,"header":headers,"row_count":rows,
            "width_mismatches":bad_width,"first_three_sample_rows":examples}
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    qa={"checked_at_utc":datetime.now(timezone.utc).isoformat(),
        "catalog":CATALOG,"status":"failed_or_unavailable","resources":{},
        "purpose":"source discovery and schema QA only; NO monetary comparison"}
    try:
        body,catsha=fetch(CATALOG,2_000_000)
        obj=json.loads(body)
        if not obj.get("success"):raise ValueError("ckan_catalog_not_successful")
        qa["catalog_sha256"]=catsha
        resources={x.get("id"):x for x in obj["result"]["resources"]}
        for label,rid in RESOURCE_IDS.items():
            report={"resource_id":rid,"stage":"catalog"}
            try:
                x=resources[rid]
                url=x["url"]
                if not url.startswith("https://www.tesourotransparente.gov.br/ckan/"):
                    raise ValueError("unexpected_official_origin")
                report.update({"catalog_name":x.get("name"),"catalog_size":x.get("size"),"url":url,"stage":"download"})
                blob,digest=fetch(url,MAX_BYTES)
                report.update({"download_bytes":len(blob),"sha256":digest,"stage":"schema"})
                report.update(inspect(blob))
                report["status"]="qa_pass_layout_only" if report["row_count"]>0 and report["width_mismatches"]==0 else "partial"
            except Exception as exc:
                report.update({"status":"failed_or_unavailable","error":f"{type(exc).__name__}: {str(exc)[:250]}"})
            qa["resources"][label]=report
            time.sleep(1.25)
        qa["status"]="qa_pass_layout_only" if all(v["status"]=="qa_pass_layout_only" for v in qa["resources"].values()) else "partial"
        qa["limitations"]=["The two sources may have different periods from the first STN September 2026 dataset",
                           "Their source schema does not imply equivalence with municipal cash or budget revenues",
                           "No R2 writes, SQLite writes, or monetary totals"]
    except Exception as e:
        qa["error"]=f"{type(e).__name__}: {str(e)[:250]}"
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(qa,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":qa["status"],"sources":{k:v["status"] for k,v in qa["resources"].items()}},ensure_ascii=False))
    if qa["status"]!="qa_pass_layout_only":raise SystemExit(2)
if __name__=="__main__":main()
