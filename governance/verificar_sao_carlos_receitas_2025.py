#!/usr/bin/env python3
"""Compare statewide TCESP 2024 receipts for Bernardino de Campos with its municipal ZIP."""
import csv,io,json,decimal,hashlib,pathlib,urllib.request,zipfile,collections
Y=2025
CITY="São Carlos"
SLUG="sao-carlos"
urls={
 "state":"https://transparencia.tce.sp.gov.br/sites/default/files/conjunto-dados/receitas-2024.zip",
 "municipal":f"https://transparencia.tce.sp.gov.br/sites/default/files/csv/receitas-{SLUG}-{Y}.zip"
}
out=pathlib.Path("build/tcesp-receitas-sao-carlos-2025");out.mkdir(parents=True,exist_ok=True)
result={"municipio":CITY,"ano":Y,"fontes":{},"comparacao":{},"recomendacao":"No missing month is assumed to equal zero."}
for kind,url in urls.items():
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"}),timeout=240) as response:
   contents=response.read(70000000)
  if len(contents)>=70000000:raise ValueError("ZIP exceeds 70MB safety limit")
  z=zipfile.ZipFile(io.BytesIO(contents))
  names=[s for s in z.namelist() if s.lower().endswith(".csv")]
  if len(names)!=1:raise ValueError("unexpected CSV count "+str(names))
  counts=collections.Counter();totals=collections.Counter();invalid=0;selected=0
  with z.open(names[0]) as inp:
   reader=csv.DictReader(io.TextIOWrapper(inp,encoding="latin-1",newline=""),delimiter=";")
   columns=reader.fieldnames
   for row in reader:
    if kind=="state" and (row.get("ds_municipio") or "").strip().casefold()!=CITY.casefold():continue
    selected+=1
    m=(row.get("mes_referencia") or "").strip()
    counts[m]+=1
    val=(row.get("vl_arrecadacao") or "").strip()
    try:
     cents=decimal.Decimal(val.replace(".","").replace(",","."))*100
     if not cents.is_finite() or cents!=cents.to_integral_value():raise ValueError("not cents")
     totals[m]+=int(cents)
    except (ValueError,decimal.InvalidOperation):invalid+=1
  result["fontes"][kind]={"url":url,"sha256_zip":hashlib.sha256(contents).hexdigest(),"file":names[0],"columns":columns,"rows_selected":selected,"rows_by_month":dict(sorted(counts.items())),"total_centavos_by_month":dict(sorted(totals.items())),"invalid_values":invalid,"month_6_present":counts["6"]>0}
 except Exception as e:
  result["fontes"][kind]={"url":url,"error":type(e).__name__+": "+str(e)}
if all("error" not in v for v in result["fontes"].values()):
 a,b=result["fontes"]["state"],result["fontes"]["municipal"]
 result["comparacao"]={"junho_estadual":a["month_6_present"],"junho_municipal":b["month_6_present"],"divergencias_mensais":[{"mes":str(m),"estadual_centavos":a["total_centavos_by_month"].get(str(m)),"municipal_centavos":b["total_centavos_by_month"].get(str(m))} for m in range(1,13) if a["total_centavos_by_month"].get(str(m))!=b["total_centavos_by_month"].get(str(m))],"esquema_compativel":a["columns"]==b["columns"]}
(out/"auditoria.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(result,ensure_ascii=False)[:16000])
if "error" in result["fontes"]["state"]:raise SystemExit(1)
