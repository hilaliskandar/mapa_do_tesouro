from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path

MARKER_ORDER = ["base", "invest", "territ", "pessoal", "divida", "liquidez"]


def calculate_pairs(
    database: Path,
    universe_id: str = "TIC_TIM_30",
    window_id: str = "2021_2025",
    min_comparable_dimensions: int = 4,
    top_n: int = 3,
) -> dict:
    con = sqlite3.connect(database)
    con.execute("PRAGMA foreign_keys = ON")
    con.row_factory = sqlite3.Row

    municipalities = con.execute(
        """
        SELECT m.codigo_ibge,m.nome
        FROM universo_municipio u
        JOIN municipio m USING(codigo_ibge)
        WHERE u.universo_id=?
        ORDER BY m.nome,m.codigo_ibge
        """,
        (universe_id,),
    ).fetchall()
    if not municipalities:
        raise ValueError(f"Universo sem municipios: {universe_id}")

    build = con.execute(
        "SELECT build_id FROM build ORDER BY build_timestamp DESC LIMIT 1"
    ).fetchone()
    build_id = build[0] if build else None

    names = {row["codigo_ibge"]: row["nome"] for row in municipalities}
    markers: dict[str, dict[str, str]] = {}
    for code in names:
        markers[code] = {
            row["marcador_id"]: row["valor_texto"]
            for row in con.execute(
                """
                SELECT marcador_id,valor_texto
                FROM marcador_comparavel
                WHERE codigo_ibge=?
                  AND universo_id=?
                  AND janela_id=?
                  AND status='observado'
                """,
                (code, universe_id, window_id),
            )
        }

    candidates: dict[str, list[dict]] = {code: [] for code in names}

    try:
        con.execute(
            "DELETE FROM par_municipal WHERE universo_id=? AND janela_id=?",
            (universe_id, window_id),
        )

        for ref in names:
            for comp in names:
                if ref == comp:
                    continue

                comparable = []
                coincident = []
                for marker_id in MARKER_ORDER:
                    left = markers.get(ref, {}).get(marker_id)
                    right = markers.get(comp, {}).get(marker_id)
                    if left is None or right is None:
                        continue
                    comparable.append(marker_id)
                    if left == right:
                        coincident.append(marker_id)

                n_comparable = len(comparable)
                n_coincident = len(coincident)
                proportion = (
                    n_coincident / n_comparable
                    if n_comparable
                    else 0.0
                )

                item = {
                    "ref": ref,
                    "comp": comp,
                    "comparable": n_comparable,
                    "coincident": n_coincident,
                    "proportion": proportion,
                    "dimensions": coincident,
                }
                candidates[ref].append(item)

                con.execute(
                    """
                    INSERT INTO par_municipal(
                        codigo_ibge_referencia,codigo_ibge_comparado,
                        universo_id,janela_id,dimensoes_comparaveis,
                        dimensoes_coincidentes,proporcao_coincidencia,
                        ordem_prioritaria,reciproco,
                        dimensoes_coincidentes_lista,observacao,build_id
                    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
                    """,
                    (
                        ref, comp, universe_id, window_id,
                        n_comparable, n_coincident, proportion,
                        None, 0, ", ".join(coincident) if coincident else None,
                        (
                            "comparação com cobertura limitada"
                            if n_comparable < min_comparable_dimensions
                            else (
                                "coincidência categorial em seis marcadores "
                                "independentes; CAPAG e DCL não entram na assinatura"
                            )
                        ),
                        build_id,
                    ),
                )

        principal: dict[str, str] = {}
        for ref, items in candidates.items():
            eligible = [
                item
                for item in items
                if item["comparable"] >= min_comparable_dimensions
            ]
            eligible.sort(
                key=lambda item: (
                    -item["proportion"],
                    -item["coincident"],
                    -item["comparable"],
                    names[item["comp"]].casefold(),
                    item["comp"],
                )
            )
            for order, item in enumerate(eligible[:top_n], start=1):
                con.execute(
                    """
                    UPDATE par_municipal
                    SET ordem_prioritaria=?
                    WHERE codigo_ibge_referencia=?
                      AND codigo_ibge_comparado=?
                      AND universo_id=?
                      AND janela_id=?
                    """,
                    (order, ref, item["comp"], universe_id, window_id),
                )
                if order == 1:
                    principal[ref] = item["comp"]

        reciprocal_pairs = 0
        seen = set()
        for ref, comp in principal.items():
            if principal.get(comp) == ref:
                key = tuple(sorted((ref, comp)))
                if key not in seen:
                    seen.add(key)
                    reciprocal_pairs += 1
                con.execute(
                    """
                    UPDATE par_municipal
                    SET reciproco=1
                    WHERE universo_id=?
                      AND janela_id=?
                      AND (
                        (codigo_ibge_referencia=? AND codigo_ibge_comparado=?)
                        OR
                        (codigo_ibge_referencia=? AND codigo_ibge_comparado=?)
                      )
                    """,
                    (universe_id, window_id, ref, comp, comp, ref),
                )

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
        "markers": len(MARKER_ORDER),
        "directed_pairs": len(municipalities) * (len(municipalities) - 1),
        "reciprocal_principal_pairs": reciprocal_pairs,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Calcula pares comparáveis a partir dos seis marcadores."
    )
    parser.add_argument("database", type=Path)
    parser.add_argument("--universe", default="TIC_TIM_30")
    parser.add_argument("--window", default="2021_2025")
    parser.add_argument("--min-dimensions", type=int, default=4)
    parser.add_argument("--top-n", type=int, default=3)
    args = parser.parse_args()
    result = calculate_pairs(
        args.database,
        universe_id=args.universe,
        window_id=args.window,
        min_comparable_dimensions=args.min_dimensions,
        top_n=args.top_n,
    )
    for key, value in result.items():
        print(f"{key}={value}")


if __name__ == "__main__":
    main()
