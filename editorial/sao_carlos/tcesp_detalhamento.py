#!/usr/bin/env python3
"""Auditoria mensal por orgao, acao e fonte dos investimentos 4.4, TCESP Sao Carlos."""
import csv,io,json,urllib.request,zipfile,hashlib,sys,collections,decimal
ano=int(sys.argv[1]);url=f"https://transparencia.tce.sp.gov.br/sites/default/files/csv/despesas-sao-carlos-{ano}.zip"
request=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"})
data=urllib.request.urlopen(request,timeout=180).read()
assert zipfile.is_zipfile(io.BytesIO(data))
counts=collections.Counter();groups=collections.defaultdict(int);examples=collections.defaultdict(list)
with zipfile.ZipFile(io.BytesIO(data)) as z:
 name=z.namelist()[0]
 with z.open(name) as stream:
  reader=csv.DictReader(io.TextIOWrapper(stream,encoding="latin-1",newline=""),delimiter=";")
  for row in reader:
   if not (row.get("ds_elemento") or "").strip().split(" - ",1)[0].startswith("44"):continue
   typ=(row.get("tp_despesa") or "").strip();month=(row.get("mes_referencia") or "").strip()
   cents=int((decimal.Decimal((row.get("vl_despesa") or "0").replace(".","").replace(",","."))*100).quantize(decimal.Decimal("1")))
   counts[(typ,month)]+=cents
   if typ!="Valor Liquidado":continue
   org=(row.get("ds_orgao") or "").strip();prog=(row.get("cd_programa") or "").strip();acao=(row.get("cd_acao") or "").strip()
   desc=(row.get("ds_acao") or "").strip();fonte=(row.get("ds_fonte_recurso") or "").strip()
   groups[("orgao",org)]+=cents;groups[("mes",month)]+=cents;groups[("fonte",fonte)]+=cents
   groups[("acao",org,prog,acao,desc)]+=cents
   groups[("acao_mes",month,org,prog,acao,desc)]+=cents
   groups[("acao_fonte",org,prog,acao,desc,fonte)]+=cents
   key=(org,prog,acao,desc)
   if len(examples[key])<3:examples[key].append((row.get("historico_despesa") or "")[:220])
def encode():
 return {k:[{"chaves":list(key[1:]),"centavos":v} for key,v in sorted(groups.items(),key=lambda it:-it[1]) if key[0]==k] for k in ["orgao","mes","fonte","acao","acao_mes","acao_fonte"]}
total=sum(v for (typ,month),v in counts.items() if typ=="Valor Liquidado")
assert total==sum(x["centavos"] for x in encode()["orgao"])
result={"ano":ano,"url":url,"sha256_zip":hashlib.sha256(data).hexdigest(),"investimento_liquidado_centavos":total,
"por_mes_tipo":[{"tipo":t,"mes":m,"centavos":v} for (t,m),v in sorted(counts.items())],
"agrupamentos":encode(),"historicos_exemplos":[{"chaves":list(k),"exemplos":v} for k,v in examples.items()]}
print(json.dumps(result,ensure_ascii=False))
