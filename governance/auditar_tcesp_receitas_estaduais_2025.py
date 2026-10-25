#!/usr/bin/env python3
"""TCESP 2025 statewide revenues full-coverage read-only audit; no R2/API writes."""
import collections,csv,decimal,hashlib,io,json,pathlib,urllib.request,zipfile
URL="https://transparencia.tce.sp.gov.br/sites/default/files/conjunto-dados/receitas-2025.zip"
OUT=pathlib.Path("build/tcesp-receitas-full-qa"); OUT.mkdir(parents=True,exist_ok=True)
money=decimal.Decimal
req=urllib.request.Request(URL,headers={"User-Agent":"Mozilla/5.0 (TCESP read-only audit)"})
with urllib.request.urlopen(req,timeout=240) as resp:
 data=resp.read(65000000)
if len(data)>=65000000: raise RuntimeError("Oversize file")
assert zipfile.is_zipfile(io.BytesIO(data))
counts=collections.Counter();months=collections.defaultdict(set);by_city=collections.defaultdict(int);bad=collections.Counter();years=collections.Counter();organs=collections.Counter();examples={}
with zipfile.ZipFile(io.BytesIO(data)) as z:
 names=[n for n in z.namelist() if n.lower().endswith(".csv")]
 assert len(names)==1,names
 with z.open(names[0]) as raw:
  reader=csv.DictReader(io.TextIOWrapper(raw,encoding="latin-1",newline=""),delimiter=";")
  fields=reader.fieldnames
  assert {"ds_municipio","ano_exercicio","mes_referencia","vl_arrecadacao"}.issubset(fields),fields
  for i,row in enumerate(reader,1):
   municipality=(row.get("ds_municipio") or "").strip()
   year=(row.get("ano_exercicio") or "").strip()
   month=(row.get("mes_referencia") or "").strip()
   val=(row.get("vl_arrecadacao") or "").strip()
   if not municipality: bad["municipio_vazio"]+=1
   if year!="2025":bad["ano_divergente"]+=1
   if not month.isdigit() or not 1<=int(month)<=12:bad["mes_invalido"]+=1
   else:months[municipality].add(int(month))
   try:
    n=money(val.replace(".","").replace(",","."))
    cents=n*100
    if not cents.is_finite() or cents!=cents.to_integral_value(): raise ValueError()
    by_city[municipality]+=int(cents)
   except (decimal.InvalidOperation,ValueError):bad["valor_invalido"]+=1
   counts[municipality]+=1;years[year]+=1
   organs[(row.get("ds_orgao") or "").strip()]+=1
   if municipality and municipality not in examples:examples[municipality]={"ano":year,"mes":month}
result={
 "url":URL,"sha256_zip":hashlib.sha256(data).hexdigest(),"zip_bytes":len(data),
 "csv_name":names[0],"columns":fields,"rows":sum(counts.values()),"municipios_distintos":len(counts),
 "anos":dict(years),"problemas":dict(bad),"municipios_com_12_meses":sum(len(v)==12 for v in months.values()),
 "distribuicao_quantidade_meses":dict(sorted(collections.Counter(len(v) for v in months.values()).items())),
 "municipios_sem_12_meses":[{"nome":k,"meses":sorted(v)} for k,v in sorted(months.items()) if len(v)<12][:100],
 "totais_por_municipio_centavos":dict(sorted(by_city.items())),
 "linhas_por_municipio":dict(sorted(counts.items())),
 "nota":"Audit of source rows only; entities may include organizations beyond municipalities; municipality identity not yet reconciled against SP645 roster; negative adjustment values are preserved."
}
(OUT/"qa.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({k:v for k,v in result.items() if k not in ("totais_por_municipio_centavos","linhas_por_municipio")},ensure_ascii=False)[:16000])
