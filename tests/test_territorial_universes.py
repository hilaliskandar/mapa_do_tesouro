from pathlib import Path
import csv
import sqlite3

from pipeline.ingest.import_territorial_universes import (
    import_territorial_universes,
    read_territorial_catalog,
)

ROOT = Path(__file__).resolve().parents[1]


def make_db():
    con = sqlite3.connect(":memory:")
    con.execute("PRAGMA foreign_keys = ON")
    for path in sorted((ROOT / "data" / "schema").glob("[0-9][0-9][0-9]_*.sql")):
        con.executescript(path.read_text(encoding="utf-8"))
    return con


def test_territorial_catalog_contract():
    catalog = read_territorial_catalog(
        ROOT / "data" / "catalogs" / "territorial_universes_sp_2025.yml"
    )
    universes = catalog["universes"]
    assert len(universes) == 10
    assert sum(len(item["members"]) for item in universes) == 255
    assert len({code for item in universes for code in item["members"]}) == 255


def test_tictim30_decomposition_is_exact():
    catalog = read_territorial_catalog(
        ROOT / "data" / "catalogs" / "territorial_universes_sp_2025.yml"
    )
    by_id = {item["id"]: set(item["members"]) for item in catalog["universes"]}
    with (
        ROOT / "data" / "catalogs" / "tictim30_territorial_decomposition_2025.csv"
    ).open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    tic = {row["codigo_ibge"] for row in rows}
    assert len(tic) == 30
    assert tic == (
        by_id["RM_CAMPINAS"]
        | by_id["RM_JUNDIAI"]
        | {"3509007", "3516309", "3516408"}
    )
    assert by_id["RM_CAMPINAS"].issubset(tic)
    assert by_id["RM_JUNDIAI"].issubset(tic)


def test_import_territorial_universes_into_canonical_schema():
    catalog_path = ROOT / "data" / "catalogs" / "territorial_universes_sp_2025.yml"
    catalog = read_territorial_catalog(catalog_path)
    all_members = sorted({code for item in catalog["universes"] for code in item["members"]})

    con = make_db()
    try:
        for code in all_members:
            con.execute(
                "INSERT INTO municipio(codigo_ibge,nome,uf) VALUES (?,?, 'SP')",
                (code, code),
            )
        stats = import_territorial_universes(con, catalog_path)
        assert stats == {"universes": 10, "memberships": 255, "municipalities": 255}
        assert con.execute(
            "SELECT count(*) FROM universo_municipio WHERE universo_id='RM_CAMPINAS'"
        ).fetchone()[0] == 20
        assert con.execute(
            "SELECT count(*) FROM universo_municipio WHERE universo_id='RM_JUNDIAI'"
        ).fetchone()[0] == 7
        assert con.execute(
            "SELECT count(*) FROM universo_municipio WHERE universo_id='RM_SAO_PAULO'"
        ).fetchone()[0] == 39
    finally:
        con.close()
