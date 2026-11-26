"""Recover remaining SP645 municipalities from pinned periodic snapshots."""
import argparse,collections,hashlib,json,pathlib,subprocess,sys,tarfile
from pipeline.sources.siconfi import SiconfiClient
from pipeline.acquire.siconfi_legal_reports import write_raw
p=argparse.ArgumentParser();p.add_argument("--offset",type=int,required=True);p.add_argument("--limit",type=int,default=20);p.add_argument("--output",type=pathlib.Path,required=True);a=p.parse_args()
root=a.output;root.mkdir(parents=True,exist_ok=True)
catalog=json.loads(pathlib.Path("data/catalogs/siconfi_periodic_2026_r2.json").read_text())
missing=[];empty=[];observed=set();rmrp=[]
for obj in catalog["objects"]:
    path=root/f"snapshot_{obj['offset']}.tar.gz"
    subprocess.run([sys.executable,"deployment/download_r2_source.py","--object-key",obj["key"],"--expected-sha256",obj["sha256"],"--output",str(path)],check=True)
    with tarfile.open(path) as tf:
        def read(name):
            members=[m for m in tf.getmembers() if m.isfile() and pathlib.Path(m.name).name==name]
            assert len(members)==1
            return json.load(tf.extractfile(members[0]))
        qa=read("qa.json");coll=read("collection.json")
        if obj["offset"]==0:rmrp=qa["without_plan"]
        else:missing.extend(qa["without_plan"])
        for r in coll["results"]:
            if r["status"]=="observed_rows":observed.add(r["codigo_ibge"])
            else:empty.append(r)
    path.unlink()
assert len(observed)==539 and len(set(missing))==98 and len(rmrp)==8 and len(empty)==5
assert not observed.intersection(missing+rmrp)
codes=sorted(missing)[a.offset:a.offset+a.limit]
client=SiconfiClient(min_interval=1.1,timeout=25,max_retries=1)
results=[]
def query(code,typ,freq,period,annex):
    name=typ.upper()+"-Anexo "+annex
    row={"codigo_ibge":code,"endpoint":typ,"periodicity":freq,"period":period,"annex":name}
    params={"nr_periodo":period,"no_anexo":name,"co_esfera":"M","co_tipo_demonstrativo":typ.upper()}
    try:
        if typ=="rreo":r=client.fetch_rreo(year=2026,period=period,entity_id=code,annex=name)
        else:
            params.update({"in_periodicidade":freq,"co_poder":"E"})
            r=client.fetch_rgf(year=2026,periodicity=freq,period=period,entity_id=code,annex=name)
        path=root/"raw"/typ/freq/str(period)/annex/(code+".json.gz")
        write_raw(path,endpoint=typ,year=2026,entity_id=code,params=params,result=r)
        row.update(status="observed_rows" if r.items else "empty_not_zero",rows=len(r.items),file=str(path.relative_to(root)),sha256=hashlib.sha256(path.read_bytes()).hexdigest())
    except Exception as e:row.update(status="unavailable",error=f"{type(e).__name__}: {str(e)[:200]}")
    results.append(row)
    return row["status"]=="observed_rows"
for code in codes:
    for typ,freq,periods,annexes in [("rreo","B",[5,4,3,2,1],["01","02","03"]),("rgf","Q",[2,1],["01","02","04"]),("rgf","S",[1],["01","02","04"])]:
        for period in periods:
            found=[query(code,typ,freq,period,annex) for annex in annexes]
            if any(found):break
if a.offset==0:
    for r in empty:query(r["codigo_ibge"],r["endpoint"],r["periodicity"],r["period"],r["annex"].split()[-1])
keys=[(r["codigo_ibge"],r["endpoint"],r["periodicity"],r["period"],r["annex"]) for r in results]
assert len(keys)==len(set(keys))
summary={"offset":a.offset,"selected_codes":codes,"municipalities":len(codes),"requests":len(results),"status_counts":dict(collections.Counter(r["status"] for r in results)),"observed_codes":sorted({r["codigo_ibge"] for r in results if r["status"]=="observed_rows"}),"rmrp_previously_recovered_without_rows":rmrp,"publication_authorized":False}
(root/"recovery.json").write_text(json.dumps({"summary":summary,"results":results},ensure_ascii=False,indent=2))
print("STATE_RECOVERY_BATCH",json.dumps(summary),flush=True)
