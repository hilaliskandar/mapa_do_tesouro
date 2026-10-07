from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path

AGGREGATIONS = {
    "tributos_imobiliarios": ["dca_iptu_principal", "dca_itbi_principal"],
    "tributos_selecionados": [
        "dca_iptu_principal", "dca_itbi_principal", "dca_iss_principal"
    ],
    "transferencias_selecionadas": [
        "dca_fpm_cota_mensal", "dca_icms_cota_parte", "dca_ipva_cota_parte"
    ],
    "despesa_territorial": [
        "dca_func_urbanismo_liquidada",
        "dca_func_habitacao_liquidada",
        "dca_func_saneamento_liquidada",
        "dca_func_gestao_ambiental_liquidada",
        "dca_func_transporte_liquidada",
    ],
    "servico_divida_liquidado": [
        "dca_juros_encargos_liquidada",
        "dca_amortizacao_divida_liquidada",
    ],
    "receitas_capital_selecionadas": [
        "dca_operacoes_credito",
        "dca_alienacao_bens",
        "dca_transferencias_capital",
    ],
    "despesas_capital_selecionadas": [
        "dca_investimentos_liquidada",
        "dca_inversoes_financeiras_liquidada",
        "dca_amortizacao_divida_liquidada",
    ],
    "gasto_social_selecionado": [
        "dca_func_saude_liquidada",
        "dca_func_educacao_liquidada",
    ],
}

DIFFERENCES = {
    "saldo_corrente_simplificado": (
        "dca_receita_corrente_bruta",
        "dca_despesa_corrente_liquidada",
    ),
    "diferenca_capital_selecionada": (
        "receitas_capital_selecionadas",
        "despesas_capital_selecionadas",
    ),
}

RATIOS = {
    "receita_tributaria_pct_receita_corrente": (
        "dca_receita_tributaria_bruta", "dca_receita_corrente_bruta"
    ),
    "fpm_pct_receita_corrente": (
        "dca_fpm_cota_mensal", "dca_receita_corrente_bruta"
    ),
    "icms_pct_receita_corrente": (
        "dca_icms_cota_parte", "dca_receita_corrente_bruta"
    ),
    "ipva_pct_receita_corrente": (
        "dca_ipva_cota_parte", "dca_receita_corrente_bruta"
    ),
    "tributos_imobiliarios_pct_receita_tributaria": (
        "tributos_imobiliarios", "dca_receita_tributaria_bruta"
    ),
    "transferencias_selecionadas_pct_receita_corrente": (
        "transferencias_selecionadas", "dca_receita_corrente_bruta"
    ),
    "urbanismo_pct_territorial": (
        "dca_func_urbanismo_liquidada", "despesa_territorial"
    ),
    "habitacao_pct_territorial": (
        "dca_func_habitacao_liquidada", "despesa_territorial"
    ),
    "saneamento_pct_territorial": (
        "dca_func_saneamento_liquidada", "despesa_territorial"
    ),
    "gestao_ambiental_pct_territorial": (
        "dca_func_gestao_ambiental_liquidada", "despesa_territorial"
    ),
    "transporte_pct_territorial": (
        "dca_func_transporte_liquidada", "despesa_territorial"
    ),
    "investimento_pct_receita_corrente": (
        "dca_investimentos_liquidada", "dca_receita_corrente_bruta"
    ),
    "despesa_territorial_pct_despesa": (
        "despesa_territorial", "dca_despesa_total_liquidada"
    ),
    "caixa_pos_rpnp_pct_rcl": (
        "rgf_caixa_liquida_apos_rpnp", "rreo_rcl_oficial"
    ),
}

PER_CAPITA = {
    "iptu_pc": ("dca_iptu_principal", "populacao_dca"),
    "itbi_pc": ("dca_itbi_principal", "populacao_dca"),
    "iss_pc": ("dca_iss_principal", "populacao_dca"),
    "investimento_pc": ("dca_investimentos_liquidada", "populacao_dca"),
    "despesa_territorial_pc": ("despesa_territorial", "populacao_dca"),
}

def fetch_numeric(
    connection: sqlite3.Connection,
    code: str,
    year: int,
    variable_id: str,
) -> tuple[str, float | None]:
    row = connection.execute(
        """
        SELECT status, valor_num
        FROM observacao
        WHERE codigo_ibge=? AND ano=? AND variavel_id=?
        """,
        (code, year, variable_id),
    ).fetchone()
    if row is None:
        return "ausente", None
    return row[0], row[1]


def upsert_numeric(
    connection: sqlite3.Connection,
    code: str,
    year: int,
    variable_id: str,
    status: str,
    value: float | None,
    build_id: str | None,
    reference: str,
) -> None:
    connection.execute(
        """
        INSERT INTO observacao(
            codigo_ibge,ano,variavel_id,valor_num,status,
            referencia_origem,build_id
        ) VALUES (?,?,?,?,?,?,?)
        ON CONFLICT(codigo_ibge,ano,variavel_id) DO UPDATE SET
            valor_num=excluded.valor_num,
            valor_texto=NULL,
            status=excluded.status,
            referencia_origem=excluded.referencia_origem,
            build_id=excluded.build_id
        """,
        (code, year, variable_id, value, status, reference, build_id),
    )


def strict_sum(connection, code, year, components):
    observations = [
        fetch_numeric(connection, code, year, variable_id)
        for variable_id in components
    ]
    statuses = [status for status, _ in observations]

    if statuses and all(status == "nao_aplicavel" for status in statuses):
        return "nao_aplicavel", None

    if all(
        status == "observado" and value is not None
        for status, value in observations
    ):
        return "observado", sum(float(value) for _, value in observations)

    return "ausente", None


def strict_difference(connection, code, year, left, right):
    ls, lv = fetch_numeric(connection, code, year, left)
    rs, rv = fetch_numeric(connection, code, year, right)
    if ls == "nao_aplicavel" and rs == "nao_aplicavel":
        return "nao_aplicavel", None
    if ls != "observado" or rs != "observado" or lv is None or rv is None:
        return "ausente", None
    return "observado", float(lv) - float(rv)


def strict_ratio(connection, code, year, numerator, denominator, scale=1.0):
    ns, nv = fetch_numeric(connection, code, year, numerator)
    ds, dv = fetch_numeric(connection, code, year, denominator)
    if ns == "nao_aplicavel" and ds == "nao_aplicavel":
        return "nao_aplicavel", None
    if ns != "observado" or ds != "observado" or nv is None or dv is None:
        return "ausente", None
    if float(dv) == 0.0:
        return "ausente", None
    return "observado", scale * float(nv) / float(dv)


def calculate_annual(database: Path) -> dict:
    connection = sqlite3.connect(database)
    connection.execute("PRAGMA foreign_keys = ON")
    keys = connection.execute(
        "SELECT codigo_ibge, ano FROM observacao GROUP BY codigo_ibge, ano ORDER BY codigo_ibge, ano"
    ).fetchall()
    build_row = connection.execute(
        "SELECT build_id FROM build ORDER BY build_timestamp DESC LIMIT 1"
    ).fetchone()
    build_id = build_row[0] if build_row else None
    written = 0

    try:
        for code, year in keys:
            for variable_id, components in AGGREGATIONS.items():
                status, value = strict_sum(connection, code, year, components)
                upsert_numeric(
                    connection, code, year, variable_id, status, value,
                    build_id, "pipeline:aggregation_strict"
                )
                written += 1

            for variable_id, (left, right) in DIFFERENCES.items():
                status, value = strict_difference(connection, code, year, left, right)
                upsert_numeric(
                    connection, code, year, variable_id, status, value,
                    build_id, "pipeline:difference_strict"
                )
                written += 1

            for variable_id, (num, den) in RATIOS.items():
                status, value = strict_ratio(connection, code, year, num, den, scale=1.0)
                upsert_numeric(
                    connection, code, year, variable_id, status, value,
                    build_id, "pipeline:ratio"
                )
                written += 1

            for variable_id, (num, den) in PER_CAPITA.items():
                status, value = strict_ratio(connection, code, year, num, den, scale=1.0)
                upsert_numeric(
                    connection, code, year, variable_id, status, value,
                    build_id, "pipeline:per_capita"
                )
                written += 1


        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()

    return {"municipio_ano": len(keys), "written": written}


def main() -> None:
    parser = argparse.ArgumentParser(description="Calcula agregações e indicadores anuais canônicos.")
    parser.add_argument("database", type=Path)
    args = parser.parse_args()
    result = calculate_annual(args.database)
    for key, value in result.items():
        print(f"{key}={value}")


if __name__ == "__main__":
    main()
