#!/usr/bin/env python3
"""Lote anual SIAFEM: prefeituras, investimento, ano da liberacao, por IBGE7.

Usa crosswalk IBGE7 x SIAFEM previamente auditado; não descarta estornos.
Grava dados brutos somente em diretório privado; relatório público contém apenas
totais de cobertura e testes, sem identificadores de beneficiários.
"""
from __future__ import annotations
import argparse,csv,hashlib,json,re,time
from datetime import datetime,timezone
from decimal import Decimal,InvalidOperation
from pathlib import Path
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from pipeline.coleta.probe_sp_siafem_webforms import URL,form_payload

def amount_cents(raw:str) -> int|None:
    s=raw.replace("R$","").replace("\xa0","").replace(" ","").strip()
    if not s:return None
    sign=1
    if s.startswith("(") and s.endswith(")"):
        s=s[1:-1];sign=-1
    if s.startswith("-"):
        s=s[1:];sign*=-1
    s=s.replace(".","").replace(",",".")
    try:
        v=Decimal(s)
    except InvalidOperation:
        return None
    if v.as_tuple().exponent< -2:
        return None
    return sign*int(v*100)

def integer(raw:str) -> int|None:
    s=raw.strip().replace(".","")
    return int(s) if re.fullmatch(r"\d+",s) else None

def cells(tr):
    return [el.get_text(" ",strip=True) for el in tr.find_all(["th","td"],recursive=False)]

def fetch_one(code:str,year:int,sess:requests.Session) -> dict:
    page=sess.get(URL,timeout=45)
    page.raise_for_status()
    payload,_=form_payload(page.text)
    opts=BeautifulSoup(page.text,"html.parser").find("select",{"name":"Municipio"})
    if code not in {o.get("value","") for o in opts.find_all("option")}:
        raise ValueError("codigo nao existe no seletor")
    payload.update({"Municipio":code,"Beneficiado":"Prefeituras","Tipo":"Investimento",
                    "Totais":"Não","LiberacaoInicio":f"01/01/{year}",
                    "LiberacaoFim":f"31/12/{year}","btnPesquisa":"Pesquisa",
                    "__EVENTTARGET":"","__EVENTARGUMENT":""})
    r=sess.post(URL,data=payload,timeout=90,headers={"Referer":URL})
    r.raise_for_status()
    if urlparse(r.url).hostname not in ("www.fazenda.sp.gov.br","fazenda.sp.gov.br"):
        raise RuntimeError("redirect inesperado")
    doc=BeautifulSoup(r.text,"html.parser")
    table=doc.find("table",{"id":"grdTransferencia"})
    if table is None:raise ValueError("tabela de convenios nao encontrada; nao assumir zero")
    trs=table.find_all("tr")
    if not trs:raise ValueError("tabela sem cabecalho")
    heads=cells(trs[0])
    if len(heads)!=7 or "Valor Liberado/Estornado" not in heads[5]:
        raise ValueError("schema da tabela inesperado")
    instruments=[];totals=[];invalid=[]
    for idx,tr in enumerate(trs[1:],1):
        row=cells(tr)
        if len(row)!=7:invalid.append(idx);continue
        if row[1] and row[2]:
            count=integer(row[4]);amount=amount_cents(row[5])
            if count is None or amount is None:raise ValueError("valor/contagem não numérico em linha de instrumento")
            link=tr.select_one("a[href]")
            instruments.append({"row":idx,"raw_fields":row,"source_url_or_action":link.get("href","") if link else "",
                                "payments_count":count,"released_net_cents":amount})
        else:
            totals.append({"row":idx,"raw_fields":row})
    sum_cents=sum(x["released_net_cents"] for x in instruments)
    payments=sum(x["payments_count"] for x in instruments)
    # Somente comparar totalizador se a linha de soma oferecer quantidade e valor
    footer_checks=[]
    for ft in totals:
        v=ft["raw_fields"]
        footer_count=integer(v[4])
        footer_amount=amount_cents(v[5])
        if footer_count is not None and footer_amount is not None:
            footer_checks.append({"count_matches":footer_count==payments,"value_matches":footer_amount==sum_cents})
            if footer_count!=payments or footer_amount!=sum_cents:
                raise ValueError("totalizador diverge da soma das linhas de instrumento")
    if invalid:
        raise ValueError(f"{len(invalid)} linhas fora do esquema")
    if not instruments and not footer_checks:
        raise ValueError("ausencia nao comprovada; sem linha financeira e totalizador")
    return {"headers":heads,"instruments":instruments,"totals":totals,
            "payments_count":payments,"value_cents":sum_cents,
            "footer_checks":footer_checks,"table_rows":len(trs),
            "status":"consulta_validada_estruturalmente"}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--crosswalk",type=Path,required=True)
    p.add_argument("--existing-roster",type=Path,required=True)
    p.add_argument("--year",type=int,default=2025)
    p.add_argument("--limit",type=int,default=5)
    p.add_argument("--offset",type=int,default=0)
    p.add_argument("--outdir",type=Path,required=True)
    p.add_argument("--acquire",action="store_true")
    a=p.parse_args()
    if not a.acquire:p.error("usar --acquire")
    if not 1<=a.limit<=25 or a.offset<0 or not 2020<=a.year<=2026:p.error("lote fora dos limites do piloto")
    with a.crosswalk.open(encoding="utf-8-sig",newline="") as f:
        mapped=list(csv.DictReader(f,delimiter=";"))
    with a.existing_roster.open(encoding="utf-8-sig",newline="") as f:
        prior={r["codigo_ibge"] for r in csv.DictReader(f,delimiter=";")}
    chosen=[x for x in mapped if x["codigo_ibge"] not in prior and x["codigo_siafem"]]
    chosen=sorted(chosen,key=lambda x:x["codigo_ibge"])[a.offset:a.offset+a.limit]
    if len(chosen)!=a.limit:raise ValueError("cadastro de novos municipios incompleto")
    s=requests.Session()
    s.headers.update({"User-Agent":"Mozilla/5.0 (levantamento publico SP645/1.0)"})
    data=[];failures=[]
    for i,item in enumerate(chosen):
        try:
            result=fetch_one(item["codigo_siafem"],a.year,s)
            data.append({"codigo_ibge":item["codigo_ibge"],"municipio":item["municipio"],
                         "codigo_siafem":item["codigo_siafem"],**result})
        except Exception as e:
            failures.append({"codigo_ibge":item["codigo_ibge"],"reason_class":type(e).__name__,
                             "description":str(e)[:140]})
        if i<len(chosen)-1:time.sleep(1)
    payload={"url":URL,"captured_utc":datetime.now(timezone.utc).isoformat(),
             "filter":{"beneficiado":"Prefeituras","tipo":"Investimento","year":a.year},
             "crosswalk":"governance/controls/investimentos_sp645/crosswalk_ibge_siafem_2026_11_16.csv",
             "rows":data,"failed_queries":failures,
             "financial_homologated":False,"source_coverage_complete":False}
    out=a.outdir;out.mkdir(parents=True,exist_ok=True)
    raw=json.dumps(payload,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8")
    file=out/"raw.json";file.write_bytes(raw)
    sha=hashlib.sha256(raw).hexdigest()
    qa={"source":"SP_SEFAZ","snapshot_sha256":sha,"bytes":len(raw),"year":a.year,
        "offset":a.offset,"requested_ibge7":[r["codigo_ibge"] for r in chosen],
        "verified_ibge7":[r["codigo_ibge"] for r in data],
        "municipalities_requested":len(chosen),"municipalities_with_verified_table":len(data),
        "municipalities_without_valid_result":len(failures),
        "queries_with_footer_reconciliation":sum(bool(x["footer_checks"]) for x in data),
        "queries_with_no_reconciliation_footer":sum(not x["footer_checks"] for x in data),
        "instrument_year_records":sum(len(x["instruments"]) for x in data),
        "payment_count":sum(x["payments_count"] for x in data),
        "net_cents_parsed":sum(x["value_cents"] for x in data),
        "failed_ibge7":[x["codigo_ibge"] for x in failures],
        "qa_status":"pilot_regional_expansion_not_financial_homologation"}
    (out/"qa.json").write_text(json.dumps(qa,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(qa,ensure_ascii=False))
    if not data:raise SystemExit(3)  # lote sem nenhuma consulta validada
if __name__=="__main__":
    main()
