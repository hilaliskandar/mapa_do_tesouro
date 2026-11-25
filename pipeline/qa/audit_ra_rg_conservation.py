"""Check exact municipality membership and conservation of additive observed amounts."""
import argparse,csv,json,sqlite3
from collections import defaultdict
from decimal import Decimal
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("--database",required=True);p.add_argument("--output",type=Path,required=True);a=p.parse_args()
db=sqlite3.connect(a.database)
source=Path("governance/DIM_SP645_IBGE_RA_RG_SEMIL_SEADE_2026_11_14.csv")
with source.open(encoding="utf-8-sig",newline="") as f:rows=list(csv.DictReader(f,delimiter=";"))
assert len(rows)==645 and len({r["codigo_ibge"] for r in rows})==645
expected={}
for typ in ("ra","rg"):
    g=defaultdict(set)
    for r in rows:g[f"{typ.upper()}_SEADE_{int(r[typ+'_codigo']):02d}"].add(r["codigo_ibge"])
    assert len(g)==(16 if typ=="ra" else 43)
    expected.update(g)
actual=defaultdict(set)
for uid,code in db.execute("SELECT universo_id,codigo_ibge FROM universo_municipio WHERE universo_id LIKE 'RA_SEADE_%' OR universo_id LIKE 'RG_SEADE_%'"):actual[uid].add(code)
assert dict(actual)==expected
state={r["codigo_ibge"] for r in rows}
assert state=={r[0] for r in db.execute("SELECT codigo_ibge FROM universo_municipio WHERE universo_id='SP_645'")}
obs=list(db.execute("""SELECT o.codigo_ibge,o.ano,o.variavel_id,o.status,o.valor_num FROM observacao o JOIN variavel v ON v.variavel_id=o.variavel_id WHERE v.ativo=1 AND v.publicavel=1 AND v.unidade='BRL' AND v.tipo IN ('conta_oficial','agregado_analitico')"""))
base=defaultdict(lambda:[0,Decimal(0)])
parts={t:defaultdict(lambda:[0,Decimal(0)]) for t in ("ra","rg")}
mapping={t:{r["codigo_ibge"]:f"{t.upper()}_SEADE_{int(r[t+'_codigo']):02d}" for r in rows} for t in parts}
for code,year,vid,status,value in obs:
    if code not in state:continue
    key=(year,vid,status)
    v=Decimal(str(value)) if status=="observado" and value is not None else Decimal(0)
    base[key][0]+=1;base[key][1]+=v
    for t in parts:
        k=(mapping[t][code],key);parts[t][k][0]+=1;parts[t][k][1]+=v
for t,part in parts.items():
    total=defaultdict(lambda:[0,Decimal(0)])
    for (_,k),(n,v) in part.items():total[k][0]+=n;total[k][1]+=v
    assert dict(total)==dict(base),t
report={"status":"pass","municipalities":645,"ra":16,"rg":43,"observation_rows":sum(v[0] for v in base.values()),"year_variable_status_cells":len(base),"scope":"SQLite membership and additive observed BRL conservation; not fiscal homologation of new sources","publication_authorized":False}
a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,ensure_ascii=False,indent=2));print("RA_RG_CONSERVATION",json.dumps(report))
