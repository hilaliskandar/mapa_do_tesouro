#!/usr/bin/env python3
"""Compara indicadores 1-3 CAPAG por codigo IBGE com XLSX oficial de set/2026."""
import argparse,collections,hashlib,json,math,sqlite3
from pathlib import Path
import openpyxl
SHA="1b1379a5a531920223f1d448be155b70f51eb50180d8c819f1b7da3575a8eb11"
FIELDS={"indicador_1":4,"indicador_2":6,"indicador_3":8}
def audit(xlsx,db_path,out):
 if hashlib.sha256(xlsx.read_bytes()).hexdigest()!=SHA:raise ValueError("SHA CAPAG oficial divergente")
 book=openpyxl.load_workbook(xlsx,read_only=True,data_only=True)
 try:
  ws=book["Prévia da CAPAG"];reference={}
  for row in ws.iter_rows(min_row=4,max_col=9,values_only=True):
   if row[2]!="SP":continue
   code=str(row[0]).strip()
   if code in reference:raise ValueError("CAPAG IBGE duplicado: "+code)
   reference[code]=row
 finally:book.close()
 if len(reference)!=645:raise ValueError("Fonte CAPAG sem 645 codigos SP")
 counts={};mismatches=[]
 with sqlite3.connect(db_path) as con:
  for name,ix in FIELDS.items():
   candidate={c:(s,v) for c,s,v in con.execute("SELECT codigo_ibge,status,valor_num FROM observacao WHERE ano=2025 AND variavel_id=?",(name,))}
   if set(candidate)!=set(reference):raise ValueError("Conjunto de codigos diferente: "+name)
   observed=absent=0
   for code,row in reference.items():
    raw=row[ix];status,value=candidate[code]
    valid_num=isinstance(raw,(int,float)) and not isinstance(raw,bool)
    if valid_num:
     observed+=1;match=status=="observado" and value is not None and math.isclose(float(raw),float(value),rel_tol=1e-10,abs_tol=1e-10)
    else:
     absent+=1;match=status=="ausente" and value is None
    if not match:mismatches.append({"codigo_ibge":code,"variavel":name,"oficial":str(raw),"status_api":status,"valor_api":value})
   counts[name]={"observado":observed,"ausente":absent}
 result={"source_sha256":SHA,"sheet":"Prévia da CAPAG","source_columns":{"ibge":"A","indicador_1":"E","indicador_2":"G","indicador_3":"I"},"municipalities":len(reference),"coverage":counts,"comparisons":1935,"mismatch_count":len(mismatches),"mismatches":mismatches}
 out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 if len(mismatches) or counts!={"indicador_1":{"observado":644,"ausente":1},"indicador_2":{"observado":642,"ausente":3},"indicador_3":{"observado":623,"ausente":22}}:raise ValueError("Cotejo CAPAG componentes falhou")
 return result
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--xlsx",type=Path,required=True);p.add_argument("--database",type=Path,required=True);p.add_argument("--out",type=Path,required=True)
 a=p.parse_args();print(json.dumps(audit(a.xlsx,a.database,a.out)["coverage"],ensure_ascii=False))
