#!/usr/bin/env python3
"""FED18 - evidence provenance for one Guariba school and three Luiz Antonio road projects.

No inference of executed-point coordinates, street-segment polylines,
paid-to-vendor GND4, or reconciled federal expenditure.
"""
import argparse,hashlib,json,shutil,zipfile
from pathlib import Path
from pipeline.qa.validate_rmrp_api_v3_fed07 import validate
PREFIX=Path("data/api/v3/investimentos/rmrp")
SOURCES={
 "guariba_transparencia":"https://www.guariba.sp.gov.br/portal-da-transparencia/convenios/termo-de-compromisso-9590972024",
 "guariba_licitacao":"https://www.guariba.sp.gov.br/portal-da-transparencia/licitacao/editais/concorrencia-publica/0012025-concorrencia-publica-aberto",
 "guariba_obras_contrato":"https://www.guariba.sp.gov.br/portal-da-transparencia/obras/contratos-de-obras-firmados",
 "guariba_noticia_2025":"https://www.guariba.sp.gov.br/noticias/educacao/guariba-segue-avancando-na-educacao",
 "guariba_noticia_2026":"https://guariba.sp.gov.br/noticias/geral/prefeito-cumpre-agenda-em-brasilia-em-busca-de-novos-recursos-para-guariba",
 "luiz_947994":"https://luizantonio.sp.gov.br/licitacoes/documentos/20240618095938Edital%20Completo%20e%20Anexos.pdf",
 "luiz_952718_2024":"https://luizantonio.sp.gov.br/licitacoes/documentos/20240426191224EDITAL%20COMPLETO%20E%20ANEXOS.pdf",
 "luiz_952718_2025":"https://luizantonio.sp.gov.br/licitacoes/documentos/20250428132846Edital%20Completo.pdf",
 "luiz_911090":"https://luizantonio.sp.gov.br/licitacoes/documentos/20220816101942Edital%20Completo%20e%20Anexos%20-%20TP%20012-2022.pdf",
 "retificacao_dou_952718":"https://www.escavador.com/diarios/5880838/DOU/secao-3/2024-05-13?page=293",
}
ROADS_2025=[
"Avenida Primavera","Rua das Camélias","Rua das Tulipas","Rua das Hortênsias",
"Rua dos Lírios","Rua das Adálias","Rua das Palmas","Rua das Violetas",
"Rua das Orquídeas","Rua das Margaridas","Rua dos Antúrios","Rua Alagoas",
"Rua Alfredo Cordeiro","Rua José Rosatti","Rua Serrana","Rua Ribeirão Preto",
"Rua Cravinhos","Rua José Carneiro de Mesquita","Rua Eleutério Turazzi",
"Rua Expedicionários Paulistas"]
ROADS_2024=[
"Avenida da Saudade","Rua Rio de Janeiro","Rua Santa Rita do Passa Quatro",
"Rua das Palmas","Rua dos Lírios","Rua das Rosas","Rua dos Gerâneos",
"Rua das Azaléas","Rua dos Cravos","Rua das Camélias","Rua dos Girassóis",
"Rua dos Jasmins","Rua Expedicionários Paulistas","Rua Guilherme Brayn",
"Rua Manoel Francisco","Rua Salvador Gomes","Rua Sergipe",
"Rua Rio Grande do Sul","Rua São Paulo","Rua Amazonas"]
CASES={
 "37841.35-64":{
  "instrumento":"959097","municipio_proponente":"Guariba",
  "tipo_objeto":"edificacao_pontual",
  "local_documental":{
   "logradouro":"Rua Geraldo Gonçalves Santana","numero":"300",
   "bairro":"Residencial Luiz Carlos Santin","municipio":"Guariba","uf":"SP",
   "status":"endereco_previsto_no_projeto_e_localidade_de_obra_corrobora_inicio",
   "fonte":SOURCES["guariba_licitacao"],"coordenada_exata":None,
   "latitude":None,"longitude":None},
  "vinculo_documental":{
   "termo_compromisso":"959097/2024",
   "contrato_administrativo":"043/2025",
   "procedimento":"Concorrência Pública 001/2025",
   "fonte":SOURCES["guariba_obras_contrato"],
   "nota_inconsistencia":"Cabeçalho da página de transparência menciona convênio 953042/2024 apesar de identificar o termo 959097/2024; manter ambas referências separadas para conferência."},
  "execucao_corroborada":{
   "data_fonte_inicial":"2025-11-04","situacao":"terraplanagem concluida e construcao em andamento segundo a Prefeitura",
   "fonte":SOURCES["guariba_noticia_2025"],
   "fonte_2026":SOURCES["guariba_noticia_2026"],
   "atualizacao_2026":"Prefeitura informa solicitação de pagamento de medição pendente e liberação para etapa seguinte; não prova pagamento realizado.",
   "pode_afirmar_obra_iniciada":True,
   "pode_afirmar_pagamento_municipal_efetivo":False},
  "valor_repassado_ate_2026_04_24_centavos":234080005,
  "estagio_do_valor":"repassado_ao_convenente_conforme_portal_municipal_na_data_de_corte_nao_adiitvo_a_OUTROS_ESTAGIOS",
  "valor_investimento_pago_fornecedor_homologado_centavos":None,
  "fonte_valor":SOURCES["guariba_transparencia"],
  "classificacao_homologavel":"endereco_do_terreno_e_inicio_reportado_em_fontes_municipais;sem_ponto_exato"
 },
 "27422.35-03":{
  "instrumento":"947994","municipio_proponente":"Luiz Antônio",
  "tipo_objeto":"rede_de_trechos_viarios",
  "logradouro_previsto":["Rua Alexandre Belchior","Avenida Silvino Ferreira de Castro"],
  "origem":"Concorrência Eletrônica 006/2024 / Contrato de Repasse 947994/2023, Ministério das Cidades",
  "fonte":SOURCES["luiz_947994"],
  "cadastral_vs_executado":"Vias previstas em edital; sem confirmação independente de trechos executados",
  "geometria_necessaria":"lineares_com_inicio_e_fim_de_trecho",
  "pin_de_execucao_homologado":False
 },
 "29085.35-21":{
  "instrumento":"952718","municipio_proponente":"Luiz Antônio",
  "tipo_objeto":"rede_de_trechos_viarios",
  "logradouro_previsto_edital_2024":ROADS_2024,
  "logradouro_previsto_reprogramacao_2025":ROADS_2025,
  "origem":"Concorrência Eletrônica 004/2024 e reprogramação pela Concorrência Eletrônica 003/2025; Contrato de Repasse federal 952718/2023/MCIDADES/CAIXA",
  "fonte_edital_2024":SOURCES["luiz_952718_2024"],
  "fonte_reprogramacao_2025":SOURCES["luiz_952718_2025"],
  "fonte_retificacao_origem_recurso":SOURCES["retificacao_dou_952718"],
  "correcao_origem":"Edital 004/2024 inicialmente mencionou recursos estaduais; DOU de 13/05/2024 retificou para contrato federal 952718/2023.",
  "valor_orcado_reprogramacao_2025_centavos":145740869,
  "valor_orcado_nao_pago":True,
  "atencao":"Nova lista 2025 não é prova de execução nem autoriza substituir todas as fases precedentes sem documentação de reprogramação.",
  "geometria_necessaria":"trechos_viarios_versionados_por_edital_e_reprogramacao",
  "pin_de_execucao_homologado":False
 },
 "33536.35-28":{
  "instrumento":"911090","municipio_proponente":"Luiz Antônio",
  "tipo_objeto":"rede_de_trechos_viarios",
  "origem":"Tomada de Preços 012/2022, proposta SICONV 27505/2021, Operação 1076713-96, Contrato de Repasse federal 911090/2021/MDR/CAIXA",
  "fonte":SOURCES["luiz_911090"],
  "logradouros_individuais_validados":[],
  "atencao":"Objeto de recapeamento confirmado; sem discriminação de trechos no recorte auditado.",
  "geometria_necessaria":"trechos_viarios_documentados_sem_ponto_unico",
  "pin_de_execucao_homologado":False
 }
}
def load(p):return json.loads(p.read_text(encoding="utf-8"))
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
def sha(p):
 h=hashlib.sha256()
 with p.open("rb") as f:
  for x in iter(lambda:f.read(1048576),b""):h.update(x)
 return h.hexdigest()
def build(src,dest,pack):
 if not (src/".rmrp-fed07-private-preview").is_file():raise RuntimeError("Not a private source")
 if dest.exists():raise RuntimeError("Output exists")
 shutil.copytree(src,dest)
 api=dest/PREFIX
 assert len(ROADS_2025)==20 and len(ROADS_2024)==20
 for project,data in CASES.items():
  p=api/"projetos"/(project+".json")
  assert p.is_file()
  j=load(p)
  assert j["id_origem"]==project
  assert j["instrumentos_vinculados"][0]["numero"]==data["instrumento"]
  assert j["valores_investimento_pago_centavos"] is None and not j["localizacao_fisica"]["pontos"]
  j["evidencia_endereco_trechos_fed18"]={**data,
   "status_qa":"endereco_ou_trechos_documentados_sem_coordenadas_executadas",
   "valor_gnd4_pago_comprovado":False,
   "localizacao_executada_georreferenciada_homologada":False,
   "public_release_authorized":False}
  j["public_release_authorized"]=False
  write(p,j)
 manifest=load(api/"manifest.json")
 manifest["coverage"]["fed18_projetos_com_evidencia_endereco_ou_trecho"]=4
 manifest["coverage"]["fed18_equipamento_com_endereco_e_inicio_reportado"]=1
 manifest["coverage"]["fed18_projetos_viarios_sem_trechos_georreferenciados"]=3
 manifest["coverage"]["fed18_geometrias_execucao_homologadas"]=0
 manifest["public_release_authorized"]=False
 write(api/"manifest.json",manifest)
 pend=load(api/"pendencias.json")
 pend.setdefault("territorial",[]).append("FED18: escola 959097 Guariba tem endereço de terreno e notícia de início e terraplanagem; permanece SEM coordenada física exata georreferenciada e sem pagamentos comprovados à construtora.")
 pend["territorial"].append("FED18: 3 contratos de recapeamento em Luiz Antônio precisam de geometrias LINEARES/trechos, não pontos cadastrais. 952718 possui relação distinta de vias no edital 2024 e reprogramação 2025.")
 pend.setdefault("financeiro",[]).append("FED18: Guariba informa valor transferido ao convenente até 24/04/2026, não comprovante de GND4 pago; cabeçalho de transparência contém convênio 953042, distinto do termo 959097, exigir conferência.")
 write(api/"pendencias.json",pend)
 qa=validate(api)
 assert qa["technical_checks_passed"]>=1603
 arr=[load(x) for x in (api/"projetos").glob("*.json")]
 assert len(arr)==218
 assert sum("evidencia_endereco_trechos_fed18" in j for j in arr)==4
 assert all(j["valores_investimento_pago_centavos"] is None and not j["localizacao_fisica"]["pontos"] for j in arr)
 report={"version":"FED18","project_count":218,"projects_updated":4,
  "guariba_site_address_documented":True,"guariba_reported_works_started":True,
  "guariba_exact_coordinate_verified":False,
  "luiz_antonio_road_projects":3,"road_segments_geometries_verified":0,
  "federal_952718_2024_erratum_documented":True,
  "paid_capital_promoted":False,"physical_execution_points_promoted":0,
  "public_release_authorized":False,
  "qa_checks":qa["technical_checks_passed"],"sources":SOURCES}
 write(dest/"QA_FED18_ENDERECOS_E_TRECHOS_PRIVADO.json",report)
 with zipfile.ZipFile(pack,"w",zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for p in dest.rglob("*"):
   if p.is_file() and p.name!=".rmrp-fed07-private-preview":z.write(p,p.relative_to(dest))
 with zipfile.ZipFile(pack) as z:assert z.testzip() is None
 report["package_bytes"]=pack.stat().st_size;report["package_sha256"]=sha(pack)
 return report
if __name__=="__main__":
 a=argparse.ArgumentParser()
 for p in ("src","dest","package"):a.add_argument(p,type=Path)
 x=a.parse_args()
 print(json.dumps(build(x.src,x.dest,x.package),ensure_ascii=False))
