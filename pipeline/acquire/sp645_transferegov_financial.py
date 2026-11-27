"""Statewide financial event staging, by proponent; no personal payee fields."""
import argparse,collections,csv,datetime,decimal,json,sqlite3
from pathlib import Path
from pipeline.acquire.inv_sp645_transferegov_new_source_layout import acquire
from pipeline.acquire.inv_sp645_proponent_obrasgov_regional_coverage import read
p=argparse.ArgumentParser();p.add_argument("--out",type=Path,required=True);a=p.parse_args()
root=a.out;root.mkdir(parents=True,exist_ok=True)
with open("governance/DIM_SP645_IBGE_RA_RG_RM_AU_CONSOLIDADA_2026_11_14.csv",encoding="utf-8-sig") as f:geo={r["codigo_ibge"]:r for r in csv.DictReader(f,delimiter=";")}
assert len(geo)==645
meta={};counts=collections.Counter()
def source(name,required):
    path,meta[name]=acquire(root,name,650)
    for row in read(path,required):
        counts[name+"_national"]+=1
        yield row
    path.unlink()
def cents(s):
    s=s.strip()
    if "," in s:s=s.replace(".","").replace(",",".")
    x=decimal.Decimal(s)
    assert x.is_finite() and x*100==(x*100).to_integral_value()
    return int(x*100)
def date(s):
    for fmt in ("%d/%m/%Y","%Y-%m-%d","%d/%m/%Y %H:%M:%S"):
        try:return datetime.datetime.strptime(s.strip(),fmt).date().isoformat()
        except ValueError:pass
    raise ValueError("unrecognized date format")
def field(row,names):
    found=[k for k in names if k in row]
    if len(found)!=1:raise ValueError("schema field ambiguous/missing: "+str(names)+" available="+str(list(row)))
    return row[found[0]]
proposals={}
for r in source("siconv_proposta",{"ID_PROPOSTA","COD_MUNIC_IBGE","UF_PROPONENTE"}):
    code=r["COD_MUNIC_IBGE"].strip();k=r["ID_PROPOSTA"].strip()
    if code not in geo or not k:continue
    assert r["UF_PROPONENTE"].strip()=="SP" and (k not in proposals or proposals[k]==code)
    proposals[k]=code
conv={}
for r in source("siconv_convenio",{"ID_PROPOSTA","NR_CONVENIO"}):
    code=proposals.get(r["ID_PROPOSTA"].strip());k=r["NR_CONVENIO"].strip()
    if not code or not k:continue
    assert k not in conv or conv[k]==code
    conv[k]=code
db=sqlite3.connect(root/"financial.sqlite")
db.executescript("CREATE TABLE convenio(numero TEXT PRIMARY KEY,ibge TEXT NOT NULL); CREATE TABLE event(stage TEXT NOT NULL,id TEXT NOT NULL,convenio TEXT NOT NULL REFERENCES convenio(numero),date TEXT NOT NULL,cents INTEGER NOT NULL,kind TEXT NOT NULL,source_row INTEGER NOT NULL,PRIMARY KEY(stage,id)); CREATE INDEX event_convenio ON event(convenio);")
db.execute("PRAGMA foreign_keys=ON")
db.executemany("INSERT INTO convenio VALUES(?,?)",sorted(conv.items()))
for stage,name,idcol,dates,values in [
    ("desembolso","siconv_desembolso","ID_DESEMBOLSO",("DATA_DESEMBOLSO",),("VL_DESEMBOLSADO",)),
    ("pagamento","siconv_pagamento","NR_MOV_FIN",("DATA_PAG",),("VL_PAGO",))]:
    for r in source(name,{"NR_CONVENIO",idcol}):
        k=r["NR_CONVENIO"].strip()
        if k not in conv:continue
        ident=r[idcol].strip();assert ident
        d=date(field(r,dates));v=cents(field(r,values))
        kind=r.get("TP_MOV_FINANCEIRA","").strip() if stage=="pagamento" else "desembolso_ao_convenente"
        db.execute("INSERT INTO event VALUES(?,?,?,?,?,?,?)",(stage,ident,k,d,v,kind,counts[name+"_national"]))
        counts[stage+"_selected"]+=1
    db.commit()
    print("FEDERAL_STAGE",stage,counts[stage+"_selected"],flush=True)
assert db.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
assert not db.execute("PRAGMA foreign_key_check").fetchall()
with (root/"municipio_ano.csv").open("w",encoding="utf-8",newline="") as f:
    w=csv.writer(f,delimiter=";");w.writerow(["codigo_ibge","ano","estagio","tipo","eventos","centavos"])
    w.writerows(db.execute("SELECT c.ibge,substr(e.date,1,4),e.stage,e.kind,count(*),sum(e.cents) FROM event e JOIN convenio c ON c.numero=e.convenio GROUP BY 1,2,3,4 ORDER BY 1,2,3,4"))
summary=[dict(zip(("stage","events","municipalities","instruments","cents","negative","zero"),r)) for r in db.execute("SELECT e.stage,count(*),count(distinct c.ibge),count(distinct e.convenio),sum(e.cents),sum(e.cents<0),sum(e.cents=0) FROM event e JOIN convenio c ON c.numero=e.convenio GROUP BY e.stage")]
db.close()
qa={"sources":meta,"counts":dict(counts),"proposals":len(proposals),"convenios":len(conv),"summary":summary,"territorial_role":"proponent","publication_authorized":False,"not_additive":True,"natureza_capital_pago":None}
(root/"qa.json").write_text(json.dumps(qa,ensure_ascii=False,indent=2))
print("SP645_FEDERAL_FINANCIAL_QA",json.dumps(qa,ensure_ascii=False),flush=True)
