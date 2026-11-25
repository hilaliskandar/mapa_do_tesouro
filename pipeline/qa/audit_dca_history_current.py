"""Audit the historical sidecar against the current statewide v2 export, without mutation."""
import argparse,json
from collections import Counter,defaultdict
from decimal import Decimal
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument("--history",type=Path,required=True)
p.add_argument("--api",type=Path,required=True)
p.add_argument("--output",type=Path,required=True)
a=p.parse_args()
manifest=json.loads((a.history/"manifest.json").read_text())
variables=set(manifest["coverage"])
counts=defaultdict(Counter)
examples=[]
files=sorted((a.history/"municipalities").glob("*.json"))
assert len(files)==645 and len(variables)==26
assert {f.stem for f in files}=={f.stem for f in (a.api/"municipalities").glob("*.json")}
for f in files:
    hist=json.loads(f.read_text())
    core=json.loads((a.api/"municipalities"/f.name).read_text())
    assert hist["codigo_ibge"]==core["municipality"]["codigo_ibge"]==f.stem
    assert variables<=set(core["variables"])
    for var in variables:
        entries=core["variables"][var]
        by_year={str(e["year"]):e for e in entries}
        assert len(by_year)==len(entries)
        for year in manifest["years"]:
            h=hist["years"][str(year)][var]
            c=by_year.get(str(year))
            if c is None:kind="core_not_exposed"
            elif c["status"]=="nao_aplicavel":kind="core_outside_window"
            elif h["status"]==c["status"]=="ausente" and c["value"] is None:kind="equal_absent"
            elif h["status"]==c["status"]=="observado" and c["value"] is not None:
                kind="equal_value" if Decimal(h["value_decimal"])==Decimal(str(c["value"])) else "different_value"
            else:kind="different_status"
            counts[(year,var)][kind]+=1
            if kind.startswith("different") and len(examples)<40:examples.append({"code":f.stem,"year":year,"variable":var,"history":h,"core":c})
years=defaultdict(Counter)
for (year,var),v in counts.items():
    assert sum(v.values())==645
    years[year].update(v)
assert sum(sum(v.values()) for v in years.values())==218010
report={"years":dict(years),"by_year_variable":[{"year":y,"variable":v,"counts":c} for (y,v),c in sorted(counts.items())],"difference_examples":examples,"publication_authorized":False}
a.output.parent.mkdir(parents=True,exist_ok=True)
a.output.write_text(json.dumps(report,ensure_ascii=False,indent=2))
print("DCA_HISTORY_CURRENT",json.dumps(dict(years)))
assert years[2025]["equal_value"]+years[2025]["equal_absent"]==16770,"2025 parity failed"
assert all(not c["different_value"] and not c["different_status"] for c in years.values()),"overlap discrepancies"
