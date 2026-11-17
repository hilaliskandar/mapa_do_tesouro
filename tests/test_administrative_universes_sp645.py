"""Verify 59 new administrative universes and the SP645 selector contract."""
from __future__ import annotations
import csv
import sqlite3
from collections import Counter, defaultdict
from pathlib import Path

import yaml

from pipeline.ingest.import_universe_catalog import (
    import_universe_catalog, read_universe_catalog
)

ROOT = Path(__file__).resolve().parents[1]
DIM = ROOT / "governance/DIM_SP645_IBGE_RA_RG_RM_AU_CONSOLIDADA_2026_11_14.csv"
CATALOG = ROOT / "data/catalogs/administrative_universes_sp_2026.yml"
EXISTING = ROOT / "data/catalogs/territorial_universes_sp_2025.yml"


def load_dimension():
    with DIM.open(encoding="utf-8", newline="") as source:
        return list(csv.DictReader(source, delimiter=";"))


def test_territorial_catalog_count_uniqueness_and_provenance():
    data = read_universe_catalog(CATALOG)
    regional = data["universes"]
    assert len(regional) == 59
    assert sum(x["type"] == "REGIAO_ADMINISTRATIVA" for x in regional) == 16
    assert sum(x["type"] == "REGIAO_GOVERNO" for x in regional) == 43
    assert sum(x["municipality_count"] for x in regional) == 1290
    assert all(x["id"].startswith(("RA_SEADE_", "RG_SEADE_")) for x in regional)
    assert len({x["id"] for x in regional}) == 59
    assert data["source"]["municipality_table"].endswith("DIM_SP645_IBGE_RA_RG_RM_AU_CONSOLIDADA_2026_11_14.csv")


def test_each_municipality_has_exactly_one_ra_one_rg_and_rg_parent():
    records = load_dimension()
    assert len(records) == 645
    assert len({r["codigo_ibge"] for r in records}) == 645
    catalog = read_universe_catalog(CATALOG)
    membership = {u["id"]: set(u["members"]) for u in catalog["universes"]}
    ra = Counter()
    rg = Counter()
    parent = defaultdict(set)
    for row in records:
        ib = row["codigo_ibge"]
        ra_id = "RA_SEADE_" + row["ra_codigo"].zfill(2)
        rg_id = "RG_SEADE_" + row["rg_codigo"].zfill(2)
        assert ib in membership[ra_id]
        assert ib in membership[rg_id]
        ra[ib] += 1
        rg[ib] += 1
        parent[rg_id].add(ra_id)
    assert all(n == 1 for n in ra.values())
    assert all(n == 1 for n in rg.values())
    assert len(parent) == 43
    assert all(len(x) == 1 for x in parent.values())
    for u in catalog["universes"]:
        codes = {
            r["codigo_ibge"] for r in records
            if (r["ra_codigo"] if u["type"] == "REGIAO_ADMINISTRATIVA" else r["rg_codigo"]).zfill(2) == u["id"].split("_")[-1]
        }
        assert set(u["members"]) == codes


def test_catalogs_coexist_without_double_counting():
    records = load_dimension()
    old = read_universe_catalog(EXISTING)["universes"]
    administrative = read_universe_catalog(CATALOG)["universes"]
    assert len(old) == 10
    assert sum(u["municipality_count"] for u in old) == 255
    assert sum(u["municipality_count"] for u in administrative) == 1290
    for u in old:
        members = {r["codigo_ibge"] for r in records if r["rm_au_codigo"] == u["source_category_code"]}
        assert members == set(u["members"])
    assert len({r["codigo_ibge"] for r in records if r["rm_au_codigo"]}) == 255


def test_catalog_import_respects_sqlite_canonical_and_repeatability(tmp_path):
    rows = load_dimension()
    db = sqlite3.connect(":memory:")
    db.execute("PRAGMA foreign_keys = ON")
    try:
        for sql in sorted((ROOT / "data/schema").glob("[0-9][0-9][0-9]_*.sql")):
            db.executescript(sql.read_text(encoding="utf-8"))
        db.executemany(
            "INSERT INTO municipio(codigo_ibge,nome,uf) VALUES(?,?,'SP')",
            [(r["codigo_ibge"],r["municipio"]) for r in rows],
        )
        db.execute("INSERT INTO universo(universo_id,nome) VALUES('SP_645','Estado de São Paulo')")
        db.executemany(
            "INSERT INTO universo_municipio(universo_id,codigo_ibge) VALUES('SP_645',?)",
            [(r["codigo_ibge"],) for r in rows],
        )
        expected = {"universes": 59, "memberships": 1290, "municipalities": 645}
        assert import_universe_catalog(db, CATALOG) == expected
        assert import_universe_catalog(db, CATALOG) == expected
        assert db.execute(
            "SELECT COUNT(*) FROM universo WHERE ativo=1"
        ).fetchone()[0] == 60
        assert db.execute(
            "SELECT COUNT(*) FROM universo_municipio WHERE universo_id LIKE 'R%_SEADE_%'"
        ).fetchone()[0] == 1290
        assert db.execute(
            "SELECT COUNT(*) FROM universo_municipio WHERE universo_id='SP_645'"
        ).fetchone()[0] == 645
        assert db.execute("PRAGMA foreign_key_check").fetchall() == []
    finally:
        db.close()


def test_pipeline_wires_new_catalog_and_grouped_selector():
    build = (ROOT/"pipeline/build/build_sp645_private_site.py").read_text()
    js = (ROOT/"app/static/app.js").read_text()
    qa = (ROOT/"deployment/qa_sp645_pages.py").read_text()
    assert '"administrative_universes_sp_2026.yml"' in build
    assert '["regiao_administrativa", "Regiões Administrativas — Seade"]' in js
    assert '["regiao_governo", "Regiões de Governo — Seade"]' in js
    assert "EXPECTED_UNIVERSES.update(expected_administrative_universes())" in qa
