"""Audit DCA function presence before conversion to flat municipal tables."""
import argparse
import csv
import json
from collections import Counter
from pathlib import Path

from pipeline.normalize.dca import load_bundle, load_mapping, normalize_bundle
from pipeline.acquire.siconfi_dca import annex_slug

FUNCTIONS = (
    "dca_func_urbanismo_liquidada", "dca_func_habitacao_liquidada",
    "dca_func_saneamento_liquidada", "dca_func_gestao_ambiental_liquidada",
    "dca_func_transporte_liquidada",
)


def audit(root: Path, year: int, mapping_file: Path, output: Path):
    mapping = load_mapping(mapping_file)
    annex = "DCA-Anexo I-E"
    directory = root / annex_slug(annex) / str(year)
    if not directory.exists():
        raise FileNotFoundError(directory)
    details = []
    counts = {var: Counter() for var in FUNCTIONS}
    files = sorted(directory.glob("*.json.gz"))
    if not files:
        raise ValueError(f"No raw DCA annex found in {directory}")
    for f in files:
        code = f.name.removesuffix(".json.gz")
        payloads = load_bundle(root, code, year, [annex])
        result = normalize_bundle(payloads, mapping={"variables":{
            key:mapping["variables"][key] for key in FUNCTIONS
        }})
        for var in FUNCTIONS:
            entry = result["variables"][var]
            value = entry["value"]
            source = entry.get("source") or {}
            if entry["status"] == "observado":
                category = "explicit_numeric_zero" if float(value)==0 else "explicit_nonzero"
            elif entry["status"] == "em_revisao":
                category = "ambiguous_multiple_matches"
            elif source.get("rule") == "missing_annex":
                category = "missing_annex"
            elif source.get("cod_conta") is not None and source.get("conta_regex") is not None:
                category = "matching_row_not_found"
            elif source.get("conta") is not None:
                category = "matching_row_blank_value"
            else:
                category = "unclassified_missing"
            counts[var][category] += 1
            details.append({"codigo_ibge":code,"ano":year,"variavel_id":var,
                            "categoria":category,"valor":value})
    report={"source":"raw DCA I-E annex payload", "year":year,
            "annex_files":len(files),
            "coverage":{k:dict(v) for k,v in counts.items()},
            "limitations":"A missing row is not proof of declared zero."}
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    with output.with_suffix(".csv").open("w",newline="",encoding="utf-8") as file:
        writer=csv.DictWriter(file,fieldnames=list(details[0]))
        writer.writeheader()
        writer.writerows(details)
    return report


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--raw-root",type=Path,required=True)
    p.add_argument("--year",type=int,default=2025)
    p.add_argument("--mapping",type=Path,default=Path("data/mappings/dca_canonical_v1.yml"))
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    print(json.dumps(audit(a.raw_root,a.year,a.mapping,a.output),ensure_ascii=False))
