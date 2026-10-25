#!/usr/bin/env python3
"""Audita acervo de artifacts TCESP reutilizados, sem baixar arquivos da fonte."""
import argparse,csv,hashlib,json,pathlib,collections,datetime
p=argparse.ArgumentParser();p.add_argument("--root",type=pathlib.Path,required=True);p.add_argument("--roster",type=pathlib.Path,required=True);p.add_argument("--output",type=pathlib.Path,required=True);a=p.parse_args()
with a.roster.open(encoding="utf-8-sig",newline="") as f: roster=list(csv.DictReader(f))
by_slug={r["slug"]:r for r in roster}; results=[]; errors=[]; found=set()
for fp in sorted(a.root.rglob("*.json")):
 try: d=json.loads(fp.read_text(encoding="utf-8"))
 except Exception:continue
 if not {"slug","year","investimento_44_liquidado_centavos","sha256_zip"}.issubset(d):continue
 slug=d["slug"];year=int(d["year"]);key=(slug,year)
 if key in found:errors.append(f"Duplicado: {slug} {year}");continue
 found.add(key)
 try:
  assert len(d["sha256_zip"])==64 and d.get("bad_values")==0
  total=int(d["investimento_44_liquidado_centavos"])
  assert sum(int(x[-1]) for x in d["programas_44_liquidado_completos"])==total
  assert sum(int(x[-1]) for x in d["acoes_44_liquidado_completas"])==total
  status="validado"
 except Exception as e: status="falha";errors.append(f"{slug}/{year}: {e}")
 results.append({"codigo_ibge":by_slug.get(slug,{}).get("codigo_ibge", "3548906" if slug=="sao-carlos" else None),
  "slug":slug,"ano":year,"status":status,"valor_centavos":total,"fonte":d.get("url"),
  "fonte_sha256":d["sha256_zip"],"json_sha256":hashlib.sha256(fp.read_bytes()).hexdigest(),
  "arquivo":str(fp.relative_to(a.root))})
expected={(r["slug"],y) for r in roster for y in (2023,2024,2025)}|{("sao-carlos",y) for y in (2023,2024,2025,2026)}
missing=sorted(expected-found)
if missing:errors.append("Faltantes: "+str(missing))
summary={"timestamp_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"escopo_esperado":len(expected),
"extraidos":len(results),"validados":sum(x["status"]=="validado" for x in results),
"faltantes":missing,"erros":errors,"fonte_nova_consultada":False,"r2_persistido":False,"publicado":False,
"registros":results}
a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({k:v for k,v in summary.items() if k!="registros"},ensure_ascii=False))
if errors:raise SystemExit(1)
