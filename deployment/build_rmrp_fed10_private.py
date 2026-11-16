#!/usr/bin/env python3
"""FED10: add document-backed physical-stage evidence for 19 projects to PRIVATE API.
Never set execution coordinates, municipality of implementation, or investment paid.
"""
import argparse,csv,collections,hashlib,json,shutil,zipfile
from pathlib import Path
from pipeline.qa.validate_rmrp_api_v3_fed07 import validate

ROOT=Path("data/api/v3/investimentos/rmrp")
def load(p):return json.loads(p.read_text(encoding="utf-8"))
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
def sha(p):
 h=hashlib.sha256()
 with p.open("rb") as f:
  for b in iter(lambda:f.read(1048576),b""):h.update(b)
 return h.hexdigest()
def build(site,private_cases,dest,package):
 if dest.exists():raise RuntimeError("Private site destination exists")
 if not (site/".rmrp-fed07-private-preview").is_file():raise RuntimeError("Private marker missing")
 shutil.copytree(site,dest)
 root=dest/ROOT
 counts=collections.Counter()
 with private_cases.open("r",encoding="utf-8-sig",newline="") as f:
  cases=list(csv.DictReader(f,delimiter=";"))
 assert len(cases)==19 and len({x["id_projeto"] for x in cases})==19
 for case in cases:
  p=root/"projetos"/(case["id_projeto"]+".json")
  assert p.exists()
  doc=load(p)
  assert doc["instrumentos_vinculados"][0]["proposta_id"]==case["id_proposta"]
  assert doc["localizacao_fisica"]["qa_status"]=="nao_comprovada"
  assert doc["localizacao_fisica"]["pontos"]==[]
  assert doc["valores_investimento_pago_centavos"] is None
  count_cipi=int(case["registros_execucao_fisica_cipi"])
  count_med=int(case["registros_medicao"])
  count_accepted=int(case["medicoes_aceitas"])
  count_basic=int(case["registros_projeto_basico"])
  assert count_accepted<=count_med
  doc["evidencia_adicional_execucao_fisica"]={
   "origem":"siconv_execucao_fisica_cipi|siconv_acomp_obras_contratos_medicoes_modulo_empresas|siconv_resumo_fisico_financeiro|siconv_projeto_basico_acffo_modulo_empresas",
   "registros_execucao_fisica_cipi":count_cipi,
   "registros_medicao":count_med,
   "medicoes_aceitas":count_accepted,
   "registros_projeto_basico":count_basic,
   "possui_resumo_fisico_financeiro":case["possui_resumo_fisico_financeiro"]=="True",
   "localizacao_fisica_efetiva_homologada":False,
   "financeiro_gnd4_pago_homologado":False,
   "qa_status":"documental_cadastral_sem_comprovacao_local",
   "nota":"Registros de andamento e medicao nao documentam por si as coordenadas exatas de execucao fisica."
  }
  doc["public_release_authorized"]=False
  counts["projects_updated"]+=1
  if count_cipi:counts["projects_cipi"]+=1
  if count_med:counts["projects_measurement"]+=1
  if count_accepted:counts["projects_accepted_measurement"]+=1
  if count_basic:counts["projects_basic"]+=1
  save(p,doc)
 assert counts=={"projects_updated":19,"projects_cipi":15,"projects_measurement":12,
                "projects_accepted_measurement":7,"projects_basic":18}
 manifest=load(root/"manifest.json")
 manifest["coverage"]["projetos_divergentes_com_evidencia_documental_avaliada"]=19
 manifest["coverage"]["projetos_divergentes_com_execucao_fisica_cipi"]=15
 manifest["coverage"]["projetos_divergentes_com_medicao_aceita"]=7
 manifest["coverage"]["projetos_divergentes_com_local_execucao_homologado"]=0
 assert manifest["public_release_authorized"] is False
 save(root/"manifest.json",manifest)
 pending=load(root/"pendencias.json")
 pending.setdefault("territorial",[]).append("FED10: 19 projetos espacialmente divergentes tiveram bases de medicao/projeto-basico consultadas; nenhum ponto de execucao foi comprovado por endereco ou documento georreferenciado.")
 save(root/"pendencias.json",pending)
 technical=validate(root)
 assert technical["technical_checks_passed"]>=1603
 for file in (root/"projetos").glob("*.json"):
  x=load(file)
  assert x["localizacao_fisica"]["qa_status"]=="nao_comprovada"
  assert not x["localizacao_fisica"]["pontos"]
  assert x["valores_investimento_pago_centavos"] is None
 out={"version":"FED10_private_execution_evidence","audit_source_snapshot":"2026-11-15",
      "counts":dict(counts),"qa":technical,
      "public_release_authorized":False,"physical_locations_homologated":0}
 save(dest/"QA_FED10_EVIDENCIA_EXECUCAO_PRIVADA.json",out)
 with zipfile.ZipFile(package,"w",zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for f in dest.rglob("*"):
   if f.is_file() and f.name!=".rmrp-fed07-private-preview":z.write(f,f.relative_to(dest))
 with zipfile.ZipFile(package) as z:assert z.testzip() is None
 out["package_bytes"]=package.stat().st_size;out["package_sha256"]=sha(package)
 return out
if __name__=="__main__":
 ap=argparse.ArgumentParser();ap.add_argument("site",type=Path)
 ap.add_argument("cases_csv",type=Path);ap.add_argument("output_site",type=Path)
 ap.add_argument("output_zip",type=Path)
 a=ap.parse_args()
 print(json.dumps(build(a.site,a.cases_csv,a.output_site,a.output_zip),ensure_ascii=False))
