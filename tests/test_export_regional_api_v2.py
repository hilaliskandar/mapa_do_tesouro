from pathlib import Path
import sqlite3
import json
from pipeline.build.export_regional_api_v2 import export_regional_api

ROOT = Path(__file__).resolve().parents[1]

def test_regional_api_coverage(tmp_path):
    db = tmp_path / "test.db"
    con = sqlite3.connect(db)
    for p in sorted((ROOT / "data/schema").glob("[0-9][0-9][0-9]_*.sql")):
        con.executescript(p.read_text(encoding="utf-8"))
    con.execute("INSERT INTO universo(universo_id,nome) VALUES('U','Teste')")
    for code in ("3500001","3500002","3500003"):
        con.execute("INSERT INTO municipio(codigo_ibge,nome,uf) VALUES(?,?,'SP')",(code,code))
        con.execute("INSERT INTO universo_municipio(universo_id,codigo_ibge) VALUES('U',?)",(code,))
    con.execute("INSERT INTO variavel(variavel_id,nome,grupo,tipo,unidade,definicao) VALUES('v','Teste','receitas','conta_oficial','BRL','Teste')")
    con.execute("INSERT INTO observacao(codigo_ibge,ano,variavel_id,status,valor_num) VALUES('3500001',2025,'v','observado',0)")
    con.execute("INSERT INTO observacao(codigo_ibge,ano,variavel_id,status) VALUES('3500002',2025,'v','ausente')")
    con.commit()
    con.close()
    out = tmp_path / "api"
    export_regional_api(db,out)
    rows = json.loads((out / "universes/U/coverage.json").read_text())["coverage"]
    x = rows[0]
    assert x["status_counts"]["observado"] == 1
    assert x["status_counts"]["ausente"] == 1
    assert x["status_counts"]["sem_registro"] == 1
    assert x["observed_numeric"]["sum"] == 0
