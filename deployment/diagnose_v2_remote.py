#!/usr/bin/env python3
"""Read-only external endpoint diagnostics. No authentication, deploy or mutation."""
import argparse,json,urllib.request,urllib.error,datetime,pathlib
p=argparse.ArgumentParser();p.add_argument("--base-url",required=True);p.add_argument("--report",type=pathlib.Path,required=True);a=p.parse_args()
paths=["/data/manifest.json","/data/api/v2/manifest.json","/data/api/v2/catalog/municipalities.json"]
results=[]
for path in paths:
 req=urllib.request.Request(a.base_url.rstrip("/")+path,headers={"User-Agent":"financas-sp-v2-readonly-diagnostic/1","Accept":"application/json"})
 try:
  with urllib.request.urlopen(req,timeout=25) as r:
   raw=r.read(2048);results.append({"path":path,"status":r.status,"final_url":r.url,"content_type":r.headers.get("Content-Type"),"sample_json":raw.lstrip().startswith((b"{",b"["))})
 except urllib.error.HTTPError as e:
  results.append({"path":path,"status":e.code,"final_url":e.url,"content_type":e.headers.get("Content-Type"),"error":"http"})
 except Exception as e:results.append({"path":path,"status":None,"error":type(e).__name__})
report={"checked_at_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"base_url":a.base_url,"results":results,
"v2_accessible":any(r["path"]=="/data/api/v2/manifest.json" and r["status"]==200 and r.get("sample_json") for r in results),
"notes":"Does not infer absence of v2 artifact from 403; deployment source and access rules require separate inspection."}
a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n")
print(json.dumps(report,ensure_ascii=False))
