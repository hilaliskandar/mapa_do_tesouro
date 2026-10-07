from __future__ import annotations

import argparse
import sqlite3
import statistics
from collections import defaultdict
from pathlib import Path

DEFAULT_VARIABLES = [
    "receita_tributaria_pct_receita_corrente",
    "investimento_pct_receita_corrente",
    "investimento_pc",
    "despesa_territorial_pct_despesa",
    "despesa_territorial_pc",
    "dtp_pct_rcl",
    "dc_pct_rcl",
    "dcl_pct_rcl",
    "caixa_pos_rpnp_pct_rcl",
]


def upsert_stat(
    con: sqlite3.Connection,
    code: str,
    universe: str,
    variable: str,
    window: str,
    metric: str,
    value: float | None,
    status: str,
    n: int,
    build_id: str | None,
) -> None:
    con.execute(
        """
        INSERT INTO estatistica_janela(
            codigo_ibge,universo_id,variavel_id,janela_id,metrica_id,
            valor_num,status,n_observacoes,build_id
        ) VALUES (?,?,?,?,?,?,?,?,?)
        ON CONFLICT(
            codigo_ibge,universo_id,variavel_id,janela_id,metrica_id
        ) DO UPDATE SET
            valor_num=excluded.valor_num,
            status=excluded.status,
            n_observacoes=excluded.n_observacoes,
            build_id=excluded.build_id
        """,
        (code, universe, variable, window, metric, value, status, n, build_id),
    )


def calculate_window_statistics(
    database: Path,
    universe_id: str = "TIC_TIM_30",
    window_id: str = "2021_2025",
    variables: list[str] | None = None,
) -> dict:
    variables = variables or DEFAULT_VARIABLES
    con = sqlite3.connect(database)
    con.execute("PRAGMA foreign_keys = ON")
    con.row_factory = sqlite3.Row

    window = con.execute(
        "SELECT ano_inicio,ano_fim FROM janela_analitica WHERE janela_id=?",
        (window_id,),
    ).fetchone()
    if window is None:
        raise ValueError(f"Janela inexistente: {window_id}")
    start, end = int(window["ano_inicio"]), int(window["ano_fim"])

    municipalities = [
        row[0]
        for row in con.execute(
            """
            SELECT codigo_ibge
            FROM universo_municipio
            WHERE universo_id=?
            ORDER BY codigo_ibge
            """,
            (universe_id,),
        )
    ]
    if not municipalities:
        raise ValueError(f"Universo sem municípios: {universe_id}")

    build = con.execute(
        "SELECT build_id FROM build ORDER BY build_timestamp DESC LIMIT 1"
    ).fetchone()
    build_id = build[0] if build else None
    written = 0

    try:
        for variable in variables:
            annual: dict[str, dict[int, float]] = defaultdict(dict)
            rows = con.execute(
                """
                SELECT o.codigo_ibge,o.ano,o.valor_num
                FROM observacao o
                JOIN universo_municipio u
                  ON u.codigo_ibge=o.codigo_ibge
                 AND u.universo_id=?
                WHERE o.variavel_id=?
                  AND o.ano BETWEEN ? AND ?
                  AND o.status='observado'
                  AND o.valor_num IS NOT NULL
                """,
                (universe_id, variable, start, end),
            ).fetchall()
            for row in rows:
                annual[row["codigo_ibge"]][int(row["ano"])] = float(row["valor_num"])

            medians_by_year: dict[int, float] = {}
            for year in range(start, end + 1):
                year_values = [
                    annual[code][year]
                    for code in municipalities
                    if year in annual[code]
                ]
                if year_values:
                    medians_by_year[year] = statistics.median(year_values)

            means: dict[str, float] = {}
            pending_rank: list[str] = []

            for code in municipalities:
                series = annual.get(code, {})
                values = [series[y] for y in sorted(series)]
                n = len(values)

                if n:
                    mean = statistics.fmean(values)
                    means[code] = mean
                    pending_rank.append(code)
                    upsert_stat(
                        con, code, universe_id, variable, window_id,
                        "media", mean, "observado", n, build_id,
                    )
                    amplitude = max(values) - min(values)
                    upsert_stat(
                        con, code, universe_id, variable, window_id,
                        "amplitude", amplitude, "observado", n, build_id,
                    )
                    above = sum(
                        1
                        for year, value in series.items()
                        if year in medians_by_year
                        and value >= medians_by_year[year]
                    )
                    upsert_stat(
                        con, code, universe_id, variable, window_id,
                        "anos_acima_mediana_grupo", float(above),
                        "observado", n, build_id,
                    )
                else:
                    for metric in (
                        "media", "amplitude", "anos_acima_mediana_grupo"
                    ):
                        upsert_stat(
                            con, code, universe_id, variable, window_id,
                            metric, None, "ausente", 0, build_id,
                        )

                if n >= 2:
                    std = statistics.stdev(values)
                    upsert_stat(
                        con, code, universe_id, variable, window_id,
                        "desvio", std, "observado", n, build_id,
                    )
                    mean = statistics.fmean(values)
                    if mean != 0:
                        upsert_stat(
                            con, code, universe_id, variable, window_id,
                            "cv", std / mean, "observado", n, build_id,
                        )
                    else:
                        upsert_stat(
                            con, code, universe_id, variable, window_id,
                            "cv", None, "ausente", n, build_id,
                        )
                else:
                    for metric in ("desvio", "cv"):
                        upsert_stat(
                            con, code, universe_id, variable, window_id,
                            metric, None, "ausente", n, build_id,
                        )

                if start in series and end in series:
                    upsert_stat(
                        con, code, universe_id, variable, window_id,
                        "mudanca", series[end] - series[start],
                        "observado", n, build_id,
                    )
                else:
                    upsert_stat(
                        con, code, universe_id, variable, window_id,
                        "mudanca", None, "ausente", n, build_id,
                    )

            for code in municipalities:
                if code not in means:
                    upsert_stat(
                        con, code, universe_id, variable, window_id,
                        "rank_media_desc", None, "ausente", 0, build_id,
                    )
                    continue
                value = means[code]
                rank = 1 + sum(other > value for other in means.values())
                upsert_stat(
                    con, code, universe_id, variable, window_id,
                    "rank_media_desc", float(rank), "observado",
                    len(annual.get(code, {})), build_id,
                )

            written += len(municipalities) * 7

        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()

    return {
        "universe_id": universe_id,
        "window_id": window_id,
        "variables": len(variables),
        "municipalities": len(municipalities),
        "rows_written": written,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Calcula estatísticas temporais por universo e janela."
    )
    parser.add_argument("database", type=Path)
    parser.add_argument("--universe", default="TIC_TIM_30")
    parser.add_argument("--window", default="2021_2025")
    args = parser.parse_args()
    result = calculate_window_statistics(
        args.database,
        universe_id=args.universe,
        window_id=args.window,
    )
    for key, value in result.items():
        print(f"{key}={value}")


if __name__ == "__main__":
    main()
