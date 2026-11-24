#!/usr/bin/env python3
"""Probe Seade municipal-to-region CSV independently from electoral-zone data.

Read-only diagnostic: never fabricate RA/RG assignments from voting locations.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,time,urllib.request,urllib.error
from pathlib import Path
from collections import Counter
from datetime import datetime,timezone

URL="https://repositorio.seade.gov.br/dataset/1617c335-f5ab-426c-b175-280d4e41ec1c/resource/1871ac05-7b7f-4c13-9b4a-23c7d41fd988/download/codigos_municipios_regioes.csv"
DICT_URL="https://repositorio.seade.gov.br/dataset/1617c335-f5ab-426c-b175-280d4e41ec1c/resource/af9d7eae-d979-45cf-916f-b61fdfa6ee86/download/dicvar_codigos_municipios_regioes.csv"
def fetch(url,timeout=35):
    problems=[]
    for attempt in range(3):
        try:
            req=urllib.request.Request(url,headers={"User-Agent":"SP645-territorial-source-audit/1.0","Accept":"text/csv,*/*"})
            with urllib.request.urlopen(req,timeout=timeout) as r:
                data=r.read(4_000_001)
                if len(data)>4_000_000:raise ValueError("CSV exceeds safety cap")
                if r.status!=200:raise RuntimeError("HTTP "+str(r.status))
                return data
        except Exception as e:
            problems.append(type(e).__name__+": "+str(e)[:100])
            if attempt<2:time.sleep(attempt+1)
    raise RuntimeError("Failed official download: "+" | ".join(problems))
def parse(data):
    decoded=None;encoding=None
    for candidate in ("utf-8-sig","cp1252"):
        try:
            decoded=data.decode(candidate,errors="strict");encoding=candidate;break
        except UnicodeDecodeError:pass
    if decoded is None:raise ValueError("Undecodable source")
    head=decoded.splitlines()[0]
    separator=";" if head.count(";")>=head.count(",") else ","
    reader=csv.DictReader(io.StringIO(decoded),delimiter=separator)
    hdr=reader.fieldnames or []
    records=list(reader)
    if not hdr or any(None in r for r in records):raise ValueError("Malformed CSV lines")
    return hdr,records,separator,encoding
def main():
    a=argparse.ArgumentParser();a.add_argument("--out-dir",required=True);args=a.parse_args()
    out=Path(args.out_dir);out.mkdir(parents=True,exist_ok=True)
    report={"utc":datetime.now(timezone.utc).isoformat(),"status":"in_progress","sources":[],"scope":"official Seade municipal administrative region table only; no electoral data"}
    def persist(): (out/"manifest_seade_municipios_regioes.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    persist()
    for kind,url in [("municipalities",URL),("dictionary",DICT_URL)]:
        try:
            data=fetch(url)
            hdr,records,sep,encoding=parse(data)
            report["sources"].append({"kind":kind,"url":url,"status":"retrieved","sha256":hashlib.sha256(data).hexdigest(),
               "bytes":len(data),"rows":len(records),"columns":hdr,"delimiter":sep,"encoding":encoding})
            if kind=="municipalities":
                # Do not assume column names; review source dictionary prior to selecting RA/RG.
                report["municipality_record_count"]=len(records)
                report["municipalities_count_is_645"]=len(records)==645
        except Exception as e:
            report["sources"].append({"kind":kind,"url":url,"status":"blocked","reason":str(e)[:350]})
        persist()
    report["status"]="schema_available_pending_semantic_mapping" if all(x["status"]=="retrieved" for x in report["sources"]) else "source_access_blocked_or_partial"
    persist()
    print(json.dumps(report,ensure_ascii=False),flush=True)
    if report["status"]!="schema_available_pending_semantic_mapping":raise SystemExit(2)
if __name__=="__main__":main()
