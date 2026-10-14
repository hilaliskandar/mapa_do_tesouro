"""Evidence matrix for percentage observations, with no automatic certification."""
import argparse
import json
import sqlite3
from collections import Counter
from pathlib import Path


def audit(database: Path, output: Path):
    db = sqlite3.connect(database)
    try:
        pct = [r[0] for r in db.execute(
            "SELECT variavel_id FROM variavel WHERE unidade='percentual' ORDER BY variavel_id"
        )]
        rows = db.execute(
            """SELECT ano,variavel_id,status,COALESCE(referencia_origem,'<sem_origem>'),COUNT(*)
               FROM observacao WHERE variavel_id IN (
                 SELECT variavel_id FROM variavel WHERE unidade='percentual'
               ) GROUP BY ano,variavel_id,status,COALESCE(referencia_origem,'<sem_origem>')
               ORDER BY variavel_id,ano,status"""
        ).fetchall()
    finally:
        db.close()
    metrics = {(v,y): Counter() for v in pct for y in range(2021,2026)}
    for year, v, status, origin, n in rows:
        metrics.setdefault((v,year),Counter())[(status,origin)] += n
    result = []
    for v in pct:
        years = []
        for y in sorted({year for variable, year in metrics if variable == v}):
            entries = [{"status":s,"origin":o,"count":n}
                       for (s,o),n in sorted(metrics[(v,y)].items())]
            years.append({"year":y,"entries":entries,
                          "observed":sum(e["count"] for e in entries if e["status"]=="observado"),
                          "calculated_observed":sum(e["count"] for e in entries
                                  if e["status"]=="observado" and e["origin"]=="pipeline:ratio")})
        result.append({"variable_id":v,"years":years,
                       "storage_scale_certified":False,"display_multiplier":None})
    report={"scope":"percentages by fiscal year, status, and observation provenance",
            "percent_variable_count":len(pct),"variables":result,
            "publication_approval":False,
            "warning":"Provenance and arithmetic parity do not certify percentage display scale"}
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return report


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--database",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    print(json.dumps({"variables":audit(a.database,a.output)["percent_variable_count"]}))
