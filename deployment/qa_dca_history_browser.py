import csv,io,json
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
base="http://127.0.0.1:8765"
checks=[]
with sync_playwright() as p:
    browser=p.chromium.launch()
    for viewport in ({"width":1440,"height":900},{"width":390,"height":844}):
        page=browser.new_page(viewport=viewport,accept_downloads=True)
        errors=[]
        page.on("pageerror",lambda e:errors.append(str(e)))
        page.goto(base,wait_until="networkidle")
        expect(page.locator("#history-tab")).to_be_visible(timeout=60000)
        page.locator("#history-tab").click()
        expect(page.locator("#history-body tr")).to_have_count(13)
        expect(page.locator("#history-variable option")).to_have_count(26)
        page.select_option("#history-scope","regional")
        expect(page.locator("#history-title")).to_contain_text("São Paulo")
        expect(page.locator("#history-export")).to_be_enabled()
        with page.expect_download() as download:
            page.locator("#history-export").click()
        rows=list(csv.DictReader(io.StringIO(Path(download.value.path()).read_text(encoding="utf-8-sig")),delimiter=";"))
        assert len(rows)==13 and all(r["recorte"]=="SP_645" and r["municipios"]=="645" for r in rows)
        page.select_option("#universe-select","RA_SEADE_04")
        expect(page.locator("#history-title")).to_contain_text("Campinas",timeout=60000)
        expect(page.locator("#history-export")).to_be_enabled()
        with page.expect_download() as download:
            page.locator("#history-export").click()
        rows=list(csv.DictReader(io.StringIO(Path(download.value.path()).read_text(encoding="utf-8-sig")),delimiter=";"))
        assert len(rows)==13 and all(r["recorte"]=="RA_SEADE_04" and r["municipios"]=="90" for r in rows)
        assert not errors,errors
        checks.append({"viewport":viewport,"status":"pass","years":13,"variables":26,"regional_csv":"pass"})
        page.close()
    browser.close()
Path("build/private_history/qa_browser.json").write_text(json.dumps(checks,indent=2))
print("DCA_HISTORY_BROWSER",json.dumps(checks))
