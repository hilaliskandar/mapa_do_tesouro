import json
import sqlite3

from pipeline.build.export_static_data import export_static_data
from pipeline.build.init_db import initialize_database
from pipeline.build.load_catalog import load_catalog
from pipeline.build.load_documentation import load_documentation


def test_static_first_contract(tmp_path):
    db = tmp_path / "x.sqlite"
    out = tmp_path / "public" / "data"
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

    result = export_static_data(db, out)
    assert result["municipalities"] == 1
    assert result["annual_snapshots"] == 1
    assert (out / "metadata.json").exists()
    assert (out / "annual" / "2025.json").exists()
    assert (out / "municipalities" / "3500001.json").exists()
    assert (out / "manifest.json").exists()

    annual = json.loads(
        (out / "annual" / "2025.json").read_text(encoding="utf-8")
    )
    value = annual["municipalities"][0]["values"][
        "dca_receita_corrente_bruta"
    ]
    assert value == {"status": "observado", "value": 1000.0}

    municipal = json.loads(
        (out / "municipalities" / "3500001.json").read_text(encoding="utf-8")
    )
    assert municipal["series"]["dca_receita_corrente_bruta"][0]["year"] == 2025

    manifest = json.loads(
        (out / "manifest.json").read_text(encoding="utf-8")
    )
    assert "annual/2025.json" in manifest["files"]
    assert "municipalities/3500001.json" in manifest["files"]
