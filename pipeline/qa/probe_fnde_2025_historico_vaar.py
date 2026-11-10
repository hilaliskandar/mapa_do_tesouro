#!/usr/bin/env python3
"""Compare FNDE 2025 VAAR beneficiary lists from August/December 2025 to April 2026.

PDFs are retrieved read-only and their extracted text is checked for seven-digit IBGE.
The only artifact retained is an audit JSON. Does not infer payment or fix DCA.
"""
from __future__ import annotations
from collections import Counter
from decimal import Decimal
import hashlib
import io
import json
from pathlib import Path
import re
from urllib.request import Request, urlopen
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "build" / "fed04-fnde-2025-history"
QA = ROOT / "governance" / "FED04_MATRIZ_MUNICIPAL_FNDE_DCA_FUNDEB_2025_SP645_2026_11_10.csv"
SOURCES = {
 "terceira_agosto_2025": "https://www.gov.br/fnde/pt-br/acesso-a-informacao/acoes-e-programas/financiamento/fundeb/vaat/3-publicacao/redes-beneficiadas-coeficientes-de-distribuicao-e-complementacao-vaar-prevista.pdf/@@display-file/file",
 "quinta_dezembro_2025": "https://www.gov.br/fnde/pt-br/acesso-a-informacao/acoes-e-programas/financiamento/fundeb/2025-1/5a-publicacao-2013-portaria-mec-mf-no-13-de-29-de-dezembro-de-2025/6-redes-beneficiadas-coeficientes-de-distribuicao-e-complementacao-vaar-pre.pdf/@@display-file/file",
}
REGEX = re.compile(r"\bSP\s+(.{2,100}?)\s+(35\d{5})\s+([0-9][\d,.]*)\s+([0-9][\d,.]*)", re.I)
def currency(s):
    return Decimal(s.replace(".","").replace(",","."))

def load_rows():
    import csv
    with QA.open(encoding="utf-8-sig",newline="") as f:
        return list(csv.DictReader(f,delimiter=";"))

def process(label,url):
    r={"publication":label,"url":url,"status":"not_retrieved"}
    try:
        with urlopen(Request(url,headers={"User-Agent":"Mozilla/5.0 (FED04 public document QA)"}),timeout=70) as response:
            data=response.read(13*1024*1024+1)
            r["http_status"]=response.status
            r["final_url"]=response.url
        r["bytes"]=len(data);r["sha256"]=hashlib.sha256(data).hexdigest()
        if not data.startswith(b"%PDF") or len(data)>13*1024*1024:
            r["status"]="not_pdf_or_too_large";return r,{}
        reader=PdfReader(io.BytesIO(data))
        r["pages"]=len(reader.pages)
        found={}
        suspects=[]
        page_hits={}
        for page_no,page in enumerate(reader.pages,1):
            text=page.extract_text(extraction_mode="plain") or ""
            # pypdf may split columns; do not treat a failed regex as proof of no beneficiaries.
            hits=list(REGEX.finditer(text))
            page_hits[page_no]=len(hits)
            for m in hits:
                code=m.group(2)
                try:amount=currency(m.group(4))
                except Exception:
                    suspects.append({"page":page_no,"fragment":m.group(0)[:170]});continue
                if code in found: suspects.append({"duplicate":code,"page":page_no});continue
                found[code]={"municipio":m.group(1).strip(),"amount_brl":str(amount),"page":page_no}
        r["sp_codes_extracted"]=len(found)
        r["positive_sp_codes"]=sum(Decimal(x["amount_brl"])>0 for x in found.values())
        r["page_match_count"]=sum(page_hits.values())
        r["suspects"]=suspects[:15]
        r["sample_codes"]=sorted(found)[:15]
        r["status"]="pdf_text_parsed" if found else "no_sp_codes_parse_inconclusive"
        return r,found
    except Exception as exc:
        r["status"]="retrieval_or_parse_error";r["error"]=f"{type(exc).__name__}: {str(exc)[:220]}"
        return r,{}

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    current=load_rows()
    assert len(current)==645
    pending={r["codigo_ibge"]:r for r in current if r["grupo_conciliacao"]=="somente_dca"}
    assert len(pending)==297
    results={}
    for name,url in SOURCES.items():
        meta,values=process(name,url)
        visible=set(values)
        unmatched=sorted(visible & set(pending))
        meta["dca_only_2025_matched_count"]=len(unmatched)
        meta["dca_only_2025_matched_ids"]=unmatched
        meta["dca_only_2025_matched_value_brl"]=str(sum((Decimal(pending[i]["dca_complementacao_brl"]) for i in unmatched),Decimal(0)))
        results[name]={"metadata":meta,"values":values}
    union=set().union(*(set(x["values"]) for x in results.values()))
    discovered=set(pending)&union
    report={"scope":"FNDE VAAR earlier 2025 publications compared to 297 DCA-only municipalities","source_results":[x["metadata"] for x in results.values()],
      "union_earlier_2025_vaars":len(union),"dca_only_present_in_any_earlier_publication":len(discovered),
      "dca_only_new_earlier_ids":sorted(discovered),
      "conclusion_limit":"PDF text parser may miss rows; schedules/projections not realized payments; FNDE 2024 matches already separately classified",
      "writes_to_canonical":False}
    path=OUT/"QA_FED04_FNDE_2025_PREVIOUS_PUBLICATIONS.json"
    path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("SUMMARY: "+json.dumps(report,ensure_ascii=False))
if __name__=="__main__":main()
