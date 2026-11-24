#!/usr/bin/env python3
"""HTTP smoke of private RMRP FED07 static build; no external network.
Use: python deployment/qa_rmrp_fed07_local_http.py PRIVATE_SITE_DIR
This is NOT browser visual QA, Cloudflare Pages deployment, or a public release.
"""
import argparse, functools, http.server, json, threading, urllib.request
from pathlib import Path
from pipeline.qa.validate_rmrp_api_v3_fed07 import validate

PREFIX="data/api/v3/investimentos/rmrp"
class QuietServer(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*args):pass

def smoke(site):
    site=Path(site).resolve()
    assert (site/".rmrp-fed07-private-preview").is_file(),"Private marker required"
    api=site/PREFIX
    q=validate(api)
    paths=["index.html","app.js","styles.css",f"{PREFIX}/manifest.json",
           f"{PREFIX}/municipios.json",f"{PREFIX}/pendencias.json"]
    paths += [f.relative_to(site).as_posix() for f in sorted(api.rglob("*.json"))]
    paths=list(dict.fromkeys(paths))
    handler=functools.partial(QuietServer,directory=str(site))
    server=http.server.ThreadingHTTPServer(("127.0.0.1",0),handler)
    port=server.server_address[1]
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    results={"status":"ok","url_scope":"localhost_only","http_ok":0,
             "json_checked":0,"json_invalid":0,"non_200":[],
             "api_technical_checks":q["technical_checks_passed"],
             "public_release_authorized":False}
    try:
        for p in paths:
            with urllib.request.urlopen(f"http://127.0.0.1:{port}/{p}",timeout=5) as r:
                if r.status!=200:
                    results["non_200"].append({"path":p,"status":r.status})
                    continue
                body=r.read()
                results["http_ok"]+=1
                if p.endswith(".json"):
                    json.loads(body)
                    results["json_checked"]+=1
    finally:
        server.shutdown();server.server_close();thread.join(timeout=4)
    assert not results["non_200"]
    assert results["json_checked"]>=285
    assert results["http_ok"]>=288
    return results

if __name__=="__main__":
    ap=argparse.ArgumentParser();ap.add_argument("site",type=Path)
    print(json.dumps(smoke(ap.parse_args().site),ensure_ascii=False))
