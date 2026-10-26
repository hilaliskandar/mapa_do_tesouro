#!/usr/bin/env python3
"""Import approved statewide TCESP group-44 aggregates into a DEVELOPMENT SQLite copy.
No changes to observacao; transaction rollback on missing municipalities or failed reconciliation.
"""
import argparse,collections,csv,json,sqlite3,pathlib
p=argparse.ArgumentParser();p.add_argument("--database",type=pathlib.Path,required=True);p.add_argument("--source",type=pathlib.Path,required=True);p.add_argument("--year",type=int,default=2025)
a=p.parse_args()
qa=json.loads((a.source/"qa.json").read_text(encoding="utf-8"))
assert qa["status"]=="pass" and qa["year"]==a.year and qa["issues"]=={} and qa["difference_count"]==0
lote=f"tcesp_despesas_{a.year}_run_40262193781" if a.year==2025 else f"tcesp_despesas_{a.year}_qa"
con=sqlite3.connect(a.database)
con.execute("PRAGMA foreign_keys=ON")
try:
 with con:
  con.execute("INSERT INTO tcesp_lote(lote_id,exercicio,source_sha256,artifact_run,qa_status) VALUES(?,?,?,?,?)",(lote,a.year,qa["sha256_zip"],40262193781 if a.year==2025 else 0,"pass"))
  def read(name):
   with (a.source/name).open(newline="",encoding="utf-8") as f:
    yield from csv.DictReader(f)
  for tab,name,cols in [
   ("tcesp_investimento_programa","investimentos_grupo44_por_programa.csv",["codigo_ibge","mes","estagio","orgao","cd_programa","ds_programa","centavos"]),
   ("tcesp_investimento_acao","investimentos_grupo44_por_acao.csv",["codigo_ibge","mes","estagio","orgao","cd_programa","ds_programa","cd_acao","ds_acao","centavos"])]:
   query=f"INSERT INTO {tab}(lote_id,{','.join('valor_centavos' if x=='centavos' else x for x in cols)}) VALUES({','.join('?' for _ in range(len(cols)+1))})"
   con.executemany(query,((lote,*[int(r[c]) if c in ("mes","centavos") else r[c] for c in cols]) for r in read(name)))
  def grouped(table):
   return {(r[0],r[1],r[2]):r[3] for r in con.execute(f"SELECT codigo_ibge,mes,estagio,SUM(valor_centavos) FROM {table} WHERE lote_id=? GROUP BY 1,2,3",(lote,))}
  pr=grouped("tcesp_investimento_programa");ac=grouped("tcesp_investimento_acao")
  assert pr==ac,"Programs/actions disagree"
  expected={(r["codigo_ibge"],int(r["mes"]),r["estagio"]):int(r["centavos"]) for r in read("investimentos_grupo44_por_municipio_mes_estagio.csv")}
  assert pr==expected,"Municipal stage aggregates disagree"
  assert sum(v for k,v in pr.items() if k[2]=="valor liquidado")==qa["stage_liquidado_cents"]
 print(json.dumps({"status":"pass","lote_id":lote,"rows_programas":con.execute("SELECT count(*) FROM tcesp_investimento_programa WHERE lote_id=?",(lote,)).fetchone()[0],"rows_acoes":con.execute("SELECT count(*) FROM tcesp_investimento_acao WHERE lote_id=?",(lote,)).fetchone()[0]}))
finally:con.close()
