"""Lossless staging of verified Siconfi periodic snapshots; no fiscal aggregation."""
import collections,csv,gzip,hashlib,io,json,pathlib,sqlite3,subprocess,sys,tarfile
from decimal import Decimal
root=pathlib.Path("build/siconfi-normalized");root.mkdir(parents=True,exist_ok=True)
catalog=json.loads(pathlib.Path("data/catalogs/siconfi_periodic_2026_r2.json").read_text())
with open("governance/DIM_SP645_IBGE_RA_RG_RM_AU_CONSOLIDADA_2026_11_14.csv",encoding="utf-8-sig") as f:
    roster={r["codigo_ibge"]:r for r in csv.DictReader(f,delimiter=";")}
assert len(roster)==645
db=sqlite3.connect(root/"periodic.sqlite")
db.executescript("""
CREATE TABLE reports(report_id TEXT PRIMARY KEY, ibge TEXT NOT NULL, year INTEGER NOT NULL, endpoint TEXT NOT NULL, frequency TEXT NOT NULL, period INTEGER NOT NULL, annex TEXT NOT NULL, status TEXT NOT NULL, source_object TEXT NOT NULL, source_member TEXT NOT NULL, source_sha256 TEXT NOT NULL, parameters_json TEXT NOT NULL, row_count INTEGER NOT NULL, delivery_metadata_json TEXT NOT NULL, UNIQUE(ibge,year,endpoint,frequency,period,annex));
CREATE TABLE rows(report_id TEXT NOT NULL REFERENCES reports(report_id), ordinal INTEGER NOT NULL, account_code TEXT, account_label TEXT, column_label TEXT, value_decimal TEXT, item_json TEXT NOT NULL, PRIMARY KEY(report_id,ordinal));
CREATE INDEX reports_municipality ON reports(ibge,endpoint,period);
CREATE INDEX rows_account ON rows(account_code, column_label);
""")
db.execute("PRAGMA foreign_keys=ON")
counts=collections.Counter();fields=collections.Counter();cohorts=collections.Counter();cities=set();row_count=0;duplicate_payloads=0;missing_value=0
def canonical(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(",",":"),default=str)
for obj in catalog["objects"]:
    path=root/"source.tar.gz"
    subprocess.run([sys.executable,"deployment/download_r2_source.py","--object-key",obj["key"],"--expected-sha256",obj["sha256"],"--output",str(path)],check=True)
    with tarfile.open(path) as tf:
        members={m.name.removeprefix("./"):m for m in tf.getmembers() if m.isfile()}
        matches=[m for n,m in members.items() if pathlib.Path(n).name=="collection.json"]
        assert len(matches)==1
        coll=json.load(tf.extractfile(matches[0]))
        for r in coll["results"]:
            code=r["codigo_ibge"];assert code in roster
            typ=r["endpoint"];freq=r["periodicity"];period=r["period"];annex=r["annex"]
            assert typ in ("rreo","rgf") and freq in ("B","Q","S")
            assert r["status"] in ("observed_rows","empty_not_zero")
            member=members[r["file"]]
            raw=tf.extractfile(member).read()
            assert hashlib.sha256(raw).hexdigest()==r["sha256"]
            payload=json.loads(gzip.decompress(raw),parse_float=Decimal)
            params=payload["parameters"];items=payload["items"]
            assert payload["entity_id"]==code and payload["year"]==2026 and payload["endpoint"]==typ
            assert params["nr_periodo"]==period and params["no_anexo"]==annex
            assert params.get("in_periodicidade", "B")==freq
            assert len(items)==r["row_count"] and bool(items)==(r["status"]=="observed_rows")
            key=f"{code}:2026:{typ}:{freq}:{period}:{annex}"
            db.execute("INSERT INTO reports VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",(key,code,2026,typ,freq,period,annex,r["status"],obj["key"],member.name,r["sha256"],canonical(params),len(items),canonical(r.get("delivery_metadata",[]))))
            seen=set()
            for i,item in enumerate(items):
                assert isinstance(item,dict)
                fields.update(item.keys())
                original=canonical(item)
                if original in seen:duplicate_payloads+=1
                seen.add(original)
                val=item.get("valor")
                if val is None:missing_value+=1
                else:
                    val=Decimal(str(val))
                    assert val.is_finite()
                    val=str(val)
                db.execute("INSERT INTO rows VALUES(?,?,?,?,?,?,?)",(key,i,item.get("cod_conta"),item.get("conta"),item.get("coluna"),val,original))
                row_count+=1
            counts[r["status"]]+=1
            if items:cities.add(code)
            cohorts[(typ,freq,period,annex,r["status"])]+=1
    db.commit();path.unlink()
    print("SICONFI_STAGE_BATCH",obj["offset"],row_count,flush=True)
assert counts=={"observed_rows":3220,"empty_not_zero":5}
assert len(cities)==539
assert db.execute("SELECT count(*) FROM rows").fetchone()[0]==row_count
assert db.execute("SELECT sum(row_count) FROM reports").fetchone()[0]==row_count
assert db.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
assert not db.execute("PRAGMA foreign_key_check").fetchall()
db.close()
report={"status_counts":dict(counts),"municipalities_observed":len(cities),"municipalities_without_observed_reports":sorted(set(roster)-cities),"source_rows":row_count,"identical_payload_rows_preserved":duplicate_payloads,"missing_value_rows":missing_value,"item_field_counts":dict(fields),"cohorts":[{"endpoint":k[0],"frequency":k[1],"period":k[2],"annex":k[3],"status":k[4],"reports":v} for k,v in sorted(cohorts.items())],"publication_authorized":False,"policy":"Lossless item staging with decimals as text; no semantic deduplication or cross-period sums."}
(root/"qa.json").write_text(json.dumps(report,ensure_ascii=False,indent=2))
print("SICONFI_STAGE_SUMMARY",json.dumps({k:v for k,v in report.items() if k not in ("cohorts","municipalities_without_observed_reports")}))
