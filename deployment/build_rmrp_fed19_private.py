#!/usr/bin/env python3
"""FED19 private-only project evidence overlay for five RMRP projects.

Sources: signed municipal bid, state/federal official gazette reproductions
and institutional transparency. Documents establish advertised location,
contract and procurement status; never the executed geometry or GND4 paid.
"""
import argparse,hashlib,json,shutil,zipfile
from pathlib import Path
from pipeline.qa.validate_rmrp_api_v3_fed07 import validate

PREFIX=Path("data/api/v3/investimentos/rmrp")
SOURCES={
 "monte_alto_mercado":"https://montealto.sp.gov.br/site/wp-content/uploads/2025/07/EDITAL-OBRA-DE-REFORMA-E-ADEQUACAO-MERCADO-MUNICIPAL.pdf",
 "barrinha_tp16":"https://www.escavador.com/diarios/5596121/DOU/secao-3/2022-12-09?page=271",
 "barrinha_rescisao":"https://www.escavador.com/diarios/5611006/DOESP/executivo-i/2023-01-28?page=336",
 "cravinhos_943601":"https://www.escavador.com/diarios/5784757/DOU/secao-3/2023-08-31?page=119",
 "cravinhos_pts_licitacao":"https://www.escavador.com/diarios/6179578/DOU/secao-3/2025-12-08?page=226",
 "cravinhos_pts_parecer":"https://www.escavador.com/diarios/6248203/DOESP/municipios/2026-04-08?page=9"
}
CASES={
 "27237.35-06":{
  "instrumento":"946417","tipo_objeto":"edificacao_pontual","municipio":"Monte Alto",
  "local_previsto":{
   "logradouro":"Rua Florindo Cestari","numero":"861","bairro":"Centro",
   "municipio":"Monte Alto","uf":"SP","coordenada_geografica":None,
   "origem":"Anexo II termo de referencia, Concorrencia Eletronica 99026/2025",
   "status":"endereco_de_objeto_previsto_em_edital,nao_execucao_fisica_georreferenciada"},
  "vinculo":"Contrato de Repasse 946417/2023 MAP/CAIXA explicitamente identificado no edital municipal 109/2025",
  "fonte":SOURCES["monte_alto_mercado"],
  "situacao_execucao_comprovada":False,
  "situacao_pagamento_comprovada":False,
  "alerta":"Edital inclui dotacao 4.4.90.51, que e planejamento orcamentario, nao prova de pagamento de capital."
 },
 "23598.35-24":{
  "instrumento":"916578","tipo_objeto":"rede_de_trechos_viarios","municipio":"Barrinha",
  "lote_licitacao":"Lote 02, Tomada de Precos 016/2022, processo 067/2022",
  "contrato_administrativo_rescindido":"067/B/2022",
  "contratada_no_contrato_rescindido":"NECA Engenharia e Construcoes EIRELI",
  "status_do_ato":"rescisao_amigavel_do_contrato_especifico",
  "fundamento_transcrito":"Art. 79, inciso II, Lei 8666/1993",
  "fonte_licitacao":SOURCES["barrinha_tp16"],
  "fonte_rescisao":SOURCES["barrinha_rescisao"],
  "localizacao":"trechos_viarios_nao_individualizados",
  "situacao_convenio_nao_inferida_da_rescisao":True,
  "execucao_fisica_homologada":False
 },
 "9118.35-82":{
  "instrumento":"917013","tipo_objeto":"rede_de_trechos_viarios","municipio":"Barrinha",
  "lote_licitacao":"Lote 01, Tomada de Precos 016/2022, processo 067/2022",
  "fonte":SOURCES["barrinha_tp16"],
  "rescisao_contrato_067B_aplicavel":False,
  "nota":"A rescisao publicada refere-se apenas ao lote 02 do repasse 916578, e nao se aplica automaticamente ao lote 01 de 917013.",
  "localizacao":"trechos_viarios_nao_individualizados",
  "execucao_fisica_homologada":False
 },
 "46389.35-04":{
  "instrumento":"974453","tipo_objeto":"habitação","municipio":"Cravinhos",
  "local_descritivo_previsto":"Loteamento Buenopolis I",
  "processo_acessorio":"Pregao Eletronico 071/2025, Projeto de Trabalho Social (PTS)",
  "aviso_licitacao":SOURCES["cravinhos_pts_licitacao"],
  "parecer_juridico":SOURCES["cravinhos_pts_parecer"],
  "situacao_documentada":"parecer_juridico_de_07_04_2026_opina_pela_anulacao_licitacao_PTS_e_contrato_de_30_12_2025",
  "ato_decisorio_final_de_anulacao_recuperado":False,
  "cancelamento_do_empreendimento_habitacional_comprovado":False,
  "status_execucao_habitacao_comprovado":False,
  "alerta":"O PTS e contratacao acessoria; parecer de anulacao nao equivale a ato final nem a cancelamento das moradias."
 },
 "25012.35-95":{
  "instrumento":"943601","tipo_objeto":"rede_de_trechos_viarios","municipio":"Cravinhos",
  "fonte_extrato_dou":SOURCES["cravinhos_943601"],
  "valor_global_contratado_centavos":24363312,
  "repasse_federal_previsto_centavos":23885600,
  "contrapartida_prevista_centavos":477712,
  "programa":"Mobilidade Urbana / Ministerio das Cidades",
  "natureza":"valores_de_assinatura_do_instrumento,nao_pagamentos",
  "trechos_viarios_individualizados":False,
  "executado_e_pago_comprovado":False,
  "alerta":"Extrato federal identifica o objeto e valores do contrato, mas nao as vias efetivamente executadas."
 }
}

def get(p):return json.loads(p.read_text(encoding="utf-8"))
def put(p,obj):p.write_text(json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
def sha(p):
 h=hashlib.sha256()
 with open(p,"rb") as f:
  for b in iter(lambda:f.read(1048576),b""):h.update(b)
 return h.hexdigest()
def run(src,dest,outzip):
 if not (src/".rmrp-fed07-private-preview").is_file():raise RuntimeError("Private marker required")
 if dest.exists():raise RuntimeError("Destination exists")
 shutil.copytree(src,dest)
 api=dest/PREFIX
 for id,item in CASES.items():
  p=api/"projetos"/(id+".json")
  assert p.is_file(),id
  doc=get(p)
  assert doc["id_origem"]==id
  assert doc["instrumentos_vinculados"][0]["numero"]==item["instrumento"]
  assert doc["valores_investimento_pago_centavos"] is None
  assert not doc["localizacao_fisica"]["pontos"]
  doc["evidencia_documental_fed19"]={**item,
     "qa_status":"vinculo_documental_identificado_sem_obra_executada_georreferenciada",
     "public_release_authorized":False}
  doc["public_release_authorized"]=False
  put(p,doc)
 manifest=get(api/"manifest.json")
 assert manifest["public_release_authorized"] is False
 manifest["coverage"]["fed19_projetos_com_nova_evidencia"]=5
 manifest["coverage"]["fed19_endereco_previsto_sem_coordenada_georreferenciada"]=1
 manifest["coverage"]["fed19_projetos_viarios_adicionais"]=3
 manifest["coverage"]["fed19_parecer_anulacao_pts_sem_prova_cancelamento_habitacional"]=1
 manifest["coverage"]["fed19_locais_fisicos_homologados"]=0
 manifest["public_release_authorized"]=False
 put(api/"manifest.json",manifest)
 pending=get(api/"pendencias.json")
 pending.setdefault("territorial",[]).append("FED19: Mercado Municipal Monte Alto tem endereço de projeto Rua Florindo Cestari 861, sem coordenada de execução; Barrinha lotes 1 e 2 devem ser separados, com rescisão contratual restrita ao lote 2; Cravinhos tem PTS com parecer jurídico de anulação, não prova de cancelamento habitacional.")
 pending.setdefault("financeiro",[]).append("FED19: 243.633,12 do extrato 943601 e dotação 4.4.90.51 do Mercado Municipal são contratos/orçamento, nunca GND4 pago.")
 put(api/"pendencias.json",pending)
 qa=validate(api)
 assert qa["technical_checks_passed"]>=1603
 docs=[get(p) for p in (api/"projetos").glob("*.json")]
 assert len(docs)==218 and sum("evidencia_documental_fed19" in x for x in docs)==5
 assert all(x["valores_investimento_pago_centavos"] is None and x["localizacao_fisica"]["pontos"]==[] for x in docs)
 result={"version":"FED19","projects_updated":5,"project_docs_total":218,
         "new_verified_physical_execution_points":0,
         "new_paid_capital_amounts":0,"api_checks":qa["technical_checks_passed"],
         "public_release_authorized":False,"source_urls":SOURCES,
         "warnings":["Barrinha amicable rescission applies only to a contract of Lote 02.",
                     "Cravinhos published legal opinion does not prove a final annulment decision or cancellation of housing project.",
                     "Monte Alto street address is planned works location, not geocoded execution.",
                     "Cadastral stages and contracted values do not establish paid GND4."]}
 put(dest/"QA_FED19_EVIDENCIAS_PRIVADO.json",result)
 with zipfile.ZipFile(outzip,"w",zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for p in dest.rglob("*"):
   if p.is_file() and p.name!=".rmrp-fed07-private-preview":z.write(p,p.relative_to(dest))
 with zipfile.ZipFile(outzip) as z:assert z.testzip() is None
 result["zip_bytes"]=outzip.stat().st_size
 result["zip_sha256"]=sha(outzip)
 return result
if __name__=="__main__":
 p=argparse.ArgumentParser()
 for k in ("source","destination","archive"):p.add_argument(k,type=Path)
 a=p.parse_args()
 print(json.dumps(run(a.source,a.destination,a.archive),ensure_ascii=False))
