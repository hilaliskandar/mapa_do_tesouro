#!/usr/bin/env python3
"""Independent month-by-month TCESP state/municipal parity sample. Read only."""
import collections,csv,decimal,hashlib,io,json,pathlib,urllib.request,zipfile
YEAR=2025
CITIES={"jundiai":"Jundiaí","ribeirao-preto":"Ribeirão Preto","sertaozinho":"Sertãozinho","louveira":"Louveira"}
OUT=pathlib.Path("build/tcesp-paridade-amostra");OUT.mkdir(parents=True,exist_ok=True)
BASE="https://transparencia.tce.sp.gov.br/sites/default/files"
def fetch(url,limit=70000000):
 with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"}),timeout=240) as r: data=r.read(limit+1)
 if len(data)>limit:raise ValueError("Exceeds byte limit")
 return data
def key(s):
 import unicodedata,re
 s="".join(x for x in unicodedata.normalize("NFKD",s) if not unicodedata.combining(x))
 return re.sub("[^a-z0-9]+","",s.casefold())
def values(data,selected=None):
 out=collections.defaultdict(lambda:collections.Counter());counts=collections.Counter();cols=None;bad=0
 with zipfile.ZipFile(io.BytesIO(data)) as z:
  files=[f for f in z.namelist() if f.endswith(".csv")]
  assert len(files)==1,files
  with z.open(files[0]) as stream:
   rd=csv.DictReader(io.TextIOWrapper(stream,encoding="latin-1",newline=""),delimiter=";")
   cols=rd.fieldnames
   for row in rd:
    city=(row.get("ds_municipio") or "").strip()
    if selected is not None and key(city) not in selected:continue
    month=(row.get("mes_referencia") or "").strip()
    if not month.isdigit() or not 1<=int(month)<=12:bad+=1;continue
    try:
     val=decimal.Decimal(row["vl_arrecadacao"].strip().replace(".","").replace(",", "."))*100
     assert val.is_finite() and val==val.to_integral_value()
    except (ValueError,AssertionError,decimal.InvalidOperation):bad+=1;continue
    out[key(city)][month]+=int(val);counts[key(city)]+=1
 return {"months":{k:dict(v) for k,v in out.items()},"counts":dict(counts),"columns":cols,"invalid":bad}
result={"year":YEAR,"source":"TCESP","cases":[]}
surl=f"{BASE}/conjunto-dados/receitas-{YEAR}.zip"
state=fetch(surl)
st=values(state,{key(x) for x in CITIES.values()})
result["state_sha256"]=hashlib.sha256(state).hexdigest()
for slug,name in CITIES.items():
 url=f"{BASE}/csv/receitas-{slug}-{YEAR}.zip"
 rec={"municipio":name,"slug":slug}
 try:
  data=fetch(url)
  m=values(data)
  k=key(name)
  s=st["months"].get(k,{})
  local=m["months"].get(k,{})
  rec.update({"state_rows":st["counts"].get(k,0),"municipal_rows":m["counts"].get(k,0),"state_months":sorted(map(int,s)),"municipal_months":sorted(map(int,local)),"monthly_total_equal":s==local,"row_count_equal":st["counts"].get(k,0)==m["counts"].get(k,0),"columns_equal":st["columns"]==m["columns"],"delta_months_centavos":{str(i):s.get(str(i),0)-local.get(str(i),0) for i in range(1,13) if s.get(str(i),0)!=local.get(str(i),0)},"municipal_zip_sha256":hashlib.sha256(data).hexdigest(),"invalid_values":m["invalid"]})
 except Exception as e:rec["error"]=type(e).__name__+": "+str(e)
 result["cases"].append(rec)
result["all_comparable"]=all("error" not in v and v["monthly_total_equal"] and v["row_count_equal"] and v["columns_equal"] for v in result["cases"])
(OUT/"qa.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(result,ensure_ascii=False))
