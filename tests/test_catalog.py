from pathlib import Path
import sqlite3
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from pipeline.build.init_db import initialize_database
from pipeline.build.load_catalog import load_catalog


def test_core_catalog_loads(tmp_path):
    database = tmp_path / "test.sqlite"
    initialize_database(database)
    load_catalog(database)

    con = sqlite3.connect(database)
    try:
        fontes = con.execute("SELECT count(*) FROM fonte").fetchone()[0]
        variaveis = con.execute("SELECT count(*) FROM variavel").fetchone()[0]
        assert fontes >= 7
        assert variaveis >= 20
        assert con.execute(
            "SELECT tipo FROM variavel WHERE variavel_id='capag'"
        ).fetchone()[0] == "classificacao_oficial"
        assert con.execute(
            "SELECT tipo FROM variavel WHERE variavel_id='dtp_pct_rcl'"
        ).fetchone()[0] == "indicador_legal"
    finally:
        con.close()
