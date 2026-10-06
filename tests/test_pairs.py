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
        municipal = [
            ("3500001", "Alfa"),
            ("3500002", "Beta"),
            ("3500003", "Gama"),
        ]
        profiles = {
            "3500001": ["A", "B", "C", "D", "E", "F"],
            "3500002": ["A", "B", "C", "D", "E", "F"],
            "3500003": ["A", "X", "Y", "D", "E", "F"],
        }
        marker_ids = ["base", "invest", "territ", "pessoal", "divida", "liquidez"]

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
            for marker_id, value in zip(marker_ids, profiles[code]):
                con.execute(
                    """
                    INSERT INTO marcador_comparavel(
                        codigo_ibge,universo_id,janela_id,marcador_id,
                        valor_texto,status
                    ) VALUES (?, 'TIC_TIM_30','2021_2025',?,?,'observado')
                    """,
                    (code, marker_id, value),
                )
        con.commit()
    finally:
        con.close()

    result = calculate_pairs(
        db, min_comparable_dimensions=4, top_n=2
    )
    assert result["directed_pairs"] == 6
    assert result["markers"] == 6
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
        assert pair == (6, 6, 1.0, 1, 1)

        second = con.execute(
            """
            SELECT ordem_prioritaria,dimensoes_comparaveis,dimensoes_coincidentes
            FROM par_municipal
            WHERE codigo_ibge_referencia='3500001'
              AND codigo_ibge_comparado='3500003'
            """
        ).fetchone()
        assert second == (2, 6, 4)
    finally:
        con.close()
