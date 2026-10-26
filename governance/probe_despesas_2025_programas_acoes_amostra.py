#!/usr/bin/env python3
"""Sample first 8 MB of TCESP statewide expense deflate stream via HTTP range. No full download."""
import collections,csv,decimal,io,json,pathlib,urllib.request,zlib,hashlib
url="https://transparencia.tce.sp.gov.br/sites/default/files/conjunto-dados/despesas-2025.zip"
out=pathlib.Path("build/tcesp-despesas-2025-mostra");out.mkdir(parents=True,exist_ok=True)
req=urllib.request.Request(url,headers={"Range":"bytes=0-8388607","Accept-Encoding":"identity","User-Agent":"Mozilla/5.0"})
with urllib.request.urlopen(req,timeout=180) as r:
 if r.status!=206:raise RuntimeError("Range not honored")
 raw=r.read(8388608)
assert raw[:4]==b"PK\x03\x04"
n=int.from_bytes(raw[26:28],"little");e=int.from_bytes(raw[28:30],"little")
decomp=zlib.decompressobj(-15)
plain=decomp.decompress(raw[30+n+e:])
lines=plain.decode("latin-1").splitlines()
if not plain.endswith((b"\n",b"\r")):lines=lines[:-1]
reader=csv.DictReader(lines,delimiter=";")
seen=collections.Counter();by_prog=collections.Counter();by_action=collections.Counter();stages=collections.Counter();problems=collections.Counter();total=0
for row in reader:
 total+=1
 code=(row.get("ds_elemento") or "").split(" - ",1)[0]
 if not code.startswith("44"):continue
 stage=(row.get("tp_despesa") or "").strip()
 try:
  val=decimal.Decimal((row.get("vl_despesa") or "").replace(".","").replace(",","."))*100
  if not val.is_finite() or val!=val.to_integral_value():raise ValueError()
  cents=int(val)
 except (decimal.InvalidOperation,ValueError):
  problems["invalid_cents"]+=1;continue
 stages[stage]+=cents
 if stage.casefold()!="valor liquidado":continue
 city=row.get("codigo_municipio_ibge","")
 program=(city,row.get("ds_orgao",""),row.get("cd_programa",""),row.get("ds_programa",""))
 action=program+(row.get("cd_acao",""),row.get("ds_acao",""))
 by_prog[program]+=cents;by_action[action]+=cents;seen[city]+=1
report={"source_url":url,"sample_only":True,"compressed_range_bytes":len(raw),"sample_sha256":hashlib.sha256(raw).hexdigest(),"records_complete":total,"columns":reader.fieldnames,"group_44_liquidado_rows_by_municipio":dict(seen),"group_44_liquidado_programs":len(by_prog),"group_44_liquidado_actions":len(by_action),"programs_sum_centavos":sum(by_prog.values()),"actions_sum_centavos":sum(by_action.values()),"totals_equal":sum(by_prog.values())==sum(by_action.values()),"stages_44_centavos":dict(stages),"problems":dict(problems),"note":"Contiguous prefix, not a representative statistical sample; cannot infer statewide coverage."}
(out/"qa.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps({k:v for k,v in report.items() if k!="columns"},ensure_ascii=False))
if not report["totals_equal"] or problems:raise SystemExit(1)
