#!/usr/bin/env python3
"""Inventory TCESP 2025 receipt taxonomy without assuming equivalence to DCA."""
import collections,csv,decimal,hashlib,io,json,pathlib,urllib.request,zipfile
URL="https://transparencia.tce.sp.gov.br/sites/default/files/conjunto-dados/receitas-2025.zip"
OUT=pathlib.Path("build/tcesp-receitas-taxonomia-2025");OUT.mkdir(parents=True,exist_ok=True)
with urllib.request.urlopen(urllib.request.Request(URL,headers={"User-Agent":"Mozilla/5.0"}),timeout=240) as resp:
 data=resp.read(65000000)
if len(data)>=65000000:raise RuntimeError("zip over maximum")
dims=["ds_categoria","ds_subcategoria","ds_fonte","ds_d1","ds_dd2","ds_d3","ds_tipo","ds_poder"]
frequency={x:collections.Counter() for x in dims}
totals={x:collections.Counter() for x in dims}
city_types=collections.Counter();samples={};issues=collections.Counter();rows=0
with zipfile.ZipFile(io.BytesIO(data)) as z:
 names=[x for x in z.namelist() if x.endswith(".csv")];assert len(names)==1
 with z.open(names[0]) as stream:
  reader=csv.DictReader(io.TextIOWrapper(stream,encoding="latin-1",newline=""),delimiter=";")
  for row in reader:
   rows+=1
   try:
    v=decimal.Decimal((row.get("vl_arrecadacao") or "").strip().replace(".","").replace(",","."))*100
    if not v.is_finite() or v!=v.to_integral_value():raise ValueError("centavos")
    cents=int(v)
   except (ValueError,decimal.InvalidOperation):
    issues["valor_invalido"]+=1;continue
   for d in dims:
    k=(row.get(d) or "").strip()
    frequency[d][k]+=1;totals[d][k]+=cents
    if k not in samples.setdefault(d,{}):samples[d][k]={"ds_municipio":row.get("ds_municipio"),"mes_referencia":row.get("mes_referencia")}
   city_types[((row.get("ds_municipio") or "").strip(),(row.get("ds_poder") or "").strip())]+=1
output={"ano":2025,"rows":rows,"source_sha256":hashlib.sha256(data).hexdigest(),"issues":dict(issues),"dimensions":{d:[{"valor":key,"quantidade":n,"valor_centavos":totals[d][key],"exemplo":samples[d][key]} for key,n in frequency[d].most_common()] for d in dims},"municipios_por_tipo_poder":len(city_types),"nota":"Inventory of raw classifications; NO automatic tax-category mapping or DCA parity asserted."}
(OUT/"taxonomia.json").write_text(json.dumps(output,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"rows":rows,"issues":dict(issues),"classification_cardinality":{x:len(frequency[x]) for x in dims},"sha256":output["source_sha256"]},ensure_ascii=False))
