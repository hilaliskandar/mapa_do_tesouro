#!/usr/bin/env python3
"""Diagnóstico mínimo, não persistente, de consulta SIAFEM-SP em Web Forms.

Contrato de campos descoberto por Crawl2AI em 16/11/2026.
Realiza apenas consulta mensal por município, sem publicar conteúdo recebido.
"""
from __future__ import annotations
import argparse
import json
import re
from collections import Counter
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup

URL = "https://www.fazenda.sp.gov.br/TransferenciaVoluntaria/Sistema/Novo/PesquisaComposta.aspx"

def form_payload(html: str) -> tuple[dict[str,str], list[str]]:
    doc = BeautifulSoup(html, "html.parser")
    form = doc.find("form", {"id": "form1"})
    if not form:
        raise ValueError("form1 não encontrado")
    payload: dict[str,str] = {}
    for field in form.select("input[name]"):
        kind = field.get("type","text").lower()
        if kind in ("submit", "button", "image", "file"): continue
        if kind in ("radio", "checkbox") and not field.has_attr("checked"):
            continue
        payload[field["name"]] = field.get("value", "")
    for field in form.select("select[name]"):
        option = field.find("option", selected=True) or field.find("option")
        if option:
            payload[field["name"]] = option.get("value","")
    names = sorted(payload)
    required = ("__VIEWSTATE","__EVENTVALIDATION","__VIEWSTATEGENERATOR","Municipio","LiberacaoInicio","LiberacaoFim")
    if any(n not in payload for n in required):
        raise ValueError("controles de sessão ou filtro ausentes")
    return payload, names

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--municipio-code", default="0582", help="código próprio do sistema; 0582 é Ribeirão Preto")
    ap.add_argument("--date-from", default="01/01/2025")
    ap.add_argument("--date-to", default="31/01/2025")
    a = ap.parse_args()
    session = requests.Session()
    session.headers.update({"User-Agent":"Mozilla/5.0 (compatible; pesquisa-publica-mapa-do-tesouro/1.0)"})
    response = session.get(URL, timeout=45)
    response.raise_for_status()
    payload,names = form_payload(response.text)
    if payload.get("Municipio") is None: raise AssertionError("seleção municipal ausente")
    original=BeautifulSoup(response.text, "html.parser")
    select=original.find("select",{"name":"Municipio"})
    options={x.get("value"):x.get_text(strip=True) for x in select.find_all("option")}
    if a.municipio_code not in options: raise ValueError("código não existe nas opções")
    payload.update({"Municipio":a.municipio_code,
                    "LiberacaoInicio":a.date_from,
                    "LiberacaoFim":a.date_to,
                    "Beneficiado":"Prefeituras",
                    "Totais":"Não",
                    "Tipo":"",
                    "btnPesquisa":"Pesquisa",
                    "__EVENTTARGET":"",
                    "__EVENTARGUMENT":""})
    reply=session.post(URL, data=payload, timeout=90, headers={"Referer":URL})
    reply.raise_for_status()
    if urlparse(reply.url).hostname not in ("www.fazenda.sp.gov.br","fazenda.sp.gov.br"):
        raise RuntimeError("redirect para host inesperado")
    content=reply.text
    doc=BeautifulSoup(content,"html.parser")
    tables=doc.find_all("table")
    candidates=[]
    for tab in tables:
        rs=tab.find_all("tr")
        if len(rs)>=3:
            heads=[x.get_text(" ",strip=True)[:80] for x in tab.select("th")[:15]]
            candidates.append({"id":tab.get("id",""),"rows":len(rs),"headers":heads})
    grid=doc.find("table", {"id":"grdTransferencia"})
    grid_rows=[]
    grid_header_labels=[]
    if grid:
        for i,tr in enumerate(grid.find_all("tr")):
            cells=tr.find_all(["th","td"],recursive=False)
            row_text=[c.get_text(" ",strip=True) for c in cells]
            if i==0:
                grid_header_labels=row_text
            grid_rows.append({
                "row_index":i,
                "cells":len(cells),
                "tag_types":[x.name for x in cells],
                "cell_lengths":[len(x) for x in row_text],
                "date_like_cells":sum(bool(re.search(r"\\b\\d{2}/\\d{2}/\\d{4}\\b",x)) for x in row_text),
                "numeric_like_cells":sum(bool(re.fullmatch(r"[R$\\s\\d.,()\\-]+",x)) for x in row_text if x),
                "link_cells":sum(bool(x.find("a")) for x in cells)
            })
    detail_link_patterns=[]
    if grid:
        for anchor in grid.select("a[href],a[onclick]")[:5]:
            href=(anchor.get("href") or "").strip()
            onclick=(anchor.get("onclick") or "").strip()
            href_path=href.split("?",1)[0]
            if href_path.lower().startswith("javascript:"):
                href_path=href_path.split("(",1)[0]
            fn=re.match(r"[a-zA-Z_$][a-zA-Z0-9_.$]*",onclick)
            target=None
            m=re.search(r"Open2\\s*\\(\\s*['\\\"]([^'\\\"]+)",href,re.I)
            if m:
                target=m.group(1).split("?",1)[0].split("#",1)[0][:180]
            detail_link_patterns.append({"href_path_or_function":href_path[:180],"target_path_without_params":target,"onclick_function":fn.group(0) if fn else None})
    text=doc.get_text(" ",strip=True)
    alerts=[s for s in ("Nenhum registro","Nenhuma informação","VALIDAÇÃO","Erro ao","Resultado","Total de Registros") if s.casefold() in text.casefold()]
    print(json.dumps({
        "get_status":response.status_code,"post_status":reply.status_code,
        "target_municipio_code":a.municipio_code,"dates":[a.date_from,a.date_to],
        "form_names_without_values":[x for x in names if not x.startswith("__")],
        "response_bytes":len(reply.content),
        "response_title":doc.title.get_text(" ",strip=True) if doc.title else None,
        "table_summary":candidates[:12],
        "grdTransferencia_row_structure":grid_rows[:15],
        "grdTransferencia_header_labels":grid_header_labels,
        "detail_link_patterns":detail_link_patterns,
        "alerts_keywords":alerts,
        "returned_webforms_state":bool(doc.select_one('input[name="__VIEWSTATE"]')),
        "qa":"protocolo_testado_sem_persistencia_de_linhas"
    },ensure_ascii=False))
if __name__=="__main__":
    main()
