#!/usr/bin/env python3
"""Quality gate for segregated TCESP static API, without publishing it."""
import argparse,collections,hashlib,json,pathlib,statistics
p=argparse.ArgumentParser();p.add_argument("--site",type=pathlib.Path,required=True);p.add_argument("--report",type=pathlib.Path,required=True);p.add_argument("--max-detail-bytes",type=int,default=2000000);a=p.parse_args()
root=a.site/"data/api/v2/tcesp";assert root.is_dir()
manifest=json.loads((root/"manifest.json").read_text(encoding="utf-8"))
assert manifest["status"]=="preview_not_published"
assert [z["exercicio"] for z in manifest["exercises"]]==[2023,2024,2025]
sizes=[];all_stats=[];checks=0
for year in (2023,2024,2025):
 summary=json.loads((root/str(year)/"municipios.json").read_text(encoding="utf-8"))
 grouped=collections.Counter()
 for item in summary["rows"]:grouped[(item["codigo_ibge"],item["estagio"])]+=item["valor_centavos"]
 codes={c for c,_ in grouped}
 assert len(codes)==644
 detail_files=list((root/str(year)/"municipios").glob("*.json"))
 assert len(detail_files)==644
 for file in detail_files:
  raw=file.read_bytes();sizes.append({"year":year,"code":file.stem,"bytes":len(raw)})
  obj=json.loads(raw)
  assert obj["ano"]==year and obj["codigo_ibge"]==file.stem
  pr=collections.Counter();ac=collections.Counter()
  for row in obj["programas"]:pr[row["estagio"]]+=row["valor_centavos"]
  for row in obj["acoes"]:ac[row["estagio"]]+=row["valor_centavos"]
  assert pr==ac
  assert all(pr[stage]==value for (code,stage),value in grouped.items() if code==file.stem)
  assert set(pr)=={stage for code,stage in grouped if code==file.stem}
  checks+=1
 all_stats.append({"year":year,"municipios":len(codes),"arquivos_detalhe":len(detail_files)})
largest=sorted(sizes,key=lambda item:item["bytes"],reverse=True)[:12]
report={"status":"pass" if max(s["bytes"] for s in sizes)<=a.max_detail_bytes else "oversize_review",
 "detail_files":checks,"max_detail_bytes":max(s["bytes"] for s in sizes),"median_detail_bytes":int(statistics.median(s["bytes"] for s in sizes)),
 "largest":largest,"annual":all_stats,"threshold_bytes":a.max_detail_bytes,
 "notes":"Preview-only per-city/year JSON; avoid embedding this tree in public build without approved gate."}
a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(report,ensure_ascii=False))
if report["status"]!="pass":raise SystemExit(2)
