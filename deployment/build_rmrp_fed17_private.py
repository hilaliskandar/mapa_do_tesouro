#!/usr/bin/env python3
"""FED17 — incorporar evidências de contrato, adjudicação e andamento sem promover
despesa paga ou coordenadas de execução física.
Fontes externas devem ser conferidas por URL e documento antes de rerun.
"""
from pathlib import Path
import hashlib, json, shutil, zipfile

PREFIX=Path("data/api/v3/investimentos/rmrp")
SOURCES={
 "contrato_monte_alto":"https://montealto.sp.gov.br/site/wp-content/uploads/2020/06/contr_123-K-G-Construtora-Garcia-Ltda.pdf",
 "ata_comtur_2023":"https://montealto.sp.gov.br/site/wp-content/uploads/2023/04/Ata-da-Segunda-Reuniao-11-de-abril-de-2023.pdf",
 "doesp_tp001_2017":"https://suzano.sp.gov.br/wp-content/uploads/2017/04/Unificado-Chamada-03_17_2.pdf",
 "noticia_sertaozinho_2017":"https://www.sertaozinho.sp.gov.br/portal/noticias/0/3/3145/prefeitura-investe-em-infraestrutura-esportiva-em-diferentes-regioes-da-cidade",
 "inauguracao_monte_alto_2020":"https://montealto.sp.gov.br/site/centro-de-economia-criativa-e-oficialmente-inaugurado-na-praca-sao-benedito/",
}
DATA={
 "33889.35-28":{
    "municipio":"Monte Alto","instrumento":"870332","operacao":"1058625-14",
    "contrato_administrativo":"123/2020",
    "procedimento_licitatorio":"TP 10/2020; SA/DL 48/2020",
    "parte_objeto":"reforma de edificação para implantação do Centro de Apoio ao Turista",
    "valor_global_contrato_centavos":32081272,
    "valor_pago_comprovado_centavos":None,
    "classificacao_orcamentaria_do_contrato":["44.90.51"],
    "ateste_de_medicao_no_contrato":"exigido; medições efetivas não recuperadas nesta fonte",
    "origem_pagamento":"recursos próprios e federais previstos, sem demonstrar parcelas pagas",
    "fonte_contrato":SOURCES["contrato_monte_alto"],
    "fonte_contrato_paginas_relevantes":[1,2,3,5],
    "relato_de_progresso":{
       "fonte":SOURCES["ata_comtur_2023"],
       "data":"2023-04-11",
       "texto_sintese":"Ata menciona obras federais da Praça São Benedito e Casa do Turismo, junto a outros projetos, com referência aproximada a 68%; não há base inequívoca para atribuir esse percentual exclusivamente ao contrato 870332.",
       "percentual_atribuivel_ao_projeto":None,
       "status":"referencia_contextual_ambigua"
    },
    "alerta_outro_empreendimento":{
       "fonte":SOURCES["inauguracao_monte_alto_2020"],
       "evento":"Inauguração do Centro de Economia Criativa na Praça São Benedito em 20/12/2020",
       "regra":"não equiparar automaticamente à execução dos componentes da reforma 870332 sem cadeia documental adicional"
    },
    "status_contratual":"contrato_individual_licitado_e_vinculado_expressamente_ao_repasse",
    "status_execucao_fisica_documental":"sem_medicoes_ou_termo_de_recebimento_individual_recuperados",
    "local_execucao_homologado":False
 },
 "125271.35-26":{
    "municipio":"Sertãozinho","instrumento":"839481",
    "procedimento_licitatorio":"Tomada de Preços 001/2017",
    "objeto_adjudicado":"Cobertura e arquibancada da quadra poliesportiva da Praça Franco Montoro no Conjunto Habitacional Antônio Pedro Ortolan",
    "empresa_adjudicataria":"LAMG Serviços e Construções Ltda. EPP",
    "data_homologacao_publicada":"2017-04-01",
    "fonte_adjudicacao":SOURCES["doesp_tp001_2017"],
    "fonte_noticia_execucao":SOURCES["noticia_sertaozinho_2017"],
    "valor_noticiado_obra_centavos":38638777,
    "valor_federal_pago_comprovado_centavos":None,
    "vinculo_explicito_ao_repasse_na_fonte_licitatoria":False,
    "observacao":"A adjudicação e a notícia corroboram obra/município/contratada; nenhuma dessas peças cita o repasse 839481.",
    "status_contratual":"objeto_adjudicado_a_empresa_identificada",
    "status_execucao_fisica_documental":"relato_municipal_de_obra_em_execucao",
    "local_execucao_homologado":False
 },
 "31534.35-57":{
    "municipio":"Ribeirão Preto","instrumento":"953325",
    "fonte_staging":"FED08C / Transferegov SICONV",
    "execucao_fisica_percentual_cadastral":"100,00",
    "resumo_fisico_financeiro_percentual_cadastral":"100,00",
    "linhas_medicao":1,
    "medicoes_com_situacao_aceita":0,
    "alerta":"Percentuais cadastrais de execução não comprovam local da obra nem natureza GND4 efetivamente paga.",
    "status_execucao_fisica_documental":"percentual_cadastral_nao_atesta_local",
    "local_execucao_homologado":False
 }
}
def load(p):return json.loads(p.read_text(encoding="utf-8"))
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
def sha(p):
 h=hashlib.sha256()
 with p.open("rb") as f:
  for block in iter(lambda:f.read(1048576),b""):h.update(block)
 return h.hexdigest()
def build(src,dst,zipout):
 if dst.exists():raise RuntimeError("Output already exists")
 if not (src/".rmrp-fed07-private-preview").is_file():raise RuntimeError("Not a private preview")
 shutil.copytree(src,dst)
 api=dst/PREFIX
 for project,record in DATA.items():
  p=api/"projetos"/(project+".json")
  j=load(p)
  assert j["id_origem"]==project
  assert j["instrumentos_vinculados"][0]["nr_instrumento"]==record["instrumento"]
  assert j["valores_investimento_pago_centavos"] is None
  assert j["localizacao_fisica"]["pontos"]==[]
  j["evidencia_contratual_fed17"]={**record,
     "fonte_tipo":"documentos_municipais_oficiais_e_estagio_siconv",
     "qa_status":"corroboracao_contratual_sem_homologacao_execucao_ou_pago",
     "public_release_authorized":False}
  j["public_release_authorized"]=False
  write(p,j)
 manifest=load(api/"manifest.json")
 assert manifest["public_release_authorized"] is False
 manifest["coverage"]["projetos_com_fontes_contratuais_fed17"]=3
 manifest["coverage"]["contrato_administrativo_com_vinculo_expresso_ao_repasse"]=1
 manifest["coverage"]["adjudicacao_obra_sem_referencia_direta_repasse"]=1
 manifest["coverage"]["execucao_fisica_homologada_pelo_fed17"]=0
 manifest["coverage"]["capital_pago_homologado_fed17"]=0
 write(api/"manifest.json",manifest)
 pend=load(api/"pendencias.json")
 pend.setdefault("territorial",[]).append(
 "FED17: contrato 123/2020 de Monte Alto vincula expressamente repasse 870332/2018 ao CAT; 68% em ata COMTUR 2023 tem antecedente plural ambíguo e não pode ser atribuído isoladamente a essa obra.")
 pend["territorial"].append(
 "FED17: Sertãozinho TP 001/2017 confirma adjudicação para quadra Franco Montoro à LAMG, mas não identifica o repasse federal 839481 nas peças recuperadas.")
 write(api/"pendencias.json",pend)
 from pipeline.qa.validate_rmrp_api_v3_fed07 import validate
 qa=validate(api)
 assert qa["technical_checks_passed"]>=1603 and qa["public_release_authorized"] is False
 allprojects=[load(p) for p in (api/"projetos").glob("*.json")]
 assert len(allprojects)==218
 assert sum("evidencia_contratual_fed17" in p for p in allprojects)==3
 assert all(not p["localizacao_fisica"]["pontos"] and p["valores_investimento_pago_centavos"] is None for p in allprojects)
 report={
 "snapshot":"2026-11-15","audit_date":"2026-11-16",
 "projects_enriched":3,"contract_document_explicit_870332":True,
 "contract_value_monte_alto_centavos":32081272,
 "publicly_attributable_project_68_percent":False,
 "sertaozinho_tender_adjudicated":True,
 "sertaozinho_federal_instrument_explicitly_in_tender":False,
 "hemocentro_staging_100pct_not_local_proof":True,
 "new_execution_points":0,"new_GND4_paid_amounts":0,
 "qa":qa,"public_release_authorized":False,
 "primary_source_urls":SOURCES}
 write(dst/"QA_FED17_CONTRATOS_PRIVADO.json",report)
 with zipfile.ZipFile(zipout,"w",zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for p in dst.rglob("*"):
   if p.is_file() and p.name!=".rmrp-fed07-private-preview":z.write(p,p.relative_to(dst))
 with zipfile.ZipFile(zipout) as z:assert z.testzip() is None
 report["archive_bytes"]=zipout.stat().st_size
 report["archive_sha256"]=sha(zipout)
 return report
if __name__=="__main__":
 import argparse
 a=argparse.ArgumentParser()
 for n in ("src","dst","zipout"):a.add_argument(n,type=Path)
 q=a.parse_args()
 print(json.dumps(build(q.src,q.dst,q.zipout),ensure_ascii=False))
