#!/usr/bin/env python3
"""G05-B: read private approved TCESP group-44 program/action classifications for RMSJRP."""
import collections,csv,hashlib,json,os
from decimal import Decimal
from pathlib import Path
from deployment.download_r2_source import download_r2_object
P=Path("build/rmsjrp-g05b");P.mkdir(parents=True,exist_ok=True)
bucket=os.environ["CLOUDFLARE_R2_BUCKET"]
def get(key,out):
    download_r2_object(account_id=os.environ["CLOUDFLARE_ACCOUNT_ID"],api_token=os.environ["CLOUDFLARE_API_TOKEN"],bucket=bucket,object_key=key,output=P/out)
    return hashlib.sha256((P/out).read_bytes()).hexdigest()
def read(name):
    with (P/name).open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f,delimiter=";" if name.startswith("ref_") else ","))
def write(name,rows):
    assert rows
    with (P/name).open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter=";");w.writeheader();w.writerows(rows)
    return {"name":name,"rows":len(rows),"sha256":hashlib.sha256((P/name).read_bytes()).hexdigest()}
codes={}
with Path("editorial/rmsjrp/MUNICIPIOS_SUBREGIOES_2025.csv").open(encoding="utf-8") as f:
    for row in csv.DictReader(f,delimiter=";"):codes[row["cod_ibge"]]=row["municipio"]
assert len(codes)==37
prefixes={2023:"tcesp/estadual/despesas/2023/run_40263996213",2024:"tcesp/estadual/despesas/2024/run_40263996213",2025:"tcesp/estadual/despesas/2025/run_40262193781"}
totals=collections.Counter()
byp=collections.Counter()
bya=collections.Counter()
namesP={};namesA={};sources=[]
for year,prefix in prefixes.items():
    mf=f"manifest_{year}.json";get(prefix+"/r2_manifest.json",mf)
    manifest=json.loads((P/mf).read_text(encoding="utf-8"))
    assert manifest["qa_status"]=="pass" and manifest["source_year"]==year
    objects={o["name"]:o for o in manifest["objects"]}
    for level,name in [("programa","investimentos_grupo44_por_programa.csv"),("acao","investimentos_grupo44_por_acao.csv")]:
        local=f"{level}_{year}.csv"
        digest=get(prefix+"/"+name,local)
        assert digest==objects[name]["sha256"],(name,year)
        for row in read(local):
            id=row["codigo_ibge"]
            if id not in codes or row["estagio"].strip().lower()!="valor liquidado":continue
            amount=int(row["centavos"])
            org=row["orgao"]
            prog=row["cd_programa"]
            if level=="programa":
                key=(year,id,org,prog)
                byp[key]+=amount
                if row["ds_programa"]:namesP[(id,org,prog)]=row["ds_programa"]
            else:
                action=row["cd_acao"]
                key=(year,id,org,prog,action)
                bya[key]+=amount
                if row["ds_acao"]:namesA[(id,org,prog,action)]=row["ds_acao"]
        sources.append({"ano":year,"arquivo":name,"sha256":digest})
    pt=collections.Counter()
    ac=collections.Counter()
    for (y,id,*_),c in byp.items():
        if y==year:pt[id]+=c
    for (y,id,*_),c in bya.items():
        if y==year:ac[id]+=c
    assert pt==ac,(year,"soma programa/acao divergente")
    totals.update({(year,id):value for id,value in pt.items()})
assert len(totals)==111
refs={}
get("rmsjrp/fase1/2026_11_09/tcesp/MATRIZ_TCESP_RMSJRP_2023_2025.csv","ref_tcesp.csv")
for row in read("ref_tcesp.csv"):
    if row["estagio"]=="valor liquidado":refs[(int(row["ano"]),row["cod_ibge"])]=int(row["centavos"])
assert refs==dict(totals),(len(refs),len(totals))
out=[]
for level,data in [("programa",byp),("acao",bya)]:
    keys=set((x[1:] for x in data))
    for ini,fim in [(2023,2024),(2024,2025),(2023,2025)]:
        for key in keys:
            v0=data.get((ini,)+key)
            v1=data.get((fim,)+key)
            if v0 is None and v1 is None:continue
            diff=(v1 or 0)-(v0 or 0)
            id,org,prog=key[:3]
            acao=key[3] if level=="acao" else ""
            title=namesA.get((id,org,prog,acao),"") if level=="acao" else namesP.get((id,org,prog),"")
            out.append({"nivel":level,"cod_ibge":id,"municipio":codes[id],"orgao":org,"cd_programa":prog,"cd_acao":acao,
                        "descricao_referencia":title,"inicio":ini,"fim":fim,
                        "registro_inicio":int(v0 is not None),"registro_fim":int(v1 is not None),
                        "valor_inicio_centavos":v0 if v0 is not None else "",
                        "valor_fim_centavos":v1 if v1 is not None else "",
                        "variacao_centavos":diff,
                        "aviso":"Ausencia de codigo nao comprova descontinuidade fisica de projeto"})
out.sort(key=lambda r:(r["inicio"],r["fim"],r["nivel"],r["cod_ibge"],r["orgao"],r["cd_programa"],r["cd_acao"]))
assert out
# reconcile every aggregate movement of programs/actions against municipal annual amounts
for level in ("programa","acao"):
    for ini,fim in [(2023,2024),(2024,2025),(2023,2025)]:
        subset=[x for x in out if x["nivel"]==level and x["inicio"]==ini and x["fim"]==fim]
        for code in codes:
            sum_delta=sum(int(x["variacao_centavos"]) for x in subset if x["cod_ibge"]==code)
            assert sum_delta==totals[fim,code]-totals[ini,code],(level,code,ini,fim)
res=write("G05B_TRANSICOES_PROGRAMA_ACAO_2023_2025.csv",out)
summary=[]
for level in ("programa","acao"):
    for ini,fim in [(2023,2024),(2024,2025),(2023,2025)]:
        subset=[r for r in out if r["nivel"]==level and r["inicio"]==ini and r["fim"]==fim]
        for sign in ("queda","aumento"):
            subset2=sorted([r for r in subset if int(r["variacao_centavos"])<0] if sign=="queda" else [r for r in subset if int(r["variacao_centavos"])>0],
                key=lambda r:abs(int(r["variacao_centavos"])),reverse=True)[:40]
            for pos,r in enumerate(subset2,1):
                summary.append({**r,"sinal":sign,"ordem":pos})
res2=write("G05B_MAIORES_MOVIMENTOS.csv",summary)
qa={"status":"pass","municipios":37,"anos":[2023,2024,2025],"pares_tcesp_conciliados":111,"movimentos":len(out),"top_movimentos":len(summary),
    "fontes":sources,"produtos":[res,res2],"ressalva":"Codigo de programa/acao nao prova continuidade fisica nem conclusao de obra"}
(P/"QA_G05B.json").write_text(json.dumps(qa,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"status":"pass","movimentos":len(out),"top_movimentos":len(summary),"municipios":37,"pares_conciliados":111,"top_2024_2025_programas": [dict(municipio=r["municipio"],programa=r["cd_programa"],desc=r["descricao_referencia"][:90],valor=r["variacao_centavos"]) for r in summary if r["nivel"]=="programa" and r["inicio"]==2024 and r["fim"]==2025 and r["sinal"]=="queda"][:8]},ensure_ascii=False))
