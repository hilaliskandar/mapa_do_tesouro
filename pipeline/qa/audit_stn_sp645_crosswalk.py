#!/usr/bin/env python3
"""FED00: audit R2-stored STN candidate crosswalk against the *actual* SP645 SQLite build.

Read-only against SQLite. Does not modify `municipio`, `observacao` or source files.
A matching set of IDs is necessary, but not sufficient, for publication approval.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sqlite3
import unicodedata
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

CROSSWALK_SHA = "20c80f6464de30f899430327db569fd7a52610c14bfc88678b769638572f036c"

def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fd:
        for b in iter(lambda: fd.read(1024 * 1024), b""):
            h.update(b)
    return h.hexdigest()

def simplify_name(value: str) -> str:
    import re
    value = unicodedata.normalize("NFKD", str(value).casefold())
    value = "".join(c for c in value if not unicodedata.combining(c))
    return " ".join(re.sub(r"[^a-z0-9]+", " ", value).split())

def audit(database: Path, candidate: Path) -> dict:
    result: dict = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "failed_or_unavailable",
        "scope": "SP645 SQLite municipality identity vs STN candidate; not fiscal value approval",
        "database_file": str(database),
        "candidate_file": str(candidate),
    }
    if not database.is_file() or not candidate.is_file():
        result["error"] = "missing_input_file"
        return result
    result["candidate_sha256"] = sha256_file(candidate)
    if result["candidate_sha256"] != CROSSWALK_SHA:
        result["error"] = "candidate_sha256_differs_from_approved_snapshot"
        return result
    with candidate.open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream, delimiter=";")
        expected = {"municipio_stn", "municipio_referencia", "codigo_ibge", "match_method"}
        if not expected.issubset(set(reader.fieldnames or [])):
            result["error"] = "candidate_header_contract_mismatch"
            result["fields"] = reader.fieldnames
            return result
        candidate_rows = list(reader)
    result["candidate_rows"] = len(candidate_rows)
    source_codes = [r["codigo_ibge"].strip() for r in candidate_rows]
    source_names = [r["municipio_stn"].strip() for r in candidate_rows]
    result["candidate_unique_codes"] = len(set(source_codes))
    result["candidate_unique_names"] = len(set(source_names))
    result["candidate_invalid_codes"] = sorted(
        {code for code in source_codes if len(code) != 7 or not code.isdigit() or not code.startswith("35")}
    )
    if len(candidate_rows) != 645 or len(set(source_codes)) != 645 or len(set(source_names)) != 645 or result["candidate_invalid_codes"]:
        result["error"] = "candidate_identity_count_mismatch"
        return result

    # Open database in immutable query-only mode: never silently create or modify DB.
    abs_path = database.resolve()
    uri = "file:" + quote(str(abs_path), safe="/:") + "?mode=ro"
    conn = sqlite3.connect(uri, uri=True)
    try:
        conn.execute("PRAGMA query_only=ON")
        tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        if not {"municipio", "universo_municipio", "universo"}.issubset(tables):
            result["error"] = "missing_canonical_municipality_tables"
            return result
        rows = conn.execute(
            """SELECT m.codigo_ibge, m.nome, m.uf
               FROM municipio m
               JOIN universo_municipio u ON m.codigo_ibge=u.codigo_ibge
               WHERE u.universo_id='SP_645'"""
        ).fetchall()
    finally:
        conn.close()
    original_codes = [str(r[0]) for r in rows]
    db_by_code = {str(code): {"nome": name, "uf": uf} for code, name, uf in rows}
    result["sqlite_sp645_rows"] = len(rows)
    result["sqlite_sp645_unique_codes"] = len(db_by_code)
    result["sqlite_non_sp_uf"] = sorted({str(r[2]) for r in rows if r[2] != "SP"})
    result["stn_missing_in_sqlite"] = sorted(set(source_codes) - set(db_by_code))
    result["sqlite_missing_in_stn"] = sorted(set(db_by_code) - set(source_codes))
    result["sqlite_duplicate_code_rows"] = len(rows) - len(set(original_codes))
    result["name_differences"] = [
        {"codigo_ibge": row["codigo_ibge"], "nome_stn": row["municipio_stn"],
         "nome_sqlite": db_by_code[row["codigo_ibge"]]["nome"],
         "method": row["match_method"]}
        for row in candidate_rows
        if row["codigo_ibge"] in db_by_code and
        simplify_name(row["municipio_stn"]) != simplify_name(db_by_code[row["codigo_ibge"]]["nome"])
    ]
    result["match_method_counts"] = dict(sorted(Counter(r["match_method"] for r in candidate_rows).items()))
    result["restrictions"] = [
        "Exact IBGE-code parity does not certify municipality source names as current official names",
        "This audit does not validate STN decimal scale, decendial totals, category definitions, paid amounts or fiscal accounting",
        "No SQLite writes, R2 writes or website publication are performed",
    ]
    ok = (len(rows) == 645 and len(db_by_code) == 645
          and not result["sqlite_non_sp_uf"]
          and not result["stn_missing_in_sqlite"]
          and not result["sqlite_missing_in_stn"]
          and result["sqlite_duplicate_code_rows"] == 0)
    result["status"] = "qa_pass_identity_only" if ok else "requires_review"
    return result

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--database", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = audit(args.database, args.candidate)
    except (OSError, sqlite3.DatabaseError, csv.Error, ValueError, UnicodeError) as e:
        result = {"status": "failed_or_unavailable", "error": f"{type(e).__name__}: {str(e)[:400]}"}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({k: result.get(k) for k in ("status", "candidate_rows", "sqlite_sp645_rows",
                                                   "stn_missing_in_sqlite", "sqlite_missing_in_stn", "error")},
                     ensure_ascii=False))
    if result["status"] != "qa_pass_identity_only":
        raise SystemExit(2)

if __name__ == "__main__":
    main()
