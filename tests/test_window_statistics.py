import sqlite3

from pipeline.build.init_db import initialize_database
from pipeline.build.load_catalog import load_catalog
from pipeline.transform.calculate_window_statistics import (
    calculate_window_statistics,
)


def test_window_statistics_match_block3_semantics(tmp_path):
    db = tmp_path / "x.sqlite"
    initialize_database(db)
    load_catalog(db)
    con = sqlite3.connect(db)
    try:
        con.execute(
            "INSERT INTO universo(universo_id,nome) VALUES ('TIC_TIM_30','Teste')"
        )
        for code, values in {
            "3500001": [1, 2, 3, 4, 5],
            "3500002": [2, 2, 2, 2, 2],
            "3500003": [None, None, 4, None, 6],
        }.items():
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
            for offset, value in enumerate(values):
                year = 2021 + offset
                if value is None:
                    con.execute(
                        """
                        INSERT INTO observacao(
                            codigo_ibge,ano,variavel_id,status
                        ) VALUES (?,?,?,'ausente')
                        """,
                        (code, year, "investimento_pct_receita_corrente"),
                    )
                else:
                    con.execute(
                        """
                        INSERT INTO observacao(
                            codigo_ibge,ano,variavel_id,valor_num,status
                        ) VALUES (?,?,?,?,'observado')
                        """,
                        (
                            code, year,
                            "investimento_pct_receita_corrente",
                            float(value),
                        ),
                    )
        con.commit()
    finally:
        con.close()

    calculate_window_statistics(
        db,
        variables=["investimento_pct_receita_corrente"],
    )

    con = sqlite3.connect(db)
    try:
        stats = dict(
            con.execute(
                """
                SELECT metrica_id,valor_num
                FROM estatistica_janela
                WHERE codigo_ibge='3500001'
                  AND variavel_id='investimento_pct_receita_corrente'
                """
            ).fetchall()
        )
        assert stats["media"] == 3.0
        assert stats["desvio"] > 1.58 and stats["desvio"] < 1.59
        assert stats["cv"] > 0.52 and stats["cv"] < 0.53
        assert stats["mudanca"] == 4.0
        assert stats["amplitude"] == 4.0
        assert stats["anos_acima_mediana_grupo"] == 3.0
        assert stats["rank_media_desc"] == 2.0

        sparse = dict(
            con.execute(
                """
                SELECT metrica_id,status
                FROM estatistica_janela
                WHERE codigo_ibge='3500003'
                  AND variavel_id='investimento_pct_receita_corrente'
                """
            ).fetchall()
        )
        assert sparse["mudanca"] == "ausente"
        assert sparse["media"] == "observado"
    finally:
        con.close()
