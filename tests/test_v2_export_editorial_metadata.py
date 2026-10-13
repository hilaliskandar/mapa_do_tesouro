import json
import sqlite3
from pathlib import Path
from pipeline.build.export_state_api_v2 import export_state_api

ROOT=Path(__file__).resolve().parents[1]

def test_v2_catalog_merges_editorial_documentation(tmp_path):
    db=tmp_path/"fixture.sqlite"
    con=sqlite3.connect(db)
    for schema in sorted((ROOT/"data/schema").glob("[0-9][0-9][0-9]_*.sql")):
        con.executescript(schema.read_text(encoding="utf-8"))
    con.execute("INSERT INTO municipio(codigo_ibge,nome,uf) VALUES ('3500001','Teste','SP')")
    con.execute("INSERT INTO universo(universo_id,nome) VALUES ('SP_645','Teste')")
    con.execute("INSERT INTO universo_municipio(universo_id,codigo_ibge) VALUES ('SP_645','3500001')")
    con.execute("""INSERT INTO variavel(variavel_id,nome,grupo,tipo,unidade,definicao)
                   VALUES('x','Taxa','indicadores','indicador_derivado','percentual','Teste')""")
    con.execute("""INSERT INTO variavel_documentacao(variavel_id,titulo_publico,formula_publica,
                   como_ler,limitacoes,origem_documental,documentation_version)
                   VALUES('x','Taxa pública','A / B','Ler como razão','A e B devem ser comparáveis',
                   'catálogo','v7')""")
    con.commit()
    con.close()
    root=tmp_path/"api"
    export_state_api(db,root)
    variable=json.loads((root/"catalog/variables.json").read_text())["variables"][0]
    assert variable["formula"]=="A / B"
    assert variable["como_ler"]=="Ler como razão"
    assert variable["cautelas"]=="A e B devem ser comparáveis"
    assert variable["documentacao_editorial"]["documentation_version"]=="v7"
    assert variable["display_multiplier"] is None
