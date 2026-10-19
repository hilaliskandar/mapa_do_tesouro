"""Offline TCESP program/action decomposition for an explicit regional roster.

Input: CSV with columns codigo_ibge,municipio,slug; one per city.
Requires <slug>_<year>.json for 2023, 2024 and 2025, produced by
editorial/rmj/analyze_tcesp_pilot.py. Does not fetch from TCESP.
"""
from __future__ import annotations
import argparse
import csv
import json
from pathlib import Path

YEARS=(2023,2024,2025)
FIELDS=("nivel","codigo_ibge","municipio","ano_inicial","ano_final",
        "codigo_programa","codigo_acao","descricao_ano_inicial",
        "descricao_ano_final","situacao","liquidado_inicial_centavos",
        "liquidado_final_centavos","variacao_centavos")


def roster(path:Path, expected=34):
    with path.open(encoding="utf-8-sig",newline="") as stream:
        reader=csv.DictReader(stream)
        if not {"codigo_ibge","municipio","slug"} <= set(reader.fieldnames or ()):
            raise ValueError("Roster must have codigo_ibge, municipio and slug")
        rows=list(reader)
    if len(rows)!=expected:
        raise ValueError(f"Expected {expected} municipalities; found {len(rows)}")
    codes=set();slugs=set()
    for row in rows:
        code=row["codigo_ibge"].strip();slug=row["slug"].strip()
        if len(code)!=7 or not code.isascii() or not code.isdigit():
            raise ValueError(f"Invalid municipality code: {code}")
        if not slug or "/" in slug or "\\" in slug or slug.startswith("."):
            raise ValueError(f"Unsafe slug: {slug}")
        if code in codes or slug in slugs or not row["municipio"].strip():
            raise ValueError("Duplicate or unnamed municipality")
        codes.add(code);slugs.add(slug)
    return rows


def entries(doc,level):
    key="programas_44_liquidado_completos" if level=="programa" else "acoes_44_liquidado_completas"
    out={}
    for row in doc[key]:
        if level=="programa":
            program,name,_,cents=row;ident=(str(program),"")
        else:
            program,action,name,_,cents=row;ident=(str(program),str(action))
        if ident in out:raise ValueError(f"Duplicate TCESP key: {ident}")
        if isinstance(cents,bool) or not isinstance(cents,int):
            raise ValueError("Cent amount must be integer")
        out[ident]=(str(name).strip(),cents)
    if sum(x[1] for x in out.values())!=doc["investimento_44_liquidado_centavos"]:
        raise ValueError("TCESP aggregate mismatch")
    return out


def build(roster_csv:Path,raw:Path,output_csv:Path,*,expected=34):
    cities=roster(roster_csv,expected)
    docs={}
    for city in cities:
        slug=city["slug"].strip()
        for year in YEARS:
            file=raw/f"{slug}_{year}.json"
            if not file.is_file():raise FileNotFoundError(file)
            doc=json.loads(file.read_text(encoding="utf-8"))
            if doc.get("slug")!=slug or doc.get("year")!=year or doc.get("bad_values")!=0:
                raise ValueError(f"Unusable TCESP extract: {file}")
            entries(doc,"programa");entries(doc,"acao")
            docs[(slug,year)]=doc
    result=[];checks=0
    for city in cities:
        slug=city["slug"].strip()
        for start,end in zip(YEARS,YEARS[1:]):
            for level in ("programa","acao"):
                a=entries(docs[(slug,start)],level)
                b=entries(docs[(slug,end)],level)
                delta=0
                for key in sorted(set(a)|set(b)):
                    name0,v0=a.get(key,("",0))
                    name1,v1=b.get(key,("",0))
                    status=("somente_ano_final" if key not in a else
                            "somente_ano_inicial" if key not in b else
                            "mesmo_codigo_mesmo_nome" if name0==name1 else
                            "mesmo_codigo_nome_alterado")
                    row=(level,city["codigo_ibge"],city["municipio"],start,end,
                         key[0],key[1],name0,name1,status,v0,v1,v1-v0)
                    result.append(dict(zip(FIELDS,row)))
                    delta+=v1-v0
                expected_delta=(docs[(slug,end)]["investimento_44_liquidado_centavos"]-
                                docs[(slug,start)]["investimento_44_liquidado_centavos"])
                if delta!=expected_delta:raise ValueError("Period delta mismatch")
                checks+=1
    if checks!=expected*4:raise ValueError("Incomplete reconciliations")
    output_csv.parent.mkdir(parents=True,exist_ok=True)
    with output_csv.open("w",encoding="utf-8-sig",newline="") as stream:
        writer=csv.DictWriter(stream,fieldnames=FIELDS,delimiter=";")
        writer.writeheader();writer.writerows(result)
    return {"municipalities":len(cities),"source_documents":len(docs),
            "reconciliations":checks,"rows":len(result),
            "status":"candidate_tcesp_not_dca_certified"}


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("roster_csv",type=Path)
    parser.add_argument("raw_dir",type=Path)
    parser.add_argument("output_csv",type=Path)
    args=parser.parse_args()
    print(json.dumps(build(args.roster_csv,args.raw_dir,args.output_csv),ensure_ascii=False))
