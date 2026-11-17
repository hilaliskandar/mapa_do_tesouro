#!/usr/bin/env python3
"""Inspect official national payment event types without monetary sums or payees.

Aggregates TP_MOV_FINANCEIRA distribution, sign/null/date completeness.
Does NOT infer paid GND4 investments or allocate funds territorially.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,zipfile
from collections import Counter
from datetime import datetime,timezone
from pathlib import Path
from inv_sp645_transferegov_new_source_layout import acquire

def main():
    p=argparse.ArgumentParser();p.add_argument("--out-dir",required=True);p.add_argument("--timeout",type=int,default=600)
    args=p.parse_args();out=Path(args.out_dir);out.mkdir(parents=True,exist_ok=True)
    report={"status":"in_progress","utc":datetime.now(timezone.utc).isoformat(),"dataset":"siconv_pagamento","classification":"event_types_not_investments","no_payee_details":True}
    def save(): (out/"manifest_payment_type_qa.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    save()
    try:
        path,details=acquire(out,"siconv_pagamento",args.timeout)
        report.update(details);save()
        with zipfile.ZipFile(path) as z:
            files=[x for x in z.infolist() if x.filename.lower().endswith(".csv")]
            if len(files)!=1:raise RuntimeError("expected one CSV")
            with z.open(files[0]) as raw:
                head=raw.readline()
                enc=next((x for x in ("utf-8-sig","latin-1") if _test(head,x)),None)
                if not enc:raise RuntimeError("no decodable CSV header")
                hdr=head.decode(enc)
                delimiter=";" if hdr.count(";")>=hdr.count(",") else ","
                keys=next(csv.reader([hdr],delimiter=delimiter))
                needed={"NR_MOV_FIN","NR_CONVENIO","TP_MOV_FINANCEIRA","VL_PAGO","DATA_PAG","ID_DL"}
                if not needed.issubset(keys):raise ValueError("Schema drift")
                reader=csv.DictReader(io.TextIOWrapper(raw,encoding="latin-1",errors="strict",newline=""),fieldnames=keys,delimiter=delimiter)
                types=Counter();signs=Counter();missing=Counter();per_type={}
                count=0
                for row in reader:
                    count+=1
                    if None in row:raise RuntimeError("Invalid CSV width at line "+str(count))
                    typ=(row["TP_MOV_FINANCEIRA"] or "").strip() or "__VAZIO__"
                    types[typ]+=1
                    x=per_type.setdefault(typ,Counter())
                    x["rows"]+=1
                    for key in needed:
                        if not (row.get(key) or "").strip():
                            missing[key]+=1
                            x["missing_"+key]+=1
                    v=(row.get("VL_PAGO") or "").strip()
                    sign="missing" if not v else "negative" if v.startswith("-") or (v.startswith("(") and v.endswith(")")) else "zero" if all(z in ("0",",",".","+"," ") for z in v) else "nonnegative_nonzero"
                    signs[sign]+=1;x["value_"+sign]+=1
                    if count%1000000==0:
                        report["rows_examined"]=count;save()
            if z.testzip() is not None:raise RuntimeError("CSV ZIP CRC failed")
        report.update({"status":"full_national_domain_counted","rows_examined":count,
            "types":dict(sorted(types.items())),"value_signs":dict(signs),
            "missing_by_column":dict(missing),
            "per_type":{k:dict(v) for k,v in sorted(per_type.items())},
            "zip_crc":"verified","uncompressed_bytes":files[0].file_size,
            "warning":"Do not call event types or signed rows cash expenditure until official type semantics and cancellations are verified"})
        save();path.unlink()
        print(json.dumps({k:report[k] for k in ("status","rows_examined","types","value_signs","missing_by_column")},ensure_ascii=False),flush=True)
    except Exception as exc:
        report["status"]="blocked";report["error"]=str(exc)[:350];save();raise

def _test(b,e):
    try:b.decode(e,errors="strict");return True
    except UnicodeDecodeError:return False

if __name__=="__main__":main()
