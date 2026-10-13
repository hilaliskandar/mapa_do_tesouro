"""Integration smoke: the actual SP645 build helper exports v2 files."""
import json
import sqlite3
from pathlib import Path

from pipeline.build.build_sp645_private_site import export_v2_site_artifacts

ROOT = Path(__file__).resolve().parents[1]


def test_export_v2_site_artifacts_645(tmp_path):
    database = tmp_path / "db.sqlite"
    con = sqlite3.connect(database)
    try:
        for schema in sorted((ROOT / "data/schema").glob("[0-9][0-9][0-9]_*.sql")):
            con.executescript(schema.read_text(encoding="utf-8"))
        con.execute("INSERT INTO universo(universo_id,nome) VALUES('SP_645','Teste SP645')")
        con.execute("""INSERT INTO variavel
                    (variavel_id,nome,grupo,tipo,unidade,definicao)
                    VALUES ('v','Conta','receitas','conta_oficial','BRL','Conta de teste')""")
        for i in range(645):
            code = str(3500000 + i)
            con.execute("INSERT INTO municipio(codigo_ibge,nome,uf) VALUES(?,?,'SP')",
                        (code, f"Municipio {i}"))
            con.execute("INSERT INTO universo_municipio(universo_id,codigo_ibge) VALUES('SP_645',?)",
                        (code,))
            if i == 0:
                con.execute("""INSERT INTO observacao(codigo_ibge,ano,variavel_id,valor_num,status)
                               VALUES (?,2025,'v',0,'observado')""", (code,))
        con.commit()
    finally:
        con.close()
    site = tmp_path / "site"
    result = export_v2_site_artifacts(database, site)
    root = site / "data/api/v2"
    assert result["api_v2_state"]["municipalities"] == 645
    assert len(list((root / "municipalities").glob("*.json"))) == 645
    assert (root / "catalog/universes.json").is_file()
    assert (root / "universes/SP_645/coverage.json").is_file()
    assert (root / "qa/readiness.json").is_file()
    counts = json.loads((root / "universes/SP_645/coverage.json").read_text())["coverage"][0]["status_counts"]
    assert counts["observado"] == 1
    assert counts["sem_registro"] == 644
    manifest = json.loads((root / "manifest.json").read_text())
    assert manifest["publication_qa"] == "not_evaluated"
