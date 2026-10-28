#!/usr/bin/env python3
"""Public Siconfi history: bounded, unauthenticated Taubate/2024 pilot."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

URL="https://siconfi.tesouro.gov.br/siconfi/pages/public/consulta_historico_declaracoes/historico_declaracoes_list.jsf"
OUT=Path("siconfi-history-qa")
OUT.mkdir(exist_ok=True)
report={"url":URL,"municipality":"Taubaté","ibge":3554102,"year":2024,
        "municipal_results":False,"status":"not_queried","actions":[]}
def control_snapshot(page,label):
    return page.evaluate("""() => [...document.querySelectorAll('#formHistorico select,#formHistorico input')]
      .map(e=>({id:e.id,tag:e.tagName,type:e.type,value:e.value,disabled:e.disabled,
       options:e.tagName==='SELECT'?[...e.options].slice(0,30).map(o=>({value:o.value,text:o.text.trim()})):undefined}))
      .filter(e=>e.id && !(/ViewState|captcha|token|password/i).test(e.id))""")
def choose(page,name,part):
    sel=page.locator('[id="formHistorico:'+name+'_input"]')
    if not sel.count(): sel=page.locator('[id="formHistorico:'+name+'"]')
    if not sel.count(): raise RuntimeError("missing select: "+name)
    options=sel.evaluate("(e) => [...e.options].map(o=>({value:o.value,text:o.text.trim()}))")
    match=next((o for o in options if part.casefold() in o["text"].casefold()),None)
    if not match: raise RuntimeError("option not found for "+name+": "+part)
    # PrimeFaces can hide the native select; dispatch change and wait for its AJAX updates.
    sel.evaluate("(e,v)=>{e.value=v;e.dispatchEvent(new Event('change',{bubbles:true}))}",match["value"])
    page.wait_for_timeout(1800)
    report["actions"].append({"select":name,"label":match["text"]})

with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    page=browser.new_page(accept_downloads=True,locale="pt-BR")
    try:
        response=page.goto(URL,wait_until="domcontentloaded",timeout=60000)
        page.wait_for_timeout(2400)
        report["http_status"]=response.status if response else None
        report["form_present"]=page.locator("#formHistorico").count()>0
        report["controls_initial"]=control_snapshot(page,"initial")
        if not report["form_present"]: raise RuntimeError("formHistorico absent")
        choose(page,"esfera","Municipal")
        report["controls_after_sphere"]=control_snapshot(page,"sphere")
        page.screenshot(path=str(OUT/"after_sphere.png"),full_page=False)
        # Only select if the public application exposes options; never invent ente IDs.
        try:
            choose(page,"estado","São Paulo")
            choose(page,"poder","Executivo")
            choose(page,"exercicio","2024")
            choose(page,"tipoDemonstrativo","Balanço Anual (DCA)")
            choose(page,"escopo","Declarações Homologadas")
        except RuntimeError as e:
            report["uf_selection_note"]=str(e)
        report["controls_after_uf"]=control_snapshot(page,"estado")
        report["ente_input_disabled"]=page.locator('[id="formHistorico:ente_input"]').is_disabled()
        report["orgao_input_disabled"]=page.locator('[id="formHistorico:orgao_input"]').is_disabled()
        page.screenshot(path=str(OUT/"after_filters.png"),full_page=False)
        report["status"]="partial_form_selection"
        report["next_step"]="Municipality autocomplete and institution must be resolved from live form."
    except Exception as e:
        report["status"]="blocked_or_failed"
        report["error"]=str(e)[:650]
    finally:
        (OUT/"report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
        browser.close()
# The pilot deliberately does not claim a historical value was recovered.
if report["status"]=="blocked_or_failed": raise SystemExit(1)
