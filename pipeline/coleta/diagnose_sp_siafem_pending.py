"""Directed recovery pilot. Preserve original HTML privately; never infer zero."""
from __future__ import annotations
import argparse,csv,hashlib,json,time
from pathlib import Path
from datetime import datetime,timezone
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from pipeline.coleta.collect_sp_siafem_annual_batch import fetch_one
from pipeline.coleta.probe_sp_siafem_webforms import URL

class CapturingSession(requests.Session):
    def __init__(self):
        super().__init__()
        self.last_post=None
    def post(self,*args,**kwargs):
        self.last_post=super().post(*args,**kwargs)
        return self.last_post

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--crosswalk",type=Path,required=True)
    p.add_argument("--coverage",type=Path,required=True)
    p.add_argument("--offset",type=int,default=0)
    p.add_argument("--limit",type=int,default=5)
    p.add_argument("--year",type=int,default=2025)
    p.add_argument("--outdir",type=Path,required=True)
    a=p.parse_args()
    if a.offset<0 or not 1<=a.limit<=25 or not 2020<=a.year<=2026: p.error("invalid batch")
    with a.crosswalk.open(encoding="utf-8-sig",newline="") as f:
        mapping={r["codigo_ibge"]:r for r in csv.DictReader(f,delimiter=";")}
    with a.coverage.open(encoding="utf-8-sig",newline="") as f:
        pending=sorted({r["ibge7"] for r in csv.DictReader(f,delimiter=";") if r["fonte_id"]=="SP_SEFAZ" and r["modalidade"]=="investimento" and r["ano"]==str(a.year) and r["consulta_status"]=="erro"})
    chosen=pending[a.offset:a.offset+a.limit]
    assert len(chosen)==a.limit and all(c in mapping and mapping[c]["codigo_siafem"] for c in chosen)
    a.outdir.mkdir(parents=True,exist_ok=True)
    evidence=[]; recovered=[]
    with CapturingSession() as s:
        s.headers.update({"User-Agent":"Mozilla/5.0 (levantamento publico SP645/1.0)"})
        for i,c in enumerate(chosen):
            s.last_post=None
            row={"ibge7":c}
            try:
                result=fetch_one(mapping[c]["codigo_siafem"],a.year,s)
                if not result["footer_checks"]: raise ValueError("sem totalizador conciliado")
                recovered.append({"codigo_ibge":c,"municipio":mapping[c]["municipio"],"codigo_siafem":mapping[c]["codigo_siafem"],**result})
                row["status"]="recovered_with_footer"
            except Exception as e:
                row.update(status="inconclusive",reason_class=type(e).__name__,description=str(e)[:140])
            r=s.last_post
            if r is not None and urlparse(r.url).hostname in ("www.fazenda.sp.gov.br","fazenda.sp.gov.br"):
                raw=r.content
                row.update(http_status=r.status_code,html_sha256=hashlib.sha256(raw).hexdigest(),html_bytes=len(raw))
                # Private raw evidence, not emitted to logs or public artifacts.
                row["html_hex"]=raw.hex()
                doc=BeautifulSoup(raw,"html.parser")
                grid=doc.find("table",{"id":"grdTransferencia"})
                row["grid_present"]=grid is not None
                row["grid_rows"]=len(grid.find_all("tr")) if grid else 0
                msg=doc.get_text(" ",strip=True).casefold()
                scripts=" ".join(x.get_text() for x in doc.find_all("script")).casefold()
                phrases=("nenhum registro","nenhuma informação","nenhuma informacao","não foram encontrados","nao foram encontrados","não existem registros","sem registros")
                row["message_candidates"]=[x for x in phrases if x in msg or x in scripts]
            evidence.append(row)
            if i+1<len(chosen):time.sleep(1)
    raw=json.dumps({"year":a.year,"offset":a.offset,"captured_utc":datetime.now(timezone.utc).isoformat(),"requested_ibge7":chosen,"evidence":evidence,"recovered":recovered,"financial_homologated":False,"public_release_authorized":False},ensure_ascii=False,sort_keys=True).encode()
    (a.outdir/"raw.json").write_bytes(raw)
    qa={"year":a.year,"offset":a.offset,"requested_ibge7":chosen,"recovered_ibge7":[r["codigo_ibge"] for r in recovered],"diagnostics":[{k:v for k,v in r.items() if k!="html_hex"} for r in evidence],"snapshot_sha256":hashlib.sha256(raw).hexdigest(),"bytes":len(raw),"public_release_authorized":False}
    (a.outdir/"qa.json").write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding="utf-8")
    print("SIAFEM_RECOVERY_QA",json.dumps(qa,ensure_ascii=False))
if __name__=="__main__":main()
