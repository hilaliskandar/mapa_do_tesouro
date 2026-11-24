#!/usr/bin/env python3
"""FED15 private-preview overlay with an API coverage disclaimer.
Never treat absent records in globally empty endpoints as proof of absent works.
"""
import argparse,datetime,hashlib,json,shutil,zipfile
from pathlib import Path
from pipeline.qa.validate_rmrp_api_v3_fed07 import validate

ROOT=Path("data/api/v3/investimentos/rmrp")
def read(p):return json.loads(p.read_text(encoding="utf-8"))
def save(p,obj):p.write_text(json.dumps(obj,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
def sha(p):
 h=hashlib.sha256()
 with p.open("rb") as f:
  for b in iter(lambda:f.read(1048576),b""):h.update(b)
 return h.hexdigest()
def build(src,sourceqa,source_private,dest,outzip):
 if dest.exists():raise RuntimeError("Destination exists")
 if not (src/".rmrp-fed07-private-preview").is_file():raise RuntimeError("Private marker required")
 shutil.copytree(src,dest)
 root=dest/ROOT
 qa=read(sourceqa)
 assert qa["projects_consulted"]==19 and qa["project_matches"]==19
 expected={"geometria":0,"execucao-fisica":0,"empenho":0,"contrato":0}
 for ep,total in expected.items():assert qa["global_endpoint_total_items"][ep]==total
 assert qa["global_endpoint_total_items"]["projeto-investimento"]>100000
 cases=read(source_private)
 assert len(cases)==19
 seen=set()
 for x in cases:
  project=x["project"]; assert project not in seen;seen.add(project)
  p=root/"projetos"/(project+".json")
  assert p.exists()
  obj=read(p)
  assert obj["id_origem"]==project
  assert obj["localizacao_fisica"]["qa_status"]=="nao_comprovada"
  assert obj["localizacao_fisica"]["pontos"]==[]
  assert obj["valores_investimento_pago_centavos"] is None
  obj["cobertura_api_publica_obrasgov_fed15"]={
   "snapshot_atualizacao_api":qa["source_snapshot"],
   "fonte":"https://api-publica.obrasgov.gestao.gov.br/obras",
   "cadastro_projeto_localizado":True,
   "situacao_atual_cadastro":x["situacao"],
   "endereco_cadastral_fornecido":x["has_address"],
   "cep_cadastral_fornecido":x["has_postcode"],
   "geometria_retornada":False,
   "status_endpoint_geometria":"sem_registros_na_api_global",
   "status_endpoint_execucao_fisica":"sem_registros_na_api_global",
   "status_endpoint_contratos":"sem_registros_na_api_global",
   "interpretacao":"Ausencia de retorno em endpoint globalmente vazio nao prova ausencia da intervencao nem de coordenadas noutros sistemas.",
   "ponto_de_execucao_homologado":False,
   "qa_status":"limite_cobertura_api"}
  obj["public_release_authorized"]=False
  save(p,obj)
 manifest=read(root/"manifest.json")
 manifest["coverage"]["projetos_divergentes_consultados_api_obrasgov_nova"]=19
 manifest["coverage"]["projetos_divergentes_com_endereco_disponivel_na_nova_api"]=0
 manifest["coverage"]["modulos_api_obrasgov_globalmente_sem_registros"]=[
   "geometria","execucao-fisica","empenho","contrato"]
 manifest["coverage"]["localizacoes_fisicas_homologadas"]=0
 manifest["sources_fed15"]=[{"nome":"API Obrasgov 2026","url":"https://api-publica.obrasgov.gestao.gov.br/obras","snapshot":qa["source_snapshot"],"qa":"limite_de_cobertura"}]
 manifest["public_release_authorized"]=False
 save(root/"manifest.json",manifest)
 pend=read(root/"pendencias.json")
 pend.setdefault("territorial",[]).append("FED15: os 19 projetos foram localizados no cadastro da nova API Obrasgov, sem endereco, CEP ou pins; quatro endpoints complementares estavam vazios globalmente. Tratar como indisponibilidade de dados nessa fonte, nunca como ausencia da obra.")
 save(root/"pendencias.json",pend)
 checks=validate(root)
 assert checks["technical_checks_passed"]>=1603
 projects=[read(p) for p in (root/"projetos").glob("*.json")]
 assert sum(p.get("cobertura_api_publica_obrasgov_fed15",{}).get("cadastro_projeto_localizado",False) for p in projects)==19
 assert all(not p["localizacao_fisica"]["pontos"] for p in projects)
 assert all(p["valores_investimento_pago_centavos"] is None for p in projects)
 result={"version":"FED15","projects_queried":19,"project_matches":19,
         "empty_global_modules":list(expected),"private_only":True,
         "api_checks_passed":checks["technical_checks_passed"],
         "new_physical_points":0,"public_release_authorized":False}
 save(dest/"QA_FED15_API_OBRASGOV_PRIVADO.json",result)
 with zipfile.ZipFile(outzip,"w",zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for p in dest.rglob("*"):
   if p.is_file() and p.name!=".rmrp-fed07-private-preview":z.write(p,p.relative_to(dest))
 with zipfile.ZipFile(outzip) as z:assert z.testzip() is None
 result["zip_size"]=outzip.stat().st_size;result["zip_sha256"]=sha(outzip)
 return result
if __name__=="__main__":
 ap=argparse.ArgumentParser()
 for name in ("site","qa","cases","output_site","output_zip"):ap.add_argument(name,type=Path)
 a=ap.parse_args()
 print(json.dumps(build(a.site,a.qa,a.cases,a.output_site,a.output_zip),ensure_ascii=False))
