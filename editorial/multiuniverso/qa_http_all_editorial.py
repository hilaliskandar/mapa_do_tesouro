#!/usr/bin/env python3
"""Gate HTTP completo dos 10 boletins e 280 fichas em projeto isolado."""
import argparse,hashlib,json,urllib.request,urllib.error
from pathlib import Path

def main():
 p=argparse.ArgumentParser()
 p.add_argument("--bundle",type=Path,required=True)
 p.add_argument("--root",default="https://financas-e2-homologacao.pages.dev")
 p.add_argument("--out",type=Path,required=True)
 a=p.parse_args()
 m=json.loads((a.bundle/"publicacoes/manifest.json").read_text(encoding="utf-8"))
 routes=["/data/api/v1/publication/universes.json"]
 for e in m["editions"]:
  routes.append(f'/publicacoes/{e["publication_id"]}/index.html')
 for entry in m["municipal_profiles"]:
  routes.append(f'/publicacoes/{entry["publication_id"]}/municipios/{entry["codigo_ibge"]}.html')
 report={"root":a.root,"expected_routes":len(routes),"passed":0,"failures":[]}
 for route in routes:
  local=a.bundle/route.lstrip("/")
  expected=hashlib.sha256(local.read_bytes()).hexdigest()
  try:
   req=urllib.request.Request(a.root.rstrip("/")+route,headers={"User-Agent":"E2-homologacao-externa/1.0"})
   with urllib.request.urlopen(req,timeout=25) as response:
    data=response.read()
    if response.status!=200:raise ValueError(f"HTTP {response.status}")
    if hashlib.sha256(data).hexdigest()!=expected:raise ValueError("SHA divergente do pacote")
   report["passed"]+=1
  except (urllib.error.HTTPError,urllib.error.URLError,ValueError) as exc:
   report["failures"].append({"route":route,"error":str(exc)})
   if len(report["failures"])>=10:break
 a.out.parent.mkdir(parents=True,exist_ok=True)
 a.out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print(json.dumps({k:v for k,v in report.items() if k!="failures"}))
 if report["failures"]:print(json.dumps(report["failures"],ensure_ascii=False))
 return not report["failures"] and report["passed"]==len(routes)
if __name__=="__main__":raise SystemExit(0 if main() else 1)
