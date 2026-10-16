"""Integra registros monetarios historicos RGF aprovados no Gate E ao SQLite privado."""
import csv,hashlib,json,sqlite3
from pathlib import Path
FIELDS={
"rgf_despesa_total_pessoal":"SICONFI_RGF_A01",
"rgf02_divida_consolidada":"SICONFI_RGF_A02",
"rgf02_divida_consolidada_liquida":"SICONFI_RGF_A02",
}
PIN="7faef8188fd56bff6bb8031dfe3a8eeec11fe56e67f986bdc0007a4ee7646eeb"
def integrate(database:Path,reference:Path,report:Path):
    sha=hashlib.sha256(reference.read_bytes()).hexdigest()
    if sha!=PIN:raise ValueError("Referencia RGF nao corresponde ao SHA Gate E")
    con=sqlite3.connect(database)
    changed=0;unchanged=0;empty=0;reclassified_absent=0;rows=0
    try:
        con.execute("PRAGMA foreign_keys=ON")
        with reference.open(encoding="utf-8",newline="") as h:
            for rec in csv.DictReader(h):
                year=int(rec["ano"]);code=str(rec["cod_ibge"])
                if year not in (2023,2024):raise ValueError("Exercicio fora do Gate E")
                rows+=1
                for key,source in FIELDS.items():
                    raw=rec[key]
                    previous=con.execute("SELECT status,valor_num FROM observacao WHERE codigo_ibge=? AND ano=? AND variavel_id=?",(code,year,key)).fetchone()
                    if previous is None:raise ValueError(f"Chave sem observacao no canonico: {code}/{year}/{key}")
                    if raw in ("",None):
                        empty+=1
                        if previous[0]=="nao_aplicavel":
                            con.execute("UPDATE observacao SET status='ausente',valor_num=NULL,valor_texto=NULL,fonte_id=?,referencia_origem=? WHERE codigo_ibge=? AND ano=? AND variavel_id=? AND status='nao_aplicavel'",(source,"Gate E RGF historico 2023-2024: referencia sem valor; SHA256:"+sha,code,year,key))
                            reclassified_absent+=1
                        elif previous[0]!="ausente":
                            raise ValueError(f"Referencia vazia incompatível com status: {code}/{year}/{key}: {previous[0]}")
                        continue
                    numeric=float(raw)
                    if previous[0]=="observado":
                        if previous[1] is None or abs(previous[1]-numeric)>.01:raise ValueError(f"Conflito com observacao existente: {code}/{year}/{key}")
                        unchanged+=1
                        continue
                    if previous[0]!="nao_aplicavel":raise ValueError(f"Status inesperado: {code}/{year}/{key}: {previous[0]}")
                    con.execute("UPDATE observacao SET status='observado',valor_num=?,valor_texto=NULL,fonte_id=?,referencia_origem=? WHERE codigo_ibge=? AND ano=? AND variavel_id=? AND status='nao_aplicavel'",(numeric,source,"Gate E RGF histórico 2023-2024; SHA256:"+sha,code,year,key))
                    changed+=1
        if rows!=1290:raise ValueError(f"Esperadas 1290 linhas RGF, obtidas {rows}")
        if changed==0:raise ValueError("Nenhuma observacao historica integrada")
        con.commit()
    except BaseException:
        con.rollback()
        raise
    finally:con.close()
    outcome={"sha256":sha,"reference_rows":rows,"changed":changed,"already_observed_consistent":unchanged,"empty_reference":empty,"reclassified_absent":reclassified_absent,"scope":list(FIELDS),"years":[2023,2024]}
    report.parent.mkdir(parents=True,exist_ok=True)
    report.write_text(json.dumps(outcome,indent=2,ensure_ascii=False),encoding="utf-8")
    return outcome
if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser();p.add_argument("--database",type=Path,required=True);p.add_argument("--reference",type=Path,required=True);p.add_argument("--report",type=Path,required=True)
    a=p.parse_args();print(integrate(a.database,a.reference,a.report))
