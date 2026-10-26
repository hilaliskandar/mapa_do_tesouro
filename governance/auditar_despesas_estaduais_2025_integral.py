#!/usr/bin/env python3
"""Read-only complete TCESP statewide expenses 2025 audit by municipality / program / action.
No secrets, no R2 writes; refuses invalid rows, broken ZIP and incomplete processing.
"""
import collections,csv,decimal,hashlib,json,os,pathlib,tempfile,urllib.request,zipfile
YEAR=2025
URL=f"https://transparencia.tce.sp.gov.br/sites/default/files/conjunto-dados/despesas-{YEAR}.zip"
OUT=pathlib.Path("build/tcesp-despesas-2025-integral");OUT.mkdir(parents=True,exist_ok=True)
ZIP=OUT/"source.zip"
sha=hashlib.sha256()
req=urllib.request.Request(URL,headers={"User-Agent":"Mozilla/5.0 (TCESP QA, readonly)","Accept-Encoding":"identity"})
with urllib.request.urlopen(req,timeout=240) as resp,ZIP.open("wb") as f:
 while True:
  block=resp.read(4*1024*1024)
  if not block:break
  f.write(block);sha.update(block)
 if int(resp.headers.get("Content-Length","0")) not in (0,ZIP.stat().st_size):raise RuntimeError("Truncated transfer")
print("ZIP downloaded, bytes",ZIP.stat().st_size,flush=True)
groups=collections.Counter();progs=collections.Counter();actions=collections.Counter()
month_presence=collections.defaultdict(set);rows_by_city=collections.Counter()
issues=collections.Counter();stages=collections.Counter();rows=0;investment_rows=0
D=decimal.Decimal
with zipfile.ZipFile(ZIP) as archive:
 assert archive.testzip() is None,"ZIP CRC failed"
 files=[f for f in archive.namelist() if f.lower().endswith(".csv")]
 if len(files)!=1:raise RuntimeError("Unexpected members "+str(files))
 with archive.open(files[0]) as fd:
  import io
  reader=csv.DictReader(io.TextIOWrapper(fd,encoding="latin-1",newline=""),delimiter=";")
  cols=reader.fieldnames
  required={"codigo_municipio_ibge","ano_exercicio","mes_referencia","ds_orgao","cd_programa","ds_programa","cd_acao","ds_acao","ds_elemento","tp_despesa","vl_despesa"}
  if not required.issubset(cols):raise RuntimeError("Missing fields "+str(required-set(cols)))
  for row in reader:
   rows+=1
   city=(row.get("codigo_municipio_ibge") or "").strip()
   yr=(row.get("ano_exercicio") or "").strip()
   month=(row.get("mes_referencia") or "").strip()
   if not city or not city.isdigit():issues["invalid_ibge"]+=1;continue
   if yr!=str(YEAR):issues["wrong_year"]+=1;continue
   if not month.isdigit() or int(month) not in range(1,13):issues["wrong_month"]+=1;continue
   month_presence[city].add(int(month));rows_by_city[city]+=1
   code=(row.get("ds_elemento") or "").split(" - ",1)[0].strip()
   if not code.startswith("44"):continue
   investment_rows+=1
   try:
    d=D((row.get("vl_despesa") or "").strip().replace(".","").replace(",","."))*100
    if not d.is_finite() or d!=d.to_integral_value():raise ValueError("non integer cents")
    cents=int(d)
   except (decimal.InvalidOperation,ValueError):issues["invalid_cents"]+=1;continue
   stage=(row.get("tp_despesa") or "").strip().casefold()
   stages[stage]+=1
   org=(row.get("ds_orgao") or "").strip()
   pcode=(row.get("cd_programa") or "").strip();pname=(row.get("ds_programa") or "").strip()
   acode=(row.get("cd_acao") or "").strip();aname=(row.get("ds_acao") or "").strip()
   mkey=(city,month,stage)
   pkey=mkey+(org,pcode,pname)
   akey=pkey+(acode,aname)
   groups[mkey]+=cents;progs[pkey]+=cents;actions[akey]+=cents
   if rows%2000000==0:print("processed",rows,"rows",flush=True)
def write_rows(filename,columns,mapping):
 with (OUT/filename).open("w",newline="",encoding="utf-8") as f:
  w=csv.writer(f);w.writerow(columns)
  for k,v in sorted(mapping.items()):w.writerow([*k,v])
write_rows("investimentos_grupo44_por_municipio_mes_estagio.csv",["codigo_ibge","mes","estagio","centavos"],groups)
write_rows("investimentos_grupo44_por_programa.csv",["codigo_ibge","mes","estagio","orgao","cd_programa","ds_programa","centavos"],progs)
write_rows("investimentos_grupo44_por_acao.csv",["codigo_ibge","mes","estagio","orgao","cd_programa","ds_programa","cd_acao","ds_acao","centavos"],actions)
roll_p=collections.Counter();roll_a=collections.Counter()
for k,v in progs.items():roll_p[k[:3]]+=v
for k,v in actions.items():roll_a[k[:3]]+=v
diff=[{"key":k,"agregado":v,"programa":roll_p.get(k),"acao":roll_a.get(k)} for k,v in groups.items() if v!=roll_p.get(k) or v!=roll_a.get(k)]
report={"source":URL,"year":YEAR,"sha256_zip":sha.hexdigest(),"bytes_zip":ZIP.stat().st_size,
 "rows":rows,"municipalities":len(rows_by_city),"codes":sorted(rows_by_city),
 "municipios_com_12_meses":sum(len(x)==12 for x in month_presence.values()),
 "meses_ausentes_por_codigo":{k:sorted(set(range(1,13))-v) for k,v in sorted(month_presence.items()) if len(v)<12},
 "investment_rows":investment_rows,"stages":dict(stages),"groups":len(groups),"programs":len(progs),"actions":len(actions),
 "issues":dict(issues),"differences_sample":diff[:100],"difference_count":len(diff),
 "stage_liquidado_cents":sum(v for k,v in groups.items() if k[2]=="valor liquidado"),
 "status":"pass" if not diff and not issues and len(rows_by_city)==644 else "needs_review",
 "note":"QA only, no R2 writes, full CSV and individual line items not stored in artifact."}
(OUT/"qa.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
ZIP.unlink()
print(json.dumps({k:v for k,v in report.items() if k not in ("codes","meses_ausentes_por_codigo","differences_sample")},ensure_ascii=False),flush=True)
if report["status"]!="pass":raise SystemExit(2)
