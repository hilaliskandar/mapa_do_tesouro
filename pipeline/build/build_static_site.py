from __future__ import annotations

import argparse
import json
import shutil
import sqlite3
from pathlib import Path

from pipeline.build.export_static_data import export_static_data
from pipeline.build.export_map_geojson import export_universe_geojson

ROOT = Path(__file__).resolve().parents[2]
FRONTEND = ROOT / "app" / "static"


def _universe_catalog(
    database: Path,
    universe_ids: list[str],
    default_universe_id: str,
) -> list[dict]:
    con = sqlite3.connect(database)
    con.row_factory = sqlite3.Row
    try:
        placeholders = ",".join("?" for _ in universe_ids)
        rows = [
            dict(row)
            for row in con.execute(
                f"""
                SELECT
                    u.universo_id,
                    u.nome,
                    u.descricao,
                    u.tipo,
                    COUNT(um.codigo_ibge) AS municipality_count
                FROM universo u
                LEFT JOIN universo_municipio um
                  ON um.universo_id=u.universo_id
                WHERE u.universo_id IN ({placeholders})
                GROUP BY u.universo_id,u.nome,u.descricao,u.tipo
                """,
                tuple(universe_ids),
            )
        ]
    finally:
        con.close()

    found = {row["universo_id"] for row in rows}
    missing = [value for value in universe_ids if value not in found]
    if missing:
        raise ValueError(f"Universos inexistentes no build: {missing}")

    order = {value: index for index, value in enumerate(universe_ids)}
    rows.sort(key=lambda row: order[row["universo_id"]])
    for row in rows:
        row["default"] = row["universo_id"] == default_universe_id
        row["data_path"] = (
            "."
            if row["default"]
            else f"universes/{row['universo_id']}"
        )
    return rows


def build_static_site(
    database: Path,
    output: Path,
    *,
    universe_id: str = "TIC_TIM_30",
    universe_ids: list[str] | None = None,
    source_geojson: Path | None = None,
) -> dict:
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True, exist_ok=True)

    for filename in ("index.html", "styles.css", "app.js"):
        shutil.copy2(FRONTEND / filename, output / filename)

    headers = """/*
  X-Frame-Options: DENY
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=()
  Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'none'; form-action 'self'

/data/*
  Cache-Control: public, max-age=3600, must-revalidate

/*.js
  Cache-Control: public, max-age=3600, must-revalidate

/*.css
  Cache-Control: public, max-age=3600, must-revalidate
"""
    (output / "_headers").write_text(headers, encoding="utf-8")

    selected_universes = list(dict.fromkeys(universe_ids or [universe_id]))
    if universe_id not in selected_universes:
        selected_universes.insert(0, universe_id)

    catalog = _universe_catalog(database, selected_universes, universe_id)
    data_root = output / "data"
    data_root.mkdir(parents=True, exist_ok=True)
    (data_root / "universes.json").write_text(
        json.dumps(catalog, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    result: dict = {"universes": {}}
    for item in catalog:
        current_id = item["universo_id"]
        target = (
            data_root
            if item["default"]
            else data_root / "universes" / current_id
        )
        universe_result = {
            "data": export_static_data(
                database,
                target,
                universe_id=current_id,
            )
        }
        if source_geojson is not None:
            universe_result["map"] = export_universe_geojson(
                database,
                source_geojson,
                target / "maps" / "municipalities.geojson",
                universe_id=current_id,
            )
        result["universes"][current_id] = universe_result

    default_result = result["universes"][universe_id]
    result["data"] = default_result["data"]
    if "map" in default_result:
        result["map"] = default_result["map"]
    result["universe_count"] = len(catalog)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Monta site estático autossuficiente para publicação."
    )
    parser.add_argument("database", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--universe", default="TIC_TIM_30")
    parser.add_argument("--include-universe", action="append", default=[])
    parser.add_argument("--geojson", type=Path)
    args = parser.parse_args()
    universe_ids = [args.universe, *args.include_universe]
    result = build_static_site(
        args.database,
        args.output,
        universe_id=args.universe,
        universe_ids=universe_ids,
        source_geojson=args.geojson,
    )
    print(result)


if __name__ == "__main__":
    main()
