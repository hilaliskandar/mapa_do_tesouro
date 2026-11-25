"""Aggregate canonical DCA history in separate private regional payloads."""
import argparse,json,sqlite3
from collections import Counter,defaultdict
from decimal import Decimal
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument("--history",type=Path,required=True)
p.add_argument("--database",type=Path,required=True)
p.add_argument("--output",type=Path,required=True)
a=p.parse_args()
manifest=json.loads((a.history/"manifest.json").read_text())
variables=sorted(manifest["coverage"])
years=manifest["years"]
assert len(variables)==26 and years==list(range(2013,2026))
db=sqlite3.connect(a.database)
members=defaultdict(list)
for uid,code in db.execute("SELECT universo_id,codigo_ibge FROM universo_municipio ORDER BY universo_id,codigo_ibge"):
    members[uid].append(code)
db.close()
assert len(members)==72
state=set(members["SP_645"])
assert len(state)==645
hist={f.stem:json.loads(f.read_text())["years"] for f in (a.history/"municipalities").glob("*.json")}
assert set(hist)==state
for prefix,n in (("RA_SEADE_",16),("RG_SEADE_",43)):
    groups=[v for k,v in members.items() if k.startswith(prefix)]
    assert len(groups)==n and Counter(c for g in groups for c in g)==Counter(state)
a.output.mkdir(parents=True,exist_ok=True)
results={}
for uid,codes in members.items():
    assert len(codes)==len(set(codes)) and set(codes)<=state
    payload={}
    for year in years:
        values={}
        for var in variables:
            observed=[Decimal(hist[c][str(year)][var]["value_decimal"]) for c in codes if hist[c][str(year)][var]["status"]=="observado"]
            n=len(observed)
            total=sum(observed,Decimal(0)) if n else None
            values[var]={"observed_sum_decimal":str(total) if total is not None else None,"observed":n,"absent":len(codes)-n,"municipality_count":len(codes),"status":"complete" if n==len(codes) else "partial" if n else "absent"}
        payload[str(year)]=values
    results[uid]=payload
    (a.output/(uid+".json")).write_text(json.dumps({"universe_id":uid,"years":payload,"value_policy":"nominal observed sum; partial coverage is not a full regional total","publication_authorized":False},ensure_ascii=False))
checks=0
for prefix in ("RA_SEADE_","RG_SEADE_"):
    groups=[v for k,v in results.items() if k.startswith(prefix)]
    for year in years:
        for var in variables:
            root=results["SP_645"][str(year)][var]
            cells=[g[str(year)][var] for g in groups]
            assert sum(c["observed"] for c in cells)==root["observed"]
            assert sum(c["absent"] for c in cells)==root["absent"]
            if root["observed"]:
                assert sum((Decimal(c["observed_sum_decimal"]) for c in cells if c["observed"]),Decimal(0))==Decimal(root["observed_sum_decimal"])
            else:
                assert all(c["observed_sum_decimal"] is None for c in cells)
            checks+=1
report={"status":"pass","universes":len(members),"years":years,"variables":len(variables),"aggregate_cells":len(members)*len(years)*len(variables),"partition_checks":checks,"publication_authorized":False,"policy":"RA and RG separately conserve state; other overlapping cuts are not additive; no deflation; no missing as zero"}
(a.output/"manifest.json").write_text(json.dumps(report,ensure_ascii=False,indent=2))
print("DCA_REGIONAL_HISTORY",json.dumps(report))
