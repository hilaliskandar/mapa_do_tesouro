import sqlite3

from pipeline.qa.audit_api_readiness_v2 import audit_readiness


def test_readiness_reports_missing_metadata_and_implicit_gap(tmp_path):
    db = tmp_path / "test.sqlite"
    con = sqlite3.connect(db)
    from pathlib import Path
    root = Path(__file__).resolve().parents[1]
    for file in sorted((root / "data" / "schema").glob("[0-9][0-9][0-9]_*.sql")):
        con.executescript(file.read_text(encoding="utf-8"))
    con.execute("INSERT INTO universo(universo_id,nome) VALUES('SP_645','Teste')")
    for code in ("3500001", "3500002"):
        con.execute("INSERT INTO municipio(codigo_ibge,nome,uf) VALUES(?,?,'SP')",(code,code))
        con.execute("INSERT INTO universo_municipio(universo_id,codigo_ibge) VALUES('SP_645',?)",(code,))
    con.execute("""INSERT INTO variavel(variavel_id,nome,grupo,tipo,unidade,definicao)
                   VALUES('pct','Percentual','indicadores','indicador_derivado','percentual','Definicao')""")
    con.execute("""INSERT INTO observacao(codigo_ibge,ano,variavel_id,valor_num,status)
                   VALUES('3500001',2025,'pct',0,'observado')""")
    con.commit()
    con.close()
    result = audit_readiness(db, tmp_path / "qa.json")
    assert result["municipality_count"] == 2
    assert result["summary"]["percentage_scale_audit_required"] == 1
    variable = result["variables"][0]
    assert "formula" in variable["missing_methodology_fields"]
    assert variable["years"][0]["states"]["sem_registro"] == 1
    assert variable["years"][0]["states"]["observado"] == 1
