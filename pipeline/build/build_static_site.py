from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from pipeline.build.export_static_data import export_static_data
from pipeline.build.export_map_geojson import export_universe_geojson

ROOT = Path(__file__).resolve().parents[2]
FRONTEND = ROOT / "app" / "static"


def build_static_site(
    database: Path,
    output: Path,
    *,
    universe_id: str = "TIC_TIM_30",
    source_geojson: Path | None = None,
) -> dict:
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True, exist_ok=True)

    for filename in ("index.html", "styles.css", "app.js"):
        shutil.copy2(FRONTEND / filename, output / filename)

    result = {
        "data": export_static_data(
            database,
            output / "data",
            universe_id=universe_id,
        )
    }

    if source_geojson is not None:
        result["map"] = export_universe_geojson(
            database,
            source_geojson,
            output / "data" / "maps" / "municipalities.geojson",
            universe_id=universe_id,
        )

    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Monta site estático autossuficiente para publicação."
    )
    parser.add_argument("database", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--universe", default="TIC_TIM_30")
    parser.add_argument("--geojson", type=Path)
    args = parser.parse_args()
    result = build_static_site(
        args.database,
        args.output,
        universe_id=args.universe,
        source_geojson=args.geojson,
    )
    print(result)


if __name__ == "__main__":
    main()
