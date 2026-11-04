"""Verifica distribuição da classificação CAPAG contra snapshot oficial set/2026.

A checagem agregada nao substitui correspondencia por municipio.
"""
import argparse,json,sqlite3
from pathlib import Path
import yaml
EXPECTED={"A+":27,"A":108,"B+":17,"B":68,"C":371,"D":1,"n.d.":53}
def audit(database,output):
    with sqlite3.connect(database) as db:
        rows=db.execute("SELECT valor_texto,COUNT(*) FROM observacao WHERE ano=2025 AND variavel_id='capag' AND status='observado' GROUP BY valor_texto").fetchall()
    actual={str(k):v for k,v in rows}
    report={"reference":"capag-municipios-posicao-2026-set.xlsx","snapshot_date":"2026-09-01","legal_year":2025,"reference_sha256":"1b1379a5a531920223f1d448be155b70f51eb50180d8c819f1b7da3575a8eb11","expected":EXPECTED,"actual":actual,"matches":actual==EXPECTED,"scope":"histogram only; not municipality-level parity"}
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    if actual!=EXPECTED:raise ValueError("CAPAG divergente da distribuição oficial: "+str(actual))
    print("CAPAG: distribuicao SP645 compativel com snapshot oficial")
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--database",type=Path,required=True);p.add_argument("--output",type=Path,required=True)
    a=p.parse_args();audit(a.database,a.output)
