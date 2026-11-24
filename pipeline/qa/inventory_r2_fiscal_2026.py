"""Read-only paginated R2 object inventory, no financial promotion."""
import os,json,hashlib
from pathlib import Path
from datetime import datetime,timezone
from urllib.request import Request,urlopen
from urllib.parse import urlencode
from collections import Counter
base="https://api.cloudflare.com/client/v4/accounts/"+os.environ["CLOUDFLARE_ACCOUNT_ID"]+"/r2/buckets/"+os.environ["CLOUDFLARE_R2_BUCKET"]+"/objects"
headers={"Authorization":"Bearer "+os.environ["CLOUDFLARE_API_TOKEN"],"Accept":"application/json"}
out=Path("build/r2_inventory");out.mkdir(parents=True,exist_ok=True)
objects={}
for prefix in ("tcesp/","sp_645/"):
    cursor=None;seen=set()
    while True:
        q={"prefix":prefix,"per_page":1000}
        if cursor:q["cursor"]=cursor
        with urlopen(Request(base+"?"+urlencode(q),headers=headers),timeout=90) as response:
            data=json.load(response)
        if not data.get("success"):raise RuntimeError("R2 list failed")
        result=data["result"]
        info=data.get("result_info") or {}
        if isinstance(result,dict):
            items=result.get("objects",[])
            nxt=result.get("cursor") or info.get("cursor")
            truncated=result.get("truncated",info.get("is_truncated",False))
        elif isinstance(result,list):
            items=result;nxt=info.get("cursor");truncated=info.get("is_truncated",False)
        else:raise ValueError("unexpected list response")
        for item in items:
            key=item.get("key")
            if not key or not key.startswith(prefix) or key in objects:raise ValueError("invalid or duplicate key")
            objects[key]={k:item.get(k) for k in ("key","size","uploaded","etag")}
        if not nxt:
            if truncated or len(items)>=1000:raise ValueError("pagination not certified complete")
            break
        if nxt in seen:raise ValueError("repeated cursor")
        seen.add(nxt);cursor=nxt
rows=[objects[k] for k in sorted(objects)]
raw=json.dumps(rows,ensure_ascii=False,sort_keys=True).encode()
(out/"objects.json").write_bytes(raw)
fiscal=[r for r in rows if "2026" in r["key"] and any(s in r["key"].lower() for s in ("tcesp","siconfi","rreo","rgf","msc","dca","audesp"))]
summary={"checked_utc":datetime.now(timezone.utc).isoformat(),"objects":len(rows),"prefix_counts":dict(Counter(r["key"].split("/")[0] for r in rows)),"fiscal_2026_candidates":len(fiscal),"candidate_keys":[r["key"] for r in fiscal if any(s in r["key"].lower() for s in ("manifest","qa.json","normalized","parcial"))][:120],"inventory_sha256":hashlib.sha256(raw).hexdigest(),"public_release_authorized":False,"note":"Object existence only; no verification of content, period, or financial validity."}
(out/"summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2))
print("R2_FISCAL_INVENTORY",json.dumps(summary,ensure_ascii=False))
