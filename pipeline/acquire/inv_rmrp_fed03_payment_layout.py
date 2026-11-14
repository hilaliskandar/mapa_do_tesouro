#!/usr/bin/env python3
"""INV-FED03: inspect official national payment/OBTV ZIP schemas and coverage.

Does not expose beneficiary details, payment records, identifiers or amounts.
Does not infer that payments were allocated to GND4 projects.
"""
from __future__ import annotations
import argparse,csv,hashlib,json
from collections import Counter
from datetime import datetime,timezone
from pathlib import Path
from inv_rmrp_transferegov_join import download,rows

SETS=("siconv_pagamento","siconv_obtv")
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--out-dir",required=True)
    ap.add_argument("--timeout",type=int,default=600)
    args=ap.parse_args();out=Path(args.out_dir);out.mkdir(parents=True,exist_ok=True)
    results=[]
    report={"timestamp_utc":datetime.now(timezone.utc).isoformat(),"scope":"national payment/OBTV metadata only","status":"in_progress","sources":results,"limitations":["No financial allocation to investment items","No names, CNPJ, bank data or payee rows in public artifact","No production publication or canonical DB writes"]}
    def persist(): (out/"manifest_fed03_layout.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    persist()
    for name in SETS:
        item={"dataset":name,"status":"pending"}
        results.append(item);persist()
        try:
            d=download(out,name,args.timeout)
            item.update({k:d[k] for k in ("url","sha256","bytes_zip","csv_member","csv_uncompressed_bytes")})
            count=0;heads=None
            for h,reader in rows(d["path"],d["csv_member"]):
                heads=h
                for _ in reader:count+=1
            item["columns"]=heads
            item["national_rows"]=count
            item["candidate_join_columns"]=[x for x in heads if any(k in x.upper() for k in ("PROPOSTA","CONVENIO","OBTV","DESEMBOLSO","PAGAMENTO","ITEM_PAD","EMPENHO","DOCUMENTO_HABIL"))]
            item["status"]="schema_and_rows_confirmed"
        except Exception as exc:
            item["status"]="blocked";item["error"]=repr(exc)
        persist()
        print(json.dumps({"dataset":name,"status":item["status"],"national_rows":item.get("national_rows"),"candidate_join_columns":item.get("candidate_join_columns"),"error":item.get("error")},ensure_ascii=False),flush=True)
    report["status"]="schema_probe_completed" if all(x["status"]=="schema_and_rows_confirmed" for x in results) else "partial_or_blocked"
    persist()
    if report["status"]!="schema_probe_completed":raise SystemExit(2)
if __name__=="__main__":main()
