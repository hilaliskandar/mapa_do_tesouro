#!/usr/bin/env python3
"""Verify previously audited TCESP 2025 exports, create immutable manifest. No network."""
import csv,hashlib,json,pathlib,sys,collections,datetime
year=int(sys.argv[2]);assert year in (2023,2024)
root=pathlib.Path(sys.argv[1]);qa=json.loads((root/"qa.json").read_text(encoding="utf-8"))
assert qa["status"]=="pass",qa["status"]
assert qa["year"]==year and qa["municipalities"]==644
assert qa["issues"]=={} and qa["difference_count"]==0
assert len(qa["sha256_zip"])==64
names=["investimentos_grupo44_por_municipio_mes_estagio.csv","investimentos_grupo44_por_programa.csv","investimentos_grupo44_por_acao.csv"]
fieldcounts=[4,7,9];aggregated=[];objects=[]
for i,name in enumerate(names):
 file=root/name;count=0;rolled=collections.Counter()
 with file.open(encoding="utf-8",newline="") as f:
  rd=csv.reader(f);head=next(rd)
  assert len(head)==fieldcounts[i],(name,head)
  for row in rd:
   assert len(row)==fieldcounts[i],(name,row)
   count+=1;rolled[tuple(row[:3])]+=int(row[-1])
 assert count==([qa["groups"],qa["programs"],qa["actions"]][i]),(name,count)
 aggregated.append(rolled)
 digest=hashlib.file_digest(file.open("rb"),"sha256").hexdigest()
 objects.append({"name":name,"sha256":digest,"bytes":file.stat().st_size,"rows":count})
assert aggregated[0]==aggregated[1]==aggregated[2],"Mismatch across levels"
assert sum(v for k,v in aggregated[0].items() if k[2]=="valor liquidado")==qa["stage_liquidado_cents"]
qafile=root/"qa.json"
objects.insert(0,{"name":"qa.json","sha256":hashlib.file_digest(qafile.open("rb"),"sha256").hexdigest(),"bytes":qafile.stat().st_size})
manifest={"schema_version":1,"source":"TCESP","source_year":year,"source_sha256_zip":qa["sha256_zip"],
 "source_run_id":40263996213,"source_artifact_id":({2023:12626100442,2024:12626330351}[year]),"qa_status":"pass",
 "rows_source":qa["rows"],"municipalities":qa["municipalities"],
 "investment_liquidated_centavos":qa["stage_liquidado_cents"],"objects":objects,
 "r2_prefix":f"tcesp/estadual/despesas/{year}/run_40263996213"}
(root/"r2_manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(manifest,ensure_ascii=False))
