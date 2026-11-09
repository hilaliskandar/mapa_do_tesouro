#!/usr/bin/env python3
"""FED04: actual 2025 FINBRA/SICONFI overlap audit from a rebuilt, isolated SP645 SQLite.

Read-only on temporary database. Distinguishes catalog variable, mapped source
column, actual observed vs explicit zero/absent, and external-federal concepts.
No changes to canonical observations, R2 or published site.
"""
from __future__ import annotations
import argparse,csv,json,sqlite3,hashlib
from collections import Counter
from pathlib import Path
from datetime import datetime,timezone

AUDIT_ITEMS=[
  ("STN_FPM_REGULAR","FPM regular","dca_fpm_cota_mensal","overlap_requires_accounting_reconciliation",
   "DCA annual declared regular share vs STN monthly credit; do not combine historical FPM and additional FPM twice"),
  ("STN_FPM_EXTRA","FPM cotas extraordinarias","", "potentially_new_disaggregation",
   "Historic FPM includes September supplement; keep separate from dca_fpm_cota_mensal"),
  ("STN_ITR","ITR cota-parte","", "potentially_new_explicit_variable",
   "No specific ITR variable in core catalog; may be subsumed in other DCA accounts, verify actual mapped DCA structure"),
  ("STN_FUNDEB","Fundeb transferencias e deducoes","", "requires_accounting_reconciliation",
   "Separate distributions, adjustments, 20 percent formation and municipal receipts; no summation"),
  ("STN_ROYALTIES","Royalties CFEM FEP ANP ITA","", "potentially_new_explicit_variable",
   "May be contained in broader DCA revenue categories; verify nature, category and stage"),
  ("STN_LC176","LC 176/2020","", "potentially_new_explicit_variable",
   "Check municipal revenue classification and possible consolidation in DCA before expanding indicators"),
  ("DCA_ICMS","ICMS cota-parte","dca_icms_cota_parte","already_catalogued",
   "State transfer already declared by municipalities; STN Fundeb ICMS component is not an equivalent revenue item"),
  ("DCA_IPVA","IPVA cota-parte","dca_ipva_cota_parte","already_catalogued",
   "State transfer already declared by municipalities; Fundeb component may overlap"),
  ("BCB_IPCA","IPCA nacional SGS 433","", "contextual_not_municipal",
   "Only one national deflator by time; avoid duplicating per municipality or replacing verified official series"),
  ("BCB_SELIC","Selic meta SGS 432","", "contextual_not_municipal",
   "National macroeconomic context; data source has shown future-dated anomalies in earlier probe"),
  ("BCB_ESTBAN","ESTBAN saldos bancarios municipais","", "new_subject_matter",
   "Municipal deposits and credit balances, not FINBRA revenues or STN transfers"),
  ("TRANSFEREGOV","Parcerias e execucao federal","", "new_event_detail",
   "Instrument-specific proposals, commitments and payments with distinct legal/temporal meanings"),
  ("CGU","CGU convenio emenda execucao","", "new_event_detail",
   "Federal source verification to avoid duplicated events across other federal APIs"),
  ("OBRASGOV","Obrasgov obras e projetos","", "new_event_detail",
   "Projects, geolocation and physical progress, not municipal revenues"),
]
FIELDS=["fonte_grupo","conceito","variavel_sqlite_id","classificacao_conceitual",
        "variavel_cadastrada_no_sqlite","fonte_preferencial","observacoes_2025_total",
        "observado_2025","zero_explicito_2025","ausente_2025","nao_aplicavel_2025",
        "em_revisao_2025","outra_situacao_2025","criterio_de_integracao"]
def analyze(dbpath:Path,manifest:Path,csvout:Path,qaout:Path):
    qa={"audited_at_utc":datetime.now(timezone.utc).isoformat(),"status":"failed",
        "database":str(dbpath),"scope":"isolated imported 2025 canonical workbook; not production historical SQLite"}
    try:
        uri=dbpath.resolve().as_uri()+"?mode=ro"
        db=sqlite3.connect(uri,uri=True)
        db.execute("PRAGMA query_only=ON")
        tables={r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        if not {"municipio","fonte","variavel","observacao","universo_municipio"}.issubset(tables):
            raise ValueError("canonical core tables absent")
        if db.execute("SELECT COUNT(*) FROM municipio WHERE uf='SP'").fetchone()[0]!=645:
            raise ValueError("expected 645 Sao Paulo municipalities")
        vars={r[0]:(r[1],r[2]) for r in db.execute(
            "SELECT variavel_id,fonte_preferencial_id,periodicidade FROM variavel")}
        manifestdata=json.loads(manifest.read_text(encoding="utf-8"))
        counts={}
        for label,concept,vid,category,notes in AUDIT_ITEMS:
            n=Counter()
            if vid in vars:
                for status,value,number in db.execute(
                    "SELECT status, CASE WHEN valor_num=0 AND status='observado' THEN 1 ELSE 0 END, COUNT(*) "
                    "FROM observacao WHERE ano=2025 AND variavel_id=? GROUP BY status, CASE WHEN valor_num=0 AND status='observado' THEN 1 ELSE 0 END",
                    (vid,)):
                    n[status]+=number
                    if value:n["zero"]+=number
            counts[label]=n
        rows=[]
        for label,concept,vid,category,notes in AUDIT_ITEMS:
            present=vid in vars
            n=counts[label]
            rows.append([label,concept,vid,category,"sim" if present else "nao",
                         vars[vid][0] if present else "",sum(n.values())-(n["zero"] if False else 0),
                         n["observado"],n["zero"],n["ausente"],n["nao_aplicavel"],
                         n["em_revisao"],sum(v for k,v in n.items() if k not in
                            ("observado","zero","ausente","nao_aplicavel","em_revisao")),notes])
        csvout.parent.mkdir(parents=True,exist_ok=True)
        with csvout.open("w",encoding="utf-8",newline="") as f:
            writer=csv.writer(f,delimiter=";")
            writer.writerow(FIELDS);writer.writerows(rows)
        qa.update({"status":"qa_pass_2025_actual_db_only",
                   "mun_sp":645,"catalog_variable_count":len(vars),
                   "catalog_sources":sorted({x[0] for x in db.execute("SELECT fonte_id FROM fonte")}),
                   "actual_observation_count_2025":db.execute(
                       "SELECT COUNT(*) FROM observacao WHERE ano=2025").fetchone()[0],
                   "fpm":dict(counts["STN_FPM_REGULAR"]),
                   "icms":dict(counts["DCA_ICMS"]),"ipva":dict(counts["DCA_IPVA"]),
                   "concepts_checked":len(rows),"catalog_fpm_present":"dca_fpm_cota_mensal" in vars,
                   "catalog_itr_specific_present":any("itr" in k.lower() for k in vars),
                   "catalog_fundeb_specific_present":any("fundeb" in k.lower() for k in vars),
                   "manifest_sha256":hashlib.sha256(manifest.read_bytes()).hexdigest(),
                   "csv_sha256":hashlib.sha256(csvout.read_bytes()).hexdigest(),
                   "limitations":["This is an isolated 2025 import of the current canonical 2025 R2 workbook and repo mapping; it does NOT prove full 2013-2025 SQLite availability",
                                  "Absent ITR-specific variable does not prove ITR revenue absent from broader DCA accounts",
                                  "An observed zero is a value in the municipal declared account, not a missing STN source record",
                                  "No accounting equivalence between DCA reported receipts and STN cash transfers was inferred",
                                  "No canonical SQLite, R2 nor frontend data writes"]})
        if sum(counts["STN_FPM_REGULAR"].values())!=645:
            raise ValueError("2025 FPM observation status count not 645")
        db.close()
    except Exception as e:
        qa.update({"status":"failed_or_unavailable","error":f"{type(e).__name__}: {str(e)[:370]}"})
    qaout.parent.mkdir(parents=True,exist_ok=True)
    qaout.write_text(json.dumps(qa,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:qa.get(k) for k in ("status","mun_sp","concepts_checked","actual_observation_count_2025","fpm","error")},ensure_ascii=False))
    if qa["status"]!="qa_pass_2025_actual_db_only":raise SystemExit(2)

def main():
    p=argparse.ArgumentParser()
    for n in ("database","manifest","matrix","qa"):p.add_argument("--"+n,type=Path,required=True)
    a=p.parse_args()
    analyze(a.database,a.manifest,a.matrix,a.qa)
if __name__=="__main__":main()
