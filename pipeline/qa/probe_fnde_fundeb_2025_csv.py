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
        out["nonempty_row_samples"] = [r[:18] for r in records if sum(bool(str(x).strip()) for x in r) >= 3][:9]
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


def _br_decimal(value: str):
    from decimal import Decimal, InvalidOperation
    value = str(value or "").strip().replace("R$", "").replace("\\xa0","")
    if not value or value in ("-", "-   ", "—"):
        return None
    try:
        return Decimal(value.replace(".", "").replace(",", "."))
    except InvalidOperation:
        return None


def _sp_amounts(file: str, amount_col: int) -> dict:
    """Read 2025 annex value for an IBGE7 code, ignoring repeated headers."""
    url = BASE + FILES[file] + "/@@download/file"
    with urlopen(Request(url, headers={"User-Agent": "Mozilla/5.0 (FED04 QA)"}), timeout=70) as conn:
        raw = conn.read(12 * 1024 * 1024 + 1)
    for enc in ("utf-8-sig", "windows-1252", "latin-1"):
        try:
            content = raw.decode(enc)
            break
        except UnicodeDecodeError:
            pass
    values = {}
    repeats = []
    for row in csv.reader(io.StringIO(content), delimiter=";"):
        if not row or row[0].strip() != "SP":
            continue
        ids = [v.strip() for v in row[:4] if len(v.strip())==7 and v.strip().isdigit() and v.strip().startswith("35")]
        if len(ids) != 1 or len(row) <= amount_col:
            continue
        code = ids[0]
        value = _br_decimal(row[amount_col])
        if value is None:
            continue
        if code in values:
            repeats.append(code)
        values[code] = value
    return {"values": values, "duplicates": sorted(set(repeats))}


def reconcile_annexes() -> dict:
    """Internal coherence, not equality to DCA realized revenue."""
    vaaf = _sp_amounts("vaaf_cronograma", 15)
    vaat = _sp_amounts("vaat_complementacao", 5)
    vaar = _sp_amounts("vaar_redes", 4)
    vaar_schedule = _sp_amounts("vaar_cronograma", 17)
    from decimal import Decimal
    keys = set(vaar["values"]) | set(vaar_schedule["values"])
    differences = []
    for code in sorted(keys):
        a=vaar["values"].get(code)
        b=vaar_schedule["values"].get(code)
        if a is None or b is None or abs(a-b) > Decimal("0.01"):
            differences.append({"codigo_ibge":code,"vaar_previsao":str(a),"vaar_cronograma":str(b)})
    return {
        "scope": "FNDE Portaria MEC/MF 5/2026 annual adjustment for 2025",
        "comparison": "VAAR official beneficiary annex vs VAAR official schedule",
        "vaar_beneficiaries_sp_with_amount":len(vaar["values"]),
        "vaar_schedule_sp_with_amount":len(vaar_schedule["values"]),
        "vaar_amount_parity_count":len(keys)-len(differences),
        "vaar_discrepancy_count":len(differences),
        "vaar_discrepancies_sample":differences[:20],
        "vaar_total_annex_brl":str(sum(vaar["values"].values(),Decimal(0))),
        "vaar_total_schedule_brl":str(sum(vaar_schedule["values"].values(),Decimal(0))),
        "vaat_sp_rows_with_value":len(vaat["values"]),
        "vaat_sp_positive_values":sum(v>0 for v in vaat["values"].values()),
        "vaat_sp_positive_ibge":sorted(k for k,v in vaat["values"].items() if v>0),
        "vaar_sp_positive_ibge":sorted(k for k,v in vaar["values"].items() if v>0),
        "vaat_total_brl":str(sum(vaat["values"].values(),Decimal(0))),
        "vaaf_sp_rows_with_value_index15":len(vaaf["values"]),
        "duplicates_by_annex": {name:len(res["duplicates"]) for name,res in [
          ("vaaf",vaaf),("vaat",vaat),("vaar_beneficiaries",vaar),("vaar_schedule",vaar_schedule)
        ]},
        "warning": "Final schedule includes January 2026 and annual adjustments. Do not equate to DCA cash receipts in calendar 2025."
    }


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    results = [inspect(k,v) for k,v in FILES.items()]
    reconciliation = reconcile_annexes()
    OUT.write_text(json.dumps({"release":"2025 annual-adjustment sixth publication", "not_actual_execution":True, "results":results, "reconciliation":reconciliation},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("RECONCILIATION: "+json.dumps(reconciliation,ensure_ascii=False))
    print(json.dumps(results,ensure_ascii=False))

if __name__ == "__main__":
    main()
