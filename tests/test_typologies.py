import sqlite3

from pipeline.build.init_db import initialize_database
from pipeline.build.load_catalog import load_catalog
from pipeline.transform.calculate_typologies import calculate_typologies


def test_typology_uses_medians_minimum_coverage_and_keeps_direction_metadata(tmp_path):
    db = tmp_path / "x.sqlite"
    initialize_database(db)
    load_catalog(db)
    con = sqlite3.connect(db)
    try:
        con.execute(
            "INSERT INTO universo(universo_id,nome) VALUES ('TIC_TIM_30','Teste')"
        )
        for code in ("3500001", "3500002", "3500003", "3500004"):
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

        samples = {
            "3500001": (0.10, 0.10, 5),
            "3500002": (0.20, 0.20, 5),
            "3500003": (0.30, 0.30, 5),
            "3500004": (0.40, 0.40, 2),
        }
        for code, (mean, cv, n) in samples.items():
            for metric, value in (("media", mean), ("cv", cv)):
                con.execute(
                    """
                    INSERT INTO estatistica_janela(
                        codigo_ibge,universo_id,variavel_id,janela_id,
                        metrica_id,valor_num,status,n_observacoes
                    ) VALUES (?,?,?,?,?,?,?,?)
                    """,
                    (
                        code, "TIC_TIM_30", "dtp_pct_rcl", "2021_2025",
                        metric, value, "observado", n,
                    ),
                )
        con.commit()
    finally:
        con.close()

    calculate_typologies(db)

    con = sqlite3.connect(db)
    try:
        row = con.execute(
            """
            SELECT nivel_relativo,estabilidade,quadrante,status,
                   mediana_nivel,mediana_cv
            FROM classificacao_relativa
            WHERE codigo_ibge='3500002'
              AND dimensao_id='dtp'
            """
        ).fetchone()
        assert row == (
            "abaixo da mediana",
            "mais estavel",
            "abaixo da mediana + mais estavel",
            "observado",
            0.25,
            0.25,
        )

        sparse = con.execute(
            """
            SELECT status,nivel_relativo,quadrante
            FROM classificacao_relativa
            WHERE codigo_ibge='3500004'
              AND dimensao_id='dtp'
            """
        ).fetchone()
        assert sparse == ("sem_classificacao", None, None)

        direction = con.execute(
            """
            SELECT sentido_interpretativo
            FROM dimensao_tipologia
            WHERE dimensao_id='dtp'
            """
        ).fetchone()[0]
        assert direction == "menor"
    finally:
        con.close()
