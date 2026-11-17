#!/usr/bin/env python3
"""FED12 - official QCI/ACFFO bridge for 19 RMRP projects with spatial divergence.

Joins must follow:
  project -> proposal (existing official instrument)
  proposal -> LAE (ID_PROPOSTA)
  LAE -> basic-project meta (ID_QCI_ACFFO)
  meta -> submeta (ID_META_PROJETO_BASICO)
No ID_ACFFO = ID_QCI_ACFFO joins permitted.
This is documentary/cadastral provenance, never a physical-execution coordinate.
"""
import argparse,csv,io,sqlite3,zipfile,collections,json,hashlib,shutil
from pathlib import Path
SOURCE_FILES = {
 "lae":"siconv_projeto_basico_lae_modulo_empresas.zip",
 "proposta_pb":"siconv_projeto_basico_proposta_modulo_empresas.zip",
 "historico":"siconv_historico_projeto_basico.zip",
 "meta":"siconv_projeto_basico_metas_modulo_empresas.zip",
 "submeta":"siconv_projeto_basico_submetas_modulo_empresas.zip",
 "acffo":"siconv_projeto_basico_acffo_modulo_empresas.zip",
}
def stream_csv(path):
 with zipfile.ZipFile(path) as z:
  assert z.testzip() is None
  with z.open(z.namelist()[0]) as f:
   yield from csv.DictReader(io.TextIOWrapper(f,encoding="utf-8-sig",newline=""),delimiter=";")
def sha(path):
 h=hashlib.sha256()
 with open(path,"rb") as f:
  for b in iter(lambda:f.read(1048576),b""):h.update(b)
 return h.hexdigest()
def audit(database,root8c,root11,out):
 out.mkdir(parents=True,exist_ok=True)
 source_paths={
  "lae":root11/SOURCE_FILES["lae"],
  "proposta_pb":root11/SOURCE_FILES["proposta_pb"],
  "historico":root11/SOURCE_FILES["historico"],
  "meta":root11/SOURCE_FILES["meta"],
  "submeta":root11/SOURCE_FILES["submeta"],
  "acffo":root8c/SOURCE_FILES["acffo"]
 }
 for p in source_paths.values():assert p.is_file(),p
 dest=out/"RMRP_FED12_QCI_PROJETOS_PRIVADO.sqlite"
 shutil.copyfile(database,dest)
 db=sqlite3.connect(dest)
 db.execute("PRAGMA foreign_keys=ON")
 project_rows=db.execute("""SELECT DISTINCT pc.id_projeto,v.id_proposta,ob.situacao
  FROM projeto_coordenada_candidata_fed04b pc
  JOIN coordenada_intersecao_sp_fed04c ge ON ge.source_row=pc.source_row
  JOIN vinculo_projeto_instrumento_fed04b v ON v.id_projeto=pc.id_projeto
  JOIN obra_proponente ob ON ob.projeto_id=pc.id_projeto
  WHERE ge.status_espacial <> 'no_municipio_proponente'""").fetchall()
 assert len(project_rows)==19
 projects={p:{"proposta":pr,"situacao":s} for p,pr,s in project_rows}
 proposals={r["proposta"] for r in projects.values()}
 assert len(proposals)==19
 db.executescript("""
 CREATE TABLE fed12_projetos_prioritarios(
  projeto_id TEXT PRIMARY KEY REFERENCES obra_proponente(projeto_id),
  proposta_id TEXT NOT NULL REFERENCES proposta(id),
  situacao_obrasgov TEXT NOT NULL,
  local_execucao_homologado INTEGER NOT NULL DEFAULT 0 CHECK(local_execucao_homologado=0));
 CREATE TABLE fed12_lae(
  qci_id TEXT PRIMARY KEY, acffo_id TEXT NOT NULL, proposta_id TEXT NOT NULL REFERENCES proposta(id),
  situacao_lae TEXT, emissao_lae TEXT, data_emissao_lae TEXT);
 CREATE INDEX fed12_lae_proposal ON fed12_lae(proposta_id);
 CREATE TABLE fed12_meta(
  meta_id TEXT PRIMARY KEY, qci_id TEXT NOT NULL REFERENCES fed12_lae(qci_id),
  descricao TEXT, nome_item TEXT, descricao_subitem TEXT);
 CREATE TABLE fed12_submeta(
  submeta_id TEXT PRIMARY KEY,meta_id TEXT NOT NULL REFERENCES fed12_meta(meta_id),
  descricao TEXT,localidade_uf TEXT,situacao TEXT,valor_total_literal TEXT);
 CREATE TABLE fed12_pb_proposta(
  source_row INTEGER PRIMARY KEY,proposta_id TEXT NOT NULL REFERENCES proposta(id),
  id_proposta_acffo TEXT,valor_global_literal TEXT);
 CREATE TABLE fed12_acffo(
  id_acffo TEXT PRIMARY KEY, proposta_id TEXT NOT NULL REFERENCES proposta(id),
  situacao TEXT,spa TEXT,data_aceite TEXT);
 CREATE TABLE fed12_historico(
  source_row INTEGER PRIMARY KEY,proposta_id TEXT NOT NULL REFERENCES proposta(id),
  data_historico TEXT,situacao TEXT,evento TEXT);
 """)
 db.executemany("INSERT INTO fed12_projetos_prioritarios(projeto_id,proposta_id,situacao_obrasgov) VALUES(?,?,?)",project_rows)
 raw=collections.Counter()
 for i,row in enumerate(stream_csv(source_paths["lae"]),1):
  raw["lae_national"]+=1
  pid=row["ID_PROPOSTA"].strip()
  if pid not in proposals:continue
  db.execute("INSERT INTO fed12_lae VALUES(?,?,?,?,?,?)",
   (row["ID_QCI_ACFFO"].strip(),row["ID_ACFFO"].strip(),pid,
    row["SITUACAO_LAE_PROJETO_BASICO"],row["EMISSAO_LAE_PROJETO_BASICO"],
    row["DATA_EMISSAO_LAE_PROJETO_BASICO"]))
  raw["lae_matched"]+=1
 qcis={x[0] for x in db.execute("SELECT qci_id FROM fed12_lae")}
 proposal_to_acffo=collections.defaultdict(set)
 for qci,acffo,prop in db.execute("SELECT qci_id,acffo_id,proposta_id FROM fed12_lae"):
  proposal_to_acffo[prop].add(acffo)
 for i,row in enumerate(stream_csv(source_paths["acffo"]),1):
  raw["acffo_national"]+=1
  pid=row["ID_PROPOSTA"].strip()
  if pid not in proposals:continue
  aid=row["ID_ACFFO"].strip()
  if aid not in proposal_to_acffo[pid]:
   raise AssertionError("ACFFO missing from explicit LAE bridge")
  db.execute("INSERT INTO fed12_acffo VALUES(?,?,?,?,?)",
   (aid,pid,row["SITUACAO_PROJETO_BASICO"],row["SITUACAO_SPA"],
    row["DATA_ACEITE_PROJETO_BASICO"]))
  raw["acffo_matched"]+=1
 for i,row in enumerate(stream_csv(source_paths["proposta_pb"]),1):
  raw["proposta_pb_national"]+=1
  pid=row["ID_PROPOSTA"].strip()
  if pid not in proposals:continue
  db.execute("INSERT INTO fed12_pb_proposta VALUES(?,?,?,?)",
   (i,pid,row["ID_PROPOSTA_ACFFO"],row["VALOR_GLOBAL_PROPOSTA_PROJETO_BASICO"]))
  raw["proposta_pb_matched"]+=1
 for i,row in enumerate(stream_csv(source_paths["meta"]),1):
  raw["meta_national"]+=1
  qci=row["ID_QCI_ACFFO"].strip()
  if qci not in qcis:continue
  db.execute("INSERT INTO fed12_meta VALUES(?,?,?,?,?)",
   (row["ID_META_PROJETO_BASICO"],qci,row["DESCRICAO_META_PROJETO_BASICO"],
    row["NOME_ITEM_INVESTIMENTO_META"],row["DESCRICAO_SUBITEM_INVESTIMENTO_META"]))
  raw["meta_matched"]+=1
 meta_ids={x[0] for x in db.execute("SELECT meta_id FROM fed12_meta")}
 for i,row in enumerate(stream_csv(source_paths["submeta"]),1):
  raw["submeta_national"]+=1
  mid=row["ID_META_PROJETO_BASICO"].strip()
  if mid not in meta_ids:continue
  db.execute("INSERT INTO fed12_submeta VALUES(?,?,?,?,?,?)",
   (row["ID_SUBMETA_PROJETO_BASICO"],mid,row["DESCRICAO_SUBMETA_PROJETO_BASICO"],
    row["SIGLA_LOCALIDADE_OBRA_PROJETO_BASICO"],row["SITUACAO_SUBMETA_PROJETO_BASICO"],
    row["VALOR_TOTAL_SUBMETA_PROJETO_BASICO"]))
  raw["submeta_matched"]+=1
 for i,row in enumerate(stream_csv(source_paths["historico"]),1):
  raw["historico_national"]+=1
  pid=row["ID_PROPOSTA"].strip()
  if pid not in proposals:continue
  db.execute("INSERT INTO fed12_historico VALUES(?,?,?,?,?)",
   (i,pid,row["DATA_HIST_PB_TR"],row["SITUACAO_HIST_PB_TR"],row["EVENTO_HIST_PB_TR"]))
  raw["historico_matched"]+=1
 db.commit()
 q=lambda sql:db.execute(sql).fetchone()[0]
 lae_status=dict(db.execute("SELECT situacao_lae || ' / ' || emissao_lae,COUNT(*) FROM fed12_lae GROUP BY 1").fetchall())
 states=dict(db.execute("SELECT localidade_uf,count(*) FROM fed12_submeta GROUP BY 1").fetchall())
 sub_status=dict(db.execute("SELECT situacao,count(*) FROM fed12_submeta GROUP BY 1").fetchall())
 history_status=dict(db.execute("SELECT situacao,count(*) FROM fed12_historico GROUP BY 1").fetchall())
 summary={
  "snapshot":"2026-11-15","process_date":"2026-11-16",
  "priority_projects":len(projects),"priority_proposals":len(proposals),
  "counts":dict(raw),
  "lae_unique_qci":len(qcis),
  "qci_with_meta":q("SELECT COUNT(DISTINCT qci_id) FROM fed12_meta"),
  "proposals_with_la_e_bridge":q("SELECT COUNT(DISTINCT proposta_id) FROM fed12_lae"),
  "proposals_with_meta":q("SELECT COUNT(DISTINCT l.proposta_id) FROM fed12_meta m JOIN fed12_lae l ON l.qci_id=m.qci_id"),
  "proposals_with_submeta":q("SELECT COUNT(DISTINCT l.proposta_id) FROM fed12_submeta s JOIN fed12_meta m ON m.meta_id=s.meta_id JOIN fed12_lae l ON l.qci_id=m.qci_id"),
  "UF_submeta":states,"lae_status":lae_status,"submeta_situation":sub_status,
  "history_status":history_status,
  "proposals_without_lae":sorted(proposals-{x[0] for x in db.execute("SELECT DISTINCT proposta_id FROM fed12_lae")}),
  "spa_homologada_proposals":q("SELECT COUNT(DISTINCT proposta_id) FROM fed12_acffo WHERE spa='Homologada'"),
  "description_address_like_submeta_count":q("""SELECT COUNT(*) FROM fed12_submeta
   WHERE lower(descricao) LIKE '%rua %' OR lower(descricao) LIKE '%avenida %'
      OR lower(descricao) LIKE '%bairro %' OR lower(descricao) LIKE '%rodovia %'
      OR lower(descricao) LIKE '%praça %' OR lower(descricao) LIKE '%praca %'"""),
  "coordinates_derived_or_homologated":0,
  "cross_join_rejected":"ID_ACFFO != ID_QCI_ACFFO; explicit LAE bridge mandatory",
  "integrity":db.execute("PRAGMA integrity_check").fetchone()[0],
  "fk_violations":len(db.execute("PRAGMA foreign_key_check").fetchall()),
  "source_sha256":{k:sha(p) for k,p in source_paths.items()},
  "limitations":[
    "The QCI id and ACFFO id are different entity identifiers; accidental numeric matches lead to false regional assignments.",
    "Laudo LAE, SPA, QCI, metas and submetas establish project documentation, not physical execution address.",
    "UF of submeta is only a federative unit, not georeferenced point or proof of work built.",
    "Historical status is time-varying; do not infer execution from a current row.",
    "No update of public platform and no capital paid homologation."],
  "public_release_authorized":False}
 assert raw["lae_matched"]==61 and raw["acffo_matched"]==18
 assert raw["meta_matched"]==74 and raw["submeta_matched"]==74 and raw["historico_matched"]==306
 assert summary["proposals_with_submeta"]==18 and states=={"SP":74}
 assert summary["integrity"]=="ok" and summary["fk_violations"]==0
 details=out/"FED12_SUBMETAS_COM_PROPOSTAS_PRIVADO.csv"
 with details.open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.writer(f,delimiter=";")
  w.writerow(["proposta_id","projeto_id","qci_id","meta_id","submeta_id","descricao_meta","descricao_submeta","UF_submeta","situacao_submeta"])
  w.writerows(db.execute("""SELECT l.proposta_id,p.projeto_id,l.qci_id,m.meta_id,s.submeta_id,
          m.descricao,s.descricao,s.localidade_uf,s.situacao
      FROM fed12_submeta s JOIN fed12_meta m ON m.meta_id=s.meta_id
      JOIN fed12_lae l ON l.qci_id=m.qci_id
      JOIN fed12_projetos_prioritarios p ON p.proposta_id=l.proposta_id
      ORDER BY l.proposta_id,m.meta_id,s.submeta_id"""))
 qa=out/"FED12_QA_AGREGADO.json"
 qa.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 db.close()
 pack=out/"RMRP_FED12_PONTE_QCI_ACFFO_PRIVADA_2026-11-16.zip"
 with zipfile.ZipFile(pack,"w",zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for p in (dest,details,qa):z.write(p,p.name)
 with zipfile.ZipFile(pack) as z:assert z.testzip() is None
 return {"QA":summary,"package_bytes":pack.stat().st_size,"sha256":sha(pack)}
if __name__=="__main__":
 ap=argparse.ArgumentParser()
 ap.add_argument("sqlite",type=Path)
 ap.add_argument("sources8c",type=Path)
 ap.add_argument("sources11",type=Path)
 ap.add_argument("output",type=Path)
 a=ap.parse_args()
 print(json.dumps(audit(a.sqlite,a.sources8c,a.sources11,a.output),ensure_ascii=False))
