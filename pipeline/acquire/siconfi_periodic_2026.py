"""Collect period-specific fiscal reports from the verified delivery inventory."""
import argparse,collections,csv,hashlib,json,tarfile,subprocess,sys
from pathlib import Path
from datetime import datetime,timezone
from pipeline.sources.siconfi import SiconfiClient
from pipeline.acquire.siconfi_legal_reports import write_raw
p=argparse.ArgumentParser()
p.add_argument("--output",type=Path,required=True)
p.add_argument("--limit",type=int,default=34)
p.add_argument("--offset",type=int,default=0)
p.add_argument("--plan-only",action="store_true")
a=p.parse_args()
a.output.mkdir(parents=True,exist_ok=True)
catalog=json.loads(Path("data/catalogs/siconfi_delivery_2026_r2.json").read_text())
municipalities=[]
for obj in catalog["objects"]:
    target=a.output/("inventory_"+str(obj["offset"])+".tar.gz")
    subprocess.run([sys.executable,"deployment/download_r2_source.py","--object-key",obj["key"],"--expected-sha256",obj["sha256"],"--output",str(target)],check=True)
    with tarfile.open(target) as tf:
        members=[m for m in tf.getmembers() if m.isfile() and Path(m.name).name=="inventory.json"]
        assert len(members)==1
        payload=json.load(tf.extractfile(members[0]))
        assert payload["summary"]["offset"]==obj["offset"]
        municipalities.extend(payload["municipalities"])
assert len(municipalities)==645 and len({r["codigo_ibge"] for r in municipalities})==645
types={"Relatório Resumido de Execução Orçamentária":"rreo","Relatório de Gestão Fiscal":"rgf"}
annexes={"rreo":["01","02","03"],"rgf":["01","02","04"]}
hist=collections.Counter()
plan=[]
unmatched=[]
for city in municipalities:
    code=city["codigo_ibge"]
    candidates=collections.defaultdict(list)
    for row in city.get("deliveries",[]):
        typ=types.get(row.get("entregavel"))
        if not typ:continue
        inst=str(row.get("instituicao",""))
        periodicity=str(row.get("periodicidade",""))
        status=str(row.get("status_relatorio",""))
        hist[(typ,periodicity,str(row.get("periodo")),status,inst.split(" ")[0])]+=1
        if not inst.startswith("Prefeitura"):continue
        try:period=int(row["periodo"])
        except (TypeError,ValueError,KeyError):continue
        if not ((typ=="rreo" and periodicity=="B" and 1<=period<=5) or (typ=="rgf" and periodicity=="Q" and 1<=period<=2) or (typ=="rgf" and periodicity=="S" and period==1)):continue
        if status not in ("HO","RE"):continue
        candidates[(typ,periodicity)].append((period,row))
    for (typ,periodicity),rows in candidates.items():
        latest=max(r[0] for r in rows)
        deliveries=[r for period,r in rows if period==latest]
        for annex in annexes[typ]:
            plan.append({"codigo_ibge":code,"municipio":city["municipio"],"endpoint":typ,"periodicity":periodicity,"period":latest,"annex":typ.upper()+"-Anexo "+annex,"delivery_metadata":deliveries})
    if not candidates:unmatched.append({"codigo_ibge":code,"municipio":city["municipio"],"inventory_status":city["status"]})
report={"municipalities":645,"empty":[r["codigo_ibge"] for r in municipalities if r["status"]=="empty_not_zero"],"plan_requests":len(plan),"distribution":[{"endpoint":k[0],"periodicity":k[1],"period":k[2],"status":k[3],"institution_prefix":k[4],"rows":v} for k,v in sorted(hist.items())],"unmatched":unmatched,"publication_authorized":False,"policy":"HO/RE are candidate-selection labels only; no normative interpretation. Latest available completed period by endpoint and periodicity; no cross-period aggregation."}
(a.output/"plan.json").write_text(json.dumps({"summary":report,"requests":plan},ensure_ascii=False,indent=2))
print("SICONFI_PERIOD_PLAN",json.dumps(report,ensure_ascii=False))
if a.plan_only:sys.exit(0)
assert 0<=a.offset<645 and 1<=a.limit<=645
codes={r["codigo_ibge"] for r in municipalities[a.offset:a.offset+a.limit]}
client=SiconfiClient(min_interval=1.1,timeout=35,max_retries=1)
results=[]
for task in plan:
    if task["codigo_ibge"] not in codes:continue
    typ=task["endpoint"];period=task["period"];frequency=task["periodicity"];code=task["codigo_ibge"];annex=task["annex"]
    params={"nr_periodo":period,"co_tipo_demonstrativo":typ.upper(),"no_anexo":annex,"co_esfera":"M"}
    try:
        if typ=="rreo":result=client.fetch_rreo(year=2026,period=period,entity_id=code,annex=annex)
        else:
            params.update({"in_periodicidade":frequency,"co_poder":"E"})
            result=client.fetch_rgf(year=2026,periodicity=frequency,period=period,entity_id=code,annex=annex)
        path=a.output/"raw"/typ/"2026"/frequency/str(period)/annex.replace(" ","-")/(code+".json.gz")
        write_raw(path,endpoint=typ,year=2026,entity_id=code,params=params,result=result)
        results.append({**task,"status":"observed_rows" if result.items else "empty_not_zero","row_count":len(result.items),"sha256":hashlib.sha256(path.read_bytes()).hexdigest(),"file":str(path.relative_to(a.output))})
    except Exception as exc:
        results.append({**task,"status":"unavailable","error":f"{type(exc).__name__}: {str(exc)[:200]}"})
summary={"offset":a.offset,"municipalities_selected":len(codes),"requests_planned":len([t for t in plan if t["codigo_ibge"] in codes]),"status_counts":dict(collections.Counter(r["status"] for r in results)),"publication_authorized":False}
(a.output/"collection.json").write_text(json.dumps({"summary":summary,"results":results},ensure_ascii=False,indent=2))
print("SICONFI_PERIOD_COLLECTION",json.dumps(summary))
