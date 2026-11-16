#!/usr/bin/env python3
"""FED08B: stage official SICONV empenho/transfer bridges, conserving stage and cardinality.
Only data from national official ZIPs and a private RMRP SQLite; no public microdata.
"""
import argparse,csv,datetime,hashlib,io,json,shutil,sqlite3,zipfile,collections
from decimal import Decimal,InvalidOperation
from pathlib import Path

NAMES=["siconv_empenho","siconv_empenho_desembolso","siconv_empenho_cipi"]
def rows(path):
    with zipfile.ZipFile(path) as z:
        assert z.testzip() is None
        with z.open(z.namelist()[0]) as raw:
            for i,row in enumerate(csv.DictReader(io.TextIOWrapper(raw,encoding="utf-8-sig",newline=""),delimiter=";"),1):
                yield i,row
def cents(s):
    v=(s or "").strip()
    if not v:return None
    if "," in v:v=v.replace(".","").replace(",",".")
    try:
        d=Decimal(v)
        if not d.is_finite() or d*100 != (d*100).to_integral_value():raise ValueError(f"Bad centavos: {s}")
        return int(d*100)
    except InvalidOperation as e:raise ValueError(f"Invalid amount: {s}") from e
def sha(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest()
def audit(dbpath,source,out):
    out.mkdir(parents=True,exist_ok=True)
    dbcopy=out/"RMRP_FED08B_EMPENHO_DESEMBOLSO_PRIVADO.sqlite"
    shutil.copyfile(dbpath,dbcopy)
    db=sqlite3.connect(dbcopy);db.execute("PRAGMA foreign_keys=ON")
    conv={str(x[0]) for x in db.execute("SELECT numero FROM convenio")}
    disb={str(a):int(b) for a,b in db.execute("SELECT id_desembolso,valor_centavos FROM desembolso_fluxo")}
    proj={str(x[0]) for x in db.execute("SELECT projeto_id FROM obra_proponente")}
    db.executescript("""
    CREATE TABLE empenho_fed08b(
     source_row INTEGER PRIMARY KEY,id_empenho TEXT NOT NULL, nr_convenio TEXT NOT NULL REFERENCES convenio(numero),
     nr_empenho TEXT,natureza TEXT,valor_centavos INTEGER,data_emissao TEXT,
     UNIQUE(id_empenho,nr_convenio));
    CREATE INDEX idx_fed08b_emp ON empenho_fed08b(id_empenho);
    CREATE TABLE empenho_desembolso_fed08b(
     source_row INTEGER PRIMARY KEY,id_desembolso TEXT NOT NULL REFERENCES desembolso_fluxo(id_desembolso),
     id_empenho TEXT NOT NULL,nr_convenio TEXT NOT NULL,
     valor_grupo_centavos INTEGER NOT NULL,
     FOREIGN KEY(id_empenho,nr_convenio) REFERENCES empenho_fed08b(id_empenho,nr_convenio));
    CREATE INDEX idx_fed08b_deb ON empenho_desembolso_fed08b(id_desembolso);
    CREATE TABLE empenho_cipi_fed08b(
     source_row INTEGER PRIMARY KEY,id_projeto TEXT NOT NULL REFERENCES obra_proponente(projeto_id),
     nr_empenho TEXT,natureza TEXT,valor_centavos INTEGER,data_emissao TEXT);
    CREATE TABLE desembolso_empenho_qa_fed08b(
     id_desembolso TEXT PRIMARY KEY REFERENCES desembolso_fluxo(id_desembolso),
     valor_origem_centavos INTEGER NOT NULL,valor_soma_grupos_centavos INTEGER,
     qtd_grupos INTEGER NOT NULL,status_reconciliacao TEXT NOT NULL);
    """)
    count=collections.Counter()
    for i,r in rows(source/"siconv_empenho.zip"):
        count["empenho_nacional"]+=1
        n=r["NR_CONVENIO"].strip()
        if n not in conv:continue
        db.execute("INSERT INTO empenho_fed08b(source_row,id_empenho,nr_convenio,nr_empenho,natureza,valor_centavos,data_emissao) VALUES(?,?,?,?,?,?,?)",
                   (i,r["ID_EMPENHO"].strip(),n,r["NR_EMPENHO"],r["NATUREZA_DESPESA"],cents(r["VALOR_EMPENHO"]),r["DATA_EMISSAO"]))
        count["empenho_regional"]+=1
    for i,r in rows(source/"siconv_empenho_desembolso.zip"):
        count["bridge_nacional"]+=1
        idd=r["ID_DESEMBOLSO"].strip()
        if idd not in disb:continue
        n=db.execute("SELECT numero_convenio FROM desembolso_fluxo WHERE id_desembolso=?",(idd,)).fetchone()[0]
        ie=r["ID_EMPENHO"].strip()
        if not db.execute("SELECT 1 FROM empenho_fed08b WHERE id_empenho=? AND nr_convenio=?",(ie,n)).fetchone():
            raise AssertionError("Cross-instrument or missing empenho: "+idd)
        db.execute("INSERT INTO empenho_desembolso_fed08b VALUES(?,?,?,?,?)",
                   (i,idd,ie,n,cents(r["VALOR_GRUPO"])))
        count["bridge_regional"]+=1
    for i,r in rows(source/"siconv_empenho_cipi.zip"):
        count["cipi_nacional"]+=1
        idp=r["ID_PROJETO_INVESTIMENTO"].strip()
        if idp not in proj:continue
        db.execute("INSERT INTO empenho_cipi_fed08b VALUES(?,?,?,?,?,?)",
                   (i,idp,r["NR_EMPENHO"],r["NATUREZA_DESPESA"],cents(r["VALOR_EMPENHO"]),r["DATA_EMISSAO"]))
        count["cipi_regional"]+=1
    qa_sums=[]
    for idd,amt in disb.items():
        v,n=db.execute("SELECT sum(valor_grupo_centavos),count(*) FROM empenho_desembolso_fed08b WHERE id_desembolso=?",(idd,)).fetchone()
        status="sem_ponte" if n==0 else "reconciliado" if v==amt else "divergente"
        db.execute("INSERT INTO desembolso_empenho_qa_fed08b VALUES(?,?,?,?,?)",(idd,amt,v,n,status))
        qa_sums.append((idd,amt,v,n,status))
    db.commit()
    groups=collections.Counter()
    for (nature,n) in db.execute("""SELECT substr(e.natureza,1,2),count(*)
        FROM empenho_desembolso_fed08b l
        JOIN empenho_fed08b e ON e.id_empenho=l.id_empenho AND e.nr_convenio=l.nr_convenio
        GROUP BY substr(e.natureza,1,2)"""):groups[nature or "ausente"]+=n
    clean=collections.Counter()
    for code, val in db.execute("""SELECT substr(e.natureza,1,2),sum(l.valor_grupo_centavos)
        FROM empenho_desembolso_fed08b l
        JOIN empenho_fed08b e ON e.id_empenho=l.id_empenho AND e.nr_convenio=l.nr_convenio
        JOIN desembolso_empenho_qa_fed08b q ON q.id_desembolso=l.id_desembolso
        WHERE q.status_reconciliacao='reconciliado'
        GROUP BY substr(e.natureza,1,2)"""):
        clean[code or "ausente"]=val
    stats=collections.Counter(s[4] for s in qa_sums)
    repeated_ids=db.execute("""SELECT count(*) FROM
      (SELECT id_empenho FROM empenho_fed08b GROUP BY id_empenho HAVING count(*)>1)""").fetchone()[0]
    qa={
      "snapshot":"2026-11-15","processing_date":"2026-11-16",
      "sources":{name:{"sha256":sha(source/(name+".zip")),"bytes":(source/(name+".zip")).stat().st_size} for name in NAMES},
      "source_count":dict(count),
      "disbursement_count":len(disb),
      "disbursement_reconciliation":dict(stats),
      "bridge_nature_first_two_digits":dict(groups),
      "value_centavos_by_budget_code_prefix_only_for_reconciled_disbursement_groups":dict(clean),
      "duplicate_id_empenho_across_convenios":repeated_ids,
      "cipi_projects_with_empenho":db.execute("SELECT count(distinct id_projeto) FROM empenho_cipi_fed08b").fetchone()[0],
      "integrity":db.execute("PRAGMA integrity_check").fetchone()[0],
      "foreign_key_violations":len(db.execute("PRAGMA foreign_key_check").fetchall()),
      "status":"empenho_natureza_por_desembolso_nao_e_GND4_pago",
      "publication_authorized":False,
      "limitations":["Natureza do empenho via groups of desembolso is not a homologated GND4 of payment to a beneficiary.",
        "Use two-part key (ID_EMPENHO, NR_CONVENIO); one-part join gives collisions.",
        "Never sum desembolso group values plus their parent amounts.",
        "One disbursement lacks bridge; one has monetary divergence: keep both outside classified total."]
    }
    assert count["empenho_regional"]==2486
    assert count["bridge_regional"]==2592
    assert count["cipi_regional"]==257
    assert stats=={"reconciliado":2535,"divergente":1,"sem_ponte":1}
    assert repeated_ids==2
    assert qa["integrity"]=="ok" and qa["foreign_key_violations"]==0
    j=out/"RMRP_FED08B_EMPENHO_QA_PUBLICO.json"
    j.write_text(json.dumps(qa,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    private=out/"FED08B_PENDENCIAS_DESEMBOLSO_PRIVADO.csv"
    with private.open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.writer(f,delimiter=";")
        w.writerow(["id_desembolso","valor_origem_centavos","valor_soma_grupos_centavos","quantidade_grupos","status"])
        for row in qa_sums:
            if row[4]!="reconciliado":w.writerow(row)
    db.close()
    pack=out/"RMRP_FED08B_EMPENHO_DESEMBOLSO_PRIVADO_2026-11-16.zip"
    with zipfile.ZipFile(pack,"w",zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for path in (dbcopy,j,private):z.write(path,path.name)
    with zipfile.ZipFile(pack) as z:assert z.testzip() is None
    return {"qa":qa,"zip_sha256":sha(pack),"zip_bytes":pack.stat().st_size}
if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("database",type=Path);ap.add_argument("sources",type=Path);ap.add_argument("output",type=Path)
    x=ap.parse_args();print(json.dumps(audit(x.database,x.sources,x.output),ensure_ascii=False))
