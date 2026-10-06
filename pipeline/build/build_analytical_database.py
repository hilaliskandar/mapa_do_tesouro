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


def build_analytical_database(
    workbook: Path,
    database: Path,
    *,
    overwrite: bool = False,
    static_output: Path | None = None,
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
    )
    load_documentation(database, strict=True)
    result["annual"] = calculate_annual(database)
    result["window"] = calculate_window_statistics(database)
    result["typologies"] = calculate_typologies(database)
    result["markers"] = calculate_markers(database)
    result["pairs"] = calculate_pairs(database)
    if static_output is not None:
        result["static"] = export_static_data(database, static_output)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Reconstrói a base analítica canônica dos 30 municípios."
    )
    parser.add_argument("workbook", type=Path)
    parser.add_argument(
        "--database",
        type=Path,
        default=Path("data/financas_municipais_sp.sqlite"),
    )
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--static-output", type=Path)
    args = parser.parse_args()

    result = build_analytical_database(
        args.workbook,
        args.database,
        overwrite=args.overwrite,
        static_output=args.static_output,
    )
    for stage, values in result.items():
        print(f"[{stage}]")
        for key, value in values.items():
            print(f"{key}={value}")


if __name__ == "__main__":
    main()
