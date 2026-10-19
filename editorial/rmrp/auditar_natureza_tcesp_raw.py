#!/usr/bin/env python3
"""Audit TCESP original expense element by selected action, no individual-level exports."""
import collections,csv,hashlib,io,json,os,sys,urllib.request,zipfile
from decimal import Decimal,InvalidOperation,ROUND_HALF_UP
from pathlib import Path

TARGETS=[
 ("ribeirao-preto",2024,"0","30003"),
 ("ribeirao-preto",2025,"0","30003"),
 ("sertaozinho",2025,"0","1"),
 ("guatapara",2023,None,None),
]
def centavos(raw):
    return int((Decimal(str(raw or "0").replace(".","").replace(",","."))*100).quantize(Decimal("1"),rounding=ROUND_HALF_UP))
def run(slug,year,program,action,out):
    url=f"https://transparencia.tce.sp.gov.br/sites/default/files/csv/despesas-{slug}-{year}.zip"
    req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"})
    with urllib.request.urlopen(req,timeout=200) as response: data=response.read()
    sha=hashlib.sha256(data).hexdigest()
    group=collections.defaultdict(lambda:{"rows":0,"cents":0})
    elements=collections.defaultdict(lambda:{"rows":0,"cents":0})
    types=collections.defaultdict(int)
    original_44=0
    n=0;matched=0;bad=0;sample_cols=[]
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        files=[v for v in z.namelist() if not v.endswith("/")]
        if len(files)!=1:raise ValueError("Unexpected ZIP members")
        with z.open(files[0]) as stream:
            reader=csv.DictReader(io.TextIOWrapper(stream,encoding="latin-1",newline=""),delimiter=";")
            sample_cols=reader.fieldnames
            for row in reader:
                n+=1
                tp=(row.get("tp_despesa") or "").strip()
                el=(row.get("ds_elemento") or "").strip()
                code=el.split(" - ",1)[0].strip()
                if tp.lower()!="valor liquidado" or not code.startswith("44"):continue
                try:val=centavos(row.get("vl_despesa"))
                except (InvalidOperation,ValueError):bad+=1;continue
                original_44+=val
                if program is not None:
                    if (row.get("cd_programa") or "").strip().lstrip("0")!=(program.lstrip("0") or "0"):continue
                    if (row.get("cd_acao") or "").strip().lstrip("0")!=(action.lstrip("0") or "0"):continue
                matched+=1
                group[code[:4]]["rows"]+=1;group[code[:4]]["cents"]+=val
                elements[el]["rows"]+=1;elements[el]["cents"]+=val
                types[tp]+=1
    result={"slug":slug,"year":year,"filter":{"program":program,"action":action},
       "url":url,"zip_sha256":sha,"rows_source":n,"rows_matched":matched,
       "invalid_values_44":bad,"total_source_44_cents":original_44,
       "matched_cents":sum(v["cents"] for v in elements.values()),
       "nature_groups":dict(sorted(group.items())),
       "nature_elements":dict(sorted(elements.items())),
       "available_columns":sample_cols,
       "note":"Aggregate only; no vendor, taxpayer, employee or individual transaction data published."}
    assert result["matched_cents"]==sum(v["cents"] for v in group.values())
    assert bad==0
    dest=out/f"{slug}_{year}_nature_audit.json"
    dest.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return {"slug":slug,"year":year,"rows_matched":matched,"cents":result["matched_cents"],"file":str(dest)}
def main():
    out=Path(sys.argv[1] if len(sys.argv)>1 else "build/rmrp-tcesp-nature")
    out.mkdir(parents=True,exist_ok=True)
    results=[]
    for slug,year,prog,act in TARGETS:
        results.append(run(slug,year,prog,act,out))
    (out/"SUMMARY.json").write_text(json.dumps(results,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(results,ensure_ascii=False))
if __name__=="__main__":main()
