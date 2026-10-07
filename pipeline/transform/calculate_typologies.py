from __future__ import annotations

import argparse
import sqlite3
import statistics
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CATALOG = ROOT / "data" / "catalogs" / "typology_dimensions_v7.yml"


def load_dimensions(path: Path = DEFAULT_CATALOG) -> list[dict]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return payload.get("dimensions", [])


def calculate_typologies(
    database: Path,
    universe_id: str = "TIC_TIM_30",
    window_id: str = "2021_2025",
    catalog: Path = DEFAULT_CATALOG,
) -> dict:
    dimensions = load_dimensions(catalog)
    con = sqlite3.connect(database)
    con.execute("PRAGMA foreign_keys = ON")
    con.row_factory = sqlite3.Row

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
        raise ValueError(f"Universo sem municipios: {universe_id}")

    build = con.execute(
        "SELECT build_id FROM build ORDER BY build_timestamp DESC LIMIT 1"
    ).fetchone()
    build_id = build[0] if build else None
    written = 0

    try:
        for dim in dimensions:
            con.execute(
                """
                INSERT INTO dimensao_tipologia(
                    dimensao_id,nome,variavel_id,sentido_interpretativo,
                    min_anos_observados,regra_nivel,regra_estabilidade,observacao
                ) VALUES (?,?,?,?,?,?,?,?)
                ON CONFLICT(dimensao_id) DO UPDATE SET
                    nome=excluded.nome,
                    variavel_id=excluded.variavel_id,
                    sentido_interpretativo=excluded.sentido_interpretativo,
                    min_anos_observados=excluded.min_anos_observados,
                    regra_nivel=excluded.regra_nivel,
                    regra_estabilidade=excluded.regra_estabilidade,
                    observacao=excluded.observacao
                """,
                (
                    dim["dimensao_id"],
                    dim["nome"],
                    dim["variavel_id"],
                    dim["sentido_interpretativo"],
                    int(dim.get("min_anos_observados", 3)),
                    ">= mediana: acima; < mediana: abaixo",
                    "CV <= mediana do CV: mais estavel; CV > mediana: mais volatil",
                    "Classificacao relativa; nao constitui nota de desempenho.",
                ),
            )

            rows = con.execute(
                """
                SELECT
                    e.codigo_ibge,
                    MAX(CASE WHEN e.metrica_id='media' THEN e.valor_num END) AS media,
                    MAX(CASE WHEN e.metrica_id='cv' THEN e.valor_num END) AS cv,
                    MAX(CASE WHEN e.metrica_id='media' THEN e.n_observacoes END) AS n_anos,
                    MAX(CASE WHEN e.metrica_id='media' THEN e.status END) AS media_status,
                    MAX(CASE WHEN e.metrica_id='cv' THEN e.status END) AS cv_status
                FROM estatistica_janela e
                WHERE e.universo_id=?
                  AND e.janela_id=?
                  AND e.variavel_id=?
                  AND e.metrica_id IN ('media','cv')
                GROUP BY e.codigo_ibge
                """,
                (universe_id, window_id, dim["variavel_id"]),
            ).fetchall()
            by_code = {row["codigo_ibge"]: row for row in rows}

            valid_means = [
                float(row["media"])
                for row in rows
                if row["media_status"] == "observado"
                and row["media"] is not None
            ]
            valid_cvs = [
                float(row["cv"])
                for row in rows
                if row["cv_status"] == "observado"
                and row["cv"] is not None
            ]
            median_level = statistics.median(valid_means) if valid_means else None
            median_cv = statistics.median(valid_cvs) if valid_cvs else None
            minimum = int(dim.get("min_anos_observados", 3))

            for code in municipalities:
                row = by_code.get(code)
                n = int(row["n_anos"] or 0) if row else 0
                media = float(row["media"]) if row and row["media"] is not None else None
                cv = float(row["cv"]) if row and row["cv"] is not None else None

                if n < minimum or media is None or median_level is None:
                    level = stability = quadrant = None
                    status = "sem_classificacao"
                else:
                    level = (
                        "acima da mediana"
                        if media >= median_level
                        else "abaixo da mediana"
                    )
                    if cv is None or median_cv is None:
                        stability = None
                        quadrant = None
                        status = "sem_classificacao"
                    else:
                        stability = (
                            "mais estavel"
                            if cv <= median_cv
                            else "mais volatil"
                        )
                        quadrant = f"{level} + {stability}"
                        status = "observado"

                con.execute(
                    """
                    INSERT INTO classificacao_relativa(
                        codigo_ibge,universo_id,dimensao_id,janela_id,
                        media,cv,n_anos,mediana_nivel,mediana_cv,
                        nivel_relativo,estabilidade,quadrante,status,build_id
                    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                    ON CONFLICT(
                        codigo_ibge,universo_id,dimensao_id,janela_id
                    ) DO UPDATE SET
                        media=excluded.media,
                        cv=excluded.cv,
                        n_anos=excluded.n_anos,
                        mediana_nivel=excluded.mediana_nivel,
                        mediana_cv=excluded.mediana_cv,
                        nivel_relativo=excluded.nivel_relativo,
                        estabilidade=excluded.estabilidade,
                        quadrante=excluded.quadrante,
                        status=excluded.status,
                        build_id=excluded.build_id
                    """,
                    (
                        code, universe_id, dim["dimensao_id"], window_id,
                        media, cv, n, median_level, median_cv,
                        level, stability, quadrant, status, build_id,
                    ),
                )
                written += 1

        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()

    return {
        "universe_id": universe_id,
        "window_id": window_id,
        "dimensions": len(dimensions),
        "municipalities": len(municipalities),
        "rows_written": written,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Calcula tipologias transparentes por universo e janela."
    )
    parser.add_argument("database", type=Path)
    parser.add_argument("--universe", default="TIC_TIM_30")
    parser.add_argument("--window", default="2021_2025")
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    args = parser.parse_args()
    result = calculate_typologies(
        args.database,
        universe_id=args.universe,
        window_id=args.window,
        catalog=args.catalog,
    )
    for key, value in result.items():
        print(f"{key}={value}")


if __name__ == "__main__":
    main()
