#!/usr/bin/env python3
"""FED00: exhaustive STN item×transfer class diagnostics, no financial aggregation.

Input is an immutable R2 candidate CSV with 13,889 rows. Outputs QA JSON
and a classification review matrix. Does not change canonical SQLite/R2 or
make revenue claims; raw monetary fields are inspected only for signs/formats.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

PINNED_SHA = "3b9b5bf22748579a0f90912c160159b8d50a7664294a750fc74b2f98a59657fb"
FIELDS = ("decendio_1_raw", "decendio_2_raw", "decendio_3_raw")
REQUIRED = {"codigo_ibge","municipio_stn","ano","mes","transferencia","item_transferencia",
            *FIELDS,"source_resource_id","source_sha256","data_status"}
SOURCE_SHA = "097638cec48145ac0f509d526be49d40929d177ef3a2ae3b7f77c0acd990cf24"
RESOURCE_ID = "63b5f470-135f-4431-9158-ca8b7a43f61b"

def digest(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1_048_576), b""):
            h.update(chunk)
    return h.hexdigest()

def cell_type(value: str) -> str:
    if not value: return "blank"
    if re.fullmatch(r"-?[0-9]+(?:\.[0-9]{1,2})?",value):
        if value.startswith("-"): return "negative"
        if re.fullmatch(r"0+(?:\.0+)?",value): return "zero"
        return "positive"
    return "invalid"

def interpretive_flag(classe: str, item: str) -> tuple[str,str]:
    """ONLY a screening hypothesis. Never an approved classification for summation."""
    c,i=classe.upper(),item.upper()
    if "AJUSTE" in c: return "ajuste_a_reconciliar","Ajuste retroativo; nao agregar sem validar relacao com os eventos originais"
    if "DEDU" in i or "DEDU" in c: return "deducao_a_reconciliar","Item indicativo de deducao; determinar sinal e relacao com principal"
    if c=="FUNDEB": return "fundeb_componente_a_reconciliar","Componentes do Fundeb; risco de somar parcela de formacao e repasse"
    if c=="FPM 1%": return "parcela_adicional_a_reconciliar","Parcela extraordinaria; averiguar autonomia diante de FPM regular"
    if c=="FPM": return "principal_fpm_a_reconciliar","Verificar composicao do valor e deducoes do Fundeb"
    if c=="ITR": return "principal_itr_a_reconciliar","Verificar deducoes e regras do item antes de receita comparavel"
    if "ROYALT" in c: return "royalties_a_reconciliar","Verificar natureza legal e subcomponentes antes de somar"
    return "outro_a_reconciliar","Identificar rubrica conforme metadados STN e reconciliar com natureza de receita"

def main() -> None:
    p=argparse.ArgumentParser()
    p.add_argument("--input",type=Path,required=True)
    p.add_argument("--matrix",type=Path,required=True)
    p.add_argument("--qa",type=Path,required=True)
    a=p.parse_args()
    report={"checked_at_utc":datetime.now(timezone.utc).isoformat(),
            "scope":"FED00 September 2026 STN SP645 classification screening; no amounts summed",
            "status":"failed_or_unavailable"}
    try:
        sha=digest(a.input)
        if sha!=PINNED_SHA: raise ValueError("unexpected_input_sha256")
        stats=defaultdict(lambda:{"rows":0,"municipalities":set(),"cells":Counter()})
        total_cells=Counter()
        distinct=set()
        count=0
        for_row=0
        with a.input.open("r",encoding="utf-8-sig",newline="") as f:
            reader=csv.DictReader(f,delimiter=";")
            if not REQUIRED.issubset(set(reader.fieldnames or [])):
                raise ValueError("unexpected_stage_headers")
            for row in reader:
                count+=1
                if row["ano"]!="2026" or row["mes"]!="09" or row["source_sha256"]!=SOURCE_SHA or row["source_resource_id"]!=RESOURCE_ID:
                    raise ValueError("unexpected_source_or_period")
                k=(row["codigo_ibge"],row["ano"],row["mes"],row["transferencia"],row["item_transferencia"])
                if k in distinct: raise ValueError("duplicated_row_grain")
                distinct.add(k)
                group=(row["transferencia"],row["item_transferencia"])
                stat=stats[group]
                stat["rows"]+=1
                stat["municipalities"].add(row["codigo_ibge"])
                for column in FIELDS:
                    status=cell_type(row[column].strip())
                    stat["cells"][status]+=1
                    total_cells[status]+=1
                    if status=="invalid": raise ValueError("unrecognized_monetary_cell_format")
        if count!=13889 or sum(total_cells.values())!=41667:
            raise ValueError("unexpected_row_count")
        columns=["transferencia_literal","item_transferencia_literal","qtd_linhas","qtd_municipios",
                 "celulas_positivas","celulas_negativas","celulas_zero","celulas_vazias",
                 "categoria_triagem_nao_homologada","risco_triagem","pode_somar"]
        matrix=[]
        for (c,i),st in sorted(stats.items()):
            flag,reason=interpretive_flag(c,i)
            matrix.append([c,i,st["rows"],len(st["municipalities"]),
                           st["cells"]["positive"],st["cells"]["negative"],
                           st["cells"]["zero"],st["cells"]["blank"],
                           flag,reason,"nao_sem_conciliacao"])
        a.matrix.parent.mkdir(parents=True,exist_ok=True)
        with a.matrix.open("w",encoding="utf-8",newline="") as out:
            writer=csv.writer(out,delimiter=";")
            writer.writerow(columns)
            writer.writerows(matrix)
        report.update({"status":"qa_pass_descriptive_only","input_sha256":sha,
                       "rows":count,"distinct_grain":len(distinct),
                       "distinct_transfer_item_pairs":len(stats),
                       "monetary_cells":dict(sorted(total_cells.items())),
                       "classes":dict(sorted(Counter({k:sum(s["rows"] for (c,i),s in stats.items() if c==k)
                                                     for k,_ in stats}).items())),
                       "matrix_sha256":digest(a.matrix),
                       "matrix_bytes":a.matrix.stat().st_size,
                       "limitations":["Descriptions are only editorial triage flags; no financial classification approved",
                                      "Positive/negative counts are signs of source numeric strings, not totals",
                                      "No transfer, Fundeb, adjustment or decendial amounts are summed",
                                      "No SQLite writes; no website publication"]})
    except Exception as e:
        report.update({"status":"failed_or_unavailable",
                       "error":f"{type(e).__name__}: {str(e)[:350]}"})
    a.qa.parent.mkdir(parents=True,exist_ok=True)
    a.qa.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:report.get(k) for k in ("status","rows","distinct_transfer_item_pairs","monetary_cells","error")},ensure_ascii=False))
    if report["status"]!="qa_pass_descriptive_only": raise SystemExit(2)

if __name__=="__main__":
    main()
