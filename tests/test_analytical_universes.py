from pathlib import Path
import csv
import sqlite3

from pipeline.ingest.import_universe_catalog import (
    import_universe_catalog,
    read_universe_catalog,
)

ROOT = Path(__file__).resolve().parents[1]


def make_db():
    con = sqlite3.connect(":memory:")
    con.execute("PRAGMA foreign_keys = ON")
    for path in sorted((ROOT / "data" / "schema").glob("[0-9][0-9][0-9]_*.sql")):
        con.executescript(path.read_text(encoding="utf-8"))
    return con


def test_cidades_medias_catalog_contract():
    path = ROOT / "data" / "catalogs" / "analytical_universes_sp.yml"
    catalog = read_universe_catalog(path)
    item = catalog["universes"][0]
    assert item["id"] == "CIDADES_MEDIAS"
    assert item["municipality_count"] == 33
    codes = {row["codigo_ibge"] for row in item["members"]}
    assert len(codes) == 33
    assert "3501608" in codes
    assert "3554102" in codes


def test_cidades_medias_overlap_contract():
    path = ROOT / "data" / "catalogs" / "cidades_medias_overlap_2026_10_09.csv"
    with path.open(encoding="utf-8", newline="") as handle:
        rows = {row["universo_relacionado"]: row for row in csv.DictReader(handle)}

    assert rows["TIC_TIM_30"]["municipios_cidades_medias_no_recorte"] == "5"
    assert rows["RM_SAO_PAULO"]["municipios_cidades_medias_no_recorte"] == "11"
    assert rows["RM_CAMPINAS"]["municipios_cidades_medias_no_recorte"] == "4"
    assert rows["FORA_RECORTE_METROPOLITANO_CATALOGADO"]["municipios_cidades_medias_no_recorte"] == "6"


def test_import_cidades_medias_into_canonical_schema():
    path = ROOT / "data" / "catalogs" / "analytical_universes_sp.yml"
    catalog = read_universe_catalog(path)
    item = catalog["universes"][0]

    con = make_db()
    try:
        for member in item["members"]:
            con.execute(
                "INSERT INTO municipio(codigo_ibge,nome,uf) VALUES (?,?,'SP')",
                (member["codigo_ibge"], member["municipio"]),
            )
        stats = import_universe_catalog(con, path)
        assert stats == {"universes": 1, "memberships": 33, "municipalities": 33}
        assert con.execute(
            "SELECT count(*) FROM universo_municipio WHERE universo_id='CIDADES_MEDIAS'"
        ).fetchone()[0] == 33
    finally:
        con.close()
