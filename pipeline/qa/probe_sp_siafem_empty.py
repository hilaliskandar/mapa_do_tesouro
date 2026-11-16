#!/usr/bin/env python3
"""Auditoria de retorno vazio SIAFEM sem imprimir conteúdo pessoal do HTML."""
from __future__ import annotations
import json,re,requests
from bs4 import BeautifulSoup
from pipeline.coleta.collect_sp_siafem_annual_batch import URL,form_payload,cells
def run():
    ses=requests.Session()
    ses.headers.update({"User-Agent":"Mozilla/5.0 (coleta publica SP645 QA)"})
    r=ses.get(URL,timeout=45);r.raise_for_status()
    form,_=form_payload(r.text)
    options={x.get("value"):x.get_text(" ",strip=True) for x in BeautifulSoup(r.text,"html.parser").select('select[name="Municipio"] option')}
    code=next((code for code,name in options.items() if name.upper()=="ALAMBARI"),None)
    if not code:raise ValueError("Alambari nao consta no seletor")
    form.update({"Municipio":code,"Beneficiado":"Prefeituras","Tipo":"Investimento","Totais":"Não",
                 "LiberacaoInicio":"01/01/2025","LiberacaoFim":"31/12/2025",
                 "btnPesquisa":"Pesquisa","__EVENTTARGET":"","__EVENTARGUMENT":""})
    page=ses.post(URL,data=form,timeout=90,headers={"Referer":URL});page.raise_for_status()
    doc=BeautifulSoup(page.text,"html.parser")
    tab=doc.find("table",{"id":"grdTransferencia"})
    shape=[len(cells(tr)) for tr in tab.find_all("tr")] if tab else []
    labels=[]
    for node in doc.select("span,div,td"):
        if node.find(["span","div","td"]):continue
        txt=node.get_text(" ",strip=True)
        if not txt or len(txt)>250:continue
        if re.search("nenhum|nenhuma|n[aã]o (?:existe|existem|foram|foi|h[aá]|encontrad)|sem (?:resultad|regist|inform)|0 registro",txt,re.I):
            labels.append(txt)
    print(json.dumps({"http":page.status_code,"table_present":tab is not None,
        "table_rows":shape,"empty_labels":sorted(set(labels))[:18],
        "response_bytes":len(page.content),"has_viewstate":bool(doc.select_one('input[name="__VIEWSTATE"]'))},
        ensure_ascii=False))
if __name__=="__main__":run()
