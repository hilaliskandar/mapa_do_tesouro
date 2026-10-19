"""Incremental bounded TCESP ingestion, organized by RMRP official subregions."""
import argparse
import concurrent.futures
import csv
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROSTER=Path("editorial/rmrp/municipios_subregioes_tcesp.csv")
EXPECTED={1:15,2:6,3:6,4:7}
YEARS=(2023,2024,2025)

def load_roster():
    with ROSTER.open(encoding="utf-8-sig",newline="") as f:
        rows=list(csv.DictReader(f))
    assert len(rows)==34
    assert len({r["codigo_ibge"] for r in rows})==34
    assert len({r["slug"] for r in rows})==34
    assert {int(r["subregiao"]) for r in rows}==set(EXPECTED)
    for group,n in EXPECTED.items():
        assert sum(int(r["subregiao"])==group for r in rows)==n
    return rows

def check(path,slug,year):
    doc=json.loads(path.read_text(encoding="utf-8"))
    if doc.get("slug")!=slug or doc.get("year")!=year or doc.get("bad_values")!=0:
        raise ValueError(f"Unexpected metadata: {path}")
    if len(doc.get("sha256_zip",""))!=64:
        raise ValueError("Missing original TCESP ZIP digest")
    p=sum(int(x[-1]) for x in doc["programas_44_liquidado_completos"])
    a=sum(int(x[-1]) for x in doc["acoes_44_liquidado_completas"])
    if p!=a or p!=doc["investimento_44_liquidado_centavos"]:
        raise ValueError(f"Program/action reconciliation failed: {path}")
    return {"status":"validado","source_url":doc["url"],"source_zip_sha256":doc["sha256_zip"],
            "extract_sha256":hashlib.sha256(path.read_bytes()).hexdigest(),
            "rows":doc["rows"],"investment_cents":p}

def task(row,year,root):
    slug=row["slug"];sub=int(row["subregiao"])
    path=root/f"subregiao_{sub}"/f"{slug}_{year}.json"
    path.parent.mkdir(parents=True,exist_ok=True)
    base={"codigo_ibge":row["codigo_ibge"],"municipio":row["municipio"],
          "slug":slug,"subregiao":sub,"year":year,"path":str(path)}
    if path.exists():
        try: return {**base,**check(path,slug,year),"mode":"reuse"}
        except Exception: path.unlink()
    error=""
    for attempt in range(1,4):
        temp=path.with_suffix(".json.partial")
        try:
            with temp.open("w",encoding="utf-8") as out:
                proc=subprocess.run([sys.executable,"editorial/rmj/analyze_tcesp_pilot.py",slug,str(year)],
                                    stdout=out,stderr=subprocess.PIPE,text=True,
                                    timeout=240,env={**os.environ,"TCESP_TIMEOUT_SECONDS":"180"})
            if proc.returncode:
                raise RuntimeError(proc.stderr[-800:])
            result=check(temp,slug,year)
            temp.replace(path)
            return {**base,**result,"mode":"download","attempt":attempt}
        except Exception as exc:
            error=str(exc);temp.unlink(missing_ok=True)
            time.sleep(min(4*attempt,12))
    return {**base,"status":"falha","error":error}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--subregiao",type=int,choices=EXPECTED,required=True)
    parser.add_argument("--output",type=Path,required=True)
    parser.add_argument("--workers",type=int,default=3)
    args=parser.parse_args()
    if not 1<=args.workers<=3:
        parser.error("max 3 simultaneous TCESP downloads")
    rows=[r for r in load_roster() if int(r["subregiao"])==args.subregiao]
    args.output.mkdir(parents=True,exist_ok=True)
    jobs=[(r,y) for r in rows for y in YEARS]
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures=[pool.submit(task,r,y,args.output) for r,y in jobs]
        results=[f.result() for f in concurrent.futures.as_completed(futures)]
    results.sort(key=lambda x:(x["codigo_ibge"],x["year"]))
    summary={"subregiao":args.subregiao,"municipios":len(rows),"planned":len(jobs),
             "valid":sum(r["status"]=="validado" for r in results),
             "failed":sum(r["status"]=="falha" for r in results),
             "results":results,"publication_authorized":False}
    report=args.output/f"qa_subregiao_{args.subregiao}.json"
    report.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in summary.items() if k!="results"},ensure_ascii=False))
    if summary["failed"]:sys.exit(1)

if __name__=="__main__":main()
