from pathlib import Path
import json
import sqlite3

from pipeline.build.export_publication_api import export_publication_api

ROOT = Path(__file__).resolve().parents[1]


def make_db(path: Path) -> None:
    con = sqlite3.connect(path)
    try:
        for schema in sorted((ROOT / "data" / "schema").glob("[0-9][0-9][0-9]_*.sql")):
            con.executescript(schema.read_text(encoding="utf-8"))
        con.execute(
            """
            INSERT INTO variavel(
                variavel_id,nome,grupo,tipo,unidade,definicao,periodicidade
            ) VALUES ('v_receita','Receita','receitas','conta_oficial','BRL','Teste','anual')
            """
        )
        con.execute(
            "INSERT INTO universo(universo_id,nome,tipo) VALUES ('U','Universo','analitico')"
        )
        for code, name in (("3500001", "Alfa"), ("3500002", "Beta"), ("3500003", "Gama")):
            con.execute(
                "INSERT INTO municipio(codigo_ibge,nome,uf) VALUES (?,?,'SP')",
                (code, name),
            )
            con.execute(
                "INSERT INTO universo_municipio(universo_id,codigo_ibge) VALUES ('U',?)",
                (code,),
            )
        con.execute(
            """
            INSERT INTO observacao(codigo_ibge,ano,variavel_id,valor_num,status)
            VALUES ('3500001',2025,'v_receita',100,'observado')
            """
        )
        con.execute(
            """
            INSERT INTO observacao(codigo_ibge,ano,variavel_id,valor_num,status)
            VALUES ('3500002',2025,'v_receita',200,'observado')
            """
        )
        con.execute(
            """
            INSERT INTO observacao(codigo_ibge,ano,variavel_id,status)
            VALUES ('3500003',2025,'v_receita','ausente')
            """
        )
        con.commit()
    finally:
        con.close()


def test_publication_api_exports_group_and_municipality_contexts(tmp_path):
    db = tmp_path / "db.sqlite"
    make_db(db)
    universes = tmp_path / "universes.yml"
    variables = tmp_path / "variables.yml"
    universes.write_text(
        """
version: 1
publication_universes:
  - publication_id: U_PUBLIC
    name: Universo Publicação
    source_universe_id: U
    type: ANALITICO
    exclude_members:
      - codigo_ibge: "3500003"
        municipio: Gama
        reason: exclusao de teste
""",
        encoding="utf-8",
    )
    variables.write_text(
        """
version: 1
groups:
  receitas:
    - v_receita
rules:
  absence_is_not_zero: true
""",
        encoding="utf-8",
    )

    out = tmp_path / "api"
    result = export_publication_api(
        db,
        out,
        universes_catalog=universes,
        variables_catalog=variables,
    )

    assert result == {
        "publication_universes": 1,
        "municipality_contexts": 2,
        "variables": 1,
    }

    index = json.loads(
        (out / "publication" / "universes.json").read_text(encoding="utf-8")
    )
    assert index[0]["member_count"] == 2
    assert index[0]["publication_id"] == "U_PUBLIC"

    context = json.loads(
        (
            out
            / "publication"
            / "universes"
            / "U_PUBLIC"
            / "context.json"
        ).read_text(encoding="utf-8")
    )
    latest = context["variables"]["v_receita"]["latest"]
    assert latest["observed"] == 2
    assert latest["numeric"]["median"] == 150
    assert latest["numeric"]["sum"] == 300

    alfa = json.loads(
        (
            out
            / "publication"
            / "universes"
            / "U_PUBLIC"
            / "municipalities"
            / "3500001.json"
        ).read_text(encoding="utf-8")
    )
    relative = alfa["variables"]["v_receita"]["relative_latest"]
    assert relative["rank_desc"] == 2
    assert relative["quartile"] in (1, 2)
    assert alfa["rules"]["absence_is_not_zero"] is True


def test_publication_catalog_has_11_groups_and_rmsp_excludes_capital():
    import yaml

    catalog = yaml.safe_load(
        (
            ROOT / "data" / "catalogs" / "publication_universes_sp.yml"
        ).read_text(encoding="utf-8")
    )
    groups = catalog["publication_universes"]
    assert len(groups) == 11
    rmsp = next(item for item in groups if item["publication_id"] == "RM_SAO_PAULO")
    assert rmsp["exclude_members"][0]["codigo_ibge"] == "3550308"
    assert next(
        item for item in groups if item["publication_id"] == "CIDADES_MEDIAS"
    )["source_universe_id"] == "CIDADES_MEDIAS"
