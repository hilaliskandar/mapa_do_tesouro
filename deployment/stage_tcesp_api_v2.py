#!/usr/bin/env python3
"""Opt-in TCESP preview overlay into an existing site tree; never deploys.
Refuses collisions with existing API files and validates the source QA first.
"""
from __future__ import annotations
import argparse,hashlib,json,pathlib,shutil,subprocess,sys,tempfile

def merge_tcesp_preview(*,preview:pathlib.Path,site:pathlib.Path,enabled:bool=False,allow_v1_site:bool=False)->dict:
    if not enabled: raise ValueError("TCESP overlay disabled; supply --enable-tcesp")
    with tempfile.TemporaryDirectory() as tmp:
        script=pathlib.Path(__file__).with_name('qa_tcesp_api_v2_preview.py')
        subprocess.run([sys.executable,str(script),'--site',str(preview),'--report',str(pathlib.Path(tmp)/'qa.json'),'--max-detail-bytes','2000000'],check=True)
    source=preview/"data/api/v2/tcesp"
    dest=site/"data/api/v2/tcesp"
    if dest.exists(): raise FileExistsError(f"TCESP destination exists: {dest}")
    canonical=site/"data/api/v2/manifest.json"
    if not canonical.is_file():
        if not allow_v1_site or not (site/"data/manifest.json").is_file():
            raise ValueError("Main API v2 manifest missing, refusing accidental new site")
        canonical=site/"data/manifest.json"
    assets=pathlib.Path(__file__).resolve().parents[1]/"app"/"static"
    for filename in ("tcesp-investimentos.html","tcesp-investimentos.js"):
        if (site/filename).exists(): raise FileExistsError(f"TCESP UI destination exists: {filename}")
    # No canonical API changes; stage isolated files after checking all collisions.
    shutil.copytree(source,dest)
    for filename in ("tcesp-investimentos.html","tcesp-investimentos.js"):
        shutil.copy2(assets/filename,site/filename)
    index=site/"index.html"
    if index.is_file():
        document=index.read_text(encoding="utf-8")
        anchor='    <nav class="tabs" aria-label="Seções">'
        if anchor in document and 'href="./tcesp-investimentos.html"' not in document:
            document=document.replace(anchor,'    <p class="tcesp-preview-link"><a href="./tcesp-investimentos.html">Investimentos por programa e ação — TCESP (prévia)</a></p>\\n'+anchor,1)
            index.write_text(document,encoding="utf-8")
    main_hash=hashlib.sha256(canonical.read_bytes()).hexdigest()
    result={"status":"staged_not_published","namespace":"data/api/v2/tcesp",
        "files":len(list(dest.rglob("*.json"))),"main_manifest_sha256":main_hash}
    return result

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--preview",type=pathlib.Path,required=True)
    p.add_argument("--site",type=pathlib.Path,required=True)
    p.add_argument("--enable-tcesp",action="store_true")
    p.add_argument("--allow-v1-site",action="store_true")
    a=p.parse_args()
    print(json.dumps(merge_tcesp_preview(preview=a.preview,site=a.site,enabled=a.enable_tcesp,allow_v1_site=a.allow_v1_site),ensure_ascii=False))
if __name__=="__main__": main()
