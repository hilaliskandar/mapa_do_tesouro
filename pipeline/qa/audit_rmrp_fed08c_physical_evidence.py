#!/usr/bin/env python3
"""FED08C: official execution evidence for 19 Obrasgov cases with cadastral-coordinate divergence.
Never infer actual execution coordinates or classify unverified measurements as paid spending.
"""
import argparse,collections,csv,io,json,hashlib,zipfile,sqlite3
from pathlib import Path
FILES=[
"siconv_execucao_fisica_cipi",
"siconv_acomp_obras_contratos_medicoes_modulo_empresas",
"siconv_acomp_obras_valores_itens_medicao_modulo_empresas",
"siconv_resumo_fisico_financeiro",
"siconv_projeto_basico_acffo_modulo_empresas",
]
def sha(path):
 h=hashlib.sha256()
 with open(path,"rb") as f:
  for b in iter(lambda:f.read(1048576),b""):h.update(b)
 return h.hexdigest()
def rows(path):
 with zipfile.ZipFile(path) as z:
  assert z.testzip() is None
  with z.open(z.namelist()[0]) as fd:
   yield from csv.DictReader(io.TextIOWrapper(fd,encoding="utf-8-sig",newline=""),delimiter=";")
def main(sqlite,src,out):
 out.mkdir(parents=True,exist_ok=True)
 c=sqlite3.connect(sqlite)
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 divergent=c.execute("""SELECT DISTINCT pc.id_projeto,v.id_proposta,o.situacao
  FROM projeto_coordenada_candidata_fed04b pc
  JOIN coordenada_intersecao_sp_fed04c g ON g.source_row=pc.source_row
  JOIN vinculo_projeto_instrumento_fed04b v ON v.id_projeto=pc.id_projeto
  JOIN obra_proponente o ON o.projeto_id=pc.id_projeto
  WHERE g.status_espacial<>'no_municipio_proponente'""").fetchall()
 assert len(divergent)==19
 cases={k:{"id_projeto":k,"id_proposta":v,"situacao_obrasgov":s,"registros_execucao_fisica_cipi":0,
  "percentual_cipi":"", "data_situacao_cipi":"",
  "registros_medicao":0,"medicoes_aceitas":0,"datas_medicao":"",
  "possui_resumo_fisico_financeiro":False,"percentual_resumo":"",
  "registros_projeto_basico":0,"situacao_spa_projeto_basico":[],
  "local_execucao_comprovado":False} for k,v,s in divergent}
 proposals={v:k for k,v,s in divergent}
 totals=collections.Counter()
 cipi_status=collections.Counter()
 for row in rows(src/"siconv_execucao_fisica_cipi.zip"):
  totals["execucao_fisica_cipi_nacional"]+=1
  k=row["id_projeto_investimento"].strip()
  if k not in cases:continue
  obj=cases[k]
  obj["registros_execucao_fisica_cipi"]+=1
  obj["percentual_cipi"]=row.get("percentual_execucao","")
  obj["data_situacao_cipi"]=row.get("data_situacao","")
  cipi_status[row.get("id_situacao","")]+=1
  totals["execucao_fisica_cipi_divergentes"]+=1
 for row in rows(src/"siconv_acomp_obras_contratos_medicoes_modulo_empresas.zip"):
  totals["medicoes_nacionais"]+=1
  k=proposals.get(row["ID_PROPOSTA"].strip())
  if not k:continue
  o=cases[k]
  o["registros_medicao"]+=1
  if row.get("SITUACAO_MEDICAO_ACOMPANHAMENTO_OBRA")=="Aceita":o["medicoes_aceitas"]+=1
  totals["medicoes_divergentes"]+=1
 for row in rows(src/"siconv_resumo_fisico_financeiro.zip"):
  totals["resumos_nacionais"]+=1
  k=proposals.get(row["ID_PROPOSTA"].strip())
  if not k:continue
  o=cases[k]
  o["possui_resumo_fisico_financeiro"]=True
  o["percentual_resumo"]=row.get("PERCENTUAL_EXECUCAO_RESUMO_FISICO_FINANCEIRO","")
  totals["resumos_divergentes"]+=1
 for row in rows(src/"siconv_projeto_basico_acffo_modulo_empresas.zip"):
  totals["projetos_basicos_nacionais"]+=1
  k=proposals.get(row["ID_PROPOSTA"].strip())
  if not k:continue
  o=cases[k]
  o["registros_projeto_basico"]+=1
  o["situacao_spa_projeto_basico"].append(row.get("SITUACAO_SPA",""))
  totals["projetos_basicos_divergentes"]+=1
 # This table lacks ID_PROPOSTA in its schema; document it but do not infer a proposal-level link.
 val_count=0
 for row in rows(src/"siconv_acomp_obras_valores_itens_medicao_modulo_empresas.zip"):
  val_count+=1
 totals["itens_valores_medicao_nacionais_sem_chave_direta_proposta"]=val_count
 statuses=collections.Counter()
 for k,o in cases.items():
  if o["registros_execucao_fisica_cipi"]:statuses["projetos_com_execucao_cipi"]+=1
  if o["registros_medicao"]:statuses["projetos_com_medicao"]+=1
  if o["medicoes_aceitas"]:statuses["projetos_com_medicao_aceita"]+=1
  if o["possui_resumo_fisico_financeiro"]:statuses["projetos_com_resumo"]+=1
  if o["registros_projeto_basico"]:statuses["projetos_com_projeto_basico"]+=1
  if any(x=="Homologada" for x in o["situacao_spa_projeto_basico"]):statuses["projetos_com_spa_homologada"]+=1
  statuses["projetos_com_evidencia_fisica_qualquer"]+=bool(o["registros_execucao_fisica_cipi"] or o["registros_medicao"] or o["possui_resumo_fisico_financeiro"])
  statuses["projetos_com_local_execucao_comprovado"]+=bool(o["local_execucao_comprovado"])
 assert len(cases)==19
 assert statuses["projetos_com_execucao_cipi"]==15
 assert statuses["projetos_com_medicao"]==12
 assert statuses["projetos_com_resumo"]==14
 assert statuses["projetos_com_projeto_basico"]==18
 assert statuses["projetos_com_local_execucao_comprovado"]==0
 qa={"snapshot":"2026-11-15","processing_date":"2026-11-16","target":"19_obrasgov_projects_with_cadastral_coordinate_divergences",
 "national_input_sha256":{n:sha(src/(n+".zip")) for n in FILES},
 "input_line_counts":dict(totals),
 "coverage":dict(statuses),
 "status_cipi_codes":dict(cipi_status),
 "crs":"EPSG:4674 for earlier IBGE municipal intersection",
 "source_level":"records of execution status, basic-project SPA, measurement, and F-F summary",
 "territorial_attestation":"not_homologated",
 "publication_authorized":False,
 "cautions":["Execution or measurement evidence does not prove the geographical coordinate of implementation.",
 "Measurement values table has contract and subgoal IDs; requires explicit bridge before classification by proposal.",
 "Use individual official project documents to establish site and address.",
 "Never sum physical measurement values with financial payments or disbursements."]}
 assert statuses["projetos_com_execucao_cipi"]<=19
 package=out/"RMRP_FED08C_EVIDENCIAS_EXECUCAO_FISICA_PRIVADA_2026-11-16.zip"
 detail=out/"FED08C_19_PROJETOS_EVIDENCIAS_PRIVADO.csv"
 with detail.open("w",encoding="utf-8-sig",newline="") as f:
  keys=["id_projeto","id_proposta","situacao_obrasgov","registros_execucao_fisica_cipi","percentual_cipi",
   "data_situacao_cipi","registros_medicao","medicoes_aceitas","possui_resumo_fisico_financeiro",
   "percentual_resumo","registros_projeto_basico","situacao_spa_projeto_basico","local_execucao_comprovado"]
  w=csv.DictWriter(f,keys,delimiter=";");w.writeheader()
  for row in cases.values():w.writerow({k:"|".join(row[k]) if isinstance(row[k],list) else row[k] for k in keys})
 summary=out/"FED08C_QA_AGREGADO.json"
 summary.write_text(json.dumps(qa,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 with zipfile.ZipFile(package,"w",zipfile.ZIP_DEFLATED) as z:
  z.write(detail,detail.name);z.write(summary,summary.name)
 with zipfile.ZipFile(package) as z:assert z.testzip() is None
 c.close()
 return {"qa":qa,"package_bytes":package.stat().st_size,"package_sha256":sha(package)}
if __name__=="__main__":
 ap=argparse.ArgumentParser()
 ap.add_argument("sqlite",type=Path);ap.add_argument("source_dir",type=Path);ap.add_argument("out",type=Path)
 a=ap.parse_args();print(json.dumps(main(a.sqlite,a.source_dir,a.out),ensure_ascii=False))
