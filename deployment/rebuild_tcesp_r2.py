"""Reconstruct TCESP investment aggregates from pinned R2 objects; never modify core SQLite."""
import json, pathlib, subprocess, sys, sqlite3
root=pathlib.Path("build/tcesp_r2")
catalog=json.loads(pathlib.Path("data/catalogs/tcesp_investimentos_r2_2023_2025.json").read_text())
assert len(catalog["objects"])==15
for key,sha in catalog["objects"].items():
    parts=key.split("/")
    year=parts[3]
    assert year in ("2023","2024","2025")
    target=root/year/parts[-1]
    subprocess.run([sys.executable,"deployment/download_r2_source.py","--object-key",key,"--output",str(target),"--expected-sha256",sha],check=True)
database=root/"tcesp.sqlite"
db=sqlite3.connect(database)
for sql in sorted(pathlib.Path("data/schema").glob("[0-9][0-9][0-9]_*.sql")):db.executescript(sql.read_text(encoding="utf-8"))
source_qa={y:json.loads((root/str(y)/"qa.json").read_text()) for y in (2023,2024,2025)}
codes=set(source_qa[2023]["codes"])
core=sqlite3.connect("file:build/sp645_candidate.sqlite?mode=ro",uri=True)
names=dict(core.execute("SELECT codigo_ibge,nome FROM municipio"))
core.close()
assert len(codes)==644 and set(names)-codes=={"3550308"}
assert all(set(q["codes"])==codes and q["status"]=="pass" and q["difference_count"]==0 and q["issues"]=={} for q in source_qa.values())
db.executemany("INSERT INTO municipio(codigo_ibge,nome,uf) VALUES(?,?,?)",[(c,names[c],"SP") for c in sorted(codes)])
db.commit();db.close()
for year in (2023,2024,2025):
    run=40262193781 if year==2025 else 40263996213
    subprocess.run([sys.executable,"pipeline/build/import_tcesp_investimentos.py","--database",str(database),"--source",str(root/str(year)),"--year",str(year),"--source-run",str(run)],check=True)
db=sqlite3.connect(database)
assert db.execute("PRAGMA foreign_key_check").fetchall()==[]
assert db.execute("SELECT count(*) FROM observacao").fetchone()[0]==0
assert db.execute("SELECT count(*) FROM tcesp_lote").fetchone()[0]==3
report=[]
for y,q in source_qa.items():
    counts=[db.execute(f"SELECT COUNT(*) FROM {t} JOIN tcesp_lote USING(lote_id) WHERE exercicio=?",(y,)).fetchone()[0] for t in ("tcesp_investimento_programa","tcesp_investimento_acao")]
    assert counts==[q["programs"],q["actions"]]
    total=db.execute("SELECT SUM(valor_centavos) FROM tcesp_investimento_programa JOIN tcesp_lote USING(lote_id) WHERE exercicio=? AND estagio='valor liquidado'",(y,)).fetchone()[0]
    assert total==q["stage_liquidado_cents"]
    report.append({"year":y,"programs":counts[0],"actions":counts[1],"liquidado_centavos":total})
db.close()
out={"status":"pass","objects_verified":15,"municipalities":644,"excluded":["3550308"],"years":report,"publication_authorized":False}
(root/"qa_reconstruction.json").write_text(json.dumps(out,indent=2))
print("TCESP_R2_RECONSTRUCTION",json.dumps(out))
