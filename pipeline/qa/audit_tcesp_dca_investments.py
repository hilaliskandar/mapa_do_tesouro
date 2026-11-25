"""Compare nominal annual liquidated investments; differences are diagnostic, not substitutions."""
import argparse,csv,json,sqlite3
from decimal import Decimal
from pathlib import Path
from collections import Counter
p=argparse.ArgumentParser()
p.add_argument("--history",type=Path,required=True)
p.add_argument("--tcesp",type=Path,required=True)
p.add_argument("--core",type=Path,required=True)
p.add_argument("--output",type=Path,required=True)
a=p.parse_args()
a.output.mkdir(parents=True,exist_ok=True)
core=sqlite3.connect(f"file:{a.core}?mode=ro",uri=True)
members={}
for uid,code in core.execute("SELECT universo_id,codigo_ibge FROM universo_municipio ORDER BY universo_id,codigo_ibge"):
    members.setdefault(uid,[]).append(code)
core.close()
assert len(members)==72
codes=set(members["SP_645"])
assert len(codes)==645 and "3550308" in codes
history={f.stem:json.loads(f.read_text())["years"] for f in (a.history/"municipalities").glob("*.json")}
assert set(history)==codes
t=sqlite3.connect(f"file:{a.tcesp}?mode=ro",uri=True)
values={(y,c):Decimal(v)/100 for y,c,v in t.execute("""SELECT l.exercicio,p.codigo_ibge,SUM(p.valor_centavos) FROM tcesp_investimento_programa p JOIN tcesp_lote l USING(lote_id) WHERE p.estagio='valor liquidado' GROUP BY 1,2""")}
t.close()
assert all(y in (2023,2024,2025) and c in codes and c!="3550308" for y,c in values)
rows={}
for y in (2023,2024,2025):
    for c in sorted(codes):
        cell=history[c][str(y)]["dca_investimentos_liquidada"]
        d=Decimal(cell["value_decimal"]) if cell["status"]=="observado" else None
        tc=values.get((y,c))
        diff=tc-d if tc is not None and d is not None else None
        status=("capital_fora_tcesp" if c=="3550308" else "ambos_ausentes" if tc is None and d is None else "tcesp_ausente" if tc is None else "dca_ausente" if d is None else "igual" if diff==0 else "divergente")
        rows[(y,c)]={"ano":y,"codigo_ibge":c,"dca_brl":d,"tcesp_brl":tc,"diferenca_brl":diff,"status":status}
def aggregate(uid,y):
    rr=[rows[(y,c)] for c in members[uid]]
    matched=[r for r in rr if r["diferenca_brl"] is not None]
    d=sum((r["dca_brl"] for r in matched),Decimal(0)) if matched else None
    tc=sum((r["tcesp_brl"] for r in matched),Decimal(0)) if matched else None
    return {"universo_id":uid,"ano":y,"municipios":len(rr),"comparaveis":len(matched),"dca_brl_comparaveis":d,"tcesp_brl_comparaveis":tc,"diferenca_liquida_brl":tc-d if matched else None,"diferenca_absoluta_brl":sum((abs(r["diferenca_brl"]) for r in matched),Decimal(0)) if matched else None,**Counter(r["status"] for r in rr)}
def write_csv(name,records):
    keys=list(dict.fromkeys(k for r in records for k in r))
    with (a.output/name).open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(records)
regional=[aggregate(uid,y) for uid in members for y in (2023,2024,2025)]
assert len(rows)==1935 and len(regional)==216
write_csv("municipal.csv",list(rows.values()))
write_csv("regional.csv",regional)
report={"status":"diagnostic_complete","municipality_years":len(rows),"regional_years":len(regional),"state":[r for r in regional if r["universo_id"]=="SP_645"],"policy":"matched observations only; nominal BRL; TCESP group 44 liquidado versus DCA investimentos liquidada; no inferred equivalence, no missing as zero; no publication authorization"}
(a.output/"manifest.json").write_text(json.dumps(report,default=str,ensure_ascii=False,indent=2))
divergent=sorted((r for r in rows.values() if r["status"]=="divergente"),key=lambda r:abs(r["diferenca_brl"]),reverse=True)
write_csv("divergencias_ordenadas.csv",divergent)
unmatched=[r for r in rows.values() if r["status"] not in ("igual","divergente")]
print("TCESP_DCA_TOP_DIFFERENCES",json.dumps(divergent[:15],default=str,ensure_ascii=False))
print("TCESP_DCA_UNMATCHED",json.dumps(unmatched,default=str,ensure_ascii=False))
print("TCESP_DCA_COMPARISON",json.dumps(report,default=str,ensure_ascii=False))
