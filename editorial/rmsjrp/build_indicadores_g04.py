#!/usr/bin/env python3
"""Rebuild audited RMSJRP nominal, annual-average-IPCA real and per-capita DCA indicators from private R2."""
import csv,hashlib,json,os
from pathlib import Path
from decimal import Decimal,ROUND_HALF_UP
from deployment.download_r2_source import download_r2_object
root=Path("build/rmsjrp_g04");root.mkdir(parents=True,exist_ok=True)
sha="67a94313e0f0557bc23f48c78a1396fd02ae10ad7923ea2ac2e5c9f2726f65d5"
src=root/"dca.csv"
download_r2_object(account_id=os.environ["CLOUDFLARE_ACCOUNT_ID"],api_token=os.environ["CLOUDFLARE_API_TOKEN"],bucket=os.environ["CLOUDFLARE_R2_BUCKET"],object_key="sp_645/dca/2013_2025/normalized.csv",output=src)
assert hashlib.sha256(src.read_bytes()).hexdigest()==sha
def read(p,delimiter=","):
 with p.open(encoding="utf-8-sig",newline="") as f:
  yield from csv.DictReader(f,delimiter=delimiter)
cities={r["cod_ibge"]:r for r in read(Path("editorial/rmsjrp/MUNICIPIOS_SUBREGIOES_2025.csv"),";")}
factors={int(r["ano"]):Decimal(r["fator_set2026"]) for r in read(Path("editorial/rmsjrp/IPCA_MEDIA_ANUAL_SET2026.csv"),";")}
fields=["dca_receita_corrente_bruta","dca_receita_tributaria_bruta","dca_iptu_principal","dca_itbi_principal","dca_iss_principal","dca_fpm_cota_mensal","dca_icms_cota_parte","dca_ipva_cota_parte","dca_despesa_total_liquidada","dca_despesa_corrente_liquidada","dca_pessoal_encargos_liquidada","dca_investimentos_liquidada","dca_func_saude_liquidada","dca_func_educacao_liquidada","dca_func_urbanismo_liquidada"]
q=Decimal("0.01")
def dec(v):return Decimal(v) if v is not None and v!="" else None
def fmt(v):return str(v.quantize(q,rounding=ROUND_HALF_UP)) if v is not None else ""
def save(name,rows):
 p=root/name
 with p.open("w",encoding="utf-8",newline="") as f:
  wr=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter=";");wr.writeheader();wr.writerows(rows)
 return {"file":name,"rows":len(rows),"sha256":hashlib.sha256(p.read_bytes()).hexdigest(),"bytes":p.stat().st_size}
records=[]
for r in read(src):
 id=r["cod_ibge"]
 if id not in cities:continue
 y=int(r["ano"]);pop=dec(r["populacao_dca"])
 assert pop is None or pop>0
 a={"cod_ibge":id,"municipio":cities[id]["municipio"],"subregiao":cities[id]["subregiao_pdui"],"ano":str(y),"populacao_dca":str(pop) if pop is not None else "","fator_ipca_media_set2026":str(factors[y])}
 for field in fields:
  v=dec(r[field]);a[field+"_nominal"]=fmt(v);a[field+"_real_set2026"]=fmt(v*factors[y]) if v is not None else "";a[field+"_real_pc_set2026"]=fmt(v*factors[y]/pop) if v is not None and pop is not None else ""
 for field,name in [("dca_receita_tributaria_bruta","tributaria_pct_corrente"),("dca_investimentos_liquidada","investimento_pct_corrente"),("dca_fpm_cota_mensal","fpm_cota_pct_corrente"),("dca_icms_cota_parte","icms_pct_corrente")]:
  num=dec(r[field]);den=dec(r["dca_receita_corrente_bruta"])
  a[name]=fmt(Decimal(100)*num/den) if num is not None and den is not None and den>0 else ""
 records.append(a)
assert len(cities)==37 and len(records)==481
assert len({(r["cod_ibge"],r["ano"]) for r in records})==481
groups={"São José do Rio Preto":14,"José Bonifácio":11,"Tanabi":6,"Nova Granada":6}
assert {g:sum(c["subregiao_pdui"]==g for c in cities.values()) for g in groups}==groups
municipal=save("SERIES_MUNICIPAIS_2013_2025.csv",sorted(records,key=lambda r:(r["cod_ibge"],r["ano"])))
aggregates=[]
for y in range(2013,2026):
 for group in list(groups)+["RMSJRP"]:
  rr=[r for r in records if r["ano"]==str(y) and (group=="RMSJRP" or r["subregiao"]==group)]
  expected=37 if group=="RMSJRP" else groups[group]
  assert len(rr)==expected
  pp=[dec(r["populacao_dca"]) for r in rr];pop=sum(pp,Decimal(0)) if all(v is not None for v in pp) else None
  a={"territorio":group,"ano":str(y),"municipios_esperados":str(expected),"municipios_com_populacao":str(sum(v is not None for v in pp)),"populacao_total":str(pop) if pop is not None else "","fator_ipca_media_set2026":str(factors[y])}
  for field in fields:
   vv=[dec(r[field+"_nominal"]) for r in rr];n=sum(v is not None for v in vv)
   total=sum(vv,Decimal(0)) if n==expected else None
   a[field+"_observados"]=str(n);a[field+"_nominal"]=fmt(total);a[field+"_real_set2026"]=fmt(total*factors[y]) if total is not None else "";a[field+"_real_pc_set2026"]=fmt(total*factors[y]/pop) if total is not None and pop is not None and pop>0 else ""
  den=dec(a["dca_receita_corrente_bruta_nominal"])
  for field,name in [("dca_receita_tributaria_bruta","tributaria_pct_corrente"),("dca_investimentos_liquidada","investimento_pct_corrente"),("dca_fpm_cota_mensal","fpm_cota_pct_corrente"),("dca_icms_cota_parte","icms_pct_corrente")]:
   num=dec(a[field+"_nominal"]);a[name]=fmt(Decimal(100)*num/den) if num is not None and den is not None and den>0 else ""
  aggregates.append(a)
assert len(aggregates)==65
for y in range(2013,2026):
 whole=next(r for r in aggregates if r["territorio"]=="RMSJRP" and r["ano"]==str(y))
 subs=[r for r in aggregates if r["ano"]==str(y) and r["territorio"]!="RMSJRP"]
 for field in fields:
  key=field+"_nominal"
  if whole[key]:
   assert all(s[key] for s in subs)
   assert sum((dec(s[key]) for s in subs),Decimal(0))==dec(whole[key])
  else:assert any(not s[key] for s in subs)
regional=save("SERIES_TERRITORIAIS_2013_2025.csv",aggregates)
control=[{"ano":y,"receita":next(r for r in aggregates if r["territorio"]=="RMSJRP" and r["ano"]==str(y))["dca_receita_corrente_bruta_nominal"],"investimento":next(r for r in aggregates if r["territorio"]=="RMSJRP" and r["ano"]==str(y))["dca_investimentos_liquidada_nominal"]} for y in (2023,2024,2025)]
assert [r["investimento"] for r in control]==["444230252.48","480737206.37","208056124.00"]
missing_pop=[{"id":r["cod_ibge"],"ano":r["ano"]} for r in records if not r["populacao_dca"]]
qa={"status":"pass","dca_sha256":sha,"municipios":37,"pares_municipais":481,"pares_territoriais":65,"ipca_metodo":"media anual dos 12 numeros-indice, base setembro de 2026","ipca_referencia": "7695.82","ipca_fatores_fonte":"editorial/rmrp/IPCA_MEDIA_ANUAL_SET2026_LOTE17.md","populacao_ausente":missing_pop,"controle":control,"artefatos":[municipal,regional]}
(root/"QA_G04.json").write_text(json.dumps(qa,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"status":"pass","pares":481,"territorios_ano":65,"pop_ausente":len(missing_pop),"controle":control},ensure_ascii=False))
