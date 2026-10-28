#!/usr/bin/env python3
"""Non-authenticated inspection of the public Siconfi DCA history form."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

URL = "https://siconfi.tesouro.gov.br/siconfi/pages/public/consulta_historico_declaracoes/historico_declaracoes_list.jsf"
OUT = Path("siconfi-history-qa")
OUT.mkdir(exist_ok=True)
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(accept_downloads=True, locale="pt-BR")
    report = {"url": URL, "status": "not_queried", "municipal_results": False}
    try:
        response = page.goto(URL, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(3000)
        report["http_status"] = response.status if response else None
        report["title"] = page.title()
        report["form_present"] = page.locator("#formHistorico").count() > 0
        selectors = ["esfera", "ente", "poder", "exercicio", "tipoDemonstrativo", "escopo"]
        report["controls"] = {
            key: page.locator(f'[id="formHistorico:{key}"]').count() > 0
            for key in selectors
        }
        # Capture only the initial form. No attempts to bypass login or captcha.
        report["initial_form_only"] = True
        page.screenshot(path=str(OUT / "form.png"), full_page=False)
        if not report["form_present"]:
            raise RuntimeError("Siconfi history form was not found")
        report["status"] = "form_inventory_ok"
    except Exception as exc:
        report["status"] = "blocked_or_failed"
        report["error"] = str(exc)[:600]
    finally:
        (OUT / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        browser.close()
if report["status"] != "form_inventory_ok":
    raise SystemExit(1)
