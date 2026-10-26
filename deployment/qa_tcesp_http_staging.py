#!/usr/bin/env python3
"""Test HTTP delivery of the staged TCESP API without a public deployment."""
import argparse,hashlib,http.server,json,pathlib,socketserver,threading,urllib.request
p=argparse.ArgumentParser();p.add_argument("--site",type=pathlib.Path,required=True);p.add_argument("--report",type=pathlib.Path,required=True);a=p.parse_args()
root=a.site.resolve()
class Handler(http.server.SimpleHTTPRequestHandler):
 def __init__(self,*args,**kwargs):super().__init__(*args,directory=str(root),**kwargs)
 def log_message(self,*args):pass
class Server(socketserver.ThreadingMixIn,http.server.HTTPServer):daemon_threads=True
with Server(("127.0.0.1",0),Handler) as server:
 thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
 base=f"http://127.0.0.1:{server.server_address[1]}"
 paths=["data/api/v2/manifest.json","data/api/v2/tcesp/manifest.json","tcesp-investimentos.html","tcesp-investimentos.js"]
 for year in (2023,2024,2025):
  paths.append(f"data/api/v2/tcesp/{year}/municipios.json")
  for code in ("3509502","3525904","3543402"):
   paths.append(f"data/api/v2/tcesp/{year}/municipios/{code}.json")
 results=[]
 for path in paths:
  with urllib.request.urlopen(base+"/"+path,timeout=12) as response:
   assert response.status==200
   raw=response.read()
   if path.endswith(".json"): json.loads(raw)
   else:
    assert raw and (b"TCESP" in raw or b"investimentos" in raw)
   original=(root/path).read_bytes()
   assert raw==original
   results.append({"path":path,"status":response.status,"bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest()})
 server.shutdown()
a.report.parent.mkdir(parents=True,exist_ok=True)
a.report.write_text(json.dumps({"status":"pass","checked":len(results),"results":results},indent=2)+"\n")
print(json.dumps({"status":"pass","http_gets":len(results)}))
