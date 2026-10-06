import sqlite3

from pipeline.build.init_db import initialize_database
from pipeline.build.load_catalog import load_catalog
from pipeline.transform.calculate_markers import calculate_markers


def test_markers_collapse_quadrants_exactly_like_block3(tmp_path):
    db = tmp_path / "x.sqlite"
    initialize_database(db)
    load_catalog(db)
    con = sqlite3.connect(db)
    try:
        con.execute(
            "INSERT INTO universo(universo_id,nome) VALUES ('TIC_TIM_30','Teste')"
        )
        con.execute(
            "INSERT INTO municipio(codigo_ibge,nome,uf) VALUES ('3500001','Teste','SP')"
        )
        con.execute(
            """
            INSERT INTO universo_municipio(universo_id,codigo_ibge)
            VALUES ('TIC_TIM_30','3500001')
            """
        )
        rows = {
            "receita_tributaria": "acima da mediana + mais volátil",
            "investimento": "acima da mediana + mais estável",
            "territorial": "abaixo da mediana + mais volátil",
            "dtp": "acima da mediana + mais estável",
            "dc": "abaixo da mediana + mais volátil",
            "dcl": "acima da mediana + mais estável",
            "caixa": "acima da mediana + mais estável",
        }
        for dim, quadrant in rows.items():
            con.execute(
                """
                INSERT INTO dimensao_tipologia(
                    dimensao_id,nome,variavel_id,sentido_interpretativo,
                    min_anos_observados,regra_nivel,regra_estabilidade
                ) VALUES (?,?,?,'maior',3,'nivel','estabilidade')
                """,
                (dim, dim, "receita_tributaria_pct_receita_corrente"),
            )
            con.execute(
                """
                INSERT INTO classificacao_relativa(
                    codigo_ibge,universo_id,dimensao_id,janela_id,
                    n_anos,nivel_relativo,estabilidade,quadrante,status
                ) VALUES ('3500001','TIC_TIM_30',?,'2021_2025',5,'n','e',?,'observado')
                """,
                (dim, quadrant),
            )
        con.commit()
    finally:
        con.close()

    calculate_markers(db)

    con = sqlite3.connect(db)
    try:
        values = dict(
            con.execute(
                """
                SELECT marcador_id,valor_texto
                FROM marcador_comparavel
                WHERE codigo_ibge='3500001'
                ORDER BY marcador_id
                """
            ).fetchall()
        )
        assert values["base"] == "base tributária acima da mediana"
        assert values["invest"] == "investimento alto e mais estável"
        assert values["territ"] == "peso territorial baixo e mais volátil"
        assert values["pessoal"] == "DTP acima da mediana"
        assert values["divida"] == "dívida abaixo da mediana"
        assert values["liquidez"] == "liquidez acima da mediana"
        assert "dcl" not in values
    finally:
        con.close()
