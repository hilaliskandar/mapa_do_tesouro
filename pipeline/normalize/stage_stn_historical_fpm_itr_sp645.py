#!/usr/bin/env python3
"""FED03: reversible STN FPM/ITR historical source candidate (2013-2025, SP645).

Retain absence vs zero vs accounting-negative and source COD_MUN lineage.
Historical FPM includes additional FPM shares where applicable; it must not
be used as the platform's DCA monthly regular-FPM variable by default.
Never change SQLite or publish fiscal indicators. Outputs staged CSV + QA.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

HASH = {
    "FPM": "a86cad831115e02518198f4873967785a82eb3cbae651ef8505aa498c2cab088",
    "ITR": "9c93138d30b3c384ccb05ea91edbb8e6ee6f807f26ee2ce359e0a3e5b25f44ec",
    "crosswalk": "c90c31678c1f2c1dfc269e85d158aaeade790908e277dcf83c6617cf3af59b7a",
    "coverage": "678f68b588707c34c84630973629ef6722dd6e6538de56d79aaa95b644defeb3",
}
YEARS = [str(i) for i in range(2013, 2026)]
OUTPUT_FIELDS = ["codigo_ibge","uf","cod_mun_stn","municipio_origem","ano",
                 "mes","transferencia_origem","valor_raw","valor_decimal","estado_celula",
                 "source_sha256","status_contabil"]

def sha(path:Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for part in iter(lambda:f.read(1048576),b""):h.update(part)
    return h.hexdigest()

def parse(raw:str)->tuple[str,str]:
    s=raw.strip()
    if s in ("","-","—","N/A","NA"):return ("ausente","")
    paren=s.startswith("(") and s.endswith(")")
    unwrapped=s[1:-1].strip() if paren else s
    if not (re.fullmatch(r"-?(?:[0-9]{1,3}(?:\.[0-9]{3})+|[0-9]+),[0-9]{1,2}",unwrapped)
            or re.fullmatch(r"-?[0-9]+",unwrapped)):
        raise ValueError("Invalid numeric literal "+s[:60])
    d=Decimal(unwrapped.replace(".","").replace(",","."))
    if paren:
        if d<0:raise ValueError("Double negative prohibited")
        d=-d
    if d==0:status="zero_explicito"
    elif d<0:status="negativo"
    else:status="positivo"
    return status,format(d,".2f")

def stage(fpm:Path,itr:Path,crosswalk:Path,coverage:Path,out:Path,qa_path:Path)->dict:
    report={"created_utc":datetime.now(timezone.utc).isoformat(),
            "status":"failed_or_unavailable",
            "intended_scope":"STN 2013-2025 SP645 candidate, no DCA/SICONFI reconciliation"}
    try:
        checks={"FPM":sha(fpm),"ITR":sha(itr),
                "crosswalk":sha(crosswalk),"coverage":sha(coverage)}
        report["input_sha256"]=checks
        if checks!=HASH:raise ValueError("Unapproved STN source, crosswalk or coverage hash")
        by_mun={}
        with crosswalk.open(encoding="utf-8",newline="") as f:
            rd=csv.DictReader(f,delimiter=";")
            for r in rd:
                key=r["cod_mun_stn_literal"].strip()
                if key in by_mun:raise ValueError("Duplicated historical source code")
                by_mun[key]=(r["codigo_ibge"].strip(),r["municipio_stn_historico"])
        if len(by_mun)!=645 or len({v[0] for v in by_mun.values()})!=645:
            raise ValueError("Incomplete or non-unique SP645 crosswalk")
        official={}
        with coverage.open(encoding="utf-8",newline="") as f:
            for r in csv.DictReader(f,delimiter=";"):
                if r["territorio"]=="SP" and r["ano"] in YEARS:
                    official[(r["transferencia"],r["ano"])]=r
        if len(official)!=2*len(YEARS):raise ValueError("Incomplete official SP annual QA")
        records=0
        coverage_counts=defaultdict(Counter)
        seen=set()
        out.parent.mkdir(parents=True,exist_ok=True)
        with out.open("w",encoding="utf-8",newline="") as dst:
            wr=csv.DictWriter(dst,fieldnames=OUTPUT_FIELDS,delimiter=";")
            wr.writeheader()
            for source,path in (("FPM",fpm),("ITR",itr)):
                with path.open(encoding="cp1252",newline="") as inp:
                    rd=csv.DictReader(inp,delimiter=";")
                    if not set(["COD_MUN","UF","Município","Mês",*YEARS]).issubset(rd.fieldnames or []):
                        raise ValueError(source+" unexpected wide columns")
                    for row in rd:
                        if row["UF"].strip().upper()!="SP":continue
                        code=row["COD_MUN"].strip()
                        month=row["Mês"].strip()
                        if not code or not month:continue  # tracked as non-municipal rows in approved QA
                        if code not in by_mun:raise ValueError("Unmapped SP COD_MUN "+code)
                        if month not in [str(x) for x in range(1,13)]:
                            raise ValueError("Unexpected month on SP municipal row")
                        ibge,name=by_mun[code]
                        for year in YEARS:
                            key=(source,ibge,year,month)
                            if key in seen:raise ValueError("Duplicate FPM/ITR municipal year-month source key")
                            seen.add(key)
                            status,decimal=parse(row[year])
                            coverage_counts[(source,year)][status]+=1
                            wr.writerow({
                                "codigo_ibge":ibge,"uf":"SP","cod_mun_stn":code,
                                "municipio_origem":row["Município"].strip(),
                                "ano":year,"mes":month.zfill(2),
                                "transferencia_origem":source,"valor_raw":row[year].strip(),
                                "valor_decimal":decimal,
                                "estado_celula":status,
                                "source_sha256":checks[source],
                                "status_contabil":"candidato_sem_conciliacao_dca",
                            })
                            records+=1
        expected=645*12*len(YEARS)*2
        if records!=expected:raise ValueError("Expected "+str(expected)+" records, got "+str(records))
        lookup={"positivo":"celulas_positivas",
                "negativo":"celulas_negativas",
                "zero_explicito":"celulas_zeros",
                "ausente":"celulas_ausentes"}
        for (source,year),c in coverage_counts.items():
            orig=official[source,year]
            for status,header in lookup.items():
                if c[status]!=int(orig[header]):
                    raise ValueError(f"Annual coverage mismatch {source} {year} {status}")
            if int(orig["celulas_invalidas"])!=0:
                raise ValueError(f"Unrecognized original source numeric token {source} {year}")
        out_sha=sha(out)
        report.update({
            "status":"qa_pass_reversible_staging_only",
            "staged_rows":records,"municipalities":645,"years":YEARS,
            "months_per_source_per_year":645*12,
            "unique_source_ibge_year_month":len(seen),
            "output_sha256":out_sha,"output_bytes":out.stat().st_size,
            "source_status_per_year":{
                source:{year:dict(sorted(coverage_counts[source,year].items())) for year in YEARS}
                for source in ("FPM","ITR")},
            "no_fiscal_promotion":True,
            "limitations":[
                "FPM historical source may incorporate extraordinary shares: NEVER equate it to dca_fpm_cota_mensal without classification",
                "Missing source cells remain empty; literal zero is distinct",
                "Negative accounting parentheses are retained as negative Decimal",
                "Current 645-municipality mapping has not been validated for historical boundary evolution",
                "No migration, no DCA observation, no R2 source overwrite, no frontend publication",
            ],
        })
    except Exception as ex:
        report["status"]="failed_or_unavailable"
        report["error"]=type(ex).__name__+": "+str(ex)[:450]
    qa_path.parent.mkdir(parents=True,exist_ok=True)
    qa_path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:report.get(k) for k in ("status","staged_rows","output_sha256","error")},ensure_ascii=False))
    if report["status"]!="qa_pass_reversible_staging_only":raise SystemExit(2)
    return report

def main():
    p=argparse.ArgumentParser()
    for x in ("fpm","itr","crosswalk","coverage","out","qa"):
        p.add_argument("--"+x,type=Path,required=True)
    a=p.parse_args()
    stage(a.fpm,a.itr,a.crosswalk,a.coverage,a.out,a.qa)
if __name__=="__main__": main()
