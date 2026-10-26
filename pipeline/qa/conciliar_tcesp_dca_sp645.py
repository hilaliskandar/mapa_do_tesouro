#!/usr/bin/env python3
"""Audit TCESP liquidated investment totals against DCA v2 municipal observations.
Never equate missing, unavailable or non-observed records to zero.
"""
import argparse,csv,decimal,json,pathlib,collections
D=decimal.Decimal
p=argparse.ArgumentParser()
p.add_argument("--site",required=True,type=pathlib.Path)
p.add_argument("--output",required=True,type=pathlib.Path)
p.add_argument("--variable",default="dca_investimentos_liquidada")
a=p.parse_args()
root=a.site/"data/api/v2"
cat=json.loads((root/"catalog/variables.json").read_text())
variables={v["variavel_id"]:v for v in cat["variables"]}
assert a.variable in variables, "DCA variable not in v2 catalog"
codes=[m["codigo_ibge"] for m in json.loads((root/"catalog/municipalities.json").read_text())]
assert len(codes)==645 and len(set(codes))==645
rows=[];count=collections.Counter()
for year in (2023,2024,2025):
 data=json.loads((root/"tcesp"/str(year)/"municipios.json").read_text())
 grouped=collections.defaultdict(list)
 for r in data["rows"]:
  if r["estagio"]=="valor liquidado":grouped[r["codigo_ibge"]].append(r["valor_centavos"])
 assert len(grouped)==644,(year,len(grouped),sorted(set(codes)-set(grouped))[:8])
 for code in codes:
  if code not in grouped:
   rows.append({"codigo_ibge":code,"ano":year,"classificacao":"nao_confrontavel","motivo":"sem_cobertura_tcesp","tcesp_centavos":"","dca_centavos":"","diferenca_centavos":""})
   count["nao_confrontavel"]+=1
   continue
  tc=sum(grouped[code])
  doc=json.loads((root/"municipalities"/f"{code}.json").read_text())
  observations=[r for r in doc["variables"].get(a.variable,[]) if r["year"]==year]
  if len(observations)!=1:
   status="nao_confrontavel";reason="ausente_ou_duplicado";dc=None
  else:
   obs=observations[0]
   if obs["status"]!="observado" or obs["value"] is None:
    status="nao_confrontavel";reason="status_"+str(obs["status"]);dc=None
   else:
    try:
     val=D(str(obs["value"]))
     cents=val*100
     if cents!=cents.to_integral_value():raise ValueError("fração de centavo")
     dc=int(cents)
     status="concordante" if dc==tc else "divergente";reason=""
    except (decimal.InvalidOperation,ValueError):
     status="nao_confrontavel";reason="valor_dca_invalido";dc=None
  count[status]+=1
  rows.append({"codigo_ibge":code,"ano":year,"classificacao":status,"motivo":reason,"tcesp_centavos":tc,"dca_centavos":dc if dc is not None else "","diferenca_centavos":tc-dc if dc is not None else ""})
assert len(rows)==1935
a.output.parent.mkdir(parents=True,exist_ok=True)
with a.output.open("w",newline="",encoding="utf-8") as out:
 writer=csv.DictWriter(out,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
report={"status":"pass","variable":a.variable,"metric":"investimentos liquidados em centavos","years":[2023,2024,2025],"rows":len(rows),"counts":dict(count),"largest_differences":sorted((r for r in rows if r["classificacao"]=="divergente"),key=lambda r:abs(r["diferenca_centavos"]),reverse=True)[:15]}
a.output.with_suffix(".summary.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n")
print(json.dumps(report,ensure_ascii=False))
