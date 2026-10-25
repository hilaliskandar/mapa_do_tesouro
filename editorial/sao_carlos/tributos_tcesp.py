#!/usr/bin/env python3
import csv,io,json,urllib.request,zipfile,collections,decimal,sys
year=int(sys.argv[1]);url=f"https://transparencia.tce.sp.gov.br/sites/default/files/csv/receitas-sao-carlos-{year}.zip"
with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"}),timeout=180) as r: data=r.read()
totals=collections.defaultdict(int);classes=collections.Counter();months=collections.Counter()
with zipfile.ZipFile(io.BytesIO(data)) as z:
 f=next(n for n in z.namelist() if n.endswith(".csv"))
 with z.open(f) as raw:
  reader=csv.DictReader(io.TextIOWrapper(raw,encoding="latin-1",newline=""),delimiter=";")
  for row in reader:
   code=(row.get("ds_tipo") or "").split(" - ",1)[0].strip();m=int(row["mes_referencia"])
   imp=None
   if code.startswith("111250"):imp="IPTU"
   elif code.startswith("111253"):imp="ITBI"
   elif code.startswith("111451"):imp="ISS"
   if not imp:continue
   val=decimal.Decimal((row.get("vl_arrecadacao") or "0").replace(".","").replace(",","."));cents=int((val*100).quantize(decimal.Decimal("1")))
   totals[(imp,m,code)]+=cents;classes[(imp,code,(row.get("ds_tipo") or ""))]+=cents;months[m]+=1
print(json.dumps({"ano":year,"fonte":url,"dados":[{"imposto":i,"mes":m,"codigo":c,"centavos":v} for (i,m,c),v in sorted(totals.items())],
"codigos":[{"imposto":i,"codigo":c,"descricao":d,"centavos":v} for (i,c,d),v in sorted(classes.items())],"meses_tributos":dict(months)},ensure_ascii=False))
