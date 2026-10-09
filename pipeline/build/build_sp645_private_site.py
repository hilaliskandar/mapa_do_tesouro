from __future__ import annotations

import argparse
import json
from pathlib import Path

from pipeline.build.build_static_site import build_static_site
from pipeline.build.load_documentation import load_documentation
from pipeline.ingest.import_multifuentes import import_multifuentes
from pipeline.transform.calculate_annual import calculate_annual
from pipeline.transform.calculate_markers import calculate_markers
from pipeline.transform.calculate_pairs import calculate_pairs
from pipeline.transform.calculate_typologies import calculate_typologies
from pipeline.transform.calculate_window_statistics import calculate_window_statistics


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

    result["annual_2025"] = calculate_annual(database, years={2025})
    result["window"] = calculate_window_statistics(database, universe_id="SP_645")
    result["typologies"] = calculate_typologies(database, universe_id="SP_645")
    result["markers"] = calculate_markers(database, universe_id="SP_645")
    result["pairs"] = calculate_pairs(database, universe_id="SP_645")
    result["site"] = build_static_site(
        database,
        site_output,
        universe_id="SP_645",
        source_geojson=geojson,
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
