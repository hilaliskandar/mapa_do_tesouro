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
    assert (out / "coverage.json").exists()
    assert (out / "coverage_sources.json").exists()
    assert (out / "crosswalk.json").exists()

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


def test_static_export_only_includes_priority_pairs(tmp_path):
    db = tmp_path / "pairs.sqlite"
    out = tmp_path / "public" / "data"
    initialize_database(db)
    load_catalog(db)
    load_documentation(db, strict=True)

    con = sqlite3.connect(db)
    try:
        con.execute(
            "INSERT INTO universo(universo_id,nome) VALUES ('SP_TESTE','Teste')"
        )
        codes = ["3500001", "3500002", "3500003", "3500004"]
        for idx, code in enumerate(codes, start=1):
            con.execute(
                "INSERT INTO municipio(codigo_ibge,nome,uf) VALUES (?,?,?)",
                (code, f"M{idx}", "SP"),
            )
            con.execute(
                """
                INSERT INTO universo_municipio(universo_id,codigo_ibge)
                VALUES ('SP_TESTE',?)
                """,
                (code,),
            )

        pairs = [
            ("3500002", 1),
            ("3500003", None),
            ("3500004", 2),
        ]
        for compared, priority in pairs:
            con.execute(
                """
                INSERT INTO par_municipal(
                    codigo_ibge_referencia,codigo_ibge_comparado,
                    universo_id,janela_id,dimensoes_comparaveis,
                    dimensoes_coincidentes,proporcao_coincidencia,
                    ordem_prioritaria,reciproco
                ) VALUES (?,?,?,?,?,?,?,?,0)
                """,
                (
                    "3500001",
                    compared,
                    "SP_TESTE",
                    "2021_2025",
                    6,
                    4,
                    4 / 6,
                    priority,
                ),
            )
        con.commit()
    finally:
        con.close()

    export_static_data(db, out, universe_id="SP_TESTE")
    municipal = json.loads(
        (out / "municipalities" / "3500001.json").read_text(encoding="utf-8")
    )
    assert [item["codigo_ibge_comparado"] for item in municipal["pairs"]] == [
        "3500002",
        "3500004",
    ]
    assert all(item["ordem_prioritaria"] is not None for item in municipal["pairs"])



def test_static_export_includes_review_coverage(tmp_path):
    db = tmp_path / "coverage.sqlite"
    out = tmp_path / "public" / "data"
    initialize_database(db)
    load_catalog(db)
    load_documentation(db, strict=True)

    con = sqlite3.connect(db)
    try:
        con.execute(
            "INSERT INTO universo(universo_id,nome) VALUES ('SP_TESTE','Teste')"
        )
        con.execute(
            """
            INSERT INTO cobertura(
                variavel_id,ano,universo_id,esperado,
                observado,ausente,nao_aplicavel,em_revisao
            ) VALUES (
                'dca_receita_corrente_bruta',2025,'SP_TESTE',10,6,2,1,1
            )
            """
        )
        con.commit()
    finally:
        con.close()

    export_static_data(db, out, universe_id="SP_TESTE")
    coverage = json.loads(
        (out / "coverage.json").read_text(encoding="utf-8")
    )
    assert coverage[0]["em_revisao"] == 1
    assert (
        coverage[0]["observado"]
        + coverage[0]["ausente"]
        + coverage[0]["nao_aplicavel"]
        + coverage[0]["em_revisao"]
    ) == coverage[0]["esperado"]
