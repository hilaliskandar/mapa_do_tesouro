"""Auditoria independente CAPAG e RREO contra SQLite SP645 privado.

Arquivos de entrada devem ser preservados com hashes verificaveis.
Nao modifica o banco nem os dados de origem.
"""
import argparse,collections,csv,hashlib,io,json,math,sqlite3,zipfile
from pathlib import Path
import openpyxl

CAPAG_SHA="1b1379a5a531920223f1d448be155b70f51eb50180d8c819f1b7da3575a8eb11"
RREO_CSV_SHA="d66d92bd8b75e319d0c6bb432961e791f2c5ad10d25f197b3a10db512ed75ba3"
CAPAG_EXPECTED={"A+":27,"A":108,"B+":17,"B":68,"C":371,"D":1,"n.d.":53}

def sha(content):
    return hashlib.sha256(content).hexdigest()

def compare(db_path,capag_xlsx,rreo_zip,out):
    capag_bytes=capag_xlsx.read_bytes()
    if sha(capag_bytes)!=CAPAG_SHA:raise ValueError("SHA CAPAG nao corresponde ao snapshot oficial")
    wb=openpyxl.load_workbook(capag_xlsx,read_only=True,data_only=True)
    try:
        sheet=wb["Prévia da CAPAG"]
        official={}
        for cells in sheet.iter_rows(min_row=4,max_col=28,values_only=True):
            if cells[2]!="SP":continue
            code=str(cells[24]).strip()
            value=str(cells[27]).strip()
            if code in official:raise ValueError("Codigo duplicado no CAPAG "+code)
            official[code]=value
    finally:wb.close()
    if len(official)!=645 or dict(collections.Counter(official.values()))!=CAPAG_EXPECTED:
        raise ValueError("Tabela CAPAG oficial mudou ou colunas incorretas")
    with zipfile.ZipFile(rreo_zip) as z:
        raw=z.read("normalized/rreo_rcl_2025.csv")
        if sha(raw)!=RREO_CSV_SHA:raise ValueError("SHA RREO nao corresponde ao Gate C")
        reference=list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"))))
    capag_mismatch=[];rreo_mismatch=[];observed=0;absent=0
    with sqlite3.connect(db_path) as db:
        actual=dict(db.execute("SELECT codigo_ibge,valor_texto FROM observacao WHERE ano=2025 AND variavel_id='capag' AND status='observado'"))
        for code,v in official.items():
            if actual.get(code)!=v:capag_mismatch.append({"codigo_ibge":code,"oficial":v,"canonico":actual.get(code)})
        values={code:(state,val) for code,state,val in db.execute("SELECT codigo_ibge,status,valor_num FROM observacao WHERE ano=2025 AND variavel_id='rreo_rcl_oficial'")}
        for rec in reference:
            code=rec["cod_ibge"];raw=rec["rreo_rcl_total_12m"]
            status,value=values.get(code,(None,None))
            if raw in ("",None):
                absent+=1;match=status=="ausente" and value is None
            else:
                observed+=1
                match=(status=="observado" and value is not None and math.isclose(float(raw),float(value),abs_tol=.01,rel_tol=1e-10))
            if not match:rreo_mismatch.append({"codigo_ibge":code,"oficial":raw,"status":status,"canonico":value})
    result={"source_sha256":{"capag":CAPAG_SHA,"rreo_normalized_csv":RREO_CSV_SHA},
     "capag":{"scope":"Prévia da CAPAG colunas 25 e 28; nao confundir com tabela colunas 1-4","compared":len(official),"mismatches":capag_mismatch,"official_distribution":CAPAG_EXPECTED},
     "rreo":{"scope":"Anexo 03 periodo 6 2025 RCL últimos 12 meses","compared":len(reference),"observed":observed,"absent":absent,"mismatches":rreo_mismatch}}
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    if len(actual)!=645 or len(reference)!=645 or observed!=531 or absent!=114 or capag_mismatch or rreo_mismatch:
        raise ValueError("Paridade externa CAPAG/RREO reprovada")
    return result

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--database",required=True,type=Path)
    p.add_argument("--capag",required=True,type=Path)
    p.add_argument("--rreo-zip",required=True,type=Path)
    p.add_argument("--output",required=True,type=Path)
    a=p.parse_args()
    r=compare(a.database,a.capag,a.rreo_zip,a.output)
    print("CAPAG",r["capag"]["compared"],"RREO",r["rreo"]["compared"],"zero divergencias")
