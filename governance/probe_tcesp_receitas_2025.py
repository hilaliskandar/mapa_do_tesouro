#!/usr/bin/env python3
"""Read-only probe of the official TCESP statewide revenues ZIP. No persistence or API changes."""
import csv, hashlib, io, json, pathlib, sys, urllib.request, zipfile
from collections import Counter

URL = "https://transparencia.tce.sp.gov.br/sites/default/files/conjunto-dados/receitas-2025.zip"
OUT = pathlib.Path("build/tcesp-receitas-probe")
OUT.mkdir(parents=True, exist_ok=True)
req=urllib.request.Request(URL, headers={"User-Agent":"Mozilla/5.0 (TCESP schema audit)"})
try:
    with urllib.request.urlopen(req, timeout=150) as resp:
        data=resp.read(65_000_000)
    if len(data)>=65_000_000:
        raise ValueError("File exceeded probe safety limit (65 MB)")
    if not zipfile.is_zipfile(io.BytesIO(data)):
        raise ValueError("Source is not a valid ZIP")
    details=[]
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        for item in z.infolist():
            d={"name":item.filename,"uncompressed_bytes":item.file_size}
            if item.is_dir():
                continue
            with z.open(item) as f:
                head=f.read(250_000)
            txt=None
            for enc in ("utf-8-sig","latin-1"):
                try:
                    txt=head.decode(enc);d["encoding_probe"]=enc;break
                except UnicodeDecodeError:pass
            if txt is None:
                d["error"]="undecodable sample";details.append(d);continue
            first_lines=txt.splitlines()[:6]
            if first_lines:
                try:
                    dialect=csv.Sniffer().sniff("\n".join(first_lines), delimiters=";,\t|")
                    d["delimiter"]=dialect.delimiter
                    d["header"]=next(csv.reader([first_lines[0]],dialect=dialect))
                    d["sample_record_count"]=max(0,len(first_lines)-1)
                except (csv.Error, StopIteration) as exc:
                    d["error"]=f"CSV probe: {exc}"
            details.append(d)
    result={"status":"ok","url":URL,"zip_bytes":len(data),"sha256_zip":hashlib.sha256(data).hexdigest(),"zip_members":details,"note":"Only schema sample, not full parsing or municipality coverage validation; no data persisted to R2."}
except Exception as exc:
    result={"status":"error","url":URL,"error":type(exc).__name__+": "+str(exc)}
(OUT/"report.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(result,ensure_ascii=False,indent=2))
if result["status"]!="ok":sys.exit(1)
