#!/usr/bin/env python3
"""FED16: documentary planned-sites audit for RMRP with provenance.
Conservatively separates planned location from documented actual execution.
"""
from pathlib import Path
from math import radians,sin,cos,atan2,sqrt
import csv,hashlib,json,sqlite3,zipfile,shutil,requests,datetime

ROOT=Path("/home/user/rmrp_fed16")
ROOT.mkdir(parents=True,exist_ok=True)
DB=Path("/home/user/rmrp_current/fed12/RMRP_FED12_QCI_PROJETOS_PRIVADO.sqlite")
SRC=Path("/home/user/rmrp_current/fed15")
OUT=Path("/home/user/rmrp_fed16_private_site")
ARCHIVE=Path("/home/user/RMRP_FED16_SITE_PREVIA_PRIVADA_2026-11-16.zip")

SERTAO="https://www.sertaozinho.sp.gov.br/portal/noticias/0/3/3145/prefeitura-investe-em-infraestrutura-esportiva-em-diferentes-regioes-da-cidade"
MONTE="https://montealto.sp.gov.br/site/wp-content/uploads/2022/04/EDITAL-REV-PCA-S.-BENEDITO-C.-APOIO.pdf"
HEMO="https://www.hemocentro.fmrp.usp.br/wp-content/uploads/2024/05/Relatorio-de-Controle-Interno-Exercicio-2023.pdf"

def sha(b):return hashlib.sha256(b).hexdigest()
def read(path):return json.loads(path.read_text(encoding="utf-8"))
def write(path,value):path.write_text(json.dumps(value,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
def dms(deg,m,s):return -(deg+m/60+s/3600)
def hav(a,b):
 lat1,lon1=map(radians,a);lat2,lon2=map(radians,b)
 dl=lat2-lat1;do=lon2-lon1
 x=sin(dl/2)**2+cos(lat1)*cos(lat2)*sin(do/2)**2
 return 6371000*2*atan2(sqrt(x),sqrt(1-x))

db=sqlite3.connect(DB)
cases={
 "33889.35-28":{"proposal":"1347060","municipio":"Monte Alto","ibge":"3531308"},
 "125271.35-26":{"proposal":"1122551","municipio":"Sertãozinho","ibge":"3551702"},
 "31534.35-57":{"proposal":"1950015","municipio":"Ribeirão Preto","ibge":"3543402"}
}
for proj,c in cases.items():
 row=db.execute("SELECT o.ibge_proponente,v.id_proposta,v.nr_instrumento FROM obra_proponente o JOIN vinculo_projeto_instrumento_fed04b v ON o.projeto_id=v.id_projeto WHERE o.projeto_id=?",(proj,)).fetchone()
 assert (row[0],row[1])==(c["ibge"],c["proposal"])
 c["instrumento"]=row[2]
 c["coordenadas_proposta"]=[{"lat":lat,"lon":lon,"intersecao":st,"ibge_intersecao":ibge} for lat,lon,st,ibge in db.execute(
 """SELECT p.latitude,p.longitude,g.status_espacial,g.municipio_ibge
 FROM projeto_coordenada_candidata_fed04b pc JOIN coordenada_intersecao_sp_fed04c g ON g.source_row=pc.source_row
 JOIN coordenada_proposta_fed04b p ON p.source_row=g.source_row WHERE pc.id_projeto=?""",(proj,))]
assert {k:len(v["coordenadas_proposta"]) for k,v in cases.items()}=={"33889.35-28":2,"125271.35-26":1,"31534.35-57":2}

p=ROOT/"Fonte_Oficial_MonteAlto_2022_870332_Edital.pdf"
if not p.exists():
 r=requests.get(MONTE,timeout=45)
 assert r.status_code==200 and r.content.startswith(b"%PDF"),(r.status_code,r.headers.get("content-type"))
 p.write_bytes(r.content)
from pypdf import PdfReader
reader=PdfReader(str(p))
s36=reader.pages[35].extract_text()
s37=reader.pages[36].extract_text()
assert "870332/2018" in (s36+s37).replace(" ","") or "87 0332/2018" in s36
assert "21º15'41.46" in s36 and "48º29'20.80" in s36
assert "21º15'41.5" in s37 and "48º29'49.9" in s37
assert "1490" in s36
praca=[dms(21,15,41.46),dms(48,29,20.80)]
cat=[dms(21,15,41.5),dms(48,29,49.9)]
monte=cases["33889.35-28"]
candidate=next(x for x in monte["coordenadas_proposta"] if x["intersecao"]=="no_municipio_proponente")
outlier=next(x for x in monte["coordenadas_proposta"] if x["intersecao"]=="fora_sp")
metres=hav(cat,[candidate["lat"],candidate["lon"]])
km=hav(praca,[outlier["lat"],outlier["lon"]])/1000
assert metres<2 and km>2000
monte["locais_previstos_documentados"]=[
 {"componente":"Praça São Benedito / Largo do Batismo","endereco":"Praça São Benedito, Largo do Batismo, Centro, Monte Alto, SP, Brasil","lat":praca[0],"lon":praca[1],"origem_crs":"coordenada geográfica DMS, datum nao declarado no edital","classe":"local_projetado_por_documento_basico","execucao_fisica_comprovada":False,"fonte_url":MONTE,"fonte_pdf_pagina":36},
 {"componente":"Centro de Apoio ao Turista","endereco":"Rua Dr. Raul da Rocha Medeiros, 1490, Centro, Monte Alto, SP, Brasil","lat":cat[0],"lon":cat[1],"origem_crs":"coordenada geográfica DMS, datum nao declarado no edital","classe":"local_projetado_por_documento_basico","execucao_fisica_comprovada":False,"fonte_url":MONTE,"fonte_pdf_pagina":37}]
monte["analise_coordenada_cadastral"]={"ponto_conforme_centro_apoio_turista_m":round(metres,2),"ponto_fora_sp_distancia_praca_km":round(km,2),"status":"um_candidato_compatível_com_local_previsto;um_candidato_incompatível","nota":"Sem alterar o ponto de origem; distancia aproximada por Haversine. Datum das coordenadas DMS do edital nao explicitado."}

r=requests.get(SERTAO,timeout=35)
assert r.status_code==200
html=r.content
from bs4 import BeautifulSoup
site_text=BeautifulSoup(html,"html.parser").get_text(" ",strip=True)
assert "Franco Montoro" in site_text and "Antônio Pedro Ortolan" in site_text and "LAMG Serviços" in site_text
html_file=ROOT/"Fonte_Oficial_Sertaozinho_2017_PracaFranco.html"
html_file.write_bytes(html)
cases["125271.35-26"]["municipio_documentado_por_fonte_municipal"]={
 "ibge":"3551702","municipio":"Sertãozinho",
 "local":"Praça Franco Montoro, Conjunto Habitacional Antônio Pedro Ortolan (Cohab 3)",
 "fonte":SERTAO,"tipo":"noticia_municipal_de_obra_em_execucao_2017",
 "evidencia":"objeto de cobertura, arquibancada e adequações; afirma serviço em execução em Sertãozinho",
 "vinculo_ao_convenio_especifico":"correspondencia_de_objeto_e_local_sem_numero_convenio_na_noticia",
 "classe":"municipio_corrobora_objeto_e_local;sem_prova_georreferenciada",
 "coordenada_de_Suzano_utilizavel_para_execucao":False
}
cases["31534.35-57"]["evidencia_financiamento_institucional"]={
 "documento_fonte":HEMO,"convenio":"953325/2023",
 "objeto":"Reforma de unidade de atenção especializada em saúde",
 "valor_instrumento_relatado_reais":"385460.00",
 "natureza":"corroboracao_de_instrumento_em_relatorio_institucional;nao_documenta_endereco_da_obra",
 "coordenadas_Fernandopolis_Ribeirao_em_revisao":True}
cases["31534.35-57"]["locais_previstos_documentados"]=[]
cases["125271.35-26"]["locais_previstos_documentados"]=[]

if OUT.exists():raise RuntimeError("output exists")
shutil.copytree(SRC,OUT)
api=OUT/"data/api/v3/investimentos/rmrp"
updated=0
for project,data in cases.items():
 p=api/"projetos"/(project+".json")
 j=read(p); assert j["id_origem"]==project
 assert j["localizacao_fisica"]["pontos"]==[] and j["valores_investimento_pago_centavos"] is None
 j["evidencia_independente_fed16"]={
  "fontes_oficiais":([MONTE] if project=="33889.35-28" else [SERTAO] if project=="125271.35-26" else [HEMO]),
  "tipo":"projeto_basico_com_pontos_previstos" if project=="33889.35-28" else "relato_municipal_de_execucao_sem_coordenada" if project=="125271.35-26" else "relatorio_institucional_de_convenio",
  "locais_previstos_documentados":data.get("locais_previstos_documentados",[]),
  "local_execucao_final_comprovado":False,
  "municipio_corrobora_local":project in {"125271.35-26","33889.35-28"},
  "observacao":"Os pontos de projeto básico não podem migrar automaticamente para o mapa de execução física; vínculo documental e localização prevista são classes distintas."}
 j["public_release_authorized"]=False
 write(p,j);updated+=1

manifest=read(api/"manifest.json")
manifest["coverage"]["projetos_com_evidencia_independente_fed16"]=3
manifest["coverage"]["locais_previstos_em_edital_georreferenciados_sem_datum"]=2
manifest["coverage"]["locais_de_execucao_fisica_homologados"]=0
manifest["public_release_authorized"]=False
write(api/"manifest.json",manifest)
pend=read(api/"pendencias.json")
pend.setdefault("territorial",[]).append("FED16: duas coordenadas de local PREVISTO em edital municipal para o convênio 870332/2018 (Praça São Benedito e CAT), sem datum explicitado e sem prova de obra executada; não representar como pin de execução.")
pend["territorial"].append("FED16: notícia da Prefeitura corrobora quadra da Praça Franco em Sertãozinho; ponto SICONV em Suzano não deve ser usado como local da execução; falta referência explícita ao convênio na notícia.")
write(api/"pendencias.json",pend)

qa={"snapshot_federal":"2026-11-15","processamento":"2026-11-16",
    "casos_com_documento_independente":3,"locais_projetados_com_DMS_documental":2,
    "componentes_projeto_monte_alto":2,
    "distancia_ponto_CAT_a_candidato_SICONV_m":round(metres,2),
    "distancia_ponto_fora_SP_a_praca_km":round(km,2),
    "municipio_execucao_corroborado_noticia_2017":"Sertãozinho",
    "logradouro_Rua_Franco_sem_coordenada":True,
    "hemocentro_convenio_953325_corroborado_fonte_institucional":True,
    "pontos_executados_homologados":0,
    "public_release_authorized":False,
    "fonte_pdf_2022_sha256":sha(p.read_bytes()) if False else sha((ROOT/"Fonte_Oficial_MonteAlto_2022_870332_Edital.pdf").read_bytes()),
    "fonte_noticia_municipal_sha256":sha(html),
    "notas":["Coordenadas DMS provem do projeto basico e nao possuem datum geodesico explicitado.",
     "Haversine aproxima distancias em metros; não aplicar transformacao CRS que a fonte não especificou.",
     "Noticia municipal comprova relato historico sobre obra em Sertaozinho, mas nao identifica numero do contrato de repasse.",
     "Fonte Hemocentro comprova convenio, mas nao comprova endereço exato da reforma.",
     "Nunca equiparar coordenada planejada à obra efetivamente executada."]}
write(ROOT/"FED16_QA_AGREGADO.json",qa)
write(ROOT/"FED16_CASOS_FONTES_PRIVADOS.json",cases)
write(OUT/"QA_FED16_EVIDENCIAS_INDEPENDENTES_PRIVADO.json",qa)
zipsite=ARCHIVE
with zipfile.ZipFile(zipsite,"w",zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for f in OUT.rglob("*"):
  if f.is_file() and f.name!=".rmrp-fed07-private-preview":z.write(f,f.relative_to(OUT))
with zipfile.ZipFile(zipsite) as z:assert z.testzip() is None
zipaudit=ROOT/"RMRP_FED16_DOCUMENTOS_AUDITORIA_PRIVADA_2026-11-16.zip"
with zipfile.ZipFile(zipaudit,"w",zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for f in ROOT.iterdir():
  if f.is_file() and f.name!=zipaudit.name:z.write(f,f.name)
with zipfile.ZipFile(zipaudit) as z:assert z.testzip() is None
print(json.dumps({"QA":qa,"site_bytes":zipsite.stat().st_size,"site_sha":sha(zipsite.read_bytes()),
"docs_bytes":zipaudit.stat().st_size,"docs_sha":sha(zipaudit.read_bytes())},ensure_ascii=False))
