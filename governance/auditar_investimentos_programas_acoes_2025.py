#!/usr/bin/env python3
"""Audit TCESP investment decomposition in original 2025 municipal ZIPs against preserved RMJ artifacts."""
import collections,csv,decimal,hashlib,io,json,os,pathlib,sys,urllib.request,zipfile
ROOT=pathlib.Path("build/tcesp-investimentos-programas-acoes")
ROOT.mkdir(parents=True,exist_ok=True)
CASES={"jundiai":"Jundiaí","louveira":"Louveira"}
YEAR=2025
reference=pathlib.Path(sys.argv[1])
D=decimal.Decimal
report={"ano":YEAR,"cases":[],"source":"TCESP","reference_artifact":reference.name}
for slug,name in CASES.items():
 url=f"https://transparencia.tce.sp.gov.br/sites/default/files/csv/despesas-{slug}-{YEAR}.zip"
 case={"slug":slug,"municipio":name,"url":url}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"}),timeout=210) as response:
   data=response.read(120000000)
  if len(data)>=120000000:raise ValueError("ZIP too large")
  z=zipfile.ZipFile(io.BytesIO(data))
  files=[s for s in z.namelist() if s.lower().endswith(".csv")]
  if len(files)!=1:raise ValueError("Unexpected CSV member count")
  programs=collections.Counter();actions=collections.Counter();by_stage=collections.Counter()
  count=0;invalid=0;months=set()
  with z.open(files[0]) as source:
   rdr=csv.DictReader(io.TextIOWrapper(source,encoding="latin-1",newline=""),delimiter=";")
   fields=rdr.fieldnames
   needed={"ds_elemento","tp_despesa","vl_despesa","cd_programa","ds_programa","cd_acao","ds_acao"}
   if not needed.issubset(fields):raise ValueError("Missing columns "+str(sorted(needed-set(fields))))
   for row in rdr:
    count+=1
    code=(row.get("ds_elemento") or "").split(" - ",1)[0].strip()
    if not code.startswith("44"):continue
    stage=(row.get("tp_despesa") or "").strip().casefold()
    try:
     value=D((row.get("vl_despesa") or "").replace(".","").replace(",", "."))*100
     if not value.is_finite() or value!=value.to_integral_value():raise ValueError("fractional cents")
     cents=int(value)
    except (decimal.InvalidOperation,ValueError):
     invalid+=1;continue
    by_stage[stage]+=cents
    if stage!="valor liquidado":continue
    months.add((row.get("mes_referencia") or "").strip())
    p=((row.get("cd_programa") or "").strip(),(row.get("ds_programa") or "").strip())
    a=(p[0],(row.get("cd_acao") or "").strip(),(row.get("ds_acao") or "").strip())
    programs[p]+=cents;actions[a]+=cents
  total=sum(programs.values())
  candidates=list(reference.rglob(f"*{slug}*{YEAR}*.json"))
  if len(candidates)!=1:raise ValueError("Reference artifact file unresolved: "+str([str(x) for x in candidates]))
  old=json.loads(candidates[0].read_text(encoding="utf-8"))
  expected=old["investimento_44_liquidado_centavos"]
  refprogram={(str(x[0]).strip(),str(x[1]).strip()):int(x[-1]) for x in old["programas_44_liquidado_completos"]}
  refactions={(str(x[0]).strip(),str(x[1]).strip(),str(x[2]).strip()):int(x[-1]) for x in old["acoes_44_liquidado_completas"]}
  case.update({"sha256_zip":hashlib.sha256(data).hexdigest(),"rows":count,"months_liquidado":sorted(months),"programs":len(programs),"actions":len(actions),"invalid_values":invalid,"investment_liquidated_cents":total,"reference_total_cents":expected,"program_total_equals_actions":total==sum(actions.values()),"total_matches_preserved_reference":total==expected,"programs_match_preserved_reference":dict(programs)==refprogram,"actions_match_preserved_reference":dict(actions)==refactions,"stages_cents":dict(by_stage)})
 except Exception as exc:case["error"]=type(exc).__name__+": "+str(exc)
 report["cases"].append(case)
report["all_pass"]=all("error" not in x and x["invalid_values"]==0 and x["program_total_equals_actions"] and x["total_matches_preserved_reference"] and x["programs_match_preserved_reference"] and x["actions_match_preserved_reference"] for x in report["cases"])
(ROOT/"qa.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(report,ensure_ascii=False,indent=2))
if not report["all_pass"]:sys.exit(1)
