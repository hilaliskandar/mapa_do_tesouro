#!/usr/bin/env python3
"""FED04: retrieve and inspect official STN revenue ementarios without promoting data.

Only PDF/XLSX/ZIP/HTML metadata and selected account rows are reported.
Never creates municipal observations nor changes SQLite/R2.
"""
from __future__ import annotations

import csv
import hashlib
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from zipfile import is_zipfile

import openpyxl

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "build/fed04-ementarios"
SOURCES = {
    2017: "https://sisweb.tesouro.gov.br/apex/f?p=2501:9::::9:P9_ID_PUBLICACAO:43289",
    2018: "https://sisweb.tesouro.gov.br/apex/f?p=2501:9::::9:P9_ID_PUBLICACAO:27683",
    2022: "https://sisweb.tesouro.gov.br/apex/f?p=2501:9::::9:P9_ID_PUBLICACAO:40027",
    2025: "https://thot-arquivos.tesouro.gov.br/publicacao-anexo/26142",
}
LOOKUPS = {
    "fpm": ("17210102", "17180120", "17115110", "17115100"),
    "itr": ("17210105", "17180150", "17115200"),
    "fundeb_recebido": ("17240100", "17580100", "17510000"),
    "fundeb_complementacao": ("17240200", "17180900", "17150000"),
}
# Normalized accounting codes without punctuation or 'RO' prefix.
CODE_RE = re.compile(r"\b(?:RO)?\s*([0-9](?:\s*[.\-]?\s*[0-9]){6,15})\b", re.I)


def normalized(value: object) -> str:
    return re.sub("[^0-9]", "", str(value or ""))


def retrieve(year: int, url: str) -> dict:
    result = {
        "year": year, "source_url": url, "status": "not_retrieved",
        "source_type": "", "matches": [], "matching_counts": {},
    }
    try:
        request = Request(url, headers={
            "User-Agent": "Mozilla/5.0 (compatible; FED04-document-QA/1.0)",
            "Accept": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,"
                      "application/octet-stream,application/zip,application/pdf,text/html,*/*",
        })
        with urlopen(request, timeout=75) as response:
            result["final_url"] = response.url
            result["http_status"] = response.status
            result["content_type"] = response.headers.get("Content-Type", "")
            data = response.read(35 * 1024 * 1024 + 1)
        result["bytes"] = len(data)
        result["sha256"] = hashlib.sha256(data).hexdigest()
        if len(data) > 35 * 1024 * 1024:
            result["status"] = "too_large_limit_35mb"
            return result
        if data.startswith(b"PK"):
            # openpyxl reads only XLSX; preserve actual result type if zip not workbook
            result["source_type"] = "xlsx_or_zip"
            saved = OUT / f"ementario_{year}_{result['sha256'][:12]}.xlsx"
            saved.write_bytes(data)
            try:
                book = openpyxl.load_workbook(saved, read_only=True, data_only=True)
                try:
                    result["worksheets"] = book.sheetnames
                    for sheet in book:
                        sheet.reset_dimensions()
                        line_no = 0
                        for row in sheet.iter_rows(values_only=True):
                            line_no += 1
                            if not any(v is not None for v in row):
                                continue
                            cells = [str(v).strip() for v in row if v is not None][:12]
                            joined = " | ".join(cells)
                            # Exact accounting code match only, rather than regex guessing.
                            digits = [normalized(v) for v in cells]
                            for concept, codes in LOOKUPS.items():
                                if any(any(d == code or d.endswith(code) for code in codes) for d in digits):
                                    if len(result["matches"]) < 150:
                                        result["matches"].append({
                                            "concept": concept, "sheet": sheet.title,
                                            "row_number": line_no, "cells": cells[:8],
                                        })
                                    result["matching_counts"][concept] = result["matching_counts"].get(concept, 0) + 1
                        result.setdefault("sheet_rows_scanned", {})[sheet.title] = line_no
                finally:
                    book.close()
                result["status"] = "xlsx_scanned"
            except Exception as exc:
                result["status"] = "xlsx_parse_failed"
                result["parse_error"] = f"{type(exc).__name__}: {str(exc)[:240]}"
            return result
        if data.startswith(b"%PDF"):
            result["source_type"] = "pdf"
            result["status"] = "pdf_not_analyzed_binary"
            return result
        if data.lstrip()[:1] == b"<":
            result["source_type"] = "html"
            result["status"] = "html_landing_page_no_ementario_binary"
            result["title_excerpt"] = re.sub(r"\s+", " ", data[:1500].decode("utf-8", errors="replace"))[:180]
            return result
        result["source_type"] = "unknown"
        result["status"] = "unsupported_binary"
    except (HTTPError, URLError, TimeoutError) as exc:
        result["status"] = "unavailable_or_blocked"
        result["error"] = f"{type(exc).__name__}: {str(exc)[:220]}"
    except Exception as exc:
        result["status"] = "inspection_error"
        result["error"] = f"{type(exc).__name__}: {str(exc)[:220]}"
    return result


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = [retrieve(y, url) for y, url in SOURCES.items()]
    summary = {
        "status": "document_retrieval_qa_completed",
        "checked_utc": datetime.now(timezone.utc).isoformat(),
        "documentation_only": True,
        "can_homologate_all_years": False,
        "source_results": rows,
    }
    (OUT / "QA_FED04_EMENTARIOS_OFICIAIS.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        "results": [{"year": r["year"], "status": r["status"],
                     "bytes": r.get("bytes"), "sha256": r.get("sha256"),
                     "final_url": r.get("final_url"),
                     "matches": r["matching_counts"],
                     "sample": [
                         {"concept": m["concept"], "sheet": m["sheet"],
                          "row": m["row_number"], "cells": m["cells"][:5]}
                         for m in r["matches"][:24]
                     ],
                     "error": r.get("error")} for r in rows]
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
