from pathlib import Path
import sqlite3

from pipeline.build.init_db import initialize_database
from pipeline.build.load_catalog import load_catalog
from pipeline.transform.calculate_annual import calculate_annual


def seed(con, code, year, values):
    con.execute(
        "INSERT INTO municipio(codigo_ibge,nome,uf) VALUES (?,?,?)",
        (code, "Teste", "SP"),
    )
    for variable_id, value in values.items():
        con.execute(
            """
            INSERT INTO observacao(
                codigo_ibge,ano,variavel_id,valor_num,status
            ) VALUES (?,?,?,?,?)
            """,
            (code, year, variable_id, value, "observado"),
        )
    con.commit()


def test_strict_aggregations_and_ratios(tmp_path):
    db = tmp_path / "x.sqlite"
    initialize_database(db)
    load_catalog(db)

    con = sqlite3.connect(db)
    try:
        seed(
            con,
            "3500000",
            2025,
            {
                "dca_iptu_principal": 100.0,
                "dca_itbi_principal": 50.0,
                "dca_iss_principal": 150.0,
                "dca_receita_tributaria_bruta": 400.0,
                "dca_receita_corrente_bruta": 1000.0,
                "dca_fpm_cota_mensal": 100.0,
                "dca_icms_cota_parte": 200.0,
                "dca_ipva_cota_parte": 50.0,
                "dca_investimentos_liquidada": 100.0,
                "populacao_dca": 10.0,
                "dca_func_urbanismo_liquidada": 20.0,
                "dca_func_habitacao_liquidada": 10.0,
                "dca_func_saneamento_liquidada": 30.0,
                "dca_func_gestao_ambiental_liquidada": 10.0,
                "dca_func_transporte_liquidada": 30.0,
                "dca_despesa_total_liquidada": 500.0,
                "dca_despesa_corrente_liquidada": 450.0,
                "dca_juros_encargos_liquidada": 5.0,
                "dca_amortizacao_divida_liquidada": 15.0,
                "dca_operacoes_credito": 40.0,
                "dca_alienacao_bens": 10.0,
                "dca_transferencias_capital": 20.0,
                "dca_inversoes_financeiras_liquidada": 5.0,
                "dca_func_saude_liquidada": 120.0,
                "dca_func_educacao_liquidada": 130.0,
                "rgf_caixa_liquida_apos_rpnp": 50.0,
                "rreo_rcl_oficial": 1000.0,
            },
        )
    finally:
        con.close()

    calculate_annual(db)

    con = sqlite3.connect(db)
    try:
        vals = dict(
            con.execute(
                """
                SELECT variavel_id, valor_num
                FROM observacao
                WHERE codigo_ibge='3500000' AND ano=2025
                """
            ).fetchall()
        )
        assert vals["tributos_imobiliarios"] == 150.0
        assert vals["tributos_selecionados"] == 300.0
        assert vals["transferencias_selecionadas"] == 350.0
        assert vals["despesa_territorial"] == 100.0
        assert vals["servico_divida_liquidado"] == 20.0
        assert vals["receitas_capital_selecionadas"] == 70.0
        assert vals["despesas_capital_selecionadas"] == 120.0
        assert vals["gasto_social_selecionado"] == 250.0
        assert vals["saldo_corrente_simplificado"] == 550.0
        assert vals["diferenca_capital_selecionada"] == -50.0
        assert vals["receita_tributaria_pct_receita_corrente"] == 0.4
        assert vals["iptu_pc"] == 10.0
        assert vals["investimento_pct_receita_corrente"] == 0.1
        assert vals["despesa_territorial_pct_despesa"] == 0.2
        assert vals["caixa_pos_rpnp_pct_rcl"] == 0.05
    finally:
        con.close()


def test_strict_sum_propagates_absence(tmp_path):
    db = tmp_path / "x.sqlite"
    initialize_database(db)
    load_catalog(db)

    con = sqlite3.connect(db)
    try:
        con.execute(
            "INSERT INTO municipio(codigo_ibge,nome,uf) VALUES ('3500000','Teste','SP')"
        )
        con.execute(
            """
            INSERT INTO observacao(
                codigo_ibge,ano,variavel_id,valor_num,status
            ) VALUES ('3500000',2025,'dca_iptu_principal',100,'observado')
            """
        )
        con.execute(
            """
            INSERT INTO observacao(
                codigo_ibge,ano,variavel_id,status
            ) VALUES ('3500000',2025,'dca_itbi_principal','ausente')
            """
        )
        con.commit()
    finally:
        con.close()

    calculate_annual(db)

    con = sqlite3.connect(db)
    try:
        assert con.execute(
            """
            SELECT status, valor_num
            FROM observacao
            WHERE codigo_ibge='3500000'
              AND ano=2025
              AND variavel_id='tributos_imobiliarios'
            """
        ).fetchone() == ("ausente", None)
    finally:
        con.close()


def test_annual_calculation_preserves_imported_legal_indicators(tmp_path):
    db = tmp_path / "legal.sqlite"
    initialize_database(db)
    load_catalog(db)

    con = sqlite3.connect(db)
    try:
        con.execute(
            "INSERT INTO municipio(codigo_ibge,nome,uf) VALUES ('3500000','Teste','SP')"
        )
        for variable_id, value in {
            "dtp_pct_rcl": 0.3669,
            "dc_pct_rcl": 0.9322,
            "dcl_pct_rcl": 0.8368,
        }.items():
            con.execute(
                """
                INSERT INTO observacao(
                    codigo_ibge,ano,variavel_id,valor_num,status,
                    referencia_origem
                ) VALUES ('3500000',2025,?,?, 'observado','fonte_oficial')
                """,
                (variable_id, value),
            )
        con.commit()
    finally:
        con.close()

    calculate_annual(db)

    con = sqlite3.connect(db)
    try:
        values = dict(
            con.execute(
                """
                SELECT variavel_id,valor_num
                FROM observacao
                WHERE codigo_ibge='3500000'
                  AND ano=2025
                  AND variavel_id IN ('dtp_pct_rcl','dc_pct_rcl','dcl_pct_rcl')
                """
            ).fetchall()
        )
        assert values == {
            "dtp_pct_rcl": 0.3669,
            "dc_pct_rcl": 0.9322,
            "dcl_pct_rcl": 0.8368,
        }
    finally:
        con.close()


def test_strict_sum_all_not_applicable_returns_not_applicable(tmp_path):
    db = tmp_path / "all_na.sqlite"
    initialize_database(db)
    load_catalog(db)

    con = sqlite3.connect(db)
    try:
        con.execute(
            "INSERT INTO municipio(codigo_ibge,nome,uf) VALUES ('3500000','Teste','SP')"
        )
        for variable_id in ("dca_iptu_principal", "dca_itbi_principal"):
            con.execute(
                """
                INSERT INTO observacao(
                    codigo_ibge,ano,variavel_id,status
                ) VALUES ('3500000',2025,?,'nao_aplicavel')
                """,
                (variable_id,),
            )
        con.commit()
    finally:
        con.close()

    calculate_annual(db)

    con = sqlite3.connect(db)
    try:
        assert con.execute(
            """
            SELECT status, valor_num
            FROM observacao
            WHERE codigo_ibge='3500000'
              AND ano=2025
              AND variavel_id='tributos_imobiliarios'
            """
        ).fetchone() == ("nao_aplicavel", None)
    finally:
        con.close()


def test_strict_sum_mixed_not_applicable_and_observed_returns_absent(tmp_path):
    db = tmp_path / "mixed_na.sqlite"
    initialize_database(db)
    load_catalog(db)

    con = sqlite3.connect(db)
    try:
        con.execute(
            "INSERT INTO municipio(codigo_ibge,nome,uf) VALUES ('3500000','Teste','SP')"
        )
        con.execute(
            """
            INSERT INTO observacao(
                codigo_ibge,ano,variavel_id,status
            ) VALUES ('3500000',2025,'dca_iptu_principal','nao_aplicavel')
            """
        )
        con.execute(
            """
            INSERT INTO observacao(
                codigo_ibge,ano,variavel_id,valor_num,status
            ) VALUES ('3500000',2025,'dca_itbi_principal',50,'observado')
            """
        )
        con.commit()
    finally:
        con.close()

    calculate_annual(db)

    con = sqlite3.connect(db)
    try:
        assert con.execute(
            """
            SELECT status, valor_num
            FROM observacao
            WHERE codigo_ibge='3500000'
              AND ano=2025
              AND variavel_id='tributos_imobiliarios'
            """
        ).fetchone() == ("ausente", None)
    finally:
        con.close()


def test_strict_sum_not_applicable_followed_by_absent_returns_absent(tmp_path):
    db = tmp_path / "na_then_absent.sqlite"
    initialize_database(db)
    load_catalog(db)

    con = sqlite3.connect(db)
    try:
        con.execute(
            "INSERT INTO municipio(codigo_ibge,nome,uf) VALUES ('3500000','Teste','SP')"
        )
        con.execute(
            """
            INSERT INTO observacao(
                codigo_ibge,ano,variavel_id,status
            ) VALUES ('3500000',2025,'dca_iptu_principal','nao_aplicavel')
            """
        )
        con.execute(
            """
            INSERT INTO observacao(
                codigo_ibge,ano,variavel_id,status
            ) VALUES ('3500000',2025,'dca_itbi_principal','ausente')
            """
        )
        con.commit()
    finally:
        con.close()

    calculate_annual(db)

    con = sqlite3.connect(db)
    try:
        assert con.execute(
            """
            SELECT status, valor_num
            FROM observacao
            WHERE codigo_ibge='3500000'
              AND ano=2025
              AND variavel_id='tributos_imobiliarios'
            """
        ).fetchone() == ("ausente", None)
    finally:
        con.close()


def test_annual_calculation_records_component_lineage(tmp_path):
    db = tmp_path / "lineage.sqlite"
    initialize_database(db)
    load_catalog(db)

    con = sqlite3.connect(db)
    try:
        seed(
            con,
            "3500000",
            2025,
            {
                "dca_iptu_principal": 100.0,
                "dca_itbi_principal": 50.0,
            },
        )
    finally:
        con.close()

    calculate_annual(db)

    con = sqlite3.connect(db)
    try:
        lineage = con.execute(
            """
            SELECT sequencia,tipo,origem_codigo_ibge,origem_ano,
                   origem_variavel_id,regra_transformacao
            FROM observacao_proveniencia
            WHERE codigo_ibge='3500000'
              AND ano=2025
              AND variavel_id='tributos_imobiliarios'
            ORDER BY sequencia
            """
        ).fetchall()
        assert lineage == [
            (1, "observacao", "3500000", 2025, "dca_iptu_principal", "strict_sum"),
            (2, "observacao", "3500000", 2025, "dca_itbi_principal", "strict_sum"),
        ]
    finally:
        con.close()
