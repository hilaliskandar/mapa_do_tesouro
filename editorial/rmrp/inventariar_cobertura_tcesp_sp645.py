#!/usr/bin/env python3
"""Inventario SP645 TCESP: cobertura COMPROVADA, nunca inferir ausencia na fonte."""
import argparse,csv,json,pathlib,collections,datetime
p=argparse.ArgumentParser();p.add_argument("--dca",type=pathlib.Path,required=True);p.add_argument("--roster",type=pathlib.Path,required=True);p.add_argument("--historico",type=pathlib.Path,required=True);p.add_argument("--parcial",type=pathlib.Path,required=True);p.add_argument("--out",type=pathlib.Path,required=True);a=p.parse_args()
with a.dca.open(encoding="utf-8-sig",newline="") as f: rows=list(csv.DictReader(f))
fields=set(rows[0])
field=next((x for x in ("cod_ibge","codigo_ibge","municipio_ibge") if x in fields),None)
if field is None:raise SystemExit(f"No IBGE code column: {sorted(fields)}")
state={str(r[field]).strip() for r in rows if str(r.get(field,"")).strip().isdigit()}
if len(state)!=645:raise SystemExit(f"Expected 645 municipality codes; observed {len(state)}")
with a.roster.open(encoding="utf-8-sig",newline="") as f:region=list(csv.DictReader(f))
hist=json.loads(a.historico.read_text(encoding="utf-8"));partial=json.loads(a.parcial.read_text(encoding="utf-8"))
assert hist["pairs"]==102 and hist["municipios"]==34
assert partial["observacoes"]==68 and partial["municipios"]==34
rh={(str(x["municipio_ibge"]),int(x["year"])) for x in hist["records"]}
rp={(str(x["codigo_ibge"]),x["dominio"]) :x for x in partial["documentos"]}
assert len(rh)==102 and len(rp)==68
assert {str(r["codigo_ibge"]) for r in region}.issubset(state)
statuses=[];summary=collections.Counter()
for ibge in sorted(state):
 for year in (2023,2024,2025,2026):
  for domain in ("despesas","receitas"):
   status="cobertura_a_verificar";months=None;provenance=None
   if year<2026 and domain=="despesas" and (ibge,year) in rh:
    status="persistido_r2_validado";provenance="rmrp_102"
   elif year==2026 and (ibge,domain) in rp:
    status="persistido_r2_parcial";months=rp[(ibge,domain)]["ultimo_mes"];provenance="rmrp_2026_68"
   elif ibge=="3548906":
    status="artifact_temporario_verificar";provenance="sao_carlos_2023_2026"
   statuses.append({"codigo_ibge":ibge,"ano":year,"dominio":domain,"status":status,"ultimo_mes_conhecido":months,"acervo":provenance})
   summary[(year,domain,status)]+=1
a.out.mkdir(parents=True,exist_ok=True)
csvout=a.out/"matriz_cobertura_tcesp_sp645_2023_2026.csv"
with csvout.open("w",encoding="utf-8",newline="") as f:
 writer=csv.DictWriter(f,fieldnames=statuses[0].keys());writer.writeheader();writer.writerows(statuses)
manifest={"created_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"municipalities":645,
"candidate_pairs":len(statuses),"note":"cobertura_a_verificar significa NAO INVENTARIADO no acervo R2 tcesp; nao significa indisponivel TCESP.",
"source_historical":"tcesp/rmrp/2023_2025/run_39203495737/manifest.json",
"source_2026":"tcesp/rmrp/2026/run_40229219185/manifest.json",
"counts":[{"ano":y,"dominio":d,"status":s,"quantidade":n} for (y,d,s),n in sorted(summary.items())],
"publication_authorized":False}
(a.out/"manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"municipios":645,"pares":len(statuses),"contagens":manifest["counts"]},ensure_ascii=False))
