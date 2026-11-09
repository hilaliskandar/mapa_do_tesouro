#!/usr/bin/env python3
"""FED02 FPM/Fundeb: disaggregated decendial tests of a 20%-gross hypothesis.

The STN DEDU field may encompass components other than FPM. The equality
DEDU = FPM_net / 4 is a *hypothesis*, NOT an accounting rule. The tool tests
it against each of 645 municipalities and three decendios without publishing
gross revenue, net transfers or forecasts. Input immutable R2 candidate.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from decimal import Decimal, getcontext
from pathlib import Path

getcontext().prec = 36
SHA = "3b9b5bf22748579a0f90912c160159b8d50a7664294a750fc74b2f98a59657fb"
FIELDS = ("decendio_1_raw", "decendio_2_raw", "decendio_3_raw")
TARGET = (("FPM", "FPM"), ("FUNDEB", "DEDU"), ("FUNDEB", "FPM"), ("ITR", "ITR"))
TOL = Decimal("0.05")  # illustrative 5-cent threshold, not a statistical confidence limit

def quantiles(vals):
    seq = sorted(vals)
    if not seq:
        return {"n":0}
    def p(n):
        return str(seq[int((len(seq) - 1) * n)])
    return {"n":len(seq),"min":p(0),"p10":p(.10),"median":p(.50),
            "p90":p(.90),"max":p(1)}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input",required=True,type=Path)
    p.add_argument("--output",required=True,type=Path)
    a=p.parse_args()
    out={"checked_at_utc":datetime.now(timezone.utc).isoformat(),
         "source_sha256":hashlib.sha256(a.input.read_bytes()).hexdigest(),
         "status":"failed_or_unavailable","scope":"Exploratory decendial FPM/Fundeb test, NOT audited revenue"}
    try:
        if out["source_sha256"] != SHA:
            raise ValueError("unknown_source_hash")
        groups=defaultdict(dict)
        with a.input.open(encoding="utf-8",newline="") as f:
            for r in csv.DictReader(f,delimiter=";"):
                key=(r["transferencia"],r["item_transferencia"])
                if key not in TARGET:continue
                code=r["codigo_ibge"]
                if key in groups[code]:raise ValueError("source_grain_duplicate")
                groups[code][key]=tuple(Decimal(r[c]) for c in FIELDS)
        if len(groups)!=645:raise ValueError("unexpected_municipality_coverage")
        raw_rows=[]
        close_by_decendio=Counter()
        negative_residual=Counter()
        values_by_decendio=defaultdict(list)
        comparisons=Counter()
        diagnostics=defaultdict(list)
        missing_codes=[]
        for code,items in sorted(groups.items()):
            if any(k not in items for k in TARGET[:3]):
                missing_codes.append(code)
                continue
            for d in range(3):
                fpm=items[("FPM","FPM")][d]
                dedu=items[("FUNDEB","DEDU")][d]
                fundeb_fpm=items[("FUNDEB","FPM")][d]
                itr=items[("ITR","ITR")][d] if ("ITR","ITR") in items else Decimal("0")
                residual=dedu-fpm/Decimal(4)
                # Nonzero FPM only; ratio always within same decendio/municipality.
                if fpm>0:
                    comparisons[d+1]+=1
                    diagnostics["dedu_over_fpm"].append(dedu/fpm)
                    diagnostics["dedu_minus_quarter_fpm"].append(residual)
                    diagnostics["fundeb_fpm_over_fpm"].append(fundeb_fpm/fpm)
                    if abs(residual)<=TOL:close_by_decendio[d+1]+=1
                    if residual<-TOL:negative_residual[d+1]+=1
                    values_by_decendio[d+1].append(residual)
                raw_rows.append({
                    "codigo_ibge":code,"decendio":d+1,
                    "hypothesis_residual_dedu_minus_fpm_div4":str(residual),
                    "fpm_net_candidate":str(fpm),
                    "fundeb_dedu_source":str(dedu),
                    "fundeb_fpm_source":str(fundeb_fpm),
                    "itr_source":str(itr),
                })
        if missing_codes:raise ValueError("missing_required_pairs_count="+str(len(missing_codes)))
        if len(raw_rows)!=1935:raise ValueError("unexpected_decendio_count")
        # No per-municipality values exported: diagnostics retained as aggregate
        # counts and dimensionless ratios only, reducing publication risk.
        out.update({"status":"qa_pass_hypothesis_test_only",
                    "municipalities":645,"decendio_records":len(raw_rows),
                    "fpm_positive_comparisons":dict(sorted(comparisons.items())),
                    "hypothesis_abs_residual_at_most_5_cents":dict(sorted(close_by_decendio.items())),
                    "hypothesis_negative_residual_below_minus_5_cents":dict(sorted(negative_residual.items())),
                    "residual_by_decendio_brl":{str(k):quantiles(v) for k,v in sorted(values_by_decendio.items())},
                    "ratio_dedu_over_fpm":quantiles(diagnostics["dedu_over_fpm"]),
                    "other_item_present_count":sum(("ITR","ITR") in v for v in groups.values()),
                    "unit":"R$ per decendio in source; values exclusively arithmetic diagnostics",
                    "cautions":["Quarter-of-FPM-net is an algebraic hypothesis given a 20 percent gross retention and an 80 percent net basis; not a claimed STN definition",
                                "Fundeb DEDU might contain ITR or other components and FPM source values may represent different stages",
                                "A positive residual does not identify its cause",
                                "No STN or SICONFI revenues are computed or published; no schema migrations",
                                "Only official source and matching period comparisons can homologate an accounting relationship"]})
    except (ValueError,ArithmeticError,KeyError) as e:
        out["error"]=f"{type(e).__name__}: {str(e)[:350]}"
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:out.get(k) for k in ("status","municipalities","decendio_records","error")},ensure_ascii=False))
    if out["status"]!="qa_pass_hypothesis_test_only":raise SystemExit(2)

if __name__=="__main__":main()
