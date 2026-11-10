#!/usr/bin/env python3
"""Inspect official 2024 Fundeb adjustment XLSX published April 2025.
No fiscal database or production modifications.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen
import openpyxl

SOURCES={
    "vaar_2024_adjustment":"https://www.gov.br/fnde/pt-br/acesso-a-informacao/acoes-e-programas/financiamento/fundeb/2025-1/AjustedaComplementaoVAAR.xlsx/@@download/file",
    "vaat_2024_adjustment":"https://www.gov.br/fnde/pt-br/acesso-a-informacao/acoes-e-programas/financiamento/fundeb/2025-1/AjustedaComplementaoVAAT.xlsx/@@download/file",
}
OUT=Path("build/fed04-fnde-2024")
CODE_SAMPLES=("3550308","3518800","3500105","3501608","3502804")
NAME_SAMPLES=("SAO PAULO","SÃO PAULO","GUARULHOS","ADAMANTINA","AMERICANA","ARACATUBA","ARAÇATUBA")

def inspect(label,url):
    out={"label":label,"url":url,"status":"unavailable"}
    try:
        with urlopen(Request(url,headers={"User-Agent":"Mozilla/5.0 (FED04 QA)"}),timeout=75) as r:
            raw=r.read(15*1024*1024+1);out["final_url"]=r.url;out["content_type"]=r.headers.get("Content-Type")
        out["bytes"]=len(raw)
        out["sha256"]=hashlib.sha256(raw).hexdigest()
        if not raw.startswith(b"PK") or len(raw)>15*1024*1024:
            out["status"]="not_xlsx_or_over_limit";return out
        file=OUT/f"{label}.xlsx";file.write_bytes(raw)
        wb=openpyxl.load_workbook(file,read_only=True,data_only=True)
        try:
            out["worksheets"]=[]
            for ws in wb:
                ws.reset_dimensions();found=[];first=[];n=0
                for line in ws.iter_rows(values_only=True):
                    n+=1
                    vals=[str(x).strip() if x is not None else "" for x in line]
                    cells=[v for v in vals if v]
                    if len(cells)>=3 and len(first)<10:
                        first.append({"row":n,"cells":cells[:16]})
                    if any(k in vals[:8] for k in CODE_SAMPLES) or any(any(nam in v.upper() for nam in NAME_SAMPLES) for v in vals[:7]):
                        if len(found)<60:found.append({"row":n,"cells":vals[:20]})
                out["worksheets"].append({"name":ws.title,"rows_scanned":n,"first_substantive":first,"sample_matches":found})
        finally:wb.close()
        out["status"]="read_success"
    except Exception as e:
        out["status"]="read_failed";out["error"]=f"{type(e).__name__}: {str(e)[:220]}"
    return out

def reconcile_with_2025_dca() -> dict:
    """Compare actual 2024 FNDE beneficiary keys to the 2025 DCA/FNDE QA matrix."""
    from decimal import Decimal
    matrix = Path("governance/FED04_MATRIZ_MUNICIPAL_FNDE_DCA_FUNDEB_2025_SP645_2026_11_10.csv")
    if not matrix.is_file():
        raise FileNotFoundError("2025 municipal QA matrix unavailable")
    from csv import DictReader
    with matrix.open(encoding="utf-8-sig", newline="") as fd:
        observations = list(DictReader(fd, delimiter=";"))
    if len(observations) != 645:
        raise AssertionError(f"Expected 645 municipal QA entries: {len(observations)}")
    winners = {}
    details = {}
    for mode in ("vaar","vaat"):
        path = OUT / f"{mode}_2024_adjustment.xlsx"
        wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
        values = {}
        try:
            for ws in wb:
                ws.reset_dimensions()
                for row in ws.iter_rows(values_only=True):
                    if len(row) < 6 or str(row[0]).strip() != "SP":
                        continue
                    code = str(row[2] or "").strip()
                    if len(code) != 7 or not code.isdigit():
                        continue
                    due = Decimal(str(row[3] or 0))
                    distributed = Decimal(str(row[4] or 0))
                    adjust = Decimal(str(row[5] or 0))
                    if due > 0 or distributed > 0:
                        if code in values:
                            raise AssertionError(f"Duplicate SP IBGE in 2024 {mode}: {code}")
                        values[code] = {"devido_2024": str(due), "distribuido_2024": str(distributed), "ajuste_publicado_2025": str(adjust)}
        finally:
            wb.close()
        winners[mode] = set(values)
        details[mode] = values
    classes = {}
    for ob in observations:
        classes.setdefault(ob["grupo_conciliacao"],[]).append(ob)
    unmatched = classes["somente_dca"]
    matched = [ob for ob in unmatched if ob["codigo_ibge"] in winners["vaat"]|winners["vaar"]]
    not2024 = [ob for ob in unmatched if ob["codigo_ibge"] not in winners["vaat"]|winners["vaar"]]
    def money(ob):
        return Decimal(ob["dca_complementacao_brl"] or "0")
    def summary(rows):
        return {"municipios":len(rows),"dca_receita_2025_soma_brl":str(sum((money(o) for o in rows),Decimal(0)))}
    bymode = {m:summary([o for o in unmatched if o["codigo_ibge"] in winners[m]]) for m in winners}
    priority=["3550308","3518800","3500105","3502804","3501608"]
    priority_cases=[]
    for id in priority:
        o=next((x for x in observations if x["codigo_ibge"]==id),None)
        priority_cases.append({"codigo_ibge":id,"nome":o["municipio"] if o else None,"dca_receita_2025":o["dca_complementacao_brl"] if o else None,"vaar_2024":details["vaar"].get(id),"vaat_2024":details["vaat"].get(id)})
    return {
        "fnde_2024_vaat_beneficiarios_sp":len(winners["vaat"]),
        "fnde_2024_vaar_beneficiarios_sp":len(winners["vaar"]),
        "fnde_2024_uniao_beneficiarios_sp":len(winners["vaat"]|winners["vaar"]),
        "dca_2025_somente_dca_total":summary(unmatched),
        "dca_2025_somente_dca_com_beneficio_FNDE_2024":summary(matched),
        "dca_2025_somente_dca_sem_beneficio_FNDE_2024_detectado":summary(not2024),
        "dca_2025_somente_dca_com_vaat_FNDE_2024":bymode["vaat"],
        "dca_2025_somente_dca_com_vaar_FNDE_2024":bymode["vaar"],
        "codigos_sem_correspondencia_2024_2025":sorted(o["codigo_ibge"] for o in not2024),
        "priority_cases":priority_cases,
        "source_period_caveat":"2024 eligibility and adjustment of obligations does not prove exact dates/amounts of DCA recognized revenue in 2025"
    }


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    result={"origin":"FNDE Portaria MEC/MF 3 of 2025-04-28: 2024 Fundeb annual adjustment","sources":[inspect(k,v) for k,v in SOURCES.items()],"accounting_application":"not_homologated"}
    result["cross_year_qa"] = reconcile_with_2025_dca()
    (OUT/"QA_FED04_FNDE_2024_AJUSTES.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("CROSS_YEAR_RECONCILIATION: "+json.dumps(result["cross_year_qa"],ensure_ascii=False))\n    print(json.dumps({"sources":[{"label":x["label"],"status":x["status"],"sha256":x.get("sha256"),"sheets":x.get("worksheets")} for x in result["sources"]]},ensure_ascii=False))

if __name__=="__main__":main()
