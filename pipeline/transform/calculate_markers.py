from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path


MARKERS = {
    "base": ("receita_tributaria", "base"),
    "invest": ("investimento", "invest"),
    "territ": ("territorial", "territ"),
    "pessoal": ("dtp", "pessoal"),
    "divida": ("dc", "divida"),
    "liquidez": ("caixa", "liquidez"),
}


def marker_text(kind: str, quadrant: str | None) -> str | None:
    if not quadrant or quadrant == "sem classificação":
        return "sem classificação"

    above = quadrant.startswith("acima")
    stable = "mais estável" in quadrant

    if kind == "base":
        return (
            "base tributária acima da mediana"
            if above
            else "base tributária abaixo da mediana"
        )
    if kind == "invest":
        return (
            ("investimento alto e " if above else "investimento baixo e ")
            + ("mais estável" if stable else "mais volátil")
        )
    if kind == "territ":
        return (
            ("peso territorial alto e " if above else "peso territorial baixo e ")
            + ("mais estável" if stable else "mais volátil")
        )
    if kind == "pessoal":
        return "DTP acima da mediana" if above else "DTP abaixo da mediana"
    if kind == "divida":
        return "dívida acima da mediana" if above else "dívida abaixo da mediana"
    if kind == "liquidez":
        return (
            "liquidez acima da mediana"
            if above
            else "liquidez abaixo da mediana"
        )
    raise ValueError(f"Marcador desconhecido: {kind}")


def calculate_markers(
    database: Path,
    universe_id: str = "TIC_TIM_30",
    window_id: str = "2021_2025",
) -> dict:
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

    build = con.execute(
        "SELECT build_id FROM build ORDER BY build_timestamp DESC LIMIT 1"
    ).fetchone()
    build_id = build[0] if build else None
    written = 0

    try:
        for code in municipalities:
            classes = {
                row["dimensao_id"]: row["quadrante"]
                for row in con.execute(
                    """
                    SELECT dimensao_id,quadrante
                    FROM classificacao_relativa
                    WHERE codigo_ibge=?
                      AND universo_id=?
                      AND janela_id=?
                    """,
                    (code, universe_id, window_id),
                )
            }

            for marker_id, (dimension_id, kind) in MARKERS.items():
                value = marker_text(kind, classes.get(dimension_id))
                status = (
                    "sem_classificacao"
                    if value == "sem classificação"
                    else "observado"
                )
                con.execute(
                    """
                    INSERT INTO marcador_comparavel(
                        codigo_ibge,universo_id,janela_id,marcador_id,
                        valor_texto,status,build_id
                    ) VALUES (?,?,?,?,?,?,?)
                    ON CONFLICT(
                        codigo_ibge,universo_id,janela_id,marcador_id
                    ) DO UPDATE SET
                        valor_texto=excluded.valor_texto,
                        status=excluded.status,
                        build_id=excluded.build_id
                    """,
                    (
                        code, universe_id, window_id, marker_id,
                        value, status, build_id,
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
        "municipalities": len(municipalities),
        "markers": len(MARKERS),
        "rows_written": written,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Calcula os seis marcadores comparáveis do Bloco 3."
    )
    parser.add_argument("database", type=Path)
    parser.add_argument("--universe", default="TIC_TIM_30")
    parser.add_argument("--window", default="2021_2025")
    args = parser.parse_args()
    result = calculate_markers(
        args.database,
        universe_id=args.universe,
        window_id=args.window,
    )
    for key, value in result.items():
        print(f"{key}={value}")


if __name__ == "__main__":
    main()
