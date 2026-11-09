"""FED01 isolated contract tests: draft SQL is never auto-migrated."""
from pathlib import Path
import sqlite3
import pytest

ROOT=Path(__file__).resolve().parents[1]
PROPOSAL=ROOT/"governance"/"proposals"/"PROPOSTA_STN_EVENTOS_DECENDIAIS_SP645.sql"

def con():
    db=sqlite3.connect(":memory:")
    db.execute("PRAGMA foreign_keys=ON")
    db.executescript("CREATE TABLE municipio(codigo_ibge TEXT PRIMARY KEY,nome TEXT NOT NULL,uf TEXT NOT NULL);"
                     "INSERT INTO municipio VALUES('3500105','Adamantina','SP');")
    db.executescript(PROPOSAL.read_text(encoding="utf-8"))
    db.execute("""INSERT INTO stn_transferencia_lote(
      lote_id,fonte_sistema,resource_id,competencia_ano,competencia_mes,
      source_sha256,r2_object_key,criado_em_utc)
      VALUES ('lote01','STN_CKAN','resource01',2026,9,?,
      'sp_645/federal/stn/2026_09/source/source.csv','2026-11-09T00:00:00Z')""",("a"*64,))
    return db

def insert_item(db,codigo_ibge="3500105",item="FPM",status="em_revisao",
                categoria=None,regra=None):
    db.execute("""INSERT INTO stn_transferencia_item_decendial(
      lote_id,codigo_ibge,municipio_nome_origem,transferencia_origem,item_origem,
      decendio_1_raw,decendio_2_raw,decendio_3_raw,status_semantico,natureza_operacao,
      regra_classificacao_id) VALUES('lote01',?,'Adamantina','FPM',?,
      '1067115.52','0','25.50',?,?,?)""",(codigo_ibge,item,status,categoria,regra))

def test_draft_event_schema_isolated_and_references_existing_municipio():
    assert PROPOSAL.exists()
    assert PROPOSAL.parent.name=="proposals" and "data/schema" not in str(PROPOSAL)
    with con() as db:
        insert_item(db)
        assert db.execute("SELECT decendio_1_raw FROM stn_transferencia_item_decendial").fetchone()[0]=="1067115.52"
        with pytest.raises(sqlite3.IntegrityError):
            insert_item(db,item="FPM")
        with pytest.raises(sqlite3.IntegrityError):
            insert_item(db,codigo_ibge="9999999",item="ITR")
        assert "observacao" not in {r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}

def test_promotion_requires_specific_classification_rule():
    with con() as db:
        with pytest.raises(sqlite3.IntegrityError):
            insert_item(db,item="DEDU",status="documentado")
        insert_item(db,item="DEDU",status="documentado",categoria="deducao",regra="stn-01")
        assert db.execute("SELECT COUNT(*) FROM stn_transferencia_item_decendial").fetchone()[0]==1
