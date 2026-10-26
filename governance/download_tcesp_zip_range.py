#!/usr/bin/env python3
"""Resumable read-only retrieval of large official TCESP ZIPs with strict byte-range checks."""
import argparse,hashlib,json,pathlib,re,urllib.request,zipfile,time
p=argparse.ArgumentParser()
p.add_argument("--year",type=int,required=True,choices=[2023,2024,2025])
p.add_argument("--output",type=pathlib.Path,required=True)
p.add_argument("--chunk-mb",type=int,default=16)
a=p.parse_args()
url=f"https://transparencia.tce.sp.gov.br/sites/default/files/conjunto-dados/despesas-{a.year}.zip"
a.output.parent.mkdir(parents=True,exist_ok=True)
headers={"User-Agent":"Mozilla/5.0 (TCESP reproducible download)","Accept-Encoding":"identity"}
def request(method="GET",more=None):
 return urllib.request.Request(url,method=method,headers={**headers,**(more or {})})
with urllib.request.urlopen(request("HEAD"),timeout=90) as r:
 expected=int(r.headers["Content-Length"])
 assert r.status==200 and expected>1000000000,(r.status,expected)
etag=r.headers.get("ETag")
partial=a.output.with_suffix(a.output.suffix+".part")
size=partial.stat().st_size if partial.exists() else 0
print(json.dumps({"phase":"start_or_resume","year":a.year,"expected_bytes":expected,"resumed_bytes":size,"etag":etag}),flush=True)
if size and not etag: raise ValueError("Cannot safely resume without remote ETag")
if size>expected:raise ValueError("Existing part exceeds official content length")
block_size=a.chunk_mb*1024*1024
with partial.open("ab") as f:
 while size<expected:
  end=min(size+block_size,expected)-1
  with urllib.request.urlopen(request(more={"Range":f"bytes={size}-{end}",**({"If-Range":etag} if etag else {})}),timeout=180) as r:
   cr=r.headers.get("Content-Range","")
   m=re.fullmatch(r"bytes (\d+)-(\d+)/(\d+)",cr)
   if r.status!=206 or not m or tuple(map(int,m.groups()))!=(size,end,expected):
    raise ValueError(f"Invalid range response: HTTP {r.status}; Content-Range={cr}")
   remaining=end-size+1
   while remaining:
    chunk=r.read(min(1048576,remaining))
    if not chunk:raise IOError(f"Truncated range at offset {size}")
    f.write(chunk);size+=len(chunk);remaining-=len(chunk)
  f.flush()
  print(json.dumps({"phase":"download","year":a.year,"received_bytes":size,"expected_bytes":expected,"percent":round(100*size/expected,2)}),flush=True)
 if size!=expected:raise ValueError("Incomplete download")
digest=hashlib.sha256()
with partial.open("rb") as f:
 while chunk:=f.read(4*1024*1024):digest.update(chunk)
with zipfile.ZipFile(partial) as z:
 broken=z.testzip()
 if broken:raise ValueError(f"ZIP CRC failure: {broken}")
 files=[i for i in z.infolist() if i.filename.lower().endswith(".csv")]
 if len(files)!=1:raise ValueError("Expected exactly one CSV")
report={"status":"pass","year":a.year,"url":url,"bytes":expected,"sha256":digest.hexdigest(),"etag_head":etag,"zip_crc":"pass","csv_member":files[0].filename}
partial.replace(a.output)
a.output.with_suffix(".qa.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n")
print(json.dumps(report,ensure_ascii=False))
