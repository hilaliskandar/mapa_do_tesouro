#!/usr/bin/env python3
"""Perfil estatístico sem identificadores para CSV SP de convênios importado em SQLite.

Este relatório não atribui nomes financeiros às colunas; valida propriedades
e detecta drift antes de mapeamento formal com dicionário oficial.
"""
from __future__ import annotations
import argparse
import json
import re
import sqlite3
from collections import Counter
from pathlib import Path

def looks_decimal(text: str) -> bool:
    return bool(re.fullmatch(r"-?\d+(?:[.,]\d+)?", text.strip()))
def looks_date(text: str) -> bool:
    return bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4}", text.strip()))
def profile(path: Path) -> dict:
    db=sqlite3.connect(path)
    cols=[f"col_{i:02}" for i in range(1,11)]
    rows=db.execute(f"SELECT {','.join(cols)} FROM sp_convenios_raw")
    nulls=[0]*10; dates=[0]*10; numbers=[0]*10; distinct=[set() for _ in range(10)]
    total=0
    for row in rows:
        total+=1
        for i,val in enumerate(row):
            text=(val or "").strip()
            if not text:
                nulls[i]+=1
            if looks_date(text):
                dates[i]+=1
            if looks_decimal(text):
                numbers[i]+=1
            if len(distinct[i])<5000:
                distinct[i].add(text)
    res=[{"posicao":i+1,"vazios":nulls[i],"numeric_format":numbers[i],
          "date_format":dates[i],"distinct_up_to_5000":len(distinct[i])} for i in range(10)]
    return {"rows":total,"columns":10,"profile":res,
            "status":"perfil_sem_validacao_semantica","personal_identifiers_exported":False}

def main():
    a=argparse.ArgumentParser()
    a.add_argument("--db",type=Path,required=True)
    args=a.parse_args()
    print(json.dumps(profile(args.db),ensure_ascii=False,sort_keys=True))
if __name__=="__main__":
    main()
