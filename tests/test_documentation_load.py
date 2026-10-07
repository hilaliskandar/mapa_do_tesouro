from pathlib import Path
import sqlite3

from pipeline.build.init_db import initialize_database
from pipeline.build.load_catalog import load_catalog
from pipeline.build.load_documentation import load_documentation

ROOT = Path(__file__).resolve().parents[1]


def test_v7_documentation_loads_strictly_into_full_catalog(tmp_path):
    database = tmp_path / "catalog.sqlite"
    initialize_database(database)
    load_catalog(database)
    result = load_documentation(database, strict=True)

    assert result["loaded_variable_documentation"] == 75
    assert result["skipped_variables"] == []

    con = sqlite3.connect(database)
    try:
        assert con.execute("SELECT count(*) FROM variavel").fetchone()[0] == 75
        assert con.execute(
            "SELECT count(*) FROM variavel_documentacao"
        ).fetchone()[0] == 75
        assert con.execute(
            "SELECT count(*) FROM documentacao_secao"
        ).fetchone()[0] == 9
        assert con.execute(
            """
            SELECT formula_publica, como_ler, regra_ausencia
            FROM variavel_documentacao
            WHERE variavel_id='investimento_pct_receita_corrente'
            """
        ).fetchone() == (
            "Investimentos liquidados ÷ Receita Corrente bruta",
            "Mede o esforço relativo de investimento no exercício. Deve ser lido em série, pois investimentos são cíclicos e podem concentrar-se em projetos específicos.",
            "Se qualquer componente necessário estiver ausente ou não comparável, o indicador permanece NA; ausência nunca é convertida em zero.",
        )
    finally:
        con.close()
