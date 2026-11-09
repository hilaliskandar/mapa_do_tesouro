#!/usr/bin/env python3
"""FED02: test whether ITR accounts for the DEDU minus quarter-FPM residual.

Strictly exploratory identity tests on three decendios, preserving upstream R2
candidate without SQLite imports, municipal gross/net publication or claims
about the STN accounting semantics. Uses Decimal, not floating-point money.
"""
from __future__ import annotations
import argparse,csv,hashlib,json
from collections import Counter,defaultdict
from datetime import datetime,timezone
from decimal import Decimal
from pathlib import Path

SHA="3b9b5bf22748579a0f90912c160159b8d50a7664294a750fc74b2f98a59657fb"
FIELD=("decendio_1_raw","decendio_2_raw","decendio_3_raw")
REQUIRED=(("FPM","FPM"),("FUNDEB","DEDU"))
ITR=("ITR","ITR")
TOL=Decimal("0.05")
def summarize(a):
    a=sorted(a)
    if not a:return {"n":0}
    return {"n":len(a),"min":str(a[0]),"p10":str(a[(len(a)-1)//10]),
            "median":str(a[(len(a)-1)//2]),"p90":str(a[(len(a)-1)*9//10]),"max":str(a[-1])}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    d={"datetime_utc":datetime.now(timezone.utc).isoformat(),
       "input_sha256":hashlib.sha256(a.input.read_bytes()).hexdigest(),
       "status":"failed_or_unavailable",
       "hypotheses":{"h1":"DEDU = FPM / 4",
                     "h2":"DEDU = (FPM + ITR) / 4, only where source has ITR",
                     "h3":"DEDU >= FPM / 4 (allowing rounding to 5 cents)"},
       "scope":"Empirical only, no identity or accounting relation homologated"}
    try:
        if d["input_sha256"]!=SHA:raise ValueError("unapproved_source")
        src=defaultdict(dict)
        with a.input.open(encoding="utf-8",newline="") as f:
            for row in csv.DictReader(f,delimiter=";"):
                key=(row["transferencia"],row["item_transferencia"])
                if key not in (*REQUIRED,ITR):continue
                code=row["codigo_ibge"]
                if key in src[code]:raise ValueError("duplicate_event")
                src[code][key]=[Decimal(row[k]) for k in FIELD]
        if len(src)!=645:raise ValueError("unexpected_645_coverage")
        cnt=Counter()
        residuals1=[];residuals2=[];comparable_pairs=[]
        for code,items in src.items():
            if any(x not in items for x in REQUIRED):
                raise ValueError("missing_FPM_or_DEDU")
            if ITR in items:cnt["itr_municipality_rows"]+=1
            for i in range(3):
                fpm=items[REQUIRED[0]][i]
                dedu=items[REQUIRED[1]][i]
                if fpm<=0:raise ValueError("nonpositive_fpm")
                a1=dedu-fpm/4
                residuals1.append(a1)
                cnt["h1_comparisons"]+=1
                if abs(a1)<=TOL:cnt["h1_matches_5_cents"]+=1
                if a1>=-TOL:cnt["h3_nonnegative_with_5_cents"]+=1
                if ITR in items:
                    itr=items[ITR][i]
                    a2=dedu-(fpm+itr)/4
                    residuals2.append(a2)
                    comparable_pairs.append((a1,a2))
                    cnt["h2_comparisons"]+=1
                    if abs(a2)<=TOL:cnt["h2_matches_5_cents"]+=1
                    if abs(a2)<abs(a1):cnt["h2_improves_absolute_residual"]+=1
                    if abs(a2)>abs(a1):cnt["h2_worsens_absolute_residual"]+=1
                    if abs(a2)==abs(a1):cnt["h2_equal_absolute_residual"]+=1
                    if a2>=-TOL:cnt["h2_nonnegative_with_5_cents"]+=1
        if cnt["h1_comparisons"]!=1935:raise ValueError("missing_decendio")
        if cnt["h2_comparisons"]!=cnt["itr_municipality_rows"]*3:raise ValueError("ITR_decendio_mismatch")
        d.update({"status":"qa_pass_hypotheses_only","municipalities":len(src),
                  "comparisons":dict(sorted(cnt.items())),
                  "h1_residual_brl":summarize(residuals1),
                  "h2_residual_brl":summarize(residuals2),
                  "h1_residual_on_h2_common_sample_brl":summarize([x for x,y in comparable_pairs]),
                  "tolerance_brl":str(TOL),
                  "cautions":["The ITR entry may itself be net of a Fundeb retention and may be subject to other adjustments",
                              "Neither formula is a legal/contabil rule; a better fit is only empirical evidence",
                              "No municipality values or transfer totals are published",
                              "The Fundeb distribution component is distinct from a retention",
                              "Do not use ratios for RREO comparison without stage and period harmonization"]})
    except (ValueError,ArithmeticError,KeyError) as e:
        d["error"]=f"{type(e).__name__}: {str(e)[:350]}"
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:d.get(k) for k in ("status","comparisons","error")},ensure_ascii=False))
    if d["status"]!="qa_pass_hypotheses_only":raise SystemExit(2)

if __name__=="__main__":
    main()
