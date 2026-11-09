#!/usr/bin/env python3
"""Rebuild G05 RMSJRP territorial diagnosis exclusively from approved G03/G04 R2 products."""
from __future__ import annotations
import collections,csv,hashlib,json,os
from decimal import Decimal
from pathlib import Path
from deployment.download_r2_source import download_r2_object
ROOT=Path("build/rmsjrp-g05");ROOT.mkdir(parents=True,exist_ok=True)
BUCKET=os.environ["CLOUDFLARE_R2_BUCKET"]
def retrieve(path,object_key,sha):
    download_r2_object(account_id=os.environ["CLOUDFLARE_ACCOUNT_ID"],api_token=os.environ["CLOUDFLARE_API_TOKEN"],bucket=BUCKET,object_key=object_key,output=ROOT/path)
    assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==sha,(path,"source_sha_mismatch")
def read(name):
    with (ROOT/name).open(encoding="utf-8-sig",newline="") as f:
        return list(csv.DictReader(f,delimiter=";"))
def emit(name,rows):
    assert rows
    with (ROOT/name).open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter=";");w.writeheader();w.writerows(rows)
    return {"name":name,"rows":len(rows),"sha256":hashlib.sha256((ROOT/name).read_bytes()).hexdigest()}
D=Decimal;Q=D(".01")
def v(x):return D(x) if x not in ("",None) else None
def fm(x):return str(x.quantize(Q)) if x is not None else ""
def pct(num,den):return fm(num/den*100) if num is not None and den not in (None,0) else ""
srcs=[
("municipios.csv","rmsjrp/g04/2026_11_09/SERIES_MUNICIPAIS_2013_2025.csv","1f0413304c54edbe57fe129a506d088da2cd296d767f901992c02f803fbd62e5"),
("territorios.csv","rmsjrp/g04/2026_11_09/SERIES_TERRITORIAIS_2013_2025.csv","70438537957f6b31bdf80e2e6705a5153735757a42d6cc8129067006087f6268"),
("tcesp.csv","rmsjrp/fase1/2026_11_09/tcesp/MATRIZ_TCESP_RMSJRP_2023_2025.csv","5aa597f2a4f18caebdc8b652113f4745953919abe6c6c201ab9c29fc0f509a53")]
for args in srcs:retrieve(*args)
m=read("municipios.csv");r=read("territorios.csv");t=read("tcesp.csv")
assert len(m)==481 and len(r)==65
M={(z["cod_ibge"],int(z["ano"])):z for z in m}
R={(z["territorio"],int(z["ano"])):z for z in r}
assert len(M)==481 and len(R)==65
regions=["RMSJRP","São José do Rio Preto","José Bonifácio","Tanabi","Nova Granada"]
INV="dca_investimentos_liquidada_real_set2026"
REV="dca_receita_corrente_bruta_real_set2026"
series=[];deltas=[];municipal=[]
for area in regions:
    for y in [2023,2024,2025]:
        a=R[area,y]
        series.append({"territorio":area,"ano":y,"municipios":a["municipios_esperados"],"populacao_dca":a["populacao_total"],"receita_corrente_real_set2026_R$":a[REV],"investimento_real_set2026_R$":a[INV],"investimento_nominal_R$":a["dca_investimentos_liquidada_nominal"],"investimento_real_pc_R$":a["dca_investimentos_liquidada_real_pc_set2026"],"investimento_pct_receita_corrente":a["investimento_pct_corrente"]})
    for ini,fim in [(2023,2024),(2024,2025),(2023,2025)]:
        a,b=R[area,ini],R[area,fim];di=v(b[INV])-v(a[INV]);dr=v(b[REV])-v(a[REV])
        deltas.append({"territorio":area,"inicio":ini,"fim":fim,"variacao_investimento_real_R$":fm(di),"variacao_investimento_real_pct":pct(di,v(a[INV])),"variacao_receita_real_R$":fm(dr),"variacao_receita_real_pct":pct(dr,v(a[REV]))})
ids=sorted(set(code for code,_ in M))
assert len(ids)==37
for code in ids:
    for ini,fim in [(2023,2024),(2024,2025),(2023,2025)]:
        a,b=M[code,ini],M[code,fim];di=v(b[INV])-v(a[INV]);dr=v(b[REV])-v(a[REV])
        municipal.append({"cod_ibge":code,"municipio":a["municipio"],"subregiao":a["subregiao"],"inicio":ini,"fim":fim,"investimento_real_inicial_R$":a[INV],"investimento_real_final_R$":b[INV],"variacao_investimento_real_R$":fm(di),"variacao_investimento_real_pct":pct(di,v(a[INV])),"variacao_receita_real_R$":fm(dr),"variacao_receita_real_pct":pct(dr,v(a[REV]))})
assert len(municipal)==111
mov=[];direction=[]
for ini,fim in [(2023,2024),(2024,2025),(2023,2025)]:
    subset=[z for z in municipal if z["inicio"]==ini and z["fim"]==fim]
    decreases=sum((-v(z["variacao_investimento_real_R$"]) for z in subset if v(z["variacao_investimento_real_R$"])<0),D(0))
    increases=sum((v(z["variacao_investimento_real_R$"]) for z in subset if v(z["variacao_investimento_real_R$"])>0),D(0))
    regional=v(R["RMSJRP",fim][INV])-v(R["RMSJRP",ini][INV])
    assert abs((increases-decreases)-regional)<D("1.00")
    direction.append({"inicio":ini,"fim":fim,"municipios_com_queda":sum(v(z["variacao_investimento_real_R$"])<0 for z in subset),"municipios_com_aumento":sum(v(z["variacao_investimento_real_R$"])>0 for z in subset),"queda_bruta_real_R$":fm(decreases),"aumento_bruto_real_R$":fm(increases),"saldo_regional_real_R$":fm(regional)})
    for z in subset:
        diff=v(z["variacao_investimento_real_R$"])
        mov.append({**z,"participacao_na_queda_bruta_pct":pct(-diff,decreases) if diff<0 else "","participacao_no_aumento_bruto_pct":pct(diff,increases) if diff>0 else "","contribuicao_assinada_no_saldo_pct":pct(diff,regional)})
pole=[]
for y in (2023,2024,2025):
    a=M["3549805",y];allr=R["RMSJRP",y]
    for typ,ii,rv in [("polo",v(a[INV]),v(a[REV])),("demais",v(allr[INV])-v(a[INV]),v(allr[REV])-v(a[REV]))]:
        pole.append({"ano":y,"recorte":typ,"investimento_real_R$":fm(ii),"receita_real_R$":fm(rv),"participacao_investimento_pct":pct(ii,v(allr[INV])),"participacao_receita_pct":pct(rv,v(allr[REV]))})
for z in t:
    if z["estagio"]!="valor liquidado":continue
    assert v(z["centavos"])==v(M[z["cod_ibge"],int(z["ano"])]["dca_investimentos_liquidada_nominal"])*100
assert sum(x["estagio"]=="valor liquidado" for x in t)==111
outputs=[
emit("G05_TERRITORIOS_2023_2025.csv",series),
emit("G05_VARIACOES_TERRITORIAIS.csv",deltas),
emit("G05_CONTRIBUICOES_MUNICIPAIS.csv",mov),
emit("G05_POLO_DEMAIS.csv",pole),
emit("G05_DIRECAO_INVESTIMENTOS.csv",direction)]
qa={"status":"pass","municipios":37,"serie_territorial_linhas":15,"variacoes_territoriais_linhas":15,"contribuicoes_municipais_linhas":111,"tcesp_dca_confrontos":111,"source_hashes":{x[0]:x[2] for x in srcs},"outputs":outputs,"direction":direction}
(ROOT/"QA_G05.json").write_text(json.dumps(qa,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"status":"pass","direction":direction,"outputs":outputs},ensure_ascii=False))
