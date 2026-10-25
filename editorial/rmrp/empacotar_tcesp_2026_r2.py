#!/usr/bin/env python3
"""Empacota extratos TCESP 2026 ja coletados; valida antes de promover."""
import argparse,collections,datetime,gzip,hashlib,json,pathlib,tarfile
p=argparse.ArgumentParser();p.add_argument("--input",type=pathlib.Path,required=True);p.add_argument("--output",type=pathlib.Path,required=True);a=p.parse_args()
a.output.mkdir(parents=True,exist_ok=True)
entries=[];seen=set();months=collections.Counter();errors=[]
for sub in (1,2,3,4):
 d=a.input/f"subregiao_{sub}"
 m=d/"manifesto.json"
 if not m.exists():raise SystemExit(f"missing {m}")
 report=json.loads(m.read_text(encoding="utf-8"))
 if report["falhas"] or report["validados"]!=report["esperados"]:raise SystemExit(f"incomplete region {sub}")
 for fp in sorted(d.glob("*_2026_*.json")):
  x=json.loads(fp.read_text(encoding="utf-8"));k=(x["codigo_ibge"],x["dominio"],x["ano"])
  if k in seen:raise SystemExit(f"duplicate {k}")
  seen.add(k)
  if x["ano"]!=2026 or x["situacao_exercicio"]!="parcial_em_andamento" or len(x["fonte_sha256"])!=64:raise SystemExit(f"invalid metadata {k}")
  mm=x["meses_observados"]
  if mm!=list(range(1,max(mm)+1)):errors.append({"codigo_ibge":k[0],"dominio":k[1],"meses":mm,"motivo":"meses_nao_contiguos"})
  months[(x["dominio"],max(mm))]+=1
  entries.append({"codigo_ibge":k[0],"slug":x["slug"],"dominio":k[1],"ano":2026,
      "ultimo_mes":max(mm),"source_sha256":x["fonte_sha256"],"json_sha256":hashlib.sha256(fp.read_bytes()).hexdigest(),
      "path":str(fp.relative_to(a.input))})
if len(entries)!=68 or len({x["codigo_ibge"] for x in entries})!=34:raise SystemExit(f"cardinality {len(entries)}")
archive=a.output/"tcesp_rmrp_2026_68_extratos.tar.gz"
with tarfile.open(archive,"w:gz") as tf:
 for sub in (1,2,3,4):
  for f in sorted((a.input/f"subregiao_{sub}").glob("*.json")):
   tf.add(f,arcname=str(f.relative_to(a.input)),recursive=False)
h=hashlib.sha256(archive.read_bytes()).hexdigest()
manifest={"snapshot_id":"tcesp_rmrp_2026_40229219185","year":2026,"source_run_id":40229219185,
 "universo":"RMRP_34","observacoes":68,"municipios":34,"exercicio_parcial":True,
 "por_dominio_e_ultimo_mes":[{"dominio":k[0],"ultimo_mes":k[1],"quantidade":v} for k,v in sorted(months.items())],
 "lacunas_de_meses":errors,"archive_sha256":h,"archive_bytes":archive.stat().st_size,
 "armazenamento":"a_confirmar_apos_upload_e_leitura","publicacao_autorizada":False,"documentos":entries}
(a.output/"manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({k:v for k,v in manifest.items() if k!="documentos"},ensure_ascii=False))
