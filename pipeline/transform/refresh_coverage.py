from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path


STATUSES = ("observado", "ausente", "nao_aplicavel", "em_revisao")


def refresh_coverage(database: Path, universe_id: str) -> dict:
    con = sqlite3.connect(database)
    try:
        expected = con.execute(
            """
            SELECT COUNT(*)
            FROM universo_municipio
            WHERE universo_id=?
            """,
            (universe_id,),
        ).fetchone()[0]
        if expected <= 0:
            raise ValueError(f"Universo sem municipios: {universe_id}")

        keys = con.execute(
            """
            SELECT DISTINCT o.variavel_id,o.ano
            FROM observacao o
            JOIN universo_municipio u USING(codigo_ibge)
            WHERE u.universo_id=?
            ORDER BY o.variavel_id,o.ano
            """,
            (universe_id,),
        ).fetchall()

        con.execute("DELETE FROM cobertura WHERE universo_id=?", (universe_id,))
        written = 0
        missing_rows_total = 0

        for variable_id, year in keys:
            counts = {status: 0 for status in STATUSES}
            for status, count in con.execute(
                """
                SELECT o.status,COUNT(*)
                FROM observacao o
                JOIN universo_municipio u USING(codigo_ibge)
                WHERE u.universo_id=?
                  AND o.variavel_id=?
                  AND o.ano=?
                GROUP BY o.status
                """,
                (universe_id, variable_id, year),
            ):
                counts[status] = int(count)

            represented = sum(counts.values())
            if represented > expected:
                raise ValueError(
                    f"Cobertura excede universo: {variable_id}/{year}: "
                    f"{represented}>{expected}"
                )

            missing_rows = expected - represented
            counts["ausente"] += missing_rows
            missing_rows_total += missing_rows

            con.execute(
                """
                INSERT INTO cobertura(
                    variavel_id,ano,universo_id,esperado,
                    observado,ausente,nao_aplicavel,em_revisao
                ) VALUES (?,?,?,?,?,?,?,?)
                """,
                (
                    variable_id,
                    year,
                    universe_id,
                    expected,
                    counts["observado"],
                    counts["ausente"],
                    counts["nao_aplicavel"],
                    counts["em_revisao"],
                ),
            )
            written += 1

        con.commit()
        return {
            "universe_id": universe_id,
            "expected_municipalities": expected,
            "coverage_rows": written,
            "implicit_missing_rows_classified_as_absent": missing_rows_total,
        }
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Recalcula cobertura canonica a partir das observacoes finais."
    )
    parser.add_argument("database", type=Path)
    parser.add_argument("--universe", required=True)
    args = parser.parse_args()
    result = refresh_coverage(args.database, args.universe)
    for key, value in result.items():
        print(f"{key}={value}")


if __name__ == "__main__":
    main()
