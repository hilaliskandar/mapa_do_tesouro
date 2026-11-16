#!/usr/bin/env python3
"""FED20: official public land law and federal repasse/commitment amendments.
All material stays private QA; no execution geocoding or paid GND4.
"""
import argparse,hashlib,json,shutil,zipfile
from pathlib import Path
from pipeline.qa.validate_rmrp_api_v3_fed07 import validate

BASE=Path("data/api/v3/investimentos/rmrp")
SOURCES={
 "dumont_lei_2000":"https://www.dumont.sp.gov.br/portal/leis_decretos/6185/",
 "barrinha_dou_953046":"https://pastosbons.ma.gov.br/anexos-bkp/convenios/952783/952783_6_dou_26_12_2023.pdf",
 "jaboticabal_dou_969302":"https://pesquisa.in.gov.br/imprensa/servlet/INPDFViewer?captchafield=firstAccess&data=10%2F10%2F2025&jornal=530&pagina=79",
 "cravinhos_dou_939534":"https://www.chapadinha.ma.gov.br/anexos-bkp/convenios/880707/880707_chapadinha_dou_ta_de_contrapartida.pdf"
}
CASES={
 "113452.35-68":{
  "instrumento":"992467","municipio":"Dumont",
  "objeto":"unidades_habitacionais",
  "imovel_legalmente_destinado":{
   "fundamento":"Lei Municipal 2000 de 10/04/2026",
   "tipo_atual":"bem_dominial_municipal_destinado_a_habitacao",
   "identificacao":"Area Institucional 01 no loteamento Reserva do Alto",
   "area_m2_literal":"5706,61",
   "matricula":"88.873","registro":"Oficial de Registro de Imoveis da Comarca de Sertaozinho",
   "confrontacoes":"frente Rua 08, lado impar, com referencias a Ruas 07 e 02",
   "coordenadas_geograficas":None,
   "geometria_de_poligono":None,
   "status":"area_de_destinacao_legal_documentada_nao_imovel_com_execucao_fisica_comprovada",
   "fonte":SOURCES["dumont_lei_2000"]},
  "execucao_de_unidades_habitacionais_comprovada":False,
  "pendencia":"obter planta/matricula georreferenciada, licenciamento/medicoes e comprovar inicio/execucao"
 },
 "30843.35-03":{
  "instrumento":"953046","municipio":"Barrinha","objeto":"implantacao_de_calcadas",
  "contrato_de_repasse_publicado":{
   "ano":"2023","valor_global_assinatura_centavos":50000000,
   "repasse_federal_assinatura_centavos":48110400,
   "contrapartida_assinatura_centavos":1889600,
   "programa":"Mobilidade Urbana / Ministerio das Cidades",
   "fonte":"Reproducao PDF de secao 3 do Diario Oficial da Uniao em sitio de municipio, 26/12/2023",
   "url":SOURCES["barrinha_dou_953046"]},
  "trechos_calcadas_individualizados":False,
  "status":"contrato_financiamento_comprovado_sem_trechos_de_execucao",
  "pagamento_final_comprovado":False
 },
 "46797.35-41":{
  "instrumento":"969302","municipio":"Jaboticabal","objeto":"construcao_de_novos_DAFAs",
  "termo_aditivo":{
   "documento":"DOU 10/10/2025 secao 3 pagina 79",
   "data_aditivo":"2025-10-07",
   "descricao_oficial":"Altera repasse e contrapartida: R$ 1.013.465,89 e R$ 0,00",
   "valor_repasse_constante_do_extrato_centavos":101346589,
   "contrapartida_constante_do_extrato_centavos":0,
   "fonte":SOURCES["jaboticabal_dou_969302"]},
  "atenção":"valor de termo aditivo nao se soma automaticamente aos valores anteriores e nao comprova transferencia ou pagamento.",
  "local_DAFA_obra_identificado":False,
  "execucao_fisica_comprovada":False
 },
 "19211.35-11":{
  "instrumento":"939534","municipio":"Cravinhos","objeto":"pavimentacao_asfaltica",
  "termo_aditivo":{
   "documento":"DOU 21/08/2023 secao 3",
   "data_aditivo":"2023-08-18",
   "descricao":"Altera contrapartida: R$ 141.016,62",
   "valor_contrapartida_indicado_centavos":14101662,
   "fonte":SOURCES["cravinhos_dou_939534"]},
  "trechos_identificados":False,
  "pagamento_final_comprovado":False,
  "status":"aditivo_de_contrapartida_registrado_sem_prova_de_execucao_viaria"
 }
}
def get(p):return json.loads(p.read_text(encoding="utf-8"))
def put(p,j):p.write_text(json.dumps(j,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
def sha(p):
 h=hashlib.sha256()
 with p.open("rb") as f:
  for b in iter(lambda:f.read(1048576),b""):h.update(b)
 return h.hexdigest()
def build(old,new,outzip):
 if not (old/".rmrp-fed07-private-preview").is_file():raise RuntimeError("private marker absent")
 if new.exists():raise RuntimeError("refuse overwrite")
 shutil.copytree(old,new)
 api=new/BASE
 for proj,item in CASES.items():
  f=api/"projetos"/(proj+".json");doc=get(f)
  assert doc["id_origem"]==proj and doc["instrumentos_vinculados"][0]["numero"]==item["instrumento"]
  assert not doc["localizacao_fisica"]["pontos"] and doc["valores_investimento_pago_centavos"] is None
  doc["evidencia_fundiaria_e_aditivos_fed20"]={**item,
     "status_qa":"documentacao_normativa_ou_financeira_sem_prova_de_execucao_fisica",
     "public_release_authorized":False}
  doc["public_release_authorized"]=False
  put(f,doc)
 manifest=get(api/"manifest.json")
 manifest["coverage"]["fed20_projetos_com_evidencias_adicionais"]=4
 manifest["coverage"]["fed20_areas_fundiarias_identificadas_sem_geometria"]=1
 manifest["coverage"]["fed20_com_repasses_e_aditivos_orcamentarios"]=3
 manifest["coverage"]["fed20_locais_de_execucao_homologados"]=0
 manifest["public_release_authorized"]=False
 put(api/"manifest.json",manifest)
 p=api/"pendencias.json";pending=get(p)
 pending.setdefault("territorial",[]).append("FED20: Dumont lei 2000/2026 destina Area Institucional 01, Reserva do Alto, matricula 88.873, 5706,61m2 ao termo 992467/2025, mas necessita poligono georreferenciado e prova de construcao.")
 pending["territorial"].append("FED20: Calçadas Barrinha e pavimentacao Cravinhos seguem sem trechos lineares; DAFA Jaboticabal carece endereco exato, plantas e execucao.")
 pending.setdefault("financeiro",[]).append("FED20: repasse inicial, contrapartida e aditivos de contratos 953046, 969302, 939534 nao sao valores GND4 pagos ou somaveis sem controle de vigencia.")
 put(p,pending)
 qa=validate(api)
 assert qa["technical_checks_passed"]>=1603
 projects=[get(p) for p in (api/"projetos").glob("*.json")]
 assert len(projects)==218
 assert sum("evidencia_fundiaria_e_aditivos_fed20" in p for p in projects)==4
 assert all(not p["localizacao_fisica"]["pontos"] and p["valores_investimento_pago_centavos"] is None for p in projects)
 summary={"version":"FED20","projects_new":4,"total_priority_projects_with_independent_evidence":16,
          "pending_priority_projects":3,"land_identified_without_polygon":1,
          "new_execution_points":0,"new_paid_capital_values":0,
          "technical_checks":qa["technical_checks_passed"],
          "public_release_authorized":False,"source_urls":SOURCES}
 put(new/"QA_FED20_PRIVADO.json",summary)
 with zipfile.ZipFile(outzip,"w",zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for f in new.rglob("*"):
   if f.is_file() and f.name!=".rmrp-fed07-private-preview":z.write(f,f.relative_to(new))
 with zipfile.ZipFile(outzip) as z:assert z.testzip() is None
 summary["bytes"]=outzip.stat().st_size;summary["sha256"]=sha(outzip)
 return summary
if __name__=="__main__":
 a=argparse.ArgumentParser()
 for n in ("previous","output","archive"):a.add_argument(n,type=Path)
 v=a.parse_args();print(json.dumps(build(v.previous,v.output,v.archive),ensure_ascii=False))
