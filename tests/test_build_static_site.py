import json
import sqlite3

from pipeline.build.build_static_site import build_static_site
from pipeline.build.init_db import initialize_database
from pipeline.build.load_catalog import load_catalog
from pipeline.build.load_documentation import load_documentation


def test_static_site_build_is_self_contained(tmp_path):
    db = tmp_path / "x.sqlite"
    initialize_database(db)
    load_catalog(db)
    load_documentation(db, strict=True)

    con = sqlite3.connect(db)
    try:
        con.execute(
            "INSERT INTO universo(universo_id,nome) VALUES ('TIC_TIM_30','Teste')"
        )
        con.execute(
            "INSERT INTO municipio(codigo_ibge,nome,uf) VALUES ('3500001','Alfa','SP')"
        )
        con.execute(
            """
            INSERT INTO universo_municipio(universo_id,codigo_ibge)
            VALUES ('TIC_TIM_30','3500001')
            """
        )
        con.execute(
            """
            INSERT INTO observacao(
                codigo_ibge,ano,variavel_id,valor_num,status
            ) VALUES (
                '3500001',2025,'dca_receita_corrente_bruta',1000,'observado'
            )
            """
        )
        con.commit()
    finally:
        con.close()

    geo = tmp_path / "sp.geojson"
    geo.write_text(
        json.dumps(
            {
                "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "id": "3500001",
                        "properties": {"name": "Alfa"},
                        "geometry": {
                            "type": "Polygon",
                            "coordinates": [[[0,0],[1,0],[1,1],[0,1],[0,0]]],
                        },
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    out = tmp_path / "site"
    result = build_static_site(db, out, source_geojson=geo)

    for filename in ("index.html", "styles.css", "app.js", "_headers"):
        assert (out / filename).exists()

    assert (out / "data" / "metadata.json").exists()
    assert (out / "data" / "annual" / "2025.json").exists()
    assert (out / "data" / "maps" / "municipalities.geojson").exists()
    assert result["map"]["features"] == 1


def test_static_site_headers_harden_publication(tmp_path):
    db = tmp_path / "x.sqlite"
    initialize_database(db)
    load_catalog(db)
    load_documentation(db, strict=True)

    con = sqlite3.connect(db)
    try:
        con.execute("INSERT INTO universo(universo_id,nome) VALUES (\'TIC_TIM_30\',\'Teste\')")
        con.execute("INSERT INTO municipio(codigo_ibge,nome,uf) VALUES (\'3500001\',\'Alfa\',\'SP\')")
        con.execute("INSERT INTO universo_municipio(universo_id,codigo_ibge) VALUES (\'TIC_TIM_30\',\'3500001\')")
        con.execute("INSERT INTO observacao(codigo_ibge,ano,variavel_id,valor_num,status) VALUES (\'3500001\',2025,\'dca_receita_corrente_bruta\',1000,\'observado\')")
        con.commit()
    finally:
        con.close()

    out = tmp_path / "site"
    build_static_site(db, out)
    headers = (out / "_headers").read_text(encoding="utf-8")

    assert "X-Frame-Options: DENY" in headers
    assert "Content-Security-Policy:" in headers
    assert "connect-src \'self\'" in headers
    assert "/data/*" in headers


def test_static_site_can_export_multiple_universes(tmp_path):
    db = tmp_path / "multi.sqlite"
    initialize_database(db)
    load_catalog(db)
    load_documentation(db, strict=True)

    con = sqlite3.connect(db)
    try:
        con.execute(
            "INSERT INTO universo(universo_id,nome,tipo) VALUES ('SP_645','Estado','estadual')"
        )
        con.execute(
            "INSERT INTO universo(universo_id,nome,tipo) VALUES ('CIDADES_MEDIAS','Cidades Médias','analitico')"
        )
        con.execute(
            "INSERT INTO municipio(codigo_ibge,nome,uf) VALUES ('3500001','Alfa','SP')"
        )
        con.execute(
            "INSERT INTO universo_municipio(universo_id,codigo_ibge) VALUES ('SP_645','3500001')"
        )
        con.execute(
            "INSERT INTO universo_municipio(universo_id,codigo_ibge) VALUES ('CIDADES_MEDIAS','3500001')"
        )
        con.execute(
            """
            INSERT INTO observacao(
                codigo_ibge,ano,variavel_id,valor_num,status
            ) VALUES ('3500001',2025,'dca_receita_corrente_bruta',1000,'observado')
            """
        )
        con.commit()
    finally:
        con.close()

    out = tmp_path / "site"
    result = build_static_site(
        db,
        out,
        universe_id="SP_645",
        universe_ids=["SP_645", "CIDADES_MEDIAS"],
    )

    universes = json.loads(
        (out / "data" / "universes.json").read_text(encoding="utf-8")
    )
    assert result["universe_count"] == 2
    assert [item["universo_id"] for item in universes] == [
        "SP_645",
        "CIDADES_MEDIAS",
    ]
    assert universes[0]["data_path"] == "."
    assert universes[1]["data_path"] == "universes/CIDADES_MEDIAS"
    assert (
        out
        / "data"
        / "universes"
        / "CIDADES_MEDIAS"
        / "metadata.json"
    ).exists()
    assert (
        out
        / "data"
        / "universes"
        / "CIDADES_MEDIAS"
        / "annual"
        / "2025.json"
    ).exists()
