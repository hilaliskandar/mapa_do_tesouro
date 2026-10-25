#!/usr/bin/env python3
"""Diagnostico verificavel do CSV de receitas TCESP; evita inferir rubricas ausentes."""
import csv, io, json, urllib.request, zipfile, hashlib, sys, collections, decimal
y=int(sys.argv[1]);url=f"https://transparencia.tce.sp.gov.br/sites/default/files/csv/receitas-sao-carlos-{y}.zip"
req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"})
with urllib.request.urlopen(req,timeout=180) as resp: data=resp.read()
assert zipfile.is_zipfile(io.BytesIO(data))
with zipfile.ZipFile(io.BytesIO(data)) as z:
    filename=next(x for x in z.namelist() if x.lower().endswith(".csv"))
    with z.open(filename) as fh:
        reader=csv.DictReader(io.TextIOWrapper(fh,encoding="latin-1",newline=""),delimiter=";")
        cols=reader.fieldnames
        month_cols=[c for c in cols if "mes" in c.lower()]
        value_cols=[c for c in cols if c.lower().startswith("vl_") or "valor" in c.lower()]
        classified=collections.Counter();samples=[];rows=0
        for row in reader:
            rows+=1
            if rows<=4:samples.append(row)
            for key in cols:
                v=row.get(key) or ""
                if ("111250" in v or "111451" in v or "111253" in v or "ITBI" in v.upper() or "ISSQN" in v.upper()):
                    classified[key]+=1
        result={"ano":y,"url":url,"sha256_zip":hashlib.sha256(data).hexdigest(),"arquivo":filename,
            "linhas":rows,"colunas":cols,"mes_colunas":month_cols,"valor_colunas":value_cols,"campos_com_codigos_tributarios":classified,"amostras":samples}
        print(json.dumps(result,ensure_ascii=False))
