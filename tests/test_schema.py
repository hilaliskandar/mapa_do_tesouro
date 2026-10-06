from pathlib import Path
import sqlite3

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "data" / "schema" / "001_initial.sql"


def make_db():
    con = sqlite3.connect(":memory:")
    con.execute("PRAGMA foreign_keys = ON")
    for path in sorted((ROOT / "data" / "schema").glob("[0-9][0-9][0-9]_*.sql")):\n        con.executescript(path.read_text(encoding="utf-8"))
    return con


def test_schema_initializes():
    con = make_db()
    tables = {
        row[0]
        for row in con.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )
    }
    expected = {
        "schema_metadata",
        "municipio",
        "universo",
        "universo_municipio",
        "fonte",
        "variavel",
        "crosswalk_variavel",
        "observacao",
        "cobertura",
        "build",
        "build_source",
        "janela_analitica",
        "metrica_janela",
        "estatistica_janela",
        "dimensao_tipologia",
        "classificacao_relativa",
        "marcador_comparavel",
        "par_municipal",
    }
    assert expected.issubset(tables)


def test_absence_is_not_zero():
    con = make_db()
    con.execute(
        "INSERT INTO municipio(codigo_ibge,nome,uf) VALUES ('3500000','Teste','SP')"
    )
    con.execute(
        """
        INSERT INTO variavel(
            variavel_id,nome,grupo,tipo,unidade,definicao
        ) VALUES ('x','X','teste','contextual','u','Teste')
        """
    )
    con.execute(
        """
        INSERT INTO observacao(
            codigo_ibge,ano,variavel_id,status
        ) VALUES ('3500000',2025,'x','ausente')
        """
    )
    row = con.execute(
        "SELECT valor_num, valor_texto, status FROM observacao"
    ).fetchone()
    assert row == (None, None, "ausente")


def test_observed_value_must_have_exactly_one_payload():
    con = make_db()
    con.execute(
        "INSERT INTO municipio(codigo_ibge,nome,uf) VALUES ('3500000','Teste','SP')"
    )
    con.execute(
        """
        INSERT INTO variavel(
            variavel_id,nome,grupo,tipo,unidade,definicao
        ) VALUES ('x','X','teste','contextual','u','Teste')
        """
    )
    try:
        con.execute(
            """
            INSERT INTO observacao(
                codigo_ibge,ano,variavel_id,status
            ) VALUES ('3500000',2025,'x','observado')
            """
        )
    except sqlite3.IntegrityError:
        pass
    else:
        raise AssertionError("Observacao sem valor foi aceita como observada.")


def test_universe_membership_uses_ibge_key():
    con = make_db()
    con.execute(
        "INSERT INTO municipio(codigo_ibge,nome,uf) VALUES ('3500000','Teste','SP')"
    )
    con.execute(
        "INSERT INTO universo(universo_id,nome) VALUES ('TIC_TIM_30','TIC-TIM 30')"
    )
    con.execute(
        """
        INSERT INTO universo_municipio(universo_id,codigo_ibge)
        VALUES ('TIC_TIM_30','3500000')
        """
    )
    assert con.execute(
        "SELECT count(*) FROM universo_municipio"
    ).fetchone()[0] == 1
