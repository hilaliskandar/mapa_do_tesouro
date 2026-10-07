from __future__ import annotations

import argparse
from pathlib import Path

from pipeline.build.init_db import initialize_database
from pipeline.build.load_catalog import load_catalog
from pipeline.build.load_documentation import load_documentation
from pipeline.ingest.import_multifuentes import import_multifuentes
from pipeline.transform.calculate_annual import calculate_annual
from pipeline.transform.calculate_window_statistics import calculate_window_statistics
from pipeline.transform.calculate_typologies import calculate_typologies
from pipeline.transform.calculate_markers import calculate_markers
from pipeline.transform.calculate_pairs import calculate_pairs
from pipeline.build.export_static_data import export_static_data
from pipeline.build.build_static_site import build_static_site


def build_analytical_database(
    workbook: Path,
    database: Path,
    *,
    overwrite: bool = False,
    static_output: Path | None = None,
    site_output: Path | None = None,
    source_geojson: Path | None = None,
    universe_id: str | None = None,
    mapping_path: Path | None = None,
) -> dict:
    if database.exists() and not overwrite:
        raise FileExistsError(
            f"{database} já existe; use overwrite=True para reconstruir."
        )

    result = {}
    result["ingest"] = import_multifuentes(
        workbook,
        database,
        overwrite=overwrite,
        universe_id=universe_id,
        **({"mapping_path": mapping_path} if mapping_path is not None else {}),
    )
    active_universe = result["ingest"]["universe_id"]
    load_documentation(database, strict=True)
    result["annual"] = calculate_annual(database)
    result["window"] = calculate_window_statistics(
        database, universe_id=active_universe
    )
    result["typologies"] = calculate_typologies(
        database, universe_id=active_universe
    )
    result["markers"] = calculate_markers(
        database, universe_id=active_universe
    )
    result["pairs"] = calculate_pairs(
        database, universe_id=active_universe
    )
    if static_output is not None:
        result["static"] = export_static_data(
            database, static_output, universe_id=active_universe
        )
    if site_output is not None:
        result["site"] = build_static_site(
            database,
            site_output,
            source_geojson=source_geojson,
            universe_id=active_universe,
        )
    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Reconstrói uma base analítica canônica por universo municipal."
    )
    parser.add_argument("workbook", type=Path)
    parser.add_argument(
        "--database",
        type=Path,
        default=Path("data/financas_municipais_sp.sqlite"),
    )
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--static-output", type=Path)
    parser.add_argument("--site-output", type=Path)
    parser.add_argument("--geojson", type=Path)
    parser.add_argument("--universe")
    parser.add_argument("--mapping", type=Path)
    args = parser.parse_args()

    result = build_analytical_database(
        args.workbook,
        args.database,
        overwrite=args.overwrite,
        static_output=args.static_output,
        site_output=args.site_output,
        source_geojson=args.geojson,
        universe_id=args.universe,
        mapping_path=args.mapping,
    )
    for stage, values in result.items():
        print(f"[{stage}]")
        for key, value in values.items():
            print(f"{key}={value}")


if __name__ == "__main__":
    main()
