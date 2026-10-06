from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path


def normalize_code(value) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    if text.endswith(".0"):
        text = text[:-2]
    digits = "".join(ch for ch in text if ch.isdigit())
    if len(digits) == 7:
        return digits
    return None


def feature_code(feature: dict, code_field: str = "id") -> str | None:
    if code_field in feature:
        code = normalize_code(feature.get(code_field))
        if code:
            return code
    properties = feature.get("properties") or {}
    return normalize_code(properties.get(code_field))


def export_universe_geojson(
    database: Path,
    source_geojson: Path,
    output_geojson: Path,
    *,
    universe_id: str = "TIC_TIM_30",
    code_field: str = "id",
) -> dict:
    con = sqlite3.connect(database)
    try:
        codes = {
            row[0]
            for row in con.execute(
                """
                SELECT codigo_ibge
                FROM universo_municipio
                WHERE universo_id=?
                """,
                (universe_id,),
            )
        }
    finally:
        con.close()

    payload = json.loads(source_geojson.read_text(encoding="utf-8"))
    selected = []
    missing = set(codes)

    for feature in payload.get("features", []):
        code = feature_code(feature, code_field)
        if code not in codes:
            continue
        feature = dict(feature)
        feature["id"] = code
        props = dict(feature.get("properties") or {})
        props["codigo_ibge"] = code
        feature["properties"] = props
        selected.append(feature)
        missing.discard(code)

    if missing:
        raise ValueError(
            "Municípios sem geometria no GeoJSON: " + ", ".join(sorted(missing))
        )

    output_geojson.parent.mkdir(parents=True, exist_ok=True)
    output_geojson.write_text(
        json.dumps(
            {
                "type": "FeatureCollection",
                "features": selected,
                "metadata": {
                    "universe_id": universe_id,
                    "source": source_geojson.name,
                    "code_field": code_field,
                },
            },
            ensure_ascii=False,
            separators=(",", ":"),
        ),
        encoding="utf-8",
    )

    return {
        "universe_id": universe_id,
        "municipalities": len(codes),
        "features": len(selected),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Filtra a cartografia municipal para o universo ativo."
    )
    parser.add_argument("database", type=Path)
    parser.add_argument("source_geojson", type=Path)
    parser.add_argument("output_geojson", type=Path)
    parser.add_argument("--universe", default="TIC_TIM_30")
    parser.add_argument("--code-field", default="id")
    args = parser.parse_args()
    result = export_universe_geojson(
        args.database,
        args.source_geojson,
        args.output_geojson,
        universe_id=args.universe,
        code_field=args.code_field,
    )
    for key, value in result.items():
        print(f"{key}={value}")


if __name__ == "__main__":
    main()
