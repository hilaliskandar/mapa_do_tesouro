#!/usr/bin/env python3
"""Opt-in TCESP preview overlay into an existing site tree; never deploys.
Refuses collisions with existing API files and validates the source QA first.
"""
from __future__ import annotations
import argparse,hashlib,json,pathlib,shutil
from deployment.qa_tcesp_api_v2_preview import validate_tcesp_preview

def merge_tcesp_preview(*,preview:pathlib.Path,site:pathlib.Path,enabled:bool=False)->dict:
    if not enabled: raise ValueError("TCESP overlay disabled; supply --enable-tcesp")
    validate_tcesp_preview(preview, max_detail_bytes=2000000)
    source=preview/"data/api/v2/tcesp"
    dest=site/"data/api/v2/tcesp"
    if dest.exists(): raise FileExistsError(f"TCESP destination exists: {dest}")
    if not (site/"data/api/v2/manifest.json").is_file():
        raise ValueError("Main API v2 manifest missing, refusing accidental new site")
    # Copy only the isolated namespace; canonical v2 manifest stays untouched.
    shutil.copytree(source,dest)
    main_hash=hashlib.sha256((site/"data/api/v2/manifest.json").read_bytes()).hexdigest()
    result={"status":"staged_not_published","namespace":"data/api/v2/tcesp",
        "files":len(list(dest.rglob("*.json"))),"main_manifest_sha256":main_hash}
    return result

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--preview",type=pathlib.Path,required=True)
    p.add_argument("--site",type=pathlib.Path,required=True)
    p.add_argument("--enable-tcesp",action="store_true")
    a=p.parse_args()
    print(json.dumps(merge_tcesp_preview(preview=a.preview,site=a.site,enabled=a.enable_tcesp),ensure_ascii=False))
if __name__=="__main__": main()
