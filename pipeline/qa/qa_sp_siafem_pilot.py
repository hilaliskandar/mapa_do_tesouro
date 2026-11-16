#!/usr/bin/env python3
"""QA de estrutura e cardinalidade do primeiro piloto SIAFEM (sem dados pessoais no log).

Não autoriza publicação e não trata valor de convênio como transferência paga.
"""
from __future__ import annotations
import argparse
import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path

def count_integer(value: str) -> int|None:
    t=value.strip().replace(".","").replace(" ","")
    return int(t) if re.fullmatch(r"\d+",t) else None

def parse_money(value: str) -> str|None:
    t=value.strip().replace("R$","").replace(" ","")
    if not t:return None
    if t.startswith("(") and t.endswith(")"):t="-"+t[1:-1]
    t=t.replace(".","").replace(",",".")
    return t if re.fullmatch(r"-?\d+(?:\.\d{1,2})?",t) else None

def parse_date(value: str) -> datetime|None:
    s=value.strip()
    for fmt in ("%d/%m/%Y","%Y-%m-%d","%d/%m/%y"):
        try:
            return datetime.strptime(s,fmt)
        except ValueError:pass
    return None

def date_status(value: str) -> str:
    s=value.strip()
    return "valid" if parse_date(s) is not None else ("empty" if not s else "unrecognized")

def profile(data: dict) -> dict:
    instruments=data["instruments"]
    payments=data["movement_rows"]
    if len(instruments)!=data["instrument_count"] or len(payments)!=data["movement_row_count"]:
        raise ValueError("inconsistencia com manifestos de contagem")
    refs={x["instrument_source_key"] for x in instruments}
    if len(refs)!=len(instruments):raise ValueError("instrumentos repetidos por chave")
    if any(m["instrument_source_key"] not in refs for m in payments):
        raise ValueError("parcela sem instrumento")
    actual=Counter(m["instrument_source_key"] for m in payments)
    qtys=[count_integer(x["raw_fields"][4]) for x in instruments]
    quantity_matches=[actual[x["instrument_source_key"]]==qtys[i] if qtys[i] is not None else False for i,x in enumerate(instruments)]
    dates=[]
    parsed_dates=[]
    monies=[]
    for m in payments:
        hdr=m["source_headers"]
        values=m["raw_fields"]
        if len(values)!=8 or len(hdr)!=8:
            raise ValueError("detalhe fora do contrato observado")
        if "Valor liberado/estornado" not in hdr[-1]:
            raise ValueError("coluna financeira mudou")
        date_col=next((i for i,x in enumerate(hdr) if x.strip().lower()=="data"),None)
        dates.append(date_status(values[date_col]) if date_col is not None else "header_missing")
        parsed_dates.append(parse_date(values[date_col]) if date_col is not None else None)
        monies.append(parse_money(values[-1]))
    period_start=parse_date(data["query"]["liberacao_inicio"])
    period_end=parse_date(data["query"]["liberacao_fim"])
    if period_start is None or period_end is None:
        raise ValueError("periodo da consulta inesperado")
    within=[d for d in parsed_dates if d is not None and period_start<=d<=period_end]
    observed=[d for d in parsed_dates if d is not None]
    summary={
        "source_id":"SP_SEFAZ","municipality_internal_code":data["query"]["municipio_code"],
        "period": [data["query"]["liberacao_inicio"],data["query"]["liberacao_fim"]],
        "instrument_count":len(instruments),"movement_rows":len(payments),
        "declared_payment_quantities_parseable":sum(x is not None for x in qtys),
        "instruments_with_matching_payment_count":sum(quantity_matches),
        "date_status_counts":dict(Counter(dates)),
        "movement_dates_within_selected_period":len(within),
        "movement_dates_outside_selected_period":len(observed)-len(within),
        "movement_date_min":min(observed).strftime("%Y-%m-%d") if observed else None,
        "movement_date_max":max(observed).strftime("%Y-%m-%d") if observed else None,
        "monetary_value_parseable":sum(x is not None for x in monies),
        "negative_monetary_values":sum(bool(x is not None and x.startswith("-")) for x in monies),
        "zero_monetary_values":sum(x in ("0","0.0","0.00") for x in monies),
        "nonempty_unparseable_monetary_values":sum(x is None for x in monies),
        "financial_homologated":False,
        "payment_dates_homologated":False,
        "coverage_homologated":False,
        "qa_class":"pilot_schema_and_cardinality"
    }
    return summary

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source",type=Path,required=True)
    args=p.parse_args()
    result=profile(json.loads(args.source.read_text(encoding="utf-8")))
    print(json.dumps(result,ensure_ascii=False,sort_keys=True))
if __name__=="__main__":
    main()
