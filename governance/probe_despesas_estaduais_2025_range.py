#!/usr/bin/env python3
"""Read-only statewide 2025 expense ZIP central-directory and member header inspection via HTTP Range.
Does not download 2GB ZIP, and never changes R2 / SQLite.
"""
import io,json,struct,urllib.request,zipfile,pathlib,hashlib
URL="https://transparencia.tce.sp.gov.br/sites/default/files/conjunto-dados/despesas-2025.zip"
OUT=pathlib.Path("build/tcesp-despesas-2025-schema");OUT.mkdir(parents=True,exist_ok=True)
def request(method,range_spec=None):
 headers={"User-Agent":"Mozilla/5.0 (TCESP schema probe)","Accept-Encoding":"identity"}
 if range_spec:headers["Range"]=range_spec
 req=urllib.request.Request(URL,headers=headers,method=method)
 with urllib.request.urlopen(req,timeout=180) as resp:
  return resp.status,dict(resp.headers),resp.read(12000000)
result={"url":URL,"method":"HTTP range central directory / deflate sample","no_full_download":True}
try:
 status,h,_=request("HEAD")
 length=int(h.get("Content-Length","0"))
 result.update({"head_status":status,"content_length":length,"accept_ranges":h.get("Accept-Ranges")})
 if length<1000000:raise RuntimeError("Unexpected source size")
 status,h,tail=request("GET",f"bytes={length-131072}-{length-1}")
 result["range_status"]=status
 if status!=206:raise RuntimeError("Server did not honor Range; stopping without full download")
 ix=tail.rfind(b"PK\x05\x06")
 if ix<0:raise RuntimeError("End-of-central-directory signature missing")
 eocd=tail[ix:ix+22]
 _,_,_,entries_disk,entries_total,cd_size,cd_offset,comment_len=struct.unpack("<IHHHHIIH",eocd)
 result.update({"entries":entries_total,"directory_bytes":cd_size,"directory_offset":cd_offset,"zip64_unsupported":entries_total==65535})
 if entries_total==65535:raise RuntimeError("ZIP64: central directory needs separate handler")
 status,h,cd=request("GET",f"bytes={cd_offset}-{cd_offset+cd_size-1}")
 if status!=206 or len(cd)!=cd_size:raise RuntimeError("Could not retrieve directory precisely")
 members=[];pos=0
 for _ in range(entries_total):
  if cd[pos:pos+4]!=b"PK\x01\x02":raise RuntimeError("Invalid central record")
  row=struct.unpack("<IHHHHHHIIIHHHHHII",cd[pos:pos+46])
  comp,uncomp,namelen,extralen,commentlen,offset=row[8],row[9],row[10],row[11],row[12],row[16]
  name=cd[pos+46:pos+46+namelen].decode("utf-8","replace")
  members.append({"name":name,"compressed_bytes":comp,"uncompressed_bytes":uncomp,"local_header_offset":offset,"compression":row[4]})
  pos+=46+namelen+extralen+commentlen
 result["members"]=members[:25]
 if not members:raise RuntimeError("Empty ZIP")
 # local header plus first 2MB compressed, enough to find CSV header without downloading full file
 selected=next((m for m in members if m["name"].lower().endswith(".csv")),members[0])
 off=selected["local_header_offset"]
 status,h,head=request("GET",f"bytes={off}-{off+2100000}")
 if status!=206:raise RuntimeError("Range not honored on member")
 if head[:4]!=b"PK\x03\x04":raise RuntimeError("Invalid local header")
 name_len,extra_len=struct.unpack("<HH",head[26:30])
 comp_sample=head[30+name_len+extra_len:]
 if selected["compression"]==8:
  import zlib
  plaintext=zlib.decompressobj(-15).decompress(comp_sample,150000)
 elif selected["compression"]==0:plaintext=comp_sample[:150000]
 else:raise RuntimeError("Unsupported compression")
 first=plaintext.decode("latin-1","replace").splitlines()[:4]
 result["sample_lines"]=first
 result["sample_columns"]=first[0].split(";") if first else []
 result["status"]="ok"
except Exception as e:
 result["status"]="error";result["error"]=type(e).__name__+": "+str(e)
(OUT/"probe.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(result,ensure_ascii=False)[:20000])
if result["status"]!="ok":raise SystemExit(1)
