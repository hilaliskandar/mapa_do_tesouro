from __future__ import annotations

# Gate F rebuild trigger: rerun private SP645 QA after RGF02 post-processing.

import argparse
import json
import sqlite3
from pathlib import Path

from pipeline.build.build_static_site import build_static_site
from pipeline.build.export_publication_api import export_publication_api
from pipeline.build.load_documentation import load_documentation
from pipeline.ingest.import_multifuentes import import_multifuentes
from pipeline.ingest.import_universe_catalog import import_universe_catalog
from pipeline.transform.calculate_annual import calculate_annual
from pipeline.transform.refresh_coverage import refresh_coverage
from pipeline.transform.calculate_markers import calculate_markers
from pipeline.transform.calculate_pairs import calculate_pairs
from pipeline.transform.calculate_typologies import calculate_typologies
from pipeline.transform.calculate_window_statistics import calculate_window_statistics

ROOT = Path(__file__).resolve().parents[2]
PUBLICATION_UNIVERSES_CATALOG = ROOT / "data" / "catalogs" / "publication_universes_sp.yml"
PUBLICATION_VARIABLES_CATALOG = ROOT / "data" / "catalogs" / "publication_variables_v1.yml"

UNIVERSE_CATALOGS = (
    ROOT / "data" / "catalogs" / "project_universes_sp.yml",
    ROOT / "data" / "catalogs" / "territorial_universes_sp_2025.yml",
    ROOT / "data" / "catalogs" / "analytical_universes_sp.yml",
)


def _load_additional_universes(database: Path) -> list[str]:
    with sqlite3.connect(database) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        for catalog in UNIVERSE_CATALOGS:
            import_universe_catalog(connection, catalog)

        rows = connection.execute(
            """
            SELECT universo_id
            FROM universo
            WHERE ativo=1
            ORDER BY CASE universo_id
                WHEN 'SP_645' THEN 0
                WHEN 'TIC_TIM_30' THEN 1
                WHEN 'CIDADES_MEDIAS' THEN 2
                ELSE 3
            END, nome, universo_id
            """
        ).fetchall()
    return [row[0] for row in rows]


def build_sp645_private_site(
    workbook: Path,
    mapping: Path,
    database: Path,
    site_output: Path,
    geojson: Path,
) -> dict:
    result = {}
    result["ingest"] = import_multifuentes(
        workbook,
        database,
        mapping_path=mapping,
        overwrite=True,
        universe_id="SP_645",
        universe_name="São Paulo — 645 municípios",
        universe_description="Build privado estadual SP645 para QA.",
        universe_type="estadual",
    )
    load_documentation(database, strict=True)
    universe_ids = _load_additional_universes(database)
    result["universe_ids"] = universe_ids

    result["annual_2025"] = calculate_annual(database, years={2025})
    result["analysis_by_universe"] = {}
    for current_id in universe_ids:
        result["analysis_by_universe"][current_id] = {
            "coverage": refresh_coverage(database, current_id),
            "window": calculate_window_statistics(database, universe_id=current_id),
            "typologies": calculate_typologies(database, universe_id=current_id),
            "markers": calculate_markers(database, universe_id=current_id),
            "pairs": calculate_pairs(database, universe_id=current_id),
        }

    # Chaves legadas preservadas para QA e consumidores existentes.
    result["coverage"] = result["analysis_by_universe"]["SP_645"]["coverage"]
    result["window"] = result["analysis_by_universe"]["SP_645"]["window"]
    result["typologies"] = result["analysis_by_universe"]["SP_645"]["typologies"]
    result["markers"] = result["analysis_by_universe"]["SP_645"]["markers"]
    result["pairs"] = result["analysis_by_universe"]["SP_645"]["pairs"]

    result["site"] = build_static_site(
        database,
        site_output,
        universe_id="SP_645",
        universe_ids=universe_ids,
        source_geojson=geojson,
    )
    result["publication_api"] = export_publication_api(
        database,
        site_output / "data" / "api" / "v1",
        universes_catalog=PUBLICATION_UNIVERSES_CATALOG,
        variables_catalog=PUBLICATION_VARIABLES_CATALOG,
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Build private SP645 static site artifact.")
    parser.add_argument("--workbook", type=Path, required=True)
    parser.add_argument("--mapping", type=Path, required=True)
    parser.add_argument("--database", type=Path, required=True)
    parser.add_argument("--site-output", type=Path, required=True)
    parser.add_argument("--geojson", type=Path, required=True)
    args = parser.parse_args()
    result = build_sp645_private_site(
        args.workbook, args.mapping, args.database, args.site_output, args.geojson
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
