#!/usr/bin/env python3
"""Conserva resultados TCESP de Sao Carlos a partir de artifacts preexistentes."""
import argparse,hashlib,json,pathlib,tarfile,collections
p=argparse.ArgumentParser();p.add_argument("--input",type=pathlib.Path,required=True);p.add_argument("--output",type=pathlib.Path,required=True);a=p.parse_args()
required={"sao-carlos-tcesp-2023-2026":"piloto_despesas",
"sao-carlos-tcesp-detalhe-2023-2026":"investimentos_detalhados",
"sao-carlos-receitas-tcesp-esquema-2023-2026":"esquema_receitas",
"sao-carlos-tributos-2023-2026":"tributos_por_mes"}
records=[];seen=set()
for folder,kind in required.items():
 base=a.input/folder
 fs=list(base.rglob("*.json"))
 if len(fs)!=4:raise SystemExit(f"esperados 4 JSONs em {folder}; presentes {len(fs)}")
 for file in sorted(fs):
  d=json.loads(file.read_text(encoding="utf-8"))
  year=int(d.get("ano",d.get("year",0)))
  if year not in range(2023,2027):raise SystemExit(f"ano invalido {file}")
  key=(kind,year)
  if key in seen:raise SystemExit(f"duplicado {key}")
  seen.add(key)
  if kind=="investimentos_detalhados":
   assert len(d["sha256_zip"])==64
   assert d["investimento_liquidado_centavos"]==sum(x["centavos"] for x in d["agrupamentos"]["orgao"])
  if kind=="tributos_por_mes":assert len(d.get("dados",[]))>0 and d["ano"]==year
  records.append({"dominio":kind,"ano":year,"path":str(file.relative_to(a.input)),"sha256":hashlib.sha256(file.read_bytes()).hexdigest()})
assert len(records)==16
a.output.mkdir(parents=True,exist_ok=True);tar=a.output/"sao_carlos_tcesp_2023_2026.tar.gz"
with tarfile.open(tar,"w:gz") as t:
 for item in records:t.add(a.input/item["path"],arcname=item["path"])
manifest={"municipio_ibge":"3548906","municipio":"Sao Carlos","years":[2023,2024,2025,2026],
 "sources":{"piloto_despesas":40213455640,"investimentos_detalhados":40222584058,
 "esquema_receitas":40226770931,"tributos_por_mes":40226826428},
 "files":len(records),"archive_sha256":hashlib.sha256(tar.read_bytes()).hexdigest(),
 "archive_bytes":tar.stat().st_size,"items":records,"publicado":False,
 "exercicio_2026_parcial":True,"nota":"Arquivos historicos e parciais; diferencas com DCA nao eliminadas."}
(a.output/"manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"files":len(records),"sha256":manifest["archive_sha256"]}))
