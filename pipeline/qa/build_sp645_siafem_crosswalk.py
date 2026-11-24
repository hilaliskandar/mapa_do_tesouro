#!/usr/bin/env python3
"""Crosswalk IBGE7 SP645 x código municipal interno SIAFEM.

Associações exatas em nomes normalizados e alias previamente documentado.
Não faz atribuição automática por similaridade. Gera CSV auditável sem dados privados.
"""
from __future__ import annotations
import argparse,csv,json,re,unicodedata
from collections import Counter
from pathlib import Path
import requests
from bs4 import BeautifulSoup

SOURCE="https://www.fazenda.sp.gov.br/TransferenciaVoluntaria/Sistema/Novo/PesquisaComposta.aspx"
DIM="governance/DIM_SP645_IBGE_RA_RG_RM_AU_CONSOLIDADA_2026_11_14.csv"

def normalize(s):
    s=unicodedata.normalize("NFKD",s.upper())
    s="".join(c for c in s if not unicodedata.combining(c))
    s=re.sub(r"[^A-Z0-9]+"," ",s)
    return " ".join(s.split())

KNOWN_ALIASES={
    # Grafias literais do seletor SIAFEM inspecionadas via Crawl2AI em 16/11/2026.
    "BRODOWSKI":"BRODOSQUI",  # também documentado no relatório SIAFEM de 12/11
    "NOVA LUZITANIA":"NOVA LUSITANIA",
    "SALMOURAO":"SALMORAO",
    "SEVERINIA":"SEVERINEA",
    "SUD MENNUCCI":"SUD MENUCCI",
    "SUZANAPOLIS":"SUZANOPOLIS",
}

def run(roster_path:Path,output:Path,qa_path:Path):
    with roster_path.open(newline="",encoding="utf-8-sig") as f:
        roster=list(csv.DictReader(f,delimiter=";"))
    if len(roster)!=645 or len({r["codigo_ibge"] for r in roster})!=645:
        raise ValueError("cadastro não contém 645 códigos IBGE distintos")
    r=requests.get(SOURCE,timeout=60)
    r.raise_for_status()
    soup=BeautifulSoup(r.text,"html.parser")
    selector=soup.find("select",{"name":"Municipio"})
    if selector is None:raise ValueError("seletor Municipio indisponível")
    source_options=[(o.get("value",""),o.get_text(" ",strip=True)) for o in selector.find_all("option") if o.get("value","")]
    index={}
    for code,name in source_options:
        index.setdefault(normalize(name),[]).append((code,name))
    result=[];used_codes=set()
    for row in roster:
        ibge=row["codigo_ibge"]
        name=row["municipio"]
        norm=normalize(name)
        candidates=index.get(norm,[])
        status="exato"
        if not candidates and norm in KNOWN_ALIASES:
            candidates=index.get(KNOWN_ALIASES[norm],[])
            status="alias_documentado"
        if len(candidates)!=1:
            status="ausente" if not candidates else "ambiguo"
            code="";sname=""
        else:
            code,sname=candidates[0]
            if code in used_codes:
                raise ValueError("mesmo código SIAFEM associado a dois municípios")
            used_codes.add(code)
        result.append({"codigo_ibge":ibge,"municipio":name,"codigo_siafem":code,
                       "nome_siafem":sname,"estado":status})
    output.parent.mkdir(parents=True,exist_ok=True)
    with output.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=list(result[0]),delimiter=";")
        writer.writeheader();writer.writerows(result)
    stats=Counter(row["estado"] for row in result)
    qa={"source_url":SOURCE,"roster":DIM,"municipios_ibge":645,
        "source_options":len(source_options),
        "mapped":len(used_codes),
        "statuses":dict(stats),
        "unmapped_ibge7":[r["codigo_ibge"] for r in result if not r["codigo_siafem"]],
        "status":"crosswalk_apenas_correspondencia_exata_sem_fuzzy"}
    qa_path.write_text(json.dumps(qa,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(qa,ensure_ascii=False))
if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--roster",type=Path,default=Path(DIM))
    parser.add_argument("--output",type=Path,required=True)
    parser.add_argument("--qa",type=Path,required=True)
    a=parser.parse_args()
    run(a.roster,a.output,a.qa)
