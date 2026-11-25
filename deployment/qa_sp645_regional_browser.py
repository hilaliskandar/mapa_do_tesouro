"""Read-only browser regression of the isolated regional preview."""
import csv,json,io
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
BASE="https://sp645-regional-v050-qa.finbra-tic-tim-referencia.pages.dev"
out=Path("build/qa_regional_browser.json");out.parent.mkdir(parents=True,exist_ok=True)
checks=[]
with sync_playwright() as p:
    browser=p.chromium.launch()
    for viewport in ({"width":1440,"height":900},{"width":390,"height":844}):
        page=browser.new_page(viewport=viewport,accept_downloads=True)
        errors=[]
        page.on("pageerror",lambda exc:errors.append(str(exc)))
        page.goto(BASE,wait_until="networkidle",timeout=90000)
        page.wait_for_function("document.querySelector('#universe-select').options.length === 72 && document.querySelectorAll('#municipal-map path').length === 645",timeout=90000)
        catalog=page.request.get(BASE+"/data/universes.json").json()
        for uid in ("RA_SEADE_04","RG_SEADE_01","RM_RIBEIRAO_PRETO","SP_645"):
            target=next(x for x in catalog if x["universo_id"]==uid)
            count=target["municipality_count"]
            page.select_option("#universe-select",uid)
            page.wait_for_function("""([count,uid])=>document.querySelector('#universe-select').value===uid && document.querySelector('#municipality-select').options.length===count && document.querySelectorAll('#municipal-map path').length===count && document.querySelectorAll('#compare-body tr').length===count""",arg=[count,uid],timeout=90000)
            page.locator(".tab[data-target=map]").click()
            assert page.locator("#municipal-map").is_visible()
            page.locator(".tab[data-target=series]").click()
            assert page.locator("#series-table-wrap").inner_text().strip()
            with page.expect_download() as dl:page.locator("#export-csv").click()
            d=dl.value
            rows=list(csv.DictReader(io.StringIO(Path(d.path()).read_text(encoding="utf-8-sig"))))
            assert len(rows)==count and len({r["codigo_ibge"] for r in rows})==count
            assert uid in d.suggested_filename
            checks.append({"viewport":viewport,"universe":uid,"municipalities":count,"map_csv_series":"pass"})
        page.select_option("#universe-select","RA_SEADE_09")
        expect(page.locator("#regional-hierarchy-select")).to_have_value("RA_SEADE_09",timeout=90000)
        expect(page.locator("#municipal-map path")).to_have_count(53,timeout=90000)
        assert page.locator("#regional-hierarchy-select").locator("option[value='RG_SEADE_01']").count()==1
        page.select_option("#regional-hierarchy-select","RG_SEADE_01")
        expect(page.locator("#universe-select")).to_have_value("RG_SEADE_01",timeout=90000)
        expect(page.locator("#municipal-map path")).to_have_count(12,timeout=90000)
        page.select_option("#regional-hierarchy-select","RA_SEADE_09")
        expect(page.locator("#universe-select")).to_have_value("RA_SEADE_09",timeout=90000)
        expect(page.locator("#municipal-map path")).to_have_count(53,timeout=90000)
        checks.append({"viewport":viewport,"hierarchy":"RA_SEADE_09 -> RG_SEADE_01 -> RA_SEADE_09","status":"pass"})
        assert not errors,errors
        page.close()
    browser.close()
out.write_text(json.dumps({"status":"pass","checks":checks},ensure_ascii=False,indent=2))
print("REGIONAL_BROWSER_PASS",json.dumps(checks,ensure_ascii=False))
