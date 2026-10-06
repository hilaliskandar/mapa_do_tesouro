import sqlite3

from pipeline.build.init_db import initialize_database
from pipeline.build.load_catalog import load_catalog
from pipeline.transform.calculate_pairs import calculate_pairs


def test_pairs_follow_legacy_priority_rule_and_reciprocity(tmp_path):
    db = tmp_path / "x.sqlite"
    initialize_database(db)
    load_catalog(db)
    con = sqlite3.connect(db)
    try:
        con.execute(
            "INSERT INTO universo(universo_id,nome) VALUES ('TIC_TIM_30','Teste')"
        )
        dims = [
            ("a", "A", "receita_tributaria_pct_receita_corrente"),
            ("b", "B", "investimento_pct_receita_corrente"),
            ("c", "C", "dtp_pct_rcl"),
            ("d", "D", "dc_pct_rcl"),
        ]
        for dim_id, name, variable in dims:
            con.execute(
                """
                INSERT INTO dimensao_tipologia(
                    dimensao_id,nome,variavel_id,sentido_interpretativo,
                    min_anos_observados,regra_nivel,regra_estabilidade
                ) VALUES (?,?,?,'maior',3,'nivel','estabilidade')
                """,
                (dim_id, name, variable),
            )

        municipal = [
            ("3500001", "Alfa"),
            ("3500002", "Beta"),
            ("3500003", "Gama"),
        ]
        profiles = {
            "3500001": ["X", "X", "Y", "Y"],
            "3500002": ["X", "X", "Y", "Y"],
            "3500003": ["X", "Z", "Z", "Y"],
        }
        for code, name in municipal:
            con.execute(
                "INSERT INTO municipio(codigo_ibge,nome,uf) VALUES (?,?,?)",
                (code, name, "SP"),
            )
            con.execute(
                """
                INSERT INTO universo_municipio(universo_id,codigo_ibge)
                VALUES ('TIC_TIM_30',?)
                """,
                (code,),
            )
            for (dim_id, _, _), quadrant in zip(dims, profiles[code]):
                con.execute(
                    """
                    INSERT INTO classificacao_relativa(
                        codigo_ibge,universo_id,dimensao_id,janela_id,
                        n_anos,nivel_relativo,estabilidade,quadrante,status
                    ) VALUES (?,?,?,'2021_2025',5,'n','e',?,'observado')
                    """,
                    (code, "TIC_TIM_30", dim_id, quadrant),
                )
        con.commit()
    finally:
        con.close()

    result = calculate_pairs(
        db, min_comparable_dimensions=4, top_n=2
    )
    assert result["directed_pairs"] == 6
    assert result["reciprocal_principal_pairs"] == 1

    con = sqlite3.connect(db)
    try:
        pair = con.execute(
            """
            SELECT dimensoes_comparaveis,dimensoes_coincidentes,
                   proporcao_coincidencia,ordem_prioritaria,reciproco
            FROM par_municipal
            WHERE codigo_ibge_referencia='3500001'
              AND codigo_ibge_comparado='3500002'
            """
        ).fetchone()
        assert pair == (4, 4, 1.0, 1, 1)

        second = con.execute(
            """
            SELECT ordem_prioritaria
            FROM par_municipal
            WHERE codigo_ibge_referencia='3500001'
              AND codigo_ibge_comparado='3500003'
            """
        ).fetchone()[0]
        assert second == 2
    finally:
        con.close()
