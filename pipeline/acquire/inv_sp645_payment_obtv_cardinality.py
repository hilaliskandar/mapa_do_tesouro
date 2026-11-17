#!/usr/bin/env python3
"""National Transferegov payment <> OBTV candidate-key cardinality audit.

All event identifiers stay in temporary local SQLite; only aggregate counts and
hashes leave the runner. No money is summed; no investment nature is inferred.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,sqlite3,sys,zipfile
from collections import Counter
from datetime import datetime,timezone
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
from inv_sp645_transferegov_new_source_layout import acquire

NEEDED_PAYMENT={"NR_MOV_FIN","NR_CONVENIO","TP_MOV_FINANCEIRA","ID_DL"}
NEEDED_OBTV={"NR_MOV_FIN","VL_PAGO_OBTV_CONV"}
def iter_csv(path:Path,columns:set[str]):
    with zipfile.ZipFile(path) as archive:
        info=[i for i in archive.infolist() if i.filename.lower().endswith(".csv") and not i.is_dir()]
        if len(info)!=1:raise RuntimeError("Invalid one-CSV constraint")
        with archive.open(info[0]) as raw:
            first=raw.readline(1024*1024)
            encoding="utf-8-sig"
            try:first.decode(encoding,errors="strict")
            except UnicodeDecodeError:encoding="latin-1"
            header=first.decode(encoding,errors="strict")
            sep=";" if header.count(";")>=header.count(",") else ","
            fields=next(csv.reader([header],delimiter=sep))
            if len(fields)!=len(set(fields)) or not columns.issubset(fields):
                raise RuntimeError("CSV schema conflict "+str(columns-set(fields)))
            stream=io.TextIOWrapper(raw,encoding=encoding,errors="strict",newline="")
            reader=csv.DictReader(stream,fieldnames=fields,delimiter=sep)
            for record in reader:
                if None in record:raise RuntimeError("CSV width inconsistency")
                yield record
            stream.detach()
        if archive.testzip() is not None:raise RuntimeError("ZIP CRC invalid")

def chunk_insert(connection,query,batch):
    if batch:
        connection.executemany(query,batch)
        batch.clear()

def main():
    p=argparse.ArgumentParser();p.add_argument("--out-dir",required=True)
    p.add_argument("--timeout",type=int,default=650)
    args=p.parse_args();out=Path(args.out_dir);out.mkdir(parents=True,exist_ok=True)
    report={"utc":datetime.now(timezone.utc).isoformat(),"status":"in_progress",
        "scope":"national payment and OBTV cardinality, no monetary totals",
        "no_beneficiary_identifiers_exported":True,"datasets":{},"qa":{}}
    def persist():
        (out/"manifest_payment_obtv_cardinality.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    persist()
    for name in ["siconv_pagamento","siconv_obtv_convenente"]:
        path,meta=acquire(out,name,args.timeout)
        report["datasets"][name]=meta;persist()
    db=sqlite3.connect(out/"temp_sensitive_keys.sqlite")
    try:
        db.execute("PRAGMA journal_mode = OFF")
        db.execute("PRAGMA synchronous = OFF")
        db.execute("PRAGMA temp_store = FILE")
        db.execute("""CREATE TABLE payment (
               movement TEXT PRIMARY KEY NOT NULL,
               events INTEGER NOT NULL,
               obv_events INTEGER NOT NULL,
               nonobv_events INTEGER NOT NULL,
               multiple_convenios INTEGER NOT NULL DEFAULT 0,
               convenio_first TEXT,
               docs_first TEXT,
               multiple_dl INTEGER NOT NULL DEFAULT 0)""")
        q="""INSERT INTO payment(movement,events,obv_events,nonobv_events,convenio_first,docs_first)
             VALUES(?,?,?,?,?,?)
             ON CONFLICT(movement) DO UPDATE SET
               events=events+excluded.events,
               obv_events=obv_events+excluded.obv_events,
               nonobv_events=nonobv_events+excluded.nonobv_events,
               multiple_convenios=max(multiple_convenios,convenio_first<>excluded.convenio_first),
               multiple_dl=max(multiple_dl,docs_first<>excluded.docs_first)"""
        total=missing=0;types=Counter();batch=[]
        for row in iter_csv(out/"siconv_pagamento.zip",NEEDED_PAYMENT):
            total+=1
            movement=(row["NR_MOV_FIN"] or "").strip()
            if not movement:missing+=1;continue
            t=(row["TP_MOV_FINANCEIRA"] or "").strip()
            obv=int(t=="PAGAMENTO A FAVORECIDO COM OBTV")
            types[t]+=1
            batch.append((movement,1,obv,1-obv,
                (row["NR_CONVENIO"] or "").strip(),(row["ID_DL"] or "").strip()))
            if len(batch)>=10000:chunk_insert(db,q,batch)
        chunk_insert(db,q,batch);db.commit()
        report["qa"]["payment_rows"]=total
        report["qa"]["payment_rows_missing_movement_id"]=missing
        report["qa"]["payment_type_rows"]=dict(types)
        persist()
        db.execute("CREATE TABLE obtv (movement TEXT PRIMARY KEY NOT NULL,events INTEGER NOT NULL)")
        qob="""INSERT INTO obtv(movement,events) VALUES(?,1)
            ON CONFLICT(movement) DO UPDATE SET events=events+1"""
        n_obtv=empty_obtv=0;batch=[]
        for row in iter_csv(out/"siconv_obtv_convenente.zip",NEEDED_OBTV):
            n_obtv+=1
            k=(row["NR_MOV_FIN"] or "").strip()
            if not k:empty_obtv+=1;continue
            batch.append((k,))
            if len(batch)>=10000:chunk_insert(db,qob,batch)
        chunk_insert(db,qob,batch);db.commit()
        summary=db.execute("""SELECT COUNT(*),SUM(events>1),SUM(multiple_convenios),
             SUM(multiple_dl),SUM(obv_events>0 AND nonobv_events>0)
             FROM payment""").fetchone()
        obu=db.execute("SELECT COUNT(*),SUM(events>1) FROM obtv").fetchone()
        links=db.execute("""SELECT COUNT(*), COALESCE(SUM(p.events),0),COALESCE(SUM(o.events),0),
          COALESCE(SUM(p.events * o.events),0),
          COALESCE(SUM(p.obv_events * o.events),0),
          COALESCE(SUM(p.nonobv_events * o.events),0)
          FROM obtv o JOIN payment p USING(movement)""").fetchone()
        only_obtv=db.execute("""SELECT COUNT(*),COALESCE(SUM(events),0) FROM obtv
             WHERE movement NOT IN (SELECT movement FROM payment)""").fetchone()
        report["qa"].update({
          "obtv_rows":n_obtv,"obtv_rows_missing_movement_id":empty_obtv,
          "unique_payment_movement_ids":summary[0],"payment_movement_ids_repeated":summary[1] or 0,
          "payment_movement_ids_multi_convenio":summary[2] or 0,
          "payment_movement_ids_multi_dl":summary[3] or 0,
          "payment_movement_ids_mixed_event_types":summary[4] or 0,
          "unique_obtv_movement_ids":obu[0],"obtv_movement_ids_repeated":obu[1] or 0,
          "matched_movement_ids":links[0],
          "matched_payment_rows":links[1],
          "matched_obtv_rows":links[2],
          "raw_join_rows_if_naive":links[3],
          "obtv_type_join_rows_if_naive":links[4],
          "non_obtv_type_join_rows_if_naive":links[5],
          "unmatched_obtv_movement_ids":only_obtv[0],
          "unmatched_obtv_rows":only_obtv[1],
        })
        assert sum(types.values())==total-missing
        if summary[0]+missing>total or obu[0]+empty_obtv>n_obtv:
            raise RuntimeError("conservation failure")
        report["status"]="qa_candidate_cardinality_complete_no_money"
        report["warnings"]=[
          "Matching NR_MOV_FIN is NOT proof of one-to-one transaction or identical gross/net value",
          "No beneficiary data, event keys, money or personal fields in manifest",
          "No classified GND4 or territorialized transfer amount",
          "No persistent storage of temporary sensitive SQLite"]
        persist()
        print(json.dumps({"status":report["status"],"qa":report["qa"]},ensure_ascii=False),flush=True)
    except Exception as e:
        report["status"]="blocked";report["error"]=type(e).__name__+": "+str(e)[:190];persist();raise
    finally:
        db.close()
        for name in ["temp_sensitive_keys.sqlite","siconv_pagamento.zip","siconv_obtv_convenente.zip"]:
            f=out/name
            if f.exists():f.unlink()
if __name__=="__main__":main()
