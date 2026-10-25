#!/usr/bin/env python3
"""Inventario verificado por municipios/ano/dominio. Sem consultas ao TCESP."""
import argparse,csv,json,pathlib,collections
p=argparse.ArgumentParser();p.add_argument("--dca",type=pathlib.Path,required=True);p.add_argument("--rmrp-historico",type=pathlib.Path,required=True);p.add_argument("--rmrp-2026",type=pathlib.Path,required=True);p.add_argument("--sao-carlos",type=pathlib.Path,required=True);p.add_argument("--output",type=pathlib.Path,required=True);a=p.parse_args()
with a.dca.open(encoding="utf-8-sig") as f:state={r["cod_ibge"] for r in csv.DictReader(f)}
assert len(state)==645
h=json.loads(a.rmrp_historico.read_text());q=json.loads(a.rmrp_2026.read_text());s=json.loads(a.sao_carlos.read_text())
assert h["pairs"]==102 and q["observacoes"]==68 and s["files"]==16
records={}
def add(ibge,year,domain,source,detail="",month=""):
 k=(str(ibge),int(year),domain)
 if k in records:raise ValueError(f"overlap {k}")
 records[k]={"codigo_ibge":k[0],"ano":k[1],"dominio":k[2],"status":"r2_validado","origem":source,"detalhe":detail,"ultimo_mes":month}
for r in h["records"]:add(r["municipio_ibge"],r["year"],"investimentos_liquidados_44","rmrp_historico")
for r in q["documentos"]:add(r["codigo_ibge"],r["ano"],"investimentos_movimentacoes_44" if r["dominio"]=="despesas" else "tributos_iptu_iss_itbi","rmrp_2026","parcial",r["ultimo_mes"])
for r in s["items"]:
 typ=r["dominio"];domain={"piloto_despesas":"investimentos_liquidados_44","investimentos_detalhados":"investimentos_movimentacoes_44","esquema_receitas":"estrutura_receitas","tributos_por_mes":"tributos_iptu_iss_itbi"}[typ]
 add("3548906",r["ano"],domain,"sao_carlos", "parcial" if r["ano"]==2026 else "")
assert all(k[0] in state for k in records)
domains=["investimentos_liquidados_44","investimentos_movimentacoes_44","tributos_iptu_iss_itbi","estrutura_receitas"]
a.output.mkdir(parents=True,exist_ok=True)
out=a.output/"cobertura_tcesp_sp645_2023_2026.csv"
with out.open("w",encoding="utf-8",newline="") as f:
 w=csv.DictWriter(f,fieldnames=["codigo_ibge","ano","dominio","status","origem","detalhe","ultimo_mes"]);w.writeheader()
 for ibge in sorted(state):
  for y in (2023,2024,2025,2026):
   for d in domains:
    w.writerow(records.get((ibge,y,d),{"codigo_ibge":ibge,"ano":y,"dominio":d,"status":"nao_inventariado_no_r2","origem":"","detalhe":"","ultimo_mes":""}))
summary={"municipios":645,"anos":[2023,2024,2025,2026],"dominios":domains,"total_possibilidades":645*4*len(domains),
"registros_comprovados_r2":len(records),"por_origem":dict(collections.Counter(v["origem"] for v in records.values())),
"aviso":"NAO INVENTARIADO nao equivale a inexistencia no TCESP. Investimentos_liquidados e movimentacoes podem ser produtos distintos da mesma fonte; nao somar coberturas.",
"publicacao_autorizada":False}
(a.output/"resumo.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(summary,ensure_ascii=False))
