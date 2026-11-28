"""QA do crosswalk com o schema municipal do SQLite, sem rede."""

import sqlite3

import pytest

from pipeline.normalize.federal_canonical_universe import (
    load_universe_codes,
    match_with_canonical_sqlite,
)


def create_db(path, *, n=3, invalid=False, active=1):
    with sqlite3.connect(path) as conn:
        conn.executescript(
            """CREATE TABLE municipio (
                 codigo_ibge TEXT PRIMARY KEY, nome TEXT, uf TEXT, ativo INTEGER);
               CREATE TABLE universo_municipio (
                 universo_id TEXT, codigo_ibge TEXT,
                 PRIMARY KEY(universo_id, codigo_ibge));"""
        )
        for i in range(n):
            code = f"35{i:05d}"
            uf = "RJ" if invalid and i == n - 1 else "SP"
            conn.execute(
                "INSERT INTO municipio VALUES (?,?,?,?)",
                (code, f"Mun {i}", uf, active),
            )
            conn.execute(
                "INSERT INTO universo_municipio VALUES (?,?)", ("SP_645", code)
            )


def test_leitura_readonly_e_validacao_do_universo(tmp_path):
    db = tmp_path / "canonical.sqlite"
    create_db(db)
    before = db.read_bytes()
    codes = load_universe_codes(db, expected_count=3)
    assert codes == {"3500000", "3500001", "3500002"}
    assert db.read_bytes() == before


def test_universo_incompleto_rejeitado(tmp_path):
    db = tmp_path / "canonical.sqlite"
    create_db(db)
    with pytest.raises(ValueError, match="incompleto"):
        load_universe_codes(db)


def test_uf_inconsistente_rejeitada(tmp_path):
    db = tmp_path / "canonical.sqlite"
    create_db(db, invalid=True)
    with pytest.raises(ValueError, match="inválido"):
        load_universe_codes(db, expected_count=3)


def test_inativo_rejeitado(tmp_path):
    db = tmp_path / "canonical.sqlite"
    create_db(db, active=0)
    with pytest.raises(ValueError, match="inválido"):
        load_universe_codes(db, expected_count=3)


def test_crosswalk_utiliza_validador_sem_alterar_sqlite(tmp_path, monkeypatch):
    db = tmp_path / "canonical.sqlite"
    create_db(db)
    import pipeline.normalize.federal_canonical_universe as module
    original = module.load_universe_codes
    monkeypatch.setattr(module, "load_universe_codes",
                        lambda database, universe_id="SP_645": original(
                            database, universe_id=universe_id, expected_count=3
                        ))
    result = match_with_canonical_sqlite(
        {"id_proposta": 123, "cd_ibge_recebedor": "3500001"},
        database=db,
    )
    assert result.status == "confirmado_recebedor"
    assert result.role == "ente_recebedor_proposta"
