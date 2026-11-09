#!/usr/bin/env python3
"""FED00: non-published arithmetic diagnostics of FPM vs Fundeb item DEDU.

Uses official STN September 2026 SP645 candidate. Computes ratios solely to
screen item semantics; not a budget revenue, financial transfer or gross/net
classification. Does not mutate SQLite and does not aggregate statewide money.
"""
from __future__ import annotations
import argparse,csv,hashlib,json
from collections import defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path
from datetime import datetime, timezone

SHA="3b9b5bf22748579a0f90912c160159b8d50a7664294a750fc74b2f98a59657fb"
COLS=("decendio_1_raw","decendio_2_raw","decendio_3_raw")
def money(v):
    return Decimal(v)
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input",required=True,type=Path)
    ap.add_argument("--output",required=True,type=Path)
    args=ap.parse_args()
    h=hashlib.sha256(args.input.read_bytes()).hexdigest()
    qa={"input_sha256":h,"status":"failed","utc":datetime.now(timezone.utc).isoformat(),
        "scope":"non-public semantic screening; not a fiscal amount or policy conclusion"}
    try:
        if h!=SHA:raise ValueError("input hash changed")
        groups=defaultdict(dict)
        with args.input.open(encoding="utf-8",newline="") as f:
            for r in csv.DictReader(f,delimiter=";"):
                c=r["codigo_ibge"];category=r["transferencia"];item=r["item_transferencia"]
                if (category,item) not in (("FPM","FPM"),("FUNDEB","DEDU"),("FUNDEB","FPM")):
                    continue
                vals=tuple(money(r[x]) for x in COLS)
                if (category,item) in groups[c]: raise ValueError("duplicate key")
                groups[c][(category,item)]=vals
        if len(groups)!=645:raise ValueError("not 645 municipalities")
        missing=[]
        ratios_dedu=[]
        ratios_fundeb_fpm=[]
        devs=[]
        zeros=0
        for cod,dat in groups.items():
            for key in (("FPM","FPM"),("FUNDEB","DEDU"),("FUNDEB","FPM")):
                if key not in dat:missing.append((cod,str(key)))
            if any(key not in dat for key in (("FPM","FPM"),("FUNDEB","DEDU"),("FUNDEB","FPM"))):
                continue
            fpm=sum(dat[("FPM","FPM")])
            dedu=sum(dat[("FUNDEB","DEDU")])
            fd=sum(dat[("FUNDEB","FPM")])
            if fpm<=0:zeros+=1;continue
            a=dedu/fpm
            b=fd/fpm
            ratios_dedu.append(a);ratios_fundeb_fpm.append(b)
            devs.append((abs(a-Decimal("0.2")),cod,a,b))
        def summarize(seq):
            ordered=sorted(seq)
            return {"n":len(ordered),"min":str(ordered[0]),"median":str(ordered[len(ordered)//2]),
                    "max":str(ordered[-1]),
                    "near_0_2_tolerance_0_001":sum(abs(v-Decimal("0.2"))<=Decimal("0.001") for v in ordered)}
        qa.update({"status":"qa_pass_diagnostic_only","municipalities":len(groups),
                   "missing_pairs":len(missing),"zero_or_negative_fpm":zeros,
                   "ratio_fundeb_dedu_over_fpm":summarize(ratios_dedu),
                   "ratio_fundeb_fpm_item_over_fpm":summarize(ratios_fundeb_fpm),
                   "ratio_dedu_highest_deviations":[{"codigo_ibge":code,"ratio":str(a),"fundeb_fpm_item_ratio":str(b)}
                                                    for _,code,a,b in sorted(devs,reverse=True)[:10]],
                   "unit":"dimensionless within-month empirical ratios, NOT amounts",
                   "limitations":["No inference that DEDU is a negative entry: source values are positive",
                                  "A 20 percent benchmark is a screening reference, not an expected identity without confirming the gross FPM definition",
                                  "FUNDEB FPM is a source item, not necessarily a separately paid amount in the same sense",
                                  "Not an accounting or revenue reconciliation; do not use these ratios in budget estimates"]})
    except (ValueError,InvalidOperation,KeyError,ZeroDivisionError) as e:
        qa["error"]=f"{type(e).__name__}: {str(e)[:300]}"
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(qa,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:qa.get(k) for k in ("status","municipalities","missing_pairs","ratio_fundeb_dedu_over_fpm","error")},ensure_ascii=False))
    if qa["status"]!="qa_pass_diagnostic_only":raise SystemExit(2)
if __name__=="__main__":main()
