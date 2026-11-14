#!/usr/bin/env python3
"""Aggregate-only cardinality test for national Obrasgov/CIPI bridge datasets.

Outputs key-level counts only, no project identifiers, contract details or
personal data. It is not a fiscal amount or territorial attribution.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,zipfile
from collections import Counter,defaultdict
from datetime import datetime,timezone
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'acquire'))
from inv_sp645_transferegov_new_source_layout import acquire

SETS=("siconv_contrato_cipi","siconv_dados_obrasgov_geral","siconv_coordenadas_obra")

def read(path: Path, expected: set[str]):
    with zipfile.ZipFile(path) as z:
        fs=[x for x in z.namelist() if x.lower().endswith(".csv")]
        if len(fs)!=1:raise ValueError("CSV member count")
        if z.testzip() is not None:raise ValueError("ZIP CRC failure")
        with z.open(fs[0]) as bin:
            head=bin.readline()
            enc=next((e for e in ("utf-8-sig","cp1252") if _valid(head,e)),None)
            if not enc:raise ValueError("header encoding")
            hs=head.decode(enc,errors="strict")
            delim=";" if hs.count(";")>=hs.count(",") else ","
            columns=next(csv.reader([hs],delimiter=delim))
            if not expected.issubset(columns):raise ValueError("layout drift: "+str(expected-set(columns)))
            stream=io.TextIOWrapper(bin,encoding=enc,errors="strict",newline="")
            reader=csv.DictReader(stream,fieldnames=columns,delimiter=delim)
            for row in reader:
                if None in row:raise ValueError("invalid number of CSV columns")
                yield row
            stream.detach()

def _valid(v,e):
    try:v.decode(e,errors="strict");return True
    except UnicodeDecodeError:return False

def main():
    p=argparse.ArgumentParser();p.add_argument("--out-dir",required=True);p.add_argument("--timeout",type=int,default=240)
    x=p.parse_args();out=Path(x.out_dir);out.mkdir(parents=True,exist_ok=True)
    report={"utc":datetime.now(timezone.utc).isoformat(),"status":"in_progress",
      "source":"official national Transferegov CSV ZIP","no_personal_or_project_details":True,"datasets":{}}
    def save(): (out/"manifest_obra_cipi_key_qa.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    save()
    try:
        meta={}
        for name in SETS:
            path,d=acquire(out,name,x.timeout)
            meta[name]={"sha256_zip":d["sha256_zip"],"zip_bytes":d["zip_bytes"],"url":d["source_url"]}
            report["datasets"][name]=meta[name];save()
        general=Counter();n_general=0;null_general=0;instr=Counter()
        for row in read(out/"siconv_dados_obrasgov_geral.zip",{"id_projeto_investimento","nr_instrumento"}):
            n_general+=1
            key=(row.get("id_projeto_investimento") or "").strip()
            if key:general[key]+=1
            else:null_general+=1
            nr=(row.get("nr_instrumento") or "").strip()
            if nr:instr[nr]+=1
        project=Counter();n_contract=0;no_project=0;matched_rows=0
        for row in read(out/"siconv_contrato_cipi.zip",{"ID_CONTRATO","ID_PROJETO_INVESTIMENTO"}):
            n_contract+=1
            key=(row.get("ID_PROJETO_INVESTIMENTO") or "").strip()
            if not key:no_project+=1;continue
            project[key]+=1
            if key in general:matched_rows+=1
        coordinates=Counter();n_coord=0;missing_proposal=0
        for row in read(out/"siconv_coordenadas_obra.zip",{"ID_PROPOSTA","LATITUDE_CADASTRO_OBRA","LONGITUDE_CADASTRO_OBRA"}):
            n_coord+=1
            key=(row.get("ID_PROPOSTA") or "").strip()
            if key:coordinates[key]+=1
            else:missing_proposal+=1
        report["cardinality"]={
          "obrasgov_general":{"rows":n_general,"unique_project_ids":len(general),
              "missing_project_id_rows":null_general,
              "project_ids_with_repeated_rows":sum(n>1 for n in general.values()),
              "unique_instrument_numbers":len(instr),
              "instrument_numbers_with_repeated_rows":sum(n>1 for n in instr.values())},
          "contracts_cipi":{"rows":n_contract,"unique_nonempty_project_ids":len(project),
              "rows_without_project_id":no_project,
              "contract_rows_with_project_id_found_in_obrasgov_general":matched_rows,
              "distinct_contract_projects_found_in_obrasgov_general":sum(k in general for k in project),
              "contract_project_ids_with_multiple_rows":sum(n>1 for n in project.values()),
              "potential_1n_join_expansion_rows":sum(n*general[k] for k,n in project.items() if k in general)},
          "project_coordinates":{"rows":n_coord,"unique_proposal_ids":len(coordinates),
              "rows_missing_proposal_id":missing_proposal,
              "proposals_with_multiple_coordinate_rows":sum(n>1 for n in coordinates.values())}
        }
        report["status"]="qa_done_unclassified_not_territorialized";save()
        print(json.dumps({"status":report["status"],"cardinality":report["cardinality"]},ensure_ascii=False))
        for name in SETS:(out/(name+".zip")).unlink()
    except Exception as e:
        report["status"]="blocked";report["error"]=str(e)[:350];save();raise
if __name__=="__main__":main()
