#!/usr/bin/env python3
"""Inspeção segura de RCL mensal Audesp: não utiliza números presumidos.
Uso: python conferir_rcl_audesp_g24.py inspect rcl_completo.zip
     python conferir_rcl_audesp_g24.py extract rcl_completo.zip --municipio-col C --ano-col A --mes-col M --rcl-col V --out resultados.csv
Colunas C/A/M/V são exemplos: inspecionar primeiro os cabeçalhos reais.
"""
import argparse,csv,io,json,re,unicodedata,zipfile
from pathlib import Path
TARGET={"3540200":"Pontal","3505609":"Barrinha","3534302":"Orlandia"}
def normal(s):
    return re.sub("[^a-z0-9]","",unicodedata.normalize("NFKD",str(s)).encode("ascii","ignore").decode().lower())
def run():
    a=argparse.ArgumentParser()
    a.add_argument("mode",choices=("inspect","extract"));a.add_argument("zipfile",type=Path)
    for n in ("municipio","ano","mes","rcl"):a.add_argument("--"+n+"-col",default=None)
    a.add_argument("--out",default="G24_RCL_AUDESP_2025_DEZ.csv")
    v=a.parse_args()
    if not v.zipfile.exists():raise SystemExit("ZIP oficial não disponível; não imputar valores")
    with zipfile.ZipFile(v.zipfile) as z:
        if z.testzip() is not None:raise SystemExit("ZIP corrompido")
        for member in z.namelist():
            if not member.lower().endswith((".csv",".txt")):continue
            b=z.read(member)
            try:s=b.decode("utf-8-sig")
            except UnicodeError:s=b.decode("latin1")
            sep=max((";","\\t",","),key=lambda c:s[:4000].count(c))
            reader=csv.DictReader(io.StringIO(s),delimiter=sep);fields=reader.fieldnames or []
            print(json.dumps({"member":member,"columns":fields,"delimiter":sep},ensure_ascii=False))
            if v.mode=="inspect":continue
            requested=[v.municipio_col,v.ano_col,v.mes_col,v.rcl_col]
            if any(x is None for x in requested):raise SystemExit("Informar quatro nomes de colunas após inspect")
            mapping={normal(f):f for f in fields}
            try:c,y,m,r=[mapping[normal(x)] for x in requested]
            except KeyError:raise SystemExit("Cabeçalho não corresponde: revisar inspect")
            out=[]
            for row in reader:
                raw=normal(row.get(c,""))
                code=next((code for code,name in TARGET.items() if raw in (normal(code),normal(name))),None)
                if code is None or normal(row.get(y,""))!="2025" or normal(row.get(m,"")) not in ("12","dezembro","dez"):continue
                out.append({"codigo_ibge":code,"municipio":TARGET[code],"ano":"2025","mes":"12","rcl_original":row[r],"arquivo":member,"fonte":"https://www.transparencia.tce.sp.gov.br/sites/default/files/conjunto-dados/rcl_completo.zip"})
            if len(out)!=3 or len({x["codigo_ibge"] for x in out})!=3:raise SystemExit("QUARENTENA: resultado sem uma linha por municipio")
            with open(v.out,"w",encoding="utf-8-sig",newline="") as f:
                w=csv.DictWriter(f,fieldnames=list(out[0]),delimiter=";");w.writeheader();w.writerows(out)
            print("Exportados",len(out),"registros, sujeitos a conferência da metodologia")
if __name__=="__main__":run()
