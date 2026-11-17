#!/usr/bin/env python3
"""FED14: audit public Obrasgov API responses for 19 RMRP project IDs.
This is an API coverage audit, not proof of physical absence or execution.
Raw replies, including IDs and descriptions, go only to private Drive ZIP.
"""
import argparse,collections,datetime,hashlib,json,zipfile
from pathlib import Path
import requests
MODULES=["projeto-investimento","geometria","execucao-fisica","contrato"]
OTHER=["geometria","execucao-fisica","empenho","contrato"]
ROOT="https://api-publica.obrasgov.gestao.gov.br/obras"
def sha(path):
 h=hashlib.sha256()
 with open(path,"rb") as f:
  for b in iter(lambda:f.read(1048576),b""):h.update(b)
 return h.hexdigest()
def main(filesdir,out):
 out.mkdir(parents=True,exist_ok=True)
 files=list(filesdir.glob("*.json"))
 assert len(files)==19
 statuses=collections.Counter()
 projects=[]
 for path in files:
  data=json.loads(path.read_text())
  project=data["id_projeto"]
  reply=data["sources"]
  p=reply["projeto-investimento"]["payload"]
  assert reply["projeto-investimento"]["http_status"]==200
  assert len(p["data"])==1
  item=p["data"][0]
  assert item["id_projeto_investimento"]==project
  row={"project":project,"proposal":data["proposta_id"],"situacao":item.get("situacao"),
       "has_address":bool(item.get("desc_endereco")),
       "has_postcode":bool(item.get("nr_cep")),
       "has_pins":bool(item.get("pins")),
       "has_photos":bool(item.get("fotos")),
       "has_effective_start":bool(item.get("dt_inicial_efetiva")),
       "has_effective_end":bool(item.get("dt_final_efetiva"))}
  for ep in MODULES:
   r=reply[ep]
   assert r["http_status"]==200
   assert isinstance(r["payload"],dict)
   row["n_"+ep]=len(r["payload"].get("data",[]))
  statuses[item.get("situacao")]+=1
  projects.append(row)
 api=requests.Session()
 def get(path,params=None):
  r=api.get(ROOT+"/"+path,params=params,timeout=30)
  r.raise_for_status()
  return {"url":r.url,"sha256":hashlib.sha256(r.content).hexdigest(),"data":r.json()}
 general={"data_atualizacao":get("data-atualizacao"),"modulos":{}}
 for ep in ["projeto-investimento"]+OTHER:
  general["modulos"][ep]=get(ep,{"tamanho_da_pagina":1})
 assert general["modulos"]["projeto-investimento"]["data"]["total_items"]>0
 for ep in OTHER:
  assert general["modulos"][ep]["data"]["total_items"]==0
 assert all(not row["has_address"] and not row["has_postcode"] and not row["has_pins"] for row in projects)
 assert all(row["n_geometria"]==0 for row in projects)
 summary={"timestamp_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
  "api_source":ROOT,"source_snapshot":general["data_atualizacao"]["data"].get("data_ultima_atualizacao"),
  "projects_consulted":19,"project_matches":19,"status_counts":dict(statuses),
  "projects_with_registered_address":sum(x["has_address"] for x in projects),
  "projects_with_zipcode":sum(x["has_postcode"] for x in projects),
  "projects_with_pins":sum(x["has_pins"] for x in projects),
  "projects_with_geometria_endpoint_rows":sum(x["n_geometria"] for x in projects),
  "projects_with_physical_endpoint_rows":sum(x["n_execucao-fisica"] for x in projects),
  "projects_with_contract_endpoint_rows":sum(x["n_contrato"] for x in projects),
  "global_endpoint_total_items":{k:general["modulos"][k]["data"]["total_items"] for k in general["modulos"]},
  "global_endpoint_http_status":"200 (all)",
  "interpretation":"Endpoints geometria, execucao-fisica, empenho and contrato returned zero globally, so missing rows for the 19 projects are API module availability issues, not proof of absence.",
  "physical_execution_locations_homologated":0,
  "public_release_authorized":False,
  "cautions":["Project descriptions may name municipalities or sites but cannot prove actual executed coordinates.",
              "Do not replace Transferegov execution records with zero counts returned by an unpopulated API module.",
              "API returned official project's situation but no independently corroborated executed location."]}
 (out/"FED14_QA_AGREGADO.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n")
 (out/"FED14_RAW_GLOBAL_ENDPOINTS_PRIVADO.json").write_text(json.dumps(general,ensure_ascii=False,indent=2))
 (out/"FED14_19_PROJETOS_PRIVADO.json").write_text(json.dumps(projects,ensure_ascii=False,indent=2))
 zipout=out/"RMRP_FED14_API_OBRASGOV_COBERTURA_PRIVADA_2026-11-16.zip"
 with zipfile.ZipFile(zipout,"w",zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for p in files: z.write(p,"raw/19/"+p.name)
  for p in out.glob("FED14_*.json"):z.write(p,p.name)
 with zipfile.ZipFile(zipout) as z:assert z.testzip() is None
 return {"summary":summary,"zip_bytes":zipout.stat().st_size,"zip_sha256":sha(zipout)}
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("raw_dir",type=Path);p.add_argument("out",type=Path)
 a=p.parse_args()
 print(json.dumps(main(a.raw_dir,a.out),ensure_ascii=False))
