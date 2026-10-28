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
        ente = page.locator('[id="formHistorico:ente_input"]')
        if not ente.is_disabled():
            ente.click()
            ente.press("ControlOrMeta+A")
            ente.press_sequentially("Taubaté", delay=120)
            page.wait_for_timeout(4000)
            report["autocomplete_dom"] = page.evaluate("""() => Array.from(document.querySelectorAll('[id*="ente_panel"]')).map(e=>({id:e.id,visible:e.getClientRects().length>0,text:e.textContent.trim().slice(0,800),html:e.outerHTML.slice(0,1400)}))""")
            report["suggestions"] = page.evaluate("""() => Array.from(document.querySelectorAll('[id*="ente_panel"] li,[id*="ente_panel"] tr,[id*="ente_panel"] [role="option"]')).map(e=>({id:e.id,visible:e.getClientRects().length>0,text:e.textContent.trim().slice(0,140)})).slice(0,20)""")
            report["ente_hidden_value"] = page.locator('[id="formHistorico:ente_hinput"]').input_value()
            candidate=page.locator('[id="formHistorico:ente_panel"] li[data-item-value="3554102"]')
            report["candidate_count"]=candidate.count()
            if candidate.count()==1 and candidate.is_visible():
                candidate.click()
                page.wait_for_timeout(2300)
                report["municipality_selected"]=True
                report["selected_ente_hidden"]=page.locator('[id="formHistorico:ente_hinput"]').input_value()
                orgao=page.locator('[id="formHistorico:orgao_input"]')
                report["orgao_after_selection_disabled"]=orgao.is_disabled() if orgao.count() else None
                report["controls_after_municipality"]=control_snapshot(page,"municipality")
                orgao=page.locator('[id="formHistorico:orgao_input"]')
                if not orgao.is_disabled():
                    orgao.click()
                    orgao.press_sequentially("Prefeitura",delay=95)
                    page.wait_for_timeout(3200)
                    report["orgao_candidates"]=page.evaluate("""() => Array.from(document.querySelectorAll('[id*="orgao_panel"] li')).slice(0,15).map(e=>({name:e.textContent.trim().slice(0,160),value:e.getAttribute('data-item-value'),visible:e.getClientRects().length>0}))""")
                    report["orgao_hidden_before_selection"]=page.locator('[id="formHistorico:orgao_hinput"]').input_value()
                    option=page.locator('[id="formHistorico:orgao_panel"] li[data-item-value="7953"]')
                    report["verified_orgao_option_count"]=option.count()
                    if option.count()==1 and option.is_visible():
                        option.click()
                        page.wait_for_timeout(1700)
                        report["institution_selected"]=True
                        report["orgao_hidden_after_selection"]=page.locator('[id="formHistorico:orgao_hinput"]').input_value()
                        report["form_buttons"]=page.evaluate("""() => [...document.querySelectorAll('#formHistorico button,#formHistorico input[type="submit"]')].map(e=>({id:e.id,text:e.textContent.trim().slice(0,90),disabled:e.disabled}))""")
                        page.screenshot(path=str(OUT/"institution_selected.png"),full_page=False)
                        report["before_query_ui"] = page.locator("#formHistorico").inner_text()[-900:]
                        query = page.get_by_role("button", name="Consultar", exact=True)
                        if query.count()==1:
                            query.click()
                            page.wait_for_timeout(4500)
                            report["query_clicked"] = True
                            report["after_query_text"] = page.locator("body").inner_text()[-3000:]
                            report["human_verification_detected"]=page.locator('iframe[src*="captcha"],iframe[src*="recaptcha"],[class*="hcaptcha"],[id*="hcaptcha"]').count()>0
                            report["history_retrieved"]=False
                            if report["human_verification_detected"]:
                                report["status"]="human_verification_required"

                            report["after_query_messages"] = page.locator(".ui-messages,.ui-message,.ui-growl,.ui-state-error").all_inner_texts()
                            page.screenshot(path=str(OUT/"after_query.png"),full_page=False)
                            if not report.get("human_verification_detected"): report["status"] = "query_attempted_results_unverified"


                    page.screenshot(path=str(OUT/"orgao_autocomplete.png"),full_page=False)

                page.screenshot(path=str(OUT/"selected_municipality.png"),full_page=False)
            report["ente_text"] = ente.input_value()
            page.screenshot(path=str(OUT/"autocomplete.png"),full_page=False)
        if not report.get("query_clicked"): report["status"]="partial_form_selection"
        report["next_step"]="Municipality autocomplete and institution must be resolved from live form."
    except Exception as e:
        report["status"]="blocked_or_failed"
        report["error"]=str(e)[:650]
    finally:
        (OUT/"report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
        browser.close()
# The pilot deliberately does not claim a historical value was recovered.
if report["status"]=="blocked_or_failed": raise SystemExit(1)
