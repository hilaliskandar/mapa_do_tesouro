from pathlib import Path
import sqlite3

from pipeline.qa.audit_api_readiness_v2 import audit_readiness


def test_editorial_documentation_fills_only_supported_fields(tmp_path):
    root = Path(__file__).resolve().parents[1]
    db = tmp_path / "audit.sqlite"
    con = sqlite3.connect(db)
    for schema in sorted((root / "data/schema").glob("[0-9][0-9][0-9]_*.sql")):
        con.executescript(schema.read_text(encoding="utf-8"))
    con.execute("INSERT INTO municipio(codigo_ibge,nome,uf) VALUES('3500001','Teste','SP')")
    con.execute("INSERT INTO universo(universo_id,nome) VALUES('SP_645','Estado')")
    con.execute("INSERT INTO universo_municipio(universo_id,codigo_ibge) VALUES('SP_645','3500001')")
    con.execute("""INSERT INTO variavel(variavel_id,nome,grupo,tipo,unidade,definicao)
                   VALUES('a','Indicador','indicadores','indicador_derivado','percentual','Definicao')""")
    con.execute("""INSERT INTO variavel_documentacao(variavel_id,titulo_publico,
                   formula_publica,como_ler,limitacoes,documentation_version)
                   VALUES('a','Indicador','a / b','Leitura verificada',
                          'Somente comparavel sob mesma fonte','teste')""")
    con.execute("""INSERT INTO observacao(codigo_ibge,ano,variavel_id,status,valor_num)
                   VALUES('3500001',2025,'a','observado',0)""")
    con.commit()
    con.close()
    report = audit_readiness(db,tmp_path / "report.json")
    item = report["variables"][0]
    assert "formula" not in item["missing_methodology_fields"]
    assert "como_ler" not in item["missing_methodology_fields"]
    assert "cautelas" not in item["missing_methodology_fields"]
    assert item["editorial_documentation_version"] == "teste"
    assert item["scale_verified"] is False
