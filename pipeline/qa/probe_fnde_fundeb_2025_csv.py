#!/usr/bin/env python3
"""FED04: read public FNDE annual-adjustment CSV annexes, produce evidence only.

Source: 6th 2025 Fundeb publication, MEC/MF ordinance 5 of 2026-04-29.
Not monthly execution. Never writes to canonical SQLite or R2.
"""
from __future__ import annotations
import csv
import hashlib
import io
import json
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

BASE = (
    "https://www.gov.br/fnde/pt-br/acesso-a-informacao/acoes-e-programas/"
    "financiamento/fundeb/2025-1/6-publicacao-2013-portaria-mec-mf-n-5-de-29-de-abril-de-2026/"
)
FILES = {
    "receita_total": "1.ReceitatotaldoFundebporentefederado.csv",
    "vaaf_cronograma": "2.CronogramadedistribuiodacomplementaoVAAFporentefederado.csv",
    "vaat_complementacao": "3.VAATVAATMINecomplementaoVAATporentefederado.csv",
    "vaar_redes": "6.RedesbeneficiadascoeficientesdedistribuioecomplementaoVAAR.csv",
    "vaar_cronograma": "7.CronogramadedistribuiodacomplementaoVAARporentefederado.csv",
}
OUT = Path("build/fed04-fnde") / "QA_FNDE_FUNDEB_2025_PUBLICACAO_6.json"


def inspect(name: str, filename: str) -> dict:
    url = BASE + filename + "/@@download/file"
    out = {"dataset": name, "publication": "FNDE 2025 sixth publication / MEC-MF 5 of 2026-04-29", "url": url, "status": "not_downloaded"}
    try:
        req = Request(url, headers={"User-Agent":"Mozilla/5.0 (compatible; FED04 QA/1.0)", "Accept": "text/csv,*/*"})
        with urlopen(req, timeout=55) as conn:
            data = conn.read(12 * 1024 * 1024 + 1)
            out["http_status"] = conn.status
            out["content_type"] = conn.headers.get("Content-Type","")
            out["final_url"] = conn.url
        out["bytes"] = len(data)
        out["sha256"] = hashlib.sha256(data).hexdigest()
        if len(data) > 12 * 1024 * 1024:
            out["status"] = "too_large"
            return out
        if data[:4] == b"PK\x03\x04" or data.startswith(b"%PDF") or data.lstrip().startswith(b"<"):
            out["status"] = "not_csv_binary_or_html"
            out["first_bytes"] = data[:32].hex()
            return out
        text = None
        for encoding in ("utf-8-sig","windows-1252","latin-1"):
            try:
                text = data.decode(encoding)
                out["encoding"] = encoding
                break
            except UnicodeDecodeError:
                continue
        if text is None:
            out["status"] = "decode_failed"
            return out
        lines = [s for s in text.splitlines() if s.strip()]
        out["line_count"] = len(lines)
        for dialect in (csv.excel, csv.excel_tab):
            pass
        # Titles precede table headers in some FNDE annexes; retain first lines.
        out["first_lines"] = [s[:300] for s in lines[:9]]
        delims = {";": sum(s.count(";") for s in lines[:7]), ",": sum(s.count(",") for s in lines[:7]), "\t": sum(s.count("\t") for s in lines[:7])}
        sep = max(delims, key=delims.get)
        out["delimiter"] = repr(sep)
        records = list(csv.reader(io.StringIO(text), delimiter=sep))
        out["parsed_rows"] = len(records)
        # Avoid interpreting schedule as execution. Sample SP rows only for schema discovery.
        sp_rows = [r for r in records if any(str(x).strip().upper() in ("SP","SÃO PAULO","SAO PAULO") for x in r[:8])]
        out["sp_exact_token_rows"] = len(sp_rows)
        out["sp_samples"] = [r[:13] for r in sp_rows[:5]]
        out["status"] = "csv_schema_inspected_no_monetary_homologation"
    except (HTTPError, URLError, TimeoutError) as e:
        out["status"] = "unavailable"
        out["error"] = f"{type(e).__name__}: {str(e)[:200]}"
    except Exception as e:
        out["status"] = "inspection_error"
        out["error"] = f"{type(e).__name__}: {str(e)[:200]}"
    return out


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    results = [inspect(k,v) for k,v in FILES.items()]
    OUT.write_text(json.dumps({"release":"2025 annual-adjustment sixth publication", "not_actual_execution":True, "results":results},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(results,ensure_ascii=False))

if __name__ == "__main__":
    main()
