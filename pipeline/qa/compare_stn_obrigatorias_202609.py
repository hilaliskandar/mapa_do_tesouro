#!/usr/bin/env python3
"""FED02: empirical cross-source FPM/ITR comparison, September 2026.

Reads official wide historical STN CSVs, 1996-2026 annual columns, with month
rows. Compares *2026, month 9* cells against sum of three decendios of the
separate official STN 2026-09 snapshot. Does not equate source SIAFI COD_MUN
with IBGE, and never promotes values to accounts or production observations.
"""
from __future__ import annotations
import argparse,csv,hashlib,json,re,unicodedata
from collections import Counter,defaultdict
from datetime import datetime,timezone
from decimal import Decimal,InvalidOperation
from pathlib import Path

PINNED={"FPM":"a86cad831115e02518198f4873967785a82eb3cbae651ef8505aa498c2cab088",
        "ITR":"9c93138d30b3c384ccb05ea91edbb8e6ee6f807f26ee2ce359e0a3e5b25f44ec"}
STAGING_SHA="3b9b5bf22748579a0f90912c160159b8d50a7664294a750fc74b2f98a59657fb"
def digest(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda:f.read(1024*1024),b""):h.update(c)
    return h.hexdigest()
def norm(s):
    s=unicodedata.normalize("NFKD",s.casefold().replace("’","'"))
    return re.sub("[^a-z0-9]","", "".join(x for x in s if not unicodedata.combining(x)))
def br_decimal(value):
    value=value.strip()
    if not value or value in ("-","—","N/A"):return None
    x=value.replace(".","").replace(",",".")
    try:return Decimal(x)
    except InvalidOperation:raise ValueError("non_numeric_br_cell:"+value[:25])

def main():
    p=argparse.ArgumentParser()
    for key in ("fpm","itr","staging","output"):p.add_argument("--"+key,required=True,type=Path)
    a=p.parse_args()
    qa={"checked_at_utc":datetime.now(timezone.utc).isoformat(),"status":"failed",
        "scope":"STN source-vs-source September 2026; NOT certified gross/net accounting"}
    try:
        qa["input_sha256"]={k:digest(getattr(a,k)) for k in ("fpm","itr","staging")}
        if qa["input_sha256"]!={"fpm":PINNED["FPM"],"itr":PINNED["ITR"],"staging":STAGING_SHA}:
            raise ValueError("unexpected_hash_or_changed_source")
        stage=defaultdict(lambda:defaultdict(lambda:Decimal(0)))
        names={}
        with a.staging.open(encoding="utf-8",newline="") as f:
            for row in csv.DictReader(f,delimiter=";"):
                if row["ano"]!="2026" or row["mes"]!="09":raise ValueError("non_september_stage")
                if (row["transferencia"],row["item_transferencia"]) not in (("FPM","FPM"),("ITR","ITR")):continue
                code=row["codigo_ibge"]
                names[code]=row["municipio_stn"]
                item=row["transferencia"]
                stage[code][item]+=sum(Decimal(row["decendio_"+str(i)+"_raw"]) for i in (1,2,3))
        name_index=defaultdict(list)
        for code,name in names.items():name_index[norm(name)].append(code)
        qa["stn_stage_codes"]=len(names)
        stats={}
        for label,path in [("FPM",a.fpm),("ITR",a.itr)]:
            counter=Counter()
            seen=set()
            nonmatches=[];matched=[];duplicates=[];missing_amount=[]
            diff_abs=[];breakdown=[]
            with path.open(encoding="cp1252",newline="") as f:
                reader=csv.DictReader(f,delimiter=";")
                expected={"COD_MUN","Município","UF","Mês","2026"}
                if not expected.issubset(reader.fieldnames or []):raise ValueError("wide_header_mismatch_"+label)
                for row in reader:
                    counter["all_rows"]+=1
                    if row["UF"].strip().upper()!="SP" or row["Mês"].strip()!="9":continue
                    counter["sp_september_rows"]+=1
                    key=(row["COD_MUN"].strip(),row["Município"].strip())
                    if key in seen:duplicates.append(key)
                    seen.add(key)
                    value=br_decimal(row["2026"])
                    if value is None:counter["blank_or_placeholder_2026_cells"]+=1
                    possibilities=name_index.get(norm(row["Município"].strip()),[])
                    if len(possibilities)!=1:
                        nonmatches.append({"cod_mun_literal":row["COD_MUN"],
                                           "municipio":row["Município"],
                                           "match_count":len(possibilities)})
                        continue
                    code=possibilities[0]
                    if value is None:
                        missing_amount.append(code);continue
                    actual=stage[code].get(label)
                    if actual is None:
                        breakdown.append({"codigo_ibge":code,"name":row["Município"],"reason":"missing_in_stn_stage","historical_source":str(value)})
                        continue
                    delta=value-actual
                    matched.append((code,value,actual,delta))
                    diff_abs.append(abs(delta))
                    if abs(delta)<=Decimal("0.05"):counter["matched_within_5c"]+=1
                    elif abs(delta)<=Decimal("1"):counter["matched_within_1brl"]+=1
                    if len(breakdown)<15 and abs(delta)>Decimal("0.05"):
                        breakdown.append({"codigo_ibge":code,"municipio":row["Município"],
                                          "source_history_month":str(value),
                                          "source_decendial_sum":str(actual),"difference_brl":str(delta)})
            stats[label]={"counts":dict(sorted(counter.items())),
                          "matched_numeric_records":len(matched),
                          "sp_municipality_names_unmatched_count":len(nonmatches),
                          "sp_municipality_names_unmatched_sample":nonmatches[:35],
                          "stage_missing_source_rows":len(set(stage)-set(x[0] for x in matched)),
                          "literal_cod_mun_uniques":len(seen),
                          "duplicate_name_code_rows":len(duplicates),
                          "blank_or_placeholder_matched_codes":missing_amount[:30],
                          "abs_difference_max_brl":str(max(diff_abs)) if diff_abs else None,
                          "mismatch_examples_or_source_absence":breakdown}
        qa.update({"status":"qa_pass_diagnostic_only","sources":stats,
                   "limitations":["No COD_MUN(SIAFI) to IBGE conversion is performed; only exact normalized UF=SP municipality names",
                                  "Different official source datasets may define gross/net, adjustments or month differently",
                                  "No inference from blank cell to zero revenue",
                                  "Comparison is not a reconciliation to municipal accounting or the DCA",
                                  "No SQLite, R2 or frontend changes"]})
    except Exception as e:
        qa["error"]=f"{type(e).__name__}: {str(e)[:450]}"
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(qa,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":qa["status"],"summary":{k:{"matched":v["matched_numeric_records"],"counts":v["counts"]} for k,v in qa.get("sources",{}).items()},"error":qa.get("error")},ensure_ascii=False))
    if qa["status"]!="qa_pass_diagnostic_only":raise SystemExit(2)
if __name__=="__main__":main()
