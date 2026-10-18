"""Publish an immutable, SHA-pinned official source to private Cloudflare R2.

Use local credentials supplied through environment variables. Never print tokens.
"""
from __future__ import annotations
import argparse
import hashlib
import os
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen

EXPECTED_SHA="1b1379a5a531920223f1d448be155b70f51eb50180d8c819f1b7da3575a8eb11"
DEFAULT_KEY="sp_645/official_snapshots/capag/2026-09/capag-municipios-posicao-2026-set.xlsx"

def sha256(data:bytes)->str:
    return hashlib.sha256(data).hexdigest()

def upload(path:Path,account:str,token:str,bucket:str,key:str)->dict:
    data=path.read_bytes()
    if sha256(data)!=EXPECTED_SHA:
        raise ValueError("CAPAG SHA-256 diferente do snapshot oficial; upload recusado")
    url=f"https://api.cloudflare.com/client/v4/accounts/{account}/r2/buckets/{bucket}/objects/{quote(key,safe='/')}"
    headers={"Authorization":f"Bearer {token}","User-Agent":"sp645-official-source/1"}
    try:
        with urlopen(Request(url,headers=headers,method="GET"),timeout=120) as existing:
            current=existing.read()
        if sha256(current)!=EXPECTED_SHA:
            raise ValueError("Objeto R2 existente com conteudo diferente; sem sobrescrita")
        return {"status":"already_verified","key":key,"sha256":EXPECTED_SHA,"bytes":len(current)}
    except HTTPError as err:
        if err.code!=404:
            raise ValueError(f"Falha na verificacao de preexistencia R2 HTTP {err.code}") from err
    headers["Content-Type"]="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    with urlopen(Request(url,headers=headers,data=data,method="PUT"),timeout=180) as response:
        if response.status not in (200,201,204):
            raise ValueError(f"Upload recusado: HTTP {response.status}")
    with urlopen(Request(url,headers={"Authorization":f"Bearer {token}"},method="GET"),timeout=120) as downloaded:
        stored=downloaded.read()
    if sha256(stored)!=EXPECTED_SHA:raise ValueError("Falha na verificacao de leitura apos upload")
    return {"status":"uploaded_and_readback_verified","key":key,"sha256":EXPECTED_SHA,"bytes":len(stored)}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--file",type=Path,required=True)
    p.add_argument("--key",default=DEFAULT_KEY)
    a=p.parse_args()
    env={k:os.getenv(k) for k in ("CLOUDFLARE_ACCOUNT_ID","CLOUDFLARE_API_TOKEN","CLOUDFLARE_R2_BUCKET")}
    if any(not v for v in env.values()):raise SystemExit("Configuracao Cloudflare ausente")
    result=upload(a.file,env["CLOUDFLARE_ACCOUNT_ID"],env["CLOUDFLARE_API_TOKEN"],env["CLOUDFLARE_R2_BUCKET"],a.key)
    print(result)

if __name__=="__main__":main()
