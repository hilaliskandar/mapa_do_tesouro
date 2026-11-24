#!/usr/bin/env python3
"""FED13: add validated LAE/QCI/meta/submeta coverage to a PRIVATE FED10 preview.

No inferred geographic points or payment-classification corrections.
"""
import argparse,collections,hashlib,json,shutil,sqlite3,zipfile
from pathlib import Path
from pipeline.qa.validate_rmrp_api_v3_fed07 import validate

PREFIX=Path("data/api/v3/investimentos/rmrp")
def read(path):return json.loads(path.read_text(encoding="utf-8"))
def write(path,obj):path.write_text(json.dumps(obj,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
def sha(path):
 h=hashlib.sha256()
 with path.open("rb") as f:
  for b in iter(lambda:f.read(1048576),b""):h.update(b)
 return h.hexdigest()
def build(previous_site,dbpath,dest,archive):
 if dest.exists():raise RuntimeError("Output exists")
 if not (previous_site/".rmrp-fed07-private-preview").is_file():raise RuntimeError("Private marker required")
 shutil.copytree(previous_site,dest)
 api=dest/PREFIX
 db=sqlite3.connect(dbpath)
 assert db.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 assert db.execute("PRAGMA foreign_key_check").fetchall()==[]
 cases=db.execute("SELECT projeto_id,proposta_id FROM fed12_projetos_prioritarios").fetchall()
 assert len(cases)==19
 counts=collections.Counter()
 for project,proposal in cases:
  f=api/"projetos"/(project+".json")
  assert f.exists()
  obj=read(f)
  assert obj["instrumentos_vinculados"][0]["proposta_id"]==proposal
  assert obj["localizacao_fisica"]["pontos"]==[]
  assert obj["valores_investimento_pago_centavos"] is None
  qcis=db.execute("SELECT count(*),count(DISTINCT qci_id) FROM fed12_lae WHERE proposta_id=?",(proposal,)).fetchone()
  metas=db.execute("""SELECT count(*) FROM fed12_meta m JOIN fed12_lae l ON l.qci_id=m.qci_id
   WHERE l.proposta_id=?""",(proposal,)).fetchone()[0]
  submetas=db.execute("""SELECT count(*) FROM fed12_submeta s JOIN fed12_meta m ON m.meta_id=s.meta_id
   JOIN fed12_lae l ON l.qci_id=m.qci_id WHERE l.proposta_id=?""",(proposal,)).fetchone()[0]
  hist=db.execute("SELECT count(*) FROM fed12_historico WHERE proposta_id=?",(proposal,)).fetchone()[0]
  spa=db.execute("SELECT count(*) FROM fed12_acffo WHERE proposta_id=? AND spa='Homologada'",(proposal,)).fetchone()[0]
  obj["evidencia_projeto_basico_qci_fed13"]={
    "relacionamento":"proposta_id -> LAE.ID_PROPOSTA -> ID_QCI_ACFFO -> meta.ID_QCI_ACFFO -> submeta.ID_META_PROJETO_BASICO",
    "qci_lae":qcis[0],"metas":metas,"submetas":submetas,
    "historicos_projeto_basico":hist,"acffo_spa_homologadas":spa,
    "link_verificado":bool(qcis[0]),
    "estado_localidade_submetas":"SP" if submetas else None,
    "endereco_ou_localizacao_fisica_homologada":False,
    "qa_status":"cadeia_documental_verificada_local_nao_comprovado",
    "nota":"ID_ACFFO e ID_QCI_ACFFO sao chaves de entidades diferentes e nao podem ser unidos pela igualdade numerica."}
  obj["public_release_authorized"]=False
  write(f,obj)
  counts["projects_examined"]+=1
  counts["qci_rows"]+=qcis[0]
  counts["metas"]+=metas
  counts["submetas"]+=submetas
  counts["historicos"]+=hist
  counts["projects_linked"]+=bool(qcis[0])
 assert dict(counts)=={"projects_examined":19,"qci_rows":61,"metas":74,
                      "submetas":74,"historicos":306,"projects_linked":18}
 manifest=read(api/"manifest.json")
 manifest["coverage"]["projetos_divergentes_com_ponte_qci_laudo"]=18
 manifest["coverage"]["metas_de_projeto_basico_ligadas_por_qci"]=74
 manifest["coverage"]["submetas_de_projeto_basico_ligadas_por_meta"]=74
 manifest["coverage"]["projetos_divergentes_sem_ponte_qci"]=1
 manifest["coverage"]["localizacoes_fisicas_homologadas"]=0
 manifest["sources_fed13"]=[{"module":"siconv_projeto_basico_lae_modulo_empresas","sha256":"f506204d11b5e555959384886ddcd56e2b3bba700b3459ab0761c8d305bf667b"},
  {"module":"siconv_projeto_basico_metas_modulo_empresas","sha256":"f4f91ceb3e64de2fee67a0d74092e166c7883e6fbc5f3ed29de202a0909c1d99"},
  {"module":"siconv_projeto_basico_submetas_modulo_empresas","sha256":"3f64f185f03a669deae6d7cdf2dcef0828a7ef80ad3802c643742979a9fc3dd9"}]
 manifest["public_release_authorized"]=False
 write(api/"manifest.json",manifest)
 pend=read(api/"pendencias.json")
 pend.setdefault("territorial",[]).append("FED13: 18 de 19 projetos divergentes possuem ponte LAE-QCI documentada para 74 metas e 74 submetas SP, mas localizacao fisica permanece nao comprovada.")
 pend["territorial"].append("Nao confundir ID_ACFFO com ID_QCI_ACFFO; associacao numerica sem tabela LAE produz falsos vinculos interestaduais.")
 write(api/"pendencias.json",pend)
 for f in (api/"projetos").glob("*.json"):
  p=read(f)
  assert p["localizacao_fisica"]["qa_status"]=="nao_comprovada"
  assert not p["localizacao_fisica"]["pontos"]
  assert p["valores_investimento_pago_centavos"] is None
 qa=validate(api)
 assert qa["technical_checks_passed"]>=1603
 report={"version":"FED13","projects_priority":19,"with_qci":18,"qci_rows":61,"metas":74,
         "submetas":74,"history_events":306,"new_physical_locations_approved":0,
         "technical_checks":qa["technical_checks_passed"],"public_release_authorized":False}
 write(dest/"QA_FED13_QCI_PRIVADO.json",report)
 with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for f in dest.rglob("*"):
   if f.is_file() and f.name!=".rmrp-fed07-private-preview":z.write(f,f.relative_to(dest))
 with zipfile.ZipFile(archive) as z: assert z.testzip() is None
 report["archive_bytes"]=archive.stat().st_size;report["archive_sha256"]=sha(archive)
 db.close()
 return report
if __name__=="__main__":
 ap=argparse.ArgumentParser()
 ap.add_argument("site",type=Path);ap.add_argument("sqlite",type=Path)
 ap.add_argument("outsite",type=Path);ap.add_argument("outzip",type=Path)
 a=ap.parse_args();print(json.dumps(build(a.site,a.sqlite,a.outsite,a.outzip),ensure_ascii=False))
