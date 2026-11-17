#!/usr/bin/env python3
"""Coleta-piloto SIAFEM/SP: convenios e parcelas em camadas distintas.

Descoberta com Crawl2AI e consulta POST testada em GitHub Actions.
Por padrão exige --acquire e preserva campos brutos somente em diretório privado.
Não executa varredura SP645, não infere IBGE7, nem homologação financeira.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from pipeline.coleta.probe_sp_siafem_webforms import URL, form_payload

HOSTS={"www.fazenda.sp.gov.br","fazenda.sp.gov.br"}
def safe_detail_url(href: str, base: str) -> str:
    if "Open2(" not in href:
        raise ValueError("detail link sem Open2")
    raw=href.split("Open2(",1)[1]
    result=None
    for quote in ("'", '"'):
        parts=raw.split(quote)
        if len(parts)>2 and parts[1]:
            result=parts[1]
            break
    if result is None:
        raise ValueError("sem URL detalhada")
    target=urljoin(base,result)
    parsed=urlparse(target)
    if parsed.scheme!="https" or parsed.hostname not in HOSTS or not parsed.path.endswith("/Convenio.aspx"):
        raise ValueError("destino de detalhe nao autorizado")
    return target

def cells(tr):
    return [c.get_text(" ",strip=True) for c in tr.find_all(["th","td"],recursive=False)]

def payload_for(session, code: str, start: str, end: str) -> tuple[dict,str]:
    resp=session.get(URL,timeout=45)
    resp.raise_for_status()
    original=BeautifulSoup(resp.text,"html.parser")
    option=original.find("select",{"name":"Municipio"})
    choices={o.get("value"):o.get_text(" ",strip=True) for o in option.find_all("option")}
    if code not in choices:raise ValueError("municipio nao consta no seletor")
    form,_=form_payload(resp.text)
    form.update({"Municipio":code,"LiberacaoInicio":start,"LiberacaoFim":end,
                 "Beneficiado":"Prefeituras","Totais":"Não","Tipo":"",
                 "btnPesquisa":"Pesquisa","__EVENTTARGET":"","__EVENTARGUMENT":""})
    return form,choices[code]

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--acquire",action="store_true")
    p.add_argument("--municipio-code",default="0582")
    p.add_argument("--date-from",default="01/01/2025")
    p.add_argument("--date-to",default="31/01/2025")
    p.add_argument("--outdir",type=Path,default=Path("build/private_sp_siafem"))
    p.add_argument("--max-instruments",type=int,default=10)
    args=p.parse_args()
    if not args.acquire:p.error("usar --acquire explicitamente")
    if args.max_instruments<1 or args.max_instruments>30: p.error("limite de instrumentos permitido 1-30")
    session=requests.Session()
    session.headers.update({"User-Agent":"Mozilla/5.0 (pesquisa publica SIAFEM SP/1.0)"})
    filters,municipio=payload_for(session,args.municipio_code,args.date_from,args.date_to)
    response=session.post(URL,data=filters,timeout=90,headers={"Referer":URL})
    response.raise_for_status()
    if urlparse(response.url).hostname not in HOSTS:
        raise RuntimeError("redirecionamento inesperado")
    table=BeautifulSoup(response.text,"html.parser").find("table",{"id":"grdTransferencia"})
    if not table:raise ValueError("tabela principal ausente")
    trs=table.find_all("tr")
    hdr=cells(trs[0])
    if not any("Quantidade de Pagamentos" in x for x in hdr):
        raise ValueError("schema dos instrumentos mudou")
    instruments=[]
    movements=[]
    skipped=0
    for row in trs[1:]:
        values=cells(row)
        if len(values)!=7 or not values[1] or not values[2]:
            skipped+=1
            continue  # cabeçalho/totalizador
        link=row.select_one("a[href]")
        if not link:raise ValueError("instrumento sem link detalhado")
        detail_url=safe_detail_url(link.get("href",""),response.url)
        if len(instruments)>=args.max_instruments:
            raise ValueError("limite de instrumentos atingido; particionar competencia")
        detail=session.get(detail_url,timeout=45,headers={"Referer":response.url})
        detail.raise_for_status()
        doc=BeautifulSoup(detail.text,"html.parser")
        detail_table=doc.find("table",{"id":"grdTransferencia"})
        if detail_table is None:raise ValueError("tabela de parcelas ausente em ficha")
        detail_rows=detail_table.find_all("tr")
        if not detail_rows:raise ValueError("detalhe sem cabecalho")
        payment_headers=cells(detail_rows[0])
        if len(payment_headers)!=8 or "Valor liberado/estornado" not in payment_headers[-1]:
            raise ValueError("schema de parcelas inesperado")
        reference=hashlib.sha256(detail_url.encode("utf-8")).hexdigest()
        instruments.append({"instrument_source_key":reference,
                            "source_detail_url":detail_url,
                            "source_headers":hdr,"raw_fields":values,
                            "detail_http_status":detail.status_code})
        for index,r in enumerate(detail_rows[1:],1):
            vals=cells(r)
            if len(vals)!=len(payment_headers):
                raise ValueError("parcela com numero irregular de campos")
            movements.append({"instrument_source_key":reference,"row_number":index,
                              "source_headers":payment_headers,"raw_fields":vals})
    if not instruments:raise ValueError("consulta piloto sem instrumentos; verificar filtros")
    out=args.outdir
    out.mkdir(parents=True,exist_ok=True)
    stamp=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    payload={"source":"Sefaz-SP/SIAFEM-TransferenciasVoluntarias",
             "url":URL,"collected_utc":datetime.now(timezone.utc).isoformat(),
             "query":{"municipio_code":args.municipio_code,"municipio_name":municipio,
                      "liberacao_inicio":args.date_from,"liberacao_fim":args.date_to,
                      "beneficiado":"Prefeituras"},
             "instrument_count":len(instruments),
             "movement_row_count":len(movements),
             "skipped_summary_rows":skipped,
             "instruments":instruments,"movement_rows":movements,
             "financial_homologated":False,
             "municipality_ibge7_homologated":False}
    raw=json.dumps(payload,ensure_ascii=False,separators=(",",":"),sort_keys=True).encode("utf-8")
    data_path=out/f"siafem_ribeirao_2025_01_{stamp}.json"
    data_path.write_bytes(raw)
    digest=hashlib.sha256(raw).hexdigest()
    report={"source_id":"SP_SEFAZ","download_sha256":digest,"byte_count":len(raw),
            "instrument_count":len(instruments),"movement_row_count":len(movements),
            "skipped_summary_rows":skipped,"date_range":[args.date_from,args.date_to],
            "municipio_code":args.municipio_code,"qa_status":"estrutura_piloto_nao_homologada"}
    report_path=data_path.with_suffix(".qa.json")
    report_path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"data_path":str(data_path),"qa_path":str(report_path),**report},ensure_ascii=False))

if __name__=="__main__":
    main()
