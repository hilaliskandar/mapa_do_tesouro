#!/usr/bin/env python3
"""Diagnostico HTTP do Pages isolado. Nao faz deploy nem altera Cloudflare.

Distingue Cloudflare 1010 de erro de arquivo e preserva relatorio verificavel.
"""
import argparse,json,time
from pathlib import Path
from urllib.error import HTTPError,URLError
from urllib.request import Request,urlopen

DEFAULT_ROOT="https://financas-e2-homologacao.pages.dev"
PATHS=(
 "/data/api/v1/publication/universes.json",
 "/publicacoes/RM_SAO_PAULO/index.html",
 "/publicacoes/RM_SAO_PAULO/municipios/3503901.html",
)

def audit(root,output,timeout=25):
 result={"root":root,"scope":"isolated-preview","checks":[],"all_http_200":False}
 for path in PATHS:
  url=root.rstrip("/")+path
  record={"path":path,"url":url}
  try:
   req=Request(url,headers={"User-Agent":"financas-e2-auditoria/1.0","Accept":"application/json,text/html;q=0.9"})
   with urlopen(req,timeout=timeout) as resp:
    data=resp.read()
    record.update(status=resp.status,bytes=len(data),content_type=resp.headers.get("Content-Type"))
    if path.endswith(".json"):
     json.loads(data)
    elif b"<html" not in data.lower():
     record["error"]="nao_html"
  except HTTPError as exc:
   body=exc.read(500).decode("utf-8","replace")
   record.update(status=exc.code,cf_ray=exc.headers.get("CF-RAY"),content_type=exc.headers.get("Content-Type"),error="cloudflare_1010" if exc.code==403 and "error code: 1010" in body.lower() else "http_error",body_excerpt=body)
   result["checks"].append(record)
   if record["error"]=="cloudflare_1010":break
   continue
  except (URLError,TimeoutError,ValueError) as exc:
   record["error"]=type(exc).__name__
  result["checks"].append(record)
 result["all_http_200"]=len(result["checks"])==len(PATHS) and all(x.get("status")==200 and "error" not in x for x in result["checks"])
 output.parent.mkdir(parents=True,exist_ok=True)
 output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print(json.dumps(result,ensure_ascii=False))
 return result["all_http_200"]

if __name__=="__main__":
 p=argparse.ArgumentParser()
 p.add_argument("--root",default=DEFAULT_ROOT)
 p.add_argument("--out",type=Path,required=True)
 a=p.parse_args()
 raise SystemExit(0 if audit(a.root,a.out) else 1)
