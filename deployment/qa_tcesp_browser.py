#!/usr/bin/env python3
"""Real Chromium interaction gate for TCESP standalone preview, no external deployment."""
import argparse,http.server,json,pathlib,socketserver,threading
from playwright.sync_api import sync_playwright
p=argparse.ArgumentParser();p.add_argument("--site",type=pathlib.Path,required=True);p.add_argument("--report",type=pathlib.Path,required=True);a=p.parse_args()
class Handler(http.server.SimpleHTTPRequestHandler):
 def __init__(self,*args,**kwargs):super().__init__(*args,directory=str(a.site.resolve()),**kwargs)
 def log_message(self,*args):pass
class Server(socketserver.ThreadingMixIn,http.server.HTTPServer):daemon_threads=True
events=[]
with Server(("127.0.0.1",0),Handler) as server:
 threading.Thread(target=server.serve_forever,daemon=True).start()
 url=f"http://127.0.0.1:{server.server_address[1]}/tcesp-investimentos.html"
 with sync_playwright() as pw:
  browser=pw.chromium.launch(headless=True,args=["--no-sandbox"])
  page=browser.new_page()
  errors=[];page.on("pageerror",lambda err:errors.append(str(err)))
  page.goto(url,wait_until="networkidle")
  page.locator("#status").get_by_text("Consulta concluída.").wait_for(timeout=30000)
  assert page.locator("#resultado tr").count()>0
  assert "valor liquidado" in page.locator("#total").inner_text()
  events.append("default_2025_liquidado_programas")
  page.locator("#nivel").select_option("acoes")
  assert page.locator("#resultado tr").count()>0
  events.append("change_to_actions")
  page.locator("#ano").select_option("2023")
  page.locator("#consultar").click()
  page.locator("#status").get_by_text("Consulta concluída.").wait_for(timeout=30000)
  assert page.locator("#resultado tr").count()>0
  events.append("change_year_2023")
  page.locator("#filtro").fill("zzzx-nenhuma-ocorrencia")
  assert page.locator("#resultado tr").count()==0
  events.append("filter_zero_rows")
  page.locator("#filtro").fill("")
  assert page.locator("#resultado tr").count()>0
  events.append("clear_filter")
  page.locator("#municipio").fill("352590")
  page.locator("#consultar").click()
  assert "código IBGE válido" in page.locator("#status").inner_text()
  events.append("invalid_ibge_rejected")
  page.locator("#municipio").fill("3525904")
  page.locator("#consultar").click()
  page.locator("#status").get_by_text("Consulta concluída.").wait_for(timeout=30000)
  assert page.locator("#resultado tr").count()>0
  events.append("recover_after_invalid")
  assert not errors,errors
  browser.close()
 server.shutdown()
report={"status":"pass","tests":events,"js_errors":[],"browser":"chromium_headless"}
a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n")
print(json.dumps(report,ensure_ascii=False))
