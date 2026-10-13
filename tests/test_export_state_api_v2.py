import json
import sqlite3
from pathlib import Path

from pipeline.build.export_state_api_v2 import export_state_api

ROOT = Path(__file__).resolve().parents[1]


def test_state_api_fiches_and_unpublished_variable(tmp_path):
    db = tmp_path / "fixture.sqlite"
    con = sqlite3.connect(db)
    for schema in sorted((ROOT / "data" / "schema").glob("[0-9][0-9][0-9]_*.sql")):
        con.executescript(schema.read_text(encoding="utf-8"))
    con.execute("INSERT INTO universo(universo_id,nome) VALUES('SP_645','Teste')")
    for code in ("3500001", "3500002"):
        con.execute("INSERT INTO municipio(codigo_ibge,nome,uf) VALUES(?,?,'SP')", (code, code))
        con.execute("INSERT INTO universo_municipio(universo_id,codigo_ibge) VALUES('SP_645',?)", (code,))
    con.execute("""INSERT INTO variavel(variavel_id,nome,grupo,tipo,unidade,definicao)
                   VALUES('a','Conta','receitas','conta_oficial','BRL','teste')""")
    con.execute("""INSERT INTO variavel(variavel_id,nome,grupo,tipo,unidade,definicao,publicavel)
                   VALUES('b','Restrita','receitas','conta_oficial','BRL','teste',0)""")
    con.execute("""INSERT INTO observacao(codigo_ibge,ano,variavel_id,valor_num,status)
                   VALUES('3500001',2025,'a',0,'observado')""")
    con.execute("""INSERT INTO observacao(codigo_ibge,ano,variavel_id,status)
                   VALUES('3500001',2025,'b','ausente')""")
    con.commit()
    con.close()

    output = tmp_path / "api" / "v2"
    result = export_state_api(db, output)
    assert result["municipalities"] == 2
    assert result["variables"] == 2
    assert result["observations"] == 1
    a = json.loads((output / "municipalities" / "3500001.json").read_text())
    b = json.loads((output / "municipalities" / "3500002.json").read_text())
    assert a["variables"]["a"][0]["value"] == 0
    assert "b" not in a["variables"]
    assert b["variables"] == {}
    assert b["missing_record_policy"].startswith("sem_registro")
    catalog = json.loads((output / "catalog" / "variables.json").read_text())
    flags = {x["variavel_id"]: x["api_available"] for x in catalog["variables"]}
    assert flags == {"a": True, "b": False}
    manifest = json.loads((output / "manifest.json").read_text())
    assert manifest["publication_qa"] == "not_evaluated"
