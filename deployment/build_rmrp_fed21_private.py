#!/usr/bin/env python3
"""FED21: source coverage and contextual institutional evidence for last 3 RMRP cases.

No source here explicitly identifies an executed site for 974564, 996136 or
953339; do not promote location, contract payments or work completion.
"""
import argparse,hashlib,json,shutil,zipfile
from pathlib import Path
from pipeline.qa.validate_rmrp_api_v3_fed07 import validate
BASE=Path("data/api/v3/investimentos/rmrp")
CASES={
 "30158.35-25":{
  "instrumento":"953339","municipio":"Jaboticabal",
  "objeto":"Reforma da Estação de Tratamento de Esgoto",
  "evidencia_institucional":{
    "instalacao_existente":"ETE Dr. Adelson Taroco",
    "descricao_local":"Proximidades da Rodovia Carlos Tonani, em area concedida pela Unesp, Campus Jaboticabal",
    "fonte_institucional":"https://www.jaboticabal.sp.gov.br/portal/secretarias-paginas/83/tratamento-de-esgoto/",
    "fonte_operadora":"https://www.saaej.sp.gov.br/tratamento-de-esgoto/",
    "evidencia_planejamento":"LDO 2025 inclui reforma de ETE entre as prioridades com previsao aproximada de R$ 7,1 milhoes",
    "fonte_orcamentaria":"https://www.jaboticabal.sp.leg.br/imprensa/noticias/camara-municipal-de-jaboticabal-aprova-ldo-2025-por-unanimidade",
    "vinculo_explicito_ao_contrato_953339_nessas_paginas":False,
    "fonte_nao_demonstrou_endereco_do_objeto_contratado":True,
    "categoria":"hipotese_contextual_institucional_nao_homologada",
    "local_execucao_comprovado":False,
    "coordenadas_inferidas":None,
    "valor_previsto_na_ldo_nao_e_pago":True
   },
  "pendencia":"Localizar projeto basico/edital e processo administrativo que associe 953339 ao local exato da ETE e comprove a frente executada."
 },
 "50782.35-08":{
  "instrumento":"974564","municipio":"Santa Rosa de Viterbo",
  "objeto":"Implantação de Unidades Habitacionais do MCMV FNHIS Sub-50",
  "resultado_pesquisa_externa":"nenhum documento municipal encontrado vinculando terreno especifico ao termo 974564",
  "coordenadas_cadastrais_em_outro_municipio":"Cajuru",
  "hipotese_local":None,
  "nivel_de_evidencia":"apenas_cadastro_federal_preexistente",
  "endereco_homologado":False,
  "pendencia":"Obter matricula, lei de destinacao, planta aprovada ou termo do municipio que cite expressamente 974564."
 },
 "105865.35-77":{
  "instrumento":"996136","municipio":"Guatapará",
  "objeto":"Provisão de Unidades Habitacionais",
  "resultado_pesquisa_externa":"sem documento oficial municipal que vincule lote ou imovel ao instrumento 996136/2026",
  "coordenadas_cadastrais_em_outros_municipios":["Serra Azul","Cássia dos Coqueiros"],
  "hipotese_local":None,
  "nivel_de_evidencia":"apenas_cadastro_federal_preexistente",
  "endereco_homologado":False,
  "pendencia":"Obter matricula/ato atual de destinacao e plano de trabalho ligado ao termo 996136, sem transferir enderecos de iniciativas habitacionais anteriores."
 }
}
def get(p):return json.loads(p.read_text(encoding="utf-8"))
def put(p,j):p.write_text(json.dumps(j,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
def sha(p):
 h=hashlib.sha256()
 with p.open("rb") as f:
  for b in iter(lambda:f.read(1048576),b""):h.update(b)
 return h.hexdigest()
def build(src,dst,pack):
 if not (src/".rmrp-fed07-private-preview").is_file():raise ValueError("private marker absent")
 if dst.exists():raise ValueError("destination exists")
 shutil.copytree(src,dst)
 api=dst/BASE
 for project,case in CASES.items():
  path=api/"projetos"/(project+".json")
  obj=get(path)
  assert obj["id_origem"]==project
  assert obj["instrumentos_vinculados"][0]["numero"]==case["instrumento"]
  assert obj["valores_investimento_pago_centavos"] is None
  assert obj["localizacao_fisica"]["pontos"]==[]
  obj["pesquisa_documental_fed21"]={
    **case,
    "status_qa":"documento_institucional_sem_vinculo_direto_ou_pesquisa_negativa",
    "local_fisico_executado_homologado":False,
    "public_release_authorized":False
  }
  obj["public_release_authorized"]=False
  put(path,obj)
 manifest=get(api/"manifest.json")
 assert manifest["public_release_authorized"] is False
 manifest["coverage"]["fed21_projetos_restantes_examinados"]=3
 manifest["coverage"]["fed21_projeto_com_contexto_institucional_sem_vinculo_explicito"]=1
 manifest["coverage"]["fed21_projetos_sem_fonte_municipal_especifica"]=2
 manifest["coverage"]["fed21_locais_execucao_homologados"]=0
 manifest["public_release_authorized"]=False
 put(api/"manifest.json",manifest)
 pending=get(api/"pendencias.json")
 pending.setdefault("territorial",[]).append("FED21: ETE Jaboticabal Dr. Adelson Taroco tem local institucional junto Rodovia Carlos Tonani, mas fontes consultadas nao vinculam o contrato 953339 ao local; nao inferir coordenadas.")
 pending["territorial"].append("FED21: termos 974564 Santa Rosa de Viterbo e 996136 Guatapara permanecem sem terrenos municipalmente identificados; coordenadas de proposta caem em outros municipios da RMRP.")
 put(api/"pendencias.json",pending)
 qa=validate(api)
 assert qa["technical_checks_passed"]>=1603
 projects=[get(p) for p in (api/"projetos").glob("*.json")]
 assert len(projects)==218
 assert sum("pesquisa_documental_fed21" in p for p in projects)==3
 assert all(p["valores_investimento_pago_centavos"] is None and p["localizacao_fisica"]["pontos"]==[] for p in projects)
 report={
  "version":"FED21","priority_cases_covered_by_search":19,
  "prior_independent_documents_fed16_fed20":16,
  "new_independent_contract_specific_linkages":0,
  "contextual_institutional_source_not_same_as_project_proof":1,
  "negative_search_results":2,"execution_points_approved":0,
  "GND4_paid_approved":0,"api_technical_checks":qa["technical_checks_passed"],
  "public_release_authorized":False,
  "notes":["19/19 received targeted review, but only 16/19 have independent documentary evidence connected at instrument level.",
           "ETE location source identifies institutional facility, not exact reform site or contract 953339.",
           "Neither housing project may inherit coordinates or land parcels from older programs."]
 }
 put(dst/"QA_FED21_FONTES_E_PENDENCIAS_PRIVADO.json",report)
 with zipfile.ZipFile(pack,"w",zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for f in dst.rglob("*"):
   if f.is_file() and f.name!=".rmrp-fed07-private-preview":z.write(f,f.relative_to(dst))
 with zipfile.ZipFile(pack) as z:assert z.testzip() is None
 report["zip_bytes"]=pack.stat().st_size;report["zip_sha256"]=sha(pack)
 return report
if __name__=="__main__":
 ap=argparse.ArgumentParser()
 for x in ("source","output","archive"):ap.add_argument(x,type=Path)
 v=ap.parse_args();print(json.dumps(build(v.source,v.output,v.archive),ensure_ascii=False))
