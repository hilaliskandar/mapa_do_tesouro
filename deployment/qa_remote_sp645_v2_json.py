#!/usr/bin/env python3
"""Fail-closed external QA for the SP645 API v2 JSON endpoints."""
import argparse,json,pathlib,urllib.request
p=argparse.ArgumentParser();p.add_argument("--url",required=True);p.add_argument("--report",type=pathlib.Path,required=True);a=p.parse_args()
root=a.url.rstrip("/")
paths={"manifest":"/data/api/v2/manifest.json","municipalities":"/data/api/v2/catalog/municipalities.json","variables":"/data/api/v2/catalog/variables.json"}
details={}
for key,path in paths.items():
 req=urllib.request.Request(root+path,headers={"Accept":"application/json","User-Agent":"sp645-v2-json-qa/1"})
 with urllib.request.urlopen(req,timeout=35) as resp:
  raw=resp.read()
  typ=resp.headers.get("Content-Type","")
  if resp.status!=200 or "json" not in typ.lower():raise ValueError(f"{path}: HTTP {resp.status}, content-type {typ}; JSON required")
  data=json.loads(raw)
  details[key]={"status":resp.status,"content_type":typ,"bytes":len(raw)}
  if key=="manifest":
   assert data["municipality_count"]==645
   assert data["variable_catalog_count"]==75
  if key=="municipalities":assert isinstance(data,list) and len(data)==645
  if key=="variables":assert isinstance(data,dict) and len(data["variables"])==75
result={"status":"pass","base_url":root,"checks":details}
a.report.parent.mkdir(parents=True,exist_ok=True)
a.report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
print(json.dumps(result,ensure_ascii=False))
