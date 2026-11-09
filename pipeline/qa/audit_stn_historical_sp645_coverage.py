#!/usr/bin/env python3
"""FED03: exhaustive historical FPM and ITR source coverage (1996-2026).

Reads two immutable national wide STN CSV files and the previously vetted
September 2026 SP645 candidate. Outputs:
- yearly coverage by 31 years, separately for Brazil and SP
- a validated crosswalk from source COD_MUN + UF to SP IBGE7
- anomalies (duplicates, gaps, unmatched names, invalid numbers)
NO fiscal aggregation, forced missing-as-zero, SQLite writes or publishing.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

SHA = {
    "FPM": "a86cad831115e02518198f4873967785a82eb3cbae651ef8505aa498c2cab088",
    "ITR": "9c93138d30b3c384ccb05ea91edbb8e6ee6f807f26ee2ce359e0a3e5b25f44ec",
    "stage": "3b9b5bf22748579a0f90912c160159b8d50a7664294a750fc74b2f98a59657fb",
}
YEARS = [str(y) for y in range(1996, 2027)]
META = ["COD_MUN", "Município", "UF", "Município - UF", "Mês"]
CROSSWALK_HEADER = ["uf", "cod_mun_stn_literal", "municipio_stn_historico",
                    "codigo_ibge", "municipio_stn_202609",
                    "tipo_correspondencia", "prova_mes", "source_sha256"]
COVERAGE_HEADER = ["transferencia", "territorio", "ano", "linhas_municipio_mes",
                   "municipios_cod_mun_unicos", "celulas_numericas",
                   "celulas_positivas", "celulas_zeros", "celulas_negativas",
                   "celulas_ausentes", "celulas_invalidas"]

def sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1048576), b""):
            h.update(chunk)
    return h.hexdigest()

def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s.casefold().replace("’", "'"))
    return re.sub("[^a-z0-9]", "", "".join(x for x in s if not unicodedata.combining(x)))

def cell_kind(s: str) -> str:
    s = s.strip()
    if not s or s in ("-", "—", "N/A", "NA"): return "absent"
    if re.fullmatch(r"-?(?:[0-9]{1,3}(?:\.[0-9]{3})+|[0-9]+),[0-9]{1,2}", s) or re.fullmatch(r"-?[0-9]+", s):
        clean = s.replace(".", "").replace(",", ".")
        try:
            from decimal import Decimal
            n = Decimal(clean)
        except Exception:
            return "invalid"
        return "zero" if n == 0 else ("negative" if n < 0 else "positive")
    return "invalid"

def candidates(stage_path: Path) -> dict[str, tuple[str,str]]:
    names = {}
    with stage_path.open(encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f, delimiter=";"):
            if r["ano"] != "2026" or r["mes"] != "09": raise ValueError("Unexpected_stage_period")
            code = r["codigo_ibge"]
            if code in names and names[code] != r["municipio_stn"]:
                raise ValueError("Contradictory stage municipality names")
            names[code] = r["municipio_stn"]
    if len(names) != 645: raise ValueError("Stage IBGE universe is not 645 municipalities")
    inv = defaultdict(list)
    for code,name in names.items(): inv[norm(name)].append(code)
    if any(len(x)>1 for x in inv.values()): raise ValueError("Ambiguous stage municipal name")
    return {key:(codes[0],names[codes[0]]) for key,codes in inv.items()}

def run(fpm: Path, itr: Path, stage: Path, coverage: Path, crosswalk: Path, qa_path: Path) -> dict:
    qa = {"utc": datetime.now(timezone.utc).isoformat(), "status": "failed",
          "scope": "STN FPM and ITR source coverage and municipal identity, not fiscal values"}
    try:
        hashes = {"FPM":sha(fpm), "ITR":sha(itr), "stage":sha(stage)}
        qa["input_sha256"] = hashes
        if hashes != SHA: raise ValueError("Input hash does not match archived source")
        name_index = candidates(stage)
        alias = {
            ("6401", norm("Embu")): ("3515004", norm("Embu das Artes")),
            ("6717", norm("Moji Mirim")): ("3530805", norm("Mogi-Mirim")),
        }
        results = {}
        all_coverage = []
        crosswalk_by_source = {}
        for label,path in (("FPM",fpm),("ITR",itr)):
            coverage_by_year = defaultdict(lambda:{"rows":0,"places":set(),"cells":Counter()})
            refs = {}
            rowkeys = set()
            duplicate_rows = []
            month_counts = Counter()
            stn_codes = defaultdict(set)
            coverage_details = Counter()
            invalid_samples = []
            all_rows = 0
            invalid_geographic_rows = Counter()
            invalid_geographic_samples = []
            with path.open(encoding="cp1252", newline="") as f:
                rd = csv.DictReader(f, delimiter=";")
                if rd.fieldnames != META+YEARS: raise ValueError(label+": unexpected historical CSV columns")
                for r in rd:
                    all_rows += 1
                    mun = r["COD_MUN"].strip()
                    uf = r["UF"].strip().upper()
                    month = r["Mês"].strip()
                    n = r["Município"].strip()
                    if not mun or not n or not uf or month not in [str(i) for i in range(1,13)]:
                        reason=("month_outside_1_12" if month not in [str(i) for i in range(1,13)]
                                else "missing_geographic_identifier")
                        invalid_geographic_rows[reason] += 1
                        if len(invalid_geographic_samples)<25:
                            invalid_geographic_samples.append({
                                "source_line":all_rows+1,"uf":uf,"cod_mun":mun,
                                "municipio":n,"mes":month,"year_2026_cell":r.get("2026","")[:30],
                                "reason":reason})
                        continue
                    key = (uf,mun,month)
                    if key in rowkeys:
                        duplicate_rows.append(key)
                    rowkeys.add(key)
                    month_counts[month] += 1
                    stn_codes[(uf,mun)].add(n)
                    sp = uf == "SP"
                    if sp:
                        ref = name_index.get(norm(n))
                        match_kind = "normalized_name"
                        if not ref:
                            a = alias.get((mun,norm(n)))
                            if a and a[1] in name_index and name_index[a[1]][0] == a[0]:
                                ref = name_index[a[1]]
                                match_kind = "verified_historical_alias"
                        if month == "9":
                            if ref and mun in refs and refs[mun]["codigo_ibge"] != ref[0]:
                                raise ValueError(label+": conflicting SP crosswalk in September")
                            if ref:
                                refs[mun] = {"uf":"SP", "cod_mun_stn_literal":mun,
                                             "municipio_stn_historico":n,
                                             "codigo_ibge":ref[0],
                                             "municipio_stn_202609":ref[1],
                                             "tipo_correspondencia":match_kind,
                                             "prova_mes":"2026/09", "source_sha256":hashes[label]}
                            else:
                                coverage_details["sp_september_unmatched_names"] += 1
                        if not ref: coverage_details["sp_unmatched_rows"] += 1
                    for year in YEARS:
                        kind = cell_kind(r[year])
                        for territory in ("BR","SP") if sp else ("BR",):
                            entry = coverage_by_year[(territory,year)]
                            entry["rows"] += 1
                            entry["places"].add((uf,mun))
                            entry["cells"][kind] += 1
                        if kind == "invalid" and len(invalid_samples)<30:
                            invalid_samples.append({"uf":uf,"cod_mun":mun,"month":month,
                                                    "year":year,"sample":r[year][:40]})
            for (territory,year),entry in sorted(coverage_by_year.items()):
                c = entry["cells"]
                all_coverage.append([label,territory,year,entry["rows"],
                    len(entry["places"]),c["positive"]+c["negative"]+c["zero"],
                    c["positive"],c["zero"],c["negative"],c["absent"],c["invalid"]])
            results[label] = {
                "source_rows": all_rows,
                "invalid_or_auxiliary_geographic_rows":sum(invalid_geographic_rows.values()),
                "invalid_or_auxiliary_reasons":dict(sorted(invalid_geographic_rows.items())),
                "invalid_or_auxiliary_samples":invalid_geographic_samples,
                "eligible_municipal_month_rows":len(rowkeys),
                "distinct_source_municipality_uf_keys":len(stn_codes),
                "month_row_counts":dict(sorted(month_counts.items(),key=lambda x:int(x[0]))),
                "duplicate_uf_codmun_month_count":len(duplicate_rows),
                "duplicate_sample":duplicate_rows[:20],
                "source_code_conflicting_names_count":sum(len(names)>1 for names in stn_codes.values()),
                "source_code_conflicting_names_examples":[{"uf":x[0],"cod_mun":x[1],"names":sorted(v)}
                  for x,v in stn_codes.items() if len(v)>1][:20],
                "sp_2026_september_cod_mun_mapped":len(refs),
                "sp_2026_september_ibge_distinct":len({x["codigo_ibge"] for x in refs.values()}),
                "sp_2026_september_alias_rows":sum(x["tipo_correspondencia"]=="verified_historical_alias" for x in refs.values()),
                "sp_unmatched_rows":coverage_details["sp_unmatched_rows"],
                "sp_september_unmatched_names":coverage_details["sp_september_unmatched_names"],
                "invalid_cell_samples":invalid_samples
            }
            crosswalk_by_source[label] = refs
        if len(crosswalk_by_source["FPM"])!=645 or len(crosswalk_by_source["ITR"])!=645:
            raise ValueError("SP645 cod_mun crosswalk from September does not cover 645")
        fpm_codes = {k:v["codigo_ibge"] for k,v in crosswalk_by_source["FPM"].items()}
        itr_codes = {k:v["codigo_ibge"] for k,v in crosswalk_by_source["ITR"].items()}
        if fpm_codes != itr_codes or len(set(fpm_codes.values())) != 645:
            raise ValueError("FPM and ITR STN historical code crosswalks disagree")
        for label in ("FPM","ITR"):
            if results[label]["duplicate_uf_codmun_month_count"]:
                raise ValueError(label+": duplicate municipality/month source key")
        if len(all_coverage)!=len(YEARS)*4: raise ValueError("Coverage year count not 124")
        coverage.parent.mkdir(parents=True,exist_ok=True)
        with coverage.open("w",encoding="utf-8",newline="") as f:
            w=csv.writer(f,delimiter=";");w.writerow(COVERAGE_HEADER);w.writerows(all_coverage)
        crosswalk.parent.mkdir(parents=True,exist_ok=True)
        with crosswalk.open("w",encoding="utf-8",newline="") as f:
            w=csv.DictWriter(f,fieldnames=CROSSWALK_HEADER,delimiter=";")
            w.writeheader()
            for k in sorted(crosswalk_by_source["FPM"]):
                w.writerow(crosswalk_by_source["FPM"][k])
        qa.update({
            "status": "qa_pass_coverage_and_identity_only",
            "years": YEARS, "source_summary":results,
            "crosswalk_sp645_entries":645,
            "crosswalk_sha256":sha(crosswalk),"coverage_sha256":sha(coverage),
            "coverage_rows":len(all_coverage),
            "caveats":[
                "Column year exists even if every municipality has an absent value",
                "The 645-code crosswalk is checked for September 2026 SP only and must not be projected to historical extinct/created municipalities without checks",
                "Missing markers are absent observations, not zero fiscal declarations",
                "COD_MUN is a source identifier, never directly assumed to be IBGE",
                "No financial aggregation, SQLite writes, or published variables",
            ],
        })
    except Exception as e:
        qa.update({"status":"failed_or_unavailable","error":f"{type(e).__name__}: {str(e)[:450]}"})
    qa_path.parent.mkdir(parents=True,exist_ok=True)
    qa_path.write_text(json.dumps(qa,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:qa.get(k) for k in
                      ("status","coverage_rows","crosswalk_sp645_entries","error")},ensure_ascii=False))
    if qa["status"]!="qa_pass_coverage_and_identity_only": raise SystemExit(2)
    return qa

def main():
    p=argparse.ArgumentParser()
    for x in ("fpm","itr","stage","coverage","crosswalk","qa"):
        p.add_argument("--"+x,required=True,type=Path)
    a=p.parse_args()
    run(a.fpm,a.itr,a.stage,a.coverage,a.crosswalk,a.qa)
if __name__=="__main__": main()
