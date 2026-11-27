"""Teste sintético dos controles da auditoria de componentes CAPAG."""
import sqlite3
from pathlib import Path
from unittest.mock import patch
import openpyxl
import pytest
from pipeline.qa.audit_capag_official_components import audit

def test_capag_components_accept_and_detect_tampering(tmp_path):
    source=tmp_path/"capag.xlsx"
    workbook=openpyxl.Workbook()
    sheet=workbook.active
    sheet.title="Prévia da CAPAG"
    sheet.append(["Código Município Completo","Nome_Município","UF","CAPAG","Indicador 1","Nota 1","Indicador 2","Nota 2","Indicador 3"])
    sheet.append(["cabecalho",None,None,None,None,None,None,None,None])
    sheet.append(["cabecalho",None,None,None,None,None,None,None,None])
    for i in range(645):
        sheet.append([str(3500000+i),"Municipio", "SP","C", None if i==0 else float(i)/1000,None,None if i<3 else float(i)/100,None,None if i<22 else float(i)/10])
    workbook.save(source)
    import hashlib
    sha=hashlib.sha256(source.read_bytes()).hexdigest()
    database=tmp_path/"base.sqlite"
    with sqlite3.connect(database) as db:
        db.execute("CREATE TABLE observacao (codigo_ibge TEXT, ano INTEGER, variavel_id TEXT, status TEXT, valor_num REAL)")
        for i in range(645):
            for col,threshold,divisor in [("indicador_1",1,1000),("indicador_2",3,100),("indicador_3",22,10)]:
                is_missing=i<threshold
                db.execute("INSERT INTO observacao VALUES(?,?,?,?,?)",(str(3500000+i),2025,col,"ausente" if is_missing else "observado",None if is_missing else float(i)/divisor))
    with patch("pipeline.qa.audit_capag_official_components.SHA",sha):
        result=audit(source,database,tmp_path/"qa.json")
        assert result["mismatch_count"]==0 and result["comparisons"]==1935
        with sqlite3.connect(database) as db:
            db.execute("UPDATE observacao SET valor_num=999 WHERE codigo_ibge='3500001' AND variavel_id='indicador_1'")
        with pytest.raises(ValueError,match="Cotejo CAPAG"):
            audit(source,database,tmp_path/"qa_bad.json")
