import json
import sqlite3

from pipeline.build.export_map_geojson import export_universe_geojson
from pipeline.build.init_db import initialize_database


def test_map_export_filters_to_universe(tmp_path):
    db = tmp_path / "x.sqlite"
    initialize_database(db)
    con = sqlite3.connect(db)
    try:
        con.execute(
            "INSERT INTO universo(universo_id,nome) VALUES ('TIC_TIM_30','Teste')"
        )
        for code in ("3500001", "3500002"):
            con.execute(
                "INSERT INTO municipio(codigo_ibge,nome,uf) VALUES (?,?,?)",
                (code, code, "SP"),
            )
            con.execute(
                """
                INSERT INTO universo_municipio(universo_id,codigo_ibge)
                VALUES ('TIC_TIM_30',?)
                """,
                (code,),
            )
        con.commit()
    finally:
        con.close()

    source = tmp_path / "source.geojson"
    source.write_text(
        json.dumps(
            {
                "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "id": "3500001",
                        "properties": {"name": "A"},
                        "geometry": {
                            "type": "Polygon",
                            "coordinates": [[[0,0],[1,0],[1,1],[0,1],[0,0]]],
                        },
                    },
                    {
                        "type": "Feature",
                        "id": "3500002",
                        "properties": {"name": "B"},
                        "geometry": {
                            "type": "Polygon",
                            "coordinates": [[[1,0],[2,0],[2,1],[1,1],[1,0]]],
                        },
                    },
                    {
                        "type": "Feature",
                        "id": "9999999",
                        "properties": {"name": "Fora"},
                        "geometry": {
                            "type": "Polygon",
                            "coordinates": [[[2,0],[3,0],[3,1],[2,1],[2,0]]],
                        },
                    },
                ],
            }
        ),
        encoding="utf-8",
    )

    out = tmp_path / "maps" / "municipalities.geojson"
    result = export_universe_geojson(db, source, out)
    assert result["features"] == 2

    payload = json.loads(out.read_text(encoding="utf-8"))
    assert [f["id"] for f in payload["features"]] == ["3500001", "3500002"]
    assert all("codigo_ibge" in f["properties"] for f in payload["features"])
