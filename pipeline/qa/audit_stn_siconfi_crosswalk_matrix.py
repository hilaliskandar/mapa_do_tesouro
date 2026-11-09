#!/usr/bin/env python3
"""Audit all 27 STN source pairs against a conservative SICONFI crosswalk candidate.

Checks exact coverage, row counts, uniqueness, no unverified accounting codes
or approved summations. Never modifies SQLite, R2 or public variables.
"""
from __future__ import annotations
import argparse,csv,hashlib,json
from collections import Counter
from pathlib import Path
from datetime import datetime,timezone

ORIGIN_SHA="3b9b5bf22748579a0f90912c160159b8d50a7664294a750fc74b2f98a59657fb"
CSV_COLUMNS=("transferencia_literal","item_literal","registros_sp_202609",
             "classe_triagem","comportamento_sinal_em_amostra","variavel_candidata_plataforma",
             "codigo_natureza_receita_2026","regra_de_uso","confianca","status_conciliacao",
             "fonte_stn","referencia_contabil_2026","proxima_verificacao")

def hashfile(p:Path)->str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def analyze(source:Path,matrix:Path,output:Path)->dict:
    qa={"timestamp_utc":datetime.now(timezone.utc).isoformat(),
        "status":"failed_or_unavailable","scope":"non-financial classification matrix QA"}
    try:
        qa["source_sha256"]=hashfile(source)
        if qa["source_sha256"]!=ORIGIN_SHA:raise ValueError("unapproved STN candidate input")
        obs=Counter()
        with source.open(encoding="utf-8",newline="") as f:
            for r in csv.DictReader(f,delimiter=";"):
                obs[(r["transferencia"],r["item_transferencia"])]+=1
        with matrix.open(encoding="utf-8-sig",newline="") as f:
            rd=csv.DictReader(f,delimiter=";")
            if tuple(rd.fieldnames or ())!=CSV_COLUMNS:
                raise ValueError("matrix header contract changed")
            entries=list(rd)
        values={}
        for r in entries:
            key=(r["transferencia_literal"],r["item_literal"])
            if key in values:raise ValueError("duplicate matrix pair")
            values[key]=int(r["registros_sp_202609"])
            if r["codigo_natureza_receita_2026"].strip():
                raise ValueError("unverified numeric revenue code inserted")
            if r["status_conciliacao"]!="pendente_homologacao":
                raise ValueError("unapproved accounting classification was promoted")
            if r["regra_de_uso"]!="nao_totalizar_sem_crosswalk_contabil":
                raise ValueError("unsafe summation flag")
            if r["variavel_candidata_plataforma"] and key!=("FPM","FPM"):
                raise ValueError("DCA variable mapped without documentary evidence")
        if len(obs)!=27 or len(entries)!=27 or sum(obs.values())!=13889 or values!=dict(obs):
            raise ValueError("matrix does not exhaustively match 27 source pairs and counts")
        qa.update({"status":"qa_pass_inventory_only",
                   "source_rows":sum(obs.values()),"source_pair_count":len(obs),
                   "matrix_rows":len(entries),"matrix_sha256":hashfile(matrix),
                   "unmapped_accounting_codes":sum(not r["codigo_natureza_receita_2026"] for r in entries),
                   "candidate_dca_variables":{k[0]+"/"+k[1]:r["variavel_candidata_plataforma"]
                       for k,r in zip(values.keys(),entries) if r["variavel_candidata_plataforma"]},
                   "financial_promotion_allowed":False,
                   "constraints":["All rows remain review candidates","No monetary aggregation, no inferred SICONFI nature codes",
                                  "Only FPM/FPM has a platform variable candidate, not an audited financial equality"]})
    except Exception as exc:
        qa["error"]=f"{type(exc).__name__}: {str(exc)[:280]}"
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(qa,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:qa.get(k) for k in ("status","source_pair_count","source_rows","error")},ensure_ascii=False))
    if qa["status"]!="qa_pass_inventory_only":raise SystemExit(2)
    return qa

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source",type=Path,required=True)
    p.add_argument("--matrix",type=Path,required=True)
    p.add_argument("--qa",type=Path,required=True)
    a=p.parse_args()
    analyze(a.source,a.matrix,a.qa)

if __name__=="__main__": main()
