#!/usr/bin/env python3
"""Audit official Transferegov CSV ZIP layouts, without publishing microdata.

Each ZIP is acquired once per invocation. Entire compressed member is read to
validate CRC, while only the header and limited sample are decoded for layout.
No names, document identifiers, payment values or row samples are published.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
import tempfile
import time
import urllib.error
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path

URL = "https://api-publica.transferegov.gestao.gov.br/downloads/dadosgov/"
ALLOWED = {
    "siconv_itens_dl", "siconv_pagamento_tributo",
    "siconv_ingresso_contrapartida", "siconv_coordenadas_obra",
    "siconv_contrato_cipi", "siconv_dados_obrasgov_geral"
}
RETRIABLE = {429, 500, 502, 503, 504}


def acquire(folder: Path, name: str, timeout: int) -> tuple[Path, dict]:
    dest = folder / f"{name}.zip"
    issues = []
    for attempt in range(4):
        tmp = folder / (name + ".zip.partial")
        try:
            sha = hashlib.sha256()
            req = urllib.request.Request(URL + name + ".zip",
                    headers={"User-Agent":"sp645-federal-investments-schema-audit/1.0"})
            with urllib.request.urlopen(req, timeout=timeout) as response, tmp.open("wb") as target:
                for block in iter(lambda:response.read(1024 * 1024), b""):
                    sha.update(block)
                    target.write(block)
            os.replace(tmp, dest)
            return dest, {"sha256_zip":sha.hexdigest(), "zip_bytes":dest.stat().st_size,
                           "source_url":URL + name + ".zip"}
        except urllib.error.HTTPError as e:
            issues.append(f"HTTP {e.code}")
            if e.code not in RETRIABLE:raise
        except (TimeoutError, urllib.error.URLError) as e:
            issues.append(type(e).__name__)
        finally:
            if tmp.exists():tmp.unlink()
        if attempt < 3: time.sleep(3 * (attempt + 1))
    raise RuntimeError(f"{name}: source fetch failed after bounded retries: {issues}")


def audit(path: Path, sample_limit: int, full_count: bool) -> dict:
    with zipfile.ZipFile(path) as z:
        files = [x for x in z.infolist() if not x.is_dir() and x.filename.lower().endswith(".csv")]
        if len(files) != 1: raise ValueError(f"expected exactly 1 CSV; found {len(files)}")
        info = files[0]
        with z.open(info, "r") as binary:
            first = binary.readline(262145)
            if len(first) > 262144:raise ValueError("header too long")
            encoding = None
            for candidate in ("utf-8-sig", "cp1252"):
                try:
                    header = first.decode(candidate, errors="strict")
                    encoding = candidate
                    break
                except UnicodeDecodeError:pass
            if encoding is None:raise ValueError("header encoding not supported")
            delimiter = ";" if header.count(";") >= header.count(",") else ","
            columns = next(csv.reader([header], delimiter=delimiter))
            if len(columns) != len(set(columns)) or any(not x.strip() for x in columns):
                raise ValueError("empty or duplicate CSV headers")
            candidate_keys = [c for c in columns if any(s in c.upper()
                for s in ("ID_DL", "ID_ITEM", "ITEM_PAD", "PROPOSTA", "CONVENIO",
                           "NR_MOV", "ID_CONTRATO", "ID_EMPENHO", "CIPI",
                           "COORDENADA", "LATITUDE", "LONGITUDE"))]
            required_candidates = {
                "siconv_itens_dl": ["DL"],
                "siconv_pagamento_tributo": ["PAG", "MOV", "DL"],
                "siconv_coordenadas_obra": ["OBRA", "COORD", "PROPOSTA"],
                "siconv_contrato_cipi": ["CIPI", "CONTRATO"],
            }
            row_count = 0
            sample = []
            stream = io.TextIOWrapper(binary, encoding=encoding,
                       errors="strict", newline="")
            reader = csv.reader(stream, delimiter=delimiter)
            for values in reader:
                row_count += 1
                if len(values) != len(columns):
                    raise ValueError(f"CSV row width mismatch at row {row_count}")
                if len(sample) < sample_limit:
                    sample.append(tuple(bool(v.strip()) for v in values))
                if not full_count and row_count >= sample_limit:
                    break
            stream.detach()
        # ZipFile.testzip streams through the entire decompressed CSV and verifies CRC;
        # prevents a successfully fetched but truncated/corrupt compressed dataset.
        crc_failed = z.testzip()
        if crc_failed:raise ValueError("ZIP CRC invalid")
        sampled_nonempty = {
            col:sum(int(flags[i]) for flags in sample)
            for i,col in enumerate(columns)
        }
        return {"csv_member":info.filename,"csv_uncompressed_bytes":info.file_size,
                "encoding_header_and_sample":encoding,"delimiter":delimiter,
                "columns":columns, "columns_count":len(columns),
                "candidate_join_columns":candidate_keys,
                "sample_rows":len(sample),"sample_nonempty_by_column":sampled_nonempty,
                "national_rows":row_count if full_count else None,
                "full_csv_scan":full_count,"zip_crc":"verified",
                "note":"No row contents or personal records stored in output"}


def main() -> None:
    p=argparse.ArgumentParser()
    p.add_argument("--out-dir",required=True)
    p.add_argument("--dataset",action="append",required=True)
    p.add_argument("--timeout",type=int,default=240)
    p.add_argument("--sample-limit",type=int,default=1000)
    p.add_argument("--full-count",action="store_true")
    args=p.parse_args()
    if not set(args.dataset)<=ALLOWED or len(set(args.dataset))!=len(args.dataset):
        raise SystemExit("Unknown or repeated dataset")
    out=Path(args.out_dir);out.mkdir(parents=True,exist_ok=True)
    report={"timestamp_utc":datetime.now(timezone.utc).isoformat(),
       "status":"in_progress","scope":"national metadata-only ZIP inspection",
       "no_financial_classification":True,
       "not_production":True,"sources":[]}
    def save():
        (out/"manifest_new_sources.json").write_text(
            json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    save()
    for name in args.dataset:
        item={"name":name,"status":"in_progress"}
        report["sources"].append(item);save()
        try:
            path,meta=acquire(out,name,args.timeout)
            item.update(meta);save()
            item.update(audit(path,args.sample_limit,args.full_count))
            item["status"]="verified"
            path.unlink()
        except Exception as e:
            item.update({"status":"blocked","error":str(e)[:400]})
        save()
        print(json.dumps({"dataset":name,"status":item["status"],
             "columns":item.get("columns"),"rows":item.get("national_rows"),
             "sample_rows":item.get("sample_rows"),"error":item.get("error")},
              ensure_ascii=False),flush=True)
    report["status"]="verified_all" if all(x["status"]=="verified"
                        for x in report["sources"]) else "partial_or_blocked"
    save()
    if report["status"]!="verified_all":raise SystemExit(2)

if __name__=="__main__":main()
