"""End-to-end static API smoke for administrative regions within the SP645 build."""
from __future__ import annotations
import json
import sqlite3
from pathlib import Path
import csv

from pipeline.build.init_db import initialize_database
from pipeline.build.load_catalog import load_catalog
from pipeline.build.load_documentation import load_documentation
from pipeline.build.build_sp645_private_site import _load_additional_universes
from pipeline.build.build_static_site import build_static_site

ROOT = Path(__file__).resolve().parents[1]
DIM = ROOT / "governance/DIM_SP645_IBGE_RA_RG_RM_AU_CONSOLIDADA_2026_11_14.csv"


def test_real_catalogs_generate_ra_rg_selectable_data(tmp_path):
    db = tmp_path / "sp645.sqlite"
    initialize_database(db)
    load_catalog(db)
    load_documentation(db, strict=True)
    with DIM.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter=";"))
    assert len(rows) == 645
    with sqlite3.connect(db) as con:
        con.execute("PRAGMA foreign_keys=ON")
        con.executemany(
            "INSERT INTO municipio(codigo_ibge,nome,uf) VALUES (?,?, 'SP')",
            [(x["codigo_ibge"], x["municipio"]) for x in rows]
        )
        con.execute("INSERT INTO universo(universo_id,nome,tipo) VALUES ('SP_645','Estado de São Paulo','estadual')")
        con.executemany(
            "INSERT INTO universo_municipio(universo_id,codigo_ibge) VALUES ('SP_645',?)",
            [(x["codigo_ibge"],) for x in rows]
        )
        # Data is deliberately synthetic and exists only inside this temporary fixture.
        con.execute(
            """INSERT INTO observacao(codigo_ibge,ano,variavel_id,status,valor_num)
               VALUES (?,?,?,'observado',?)""",
            (rows[0]["codigo_ibge"],2025,"dca_investimentos_liquidada",1000.0)
        )
        con.commit()
    ids = _load_additional_universes(db)
    assert len(ids) == 72
    assert ids[0] == "SP_645"
    assert sum(x.startswith("RA_SEADE_") for x in ids) == 16
    assert sum(x.startswith("RG_SEADE_") for x in ids) == 43
    example = rows[0]
    ra_id = "RA_SEADE_" + example["ra_codigo"].zfill(2)
    rg_id = "RG_SEADE_" + example["rg_codigo"].zfill(2)
    output = tmp_path/"site"
    result = build_static_site(
        db,output,universe_id="SP_645",
        universe_ids=["SP_645",ra_id,rg_id],
    )
    assert result["universe_count"] == 3
    catalog=json.loads((output/"data/universes.json").read_text(encoding="utf-8"))
    assert len(catalog) == 3
    assert catalog[0]["default"] is True
    for uid in [ra_id,rg_id]:
        selected=next(x for x in catalog if x["universo_id"]==uid)
        assert selected["municipality_count"]>0
        assert selected["data_path"]=="universes/"+uid
        base=output/"data/universes"/uid
        municipalities=json.loads((base/"municipalities.json").read_text(encoding="utf-8"))
        assert len(municipalities)==selected["municipality_count"]
        assert example["codigo_ibge"] in {m["codigo_ibge"] for m in municipalities}
        metadata=json.loads((base/"metadata.json").read_text(encoding="utf-8"))
        assert metadata["universe"]["universo_id"]==uid
        annual=json.loads((base/"annual/2025.json").read_text(encoding="utf-8"))
        assert example["codigo_ibge"] in {m["codigo_ibge"] for m in annual["municipalities"]}
        assert (base/"municipalities"/(example["codigo_ibge"]+".json")).is_file()
