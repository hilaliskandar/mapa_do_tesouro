import json
import sqlite3

from pipeline.build.export_static_data import export_static_data
from pipeline.build.init_db import initialize_database
from pipeline.build.load_catalog import load_catalog
from pipeline.build.load_documentation import load_documentation
from pipeline.transform.refresh_coverage import refresh_coverage


def _base_db(path):
    initialize_database(path)
    load_catalog(path)
    load_documentation(path, strict=True)
    con = sqlite3.connect(path)
    con.execute(
        "INSERT INTO universo(universo_id,nome) VALUES ('SP_TESTE','Teste')"
    )
    for code, name in [("3500001", "Alfa"), ("3500002", "Beta")]:
        con.execute(
            "INSERT INTO municipio(codigo_ibge,nome,uf) VALUES (?,?,?)",
            (code, name, "SP"),
        )
        con.execute(
            """
            INSERT INTO universo_municipio(universo_id,codigo_ibge)
            VALUES ('SP_TESTE',?)
            """,
            (code,),
        )
    con.commit()
    con.close()


def test_refresh_coverage_uses_final_observations_and_counts_missing_rows_as_absent(tmp_path):
    db = tmp_path / "coverage.sqlite"
    _base_db(db)

    con = sqlite3.connect(db)
    try:
        con.execute(
            """
            INSERT INTO observacao(
                codigo_ibge,ano,variavel_id,fonte_id,valor_num,status
            ) VALUES (
                '3500001',2025,'dca_receita_corrente_bruta',
                'SICONFI_DCA',100,'observado'
            )
            """
        )
        con.execute(
            """
            INSERT INTO observacao(
                codigo_ibge,ano,variavel_id,status
            ) VALUES (
                '3500001',2025,'investimento_pct_receita_corrente','em_revisao'
            )
            """
        )
        con.commit()
    finally:
        con.close()

    result = refresh_coverage(db, "SP_TESTE")
    assert result["expected_municipalities"] == 2
    assert result["implicit_missing_rows_classified_as_absent"] == 2

    con = sqlite3.connect(db)
    try:
        raw = con.execute(
            """
            SELECT observado,ausente,nao_aplicavel,em_revisao
            FROM cobertura
            WHERE variavel_id='dca_receita_corrente_bruta' AND ano=2025
            """
        ).fetchone()
        assert raw == (1, 1, 0, 0)

        derived = con.execute(
            """
            SELECT observado,ausente,nao_aplicavel,em_revisao
            FROM cobertura
            WHERE variavel_id='investimento_pct_receita_corrente' AND ano=2025
            """
        ).fetchone()
        assert derived == (0, 1, 0, 1)
    finally:
        con.close()


def test_static_export_separates_total_coverage_from_source_contribution(tmp_path):
    db = tmp_path / "sources.sqlite"
    out = tmp_path / "site" / "data"
    _base_db(db)

    con = sqlite3.connect(db)
    try:
        con.execute(
            """
            INSERT INTO observacao(
                codigo_ibge,ano,variavel_id,fonte_id,valor_num,status
            ) VALUES (
                '3500001',2025,'dca_receita_corrente_bruta',
                'SICONFI_DCA',100,'observado'
            )
            """
        )
        con.execute(
            """
            INSERT INTO observacao(
                codigo_ibge,ano,variavel_id,valor_num,status
            ) VALUES (
                '3500001',2025,'investimento_pct_receita_corrente',
                0.1,'observado'
            )
            """
        )
        con.commit()
    finally:
        con.close()

    refresh_coverage(db, "SP_TESTE")
    export_static_data(db, out, universe_id="SP_TESTE")

    source_rows = json.loads(
        (out / "coverage_sources.json").read_text(encoding="utf-8")
    )
    by_variable = {row["variavel_id"]: row for row in source_rows}

    assert by_variable["dca_receita_corrente_bruta"]["fonte_id"] == "SICONFI_DCA"
    assert by_variable["dca_receita_corrente_bruta"]["observado"] == 1
    assert by_variable["dca_receita_corrente_bruta"]["universo_esperado"] == 2

    assert (
        by_variable["investimento_pct_receita_corrente"]["fonte_id"]
        == "DERIVADO_PIPELINE"
    )
    assert (out / "coverage.json").exists()
