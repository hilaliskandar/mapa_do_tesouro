#!/usr/bin/env python3
"""Territorialização reproduzível de pontos Obrasgov contra malhas IBGE da RMRP.

Entrada preferencial: index.json.gz gerado por collect_obrasgov_sp_rmrp.py.
Aceita também GeoJSON de polígonos Polygon/MultiPolygon com buracos.
Sem imputação de município por nome e sem rateio monetário por múltiplos municípios.
"""
from __future__ import annotations

import argparse
import csv
import gzip
import json
import math
from pathlib import Path


def point_on_segment(x, y, ax, ay, bx, by, epsilon=1e-10):
    cross = (x - ax) * (by - ay) - (y - ay) * (bx - ax)
    scale = max(abs(bx - ax), abs(by - ay), 1)
    if abs(cross) > epsilon * scale:
        return False
    return min(ax, bx) - epsilon <= x <= max(ax, bx) + epsilon and (
        min(ay, by) - epsilon <= y <= max(ay, by) + epsilon
    )


def ring_contains(ring, x, y):
    """Retorna (interior, na_fronteira); preserva a estrutura original do polígono."""
    inside = False
    n = len(ring)
    for i in range(n):
        a = ring[i]
        b = ring[(i + 1) % n]
        ax, ay, bx, by = a[0], a[1], b[0], b[1]
        if point_on_segment(x, y, ax, ay, bx, by):
            return True, True
        if (ay > y) != (by > y) and x < (bx - ax) * (y - ay) / (by - ay) + ax:
            inside = not inside
    return inside, False


def polygon_contains(polygon, x, y):
    exterior, border = ring_contains(polygon[0], x, y)
    if not exterior:
        return False, border
    for hole in polygon[1:]:
        in_hole, at_hole = ring_contains(hole, x, y)
        if in_hole:
            return at_hole, at_hole
    return True, border


def geometry_contains(geometry, x, y):
    if geometry["type"] == "Polygon":
        return polygon_contains(geometry["coordinates"], x, y)
    if geometry["type"] == "MultiPolygon":
        hits = [polygon_contains(polygon, x, y) for polygon in geometry["coordinates"]]
        return any(h[0] for h in hits), any(h[1] for h in hits)
    raise ValueError(f"Geometria não admitida: {geometry['type']}")


def bbox(geometry):
    polygons = [geometry["coordinates"]] if geometry["type"] == "Polygon" else geometry["coordinates"]
    vertices = [xy for polygon in polygons for ring in polygon for xy in ring]
    return min(v[0] for v in vertices), min(v[1] for v in vertices), max(v[0] for v in vertices), max(v[1] for v in vertices)


def load_polygons(path):
    data = json.loads(path.read_text(encoding="utf-8"))
    features = data["features"]
    codes = []
    polys = []
    for f in features:
        code = str(f["properties"]["codarea"])
        codes.append(code)
        polys.append({
            "codigo_ibge": code,
            "nome": f["properties"].get("name") or f["properties"].get("nome"),
            "sub_regiao": f["properties"].get("subregion"),
            "geometry": f["geometry"],
            "bbox": bbox(f["geometry"]),
        })
    if len(features) != 34 or len(set(codes)) != 34:
        raise ValueError("Malhas: esperados 34 códigos IBGE7 únicos da RMRP")
    return polys


def parse_point(pin):
    lat = pin.get("lat", pin.get("latitude"))
    lon = pin.get("lon", pin.get("longitude"))
    try:
        lat = float(lat)
        lon = float(lon)
    except (TypeError, ValueError):
        return None
    if not (math.isfinite(lat) and math.isfinite(lon) and -90 <= lat <= 90 and -180 <= lon <= 180):
        return None
    return lon, lat


def candidate_record(item, polygons):
    points = [p for p in (parse_point(q) for q in (item.get("pins") or [])) if p]
    matched = set()
    at_border = False
    for x, y in points:
        for f in polygons:
            a, b, c, d = f["bbox"]
            if not (a <= x <= c and b <= y <= d):
                continue
            inside, border = geometry_contains(f["geometry"], x, y)
            if inside:
                matched.add(f["codigo_ibge"])
            if border:
                at_border = True
    ids = sorted(matched)
    if not points:
        status = "SEM_COORDENADAS_VALIDAS"
    elif not ids:
        status = "PONTOS_FORA_DA_RMRP"
    elif len(ids) > 1:
        status = "VARIOS_MUNICIPIOS"
    elif at_border:
        status = "FRONTEIRA_REVISAR"
    else:
        status = "INTERSECAO_UNICA_CANDIDATA"
    return {
        "id_projeto_investimento": str(item.get("id_projeto_investimento") or ""),
        "titulo": item.get("desc_nome"),
        "situacao": item.get("situacao"),
        "pontos_validos": len(points),
        "municipios_ibge_intersecao": ids,
        "status_territorial": status,
        "em_fronteira": at_border,
        "qa_status": "candidato_sem_validacao_documental",
        "origem_pagina": item.get("raw_page"),
    }


def load_index(path):
    if path.suffix == ".gz":
        data = json.loads(gzip.decompress(path.read_bytes()))
    else:
        data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and "items" in data:
        return data["items"]
    raise ValueError("Formato de índice Obrasgov não reconhecido")


def execute(input_path, polygons_path, output):
    polygons = load_polygons(polygons_path)
    items = load_index(input_path)
    results = [candidate_record(x, polygons) for x in items]
    ids = [x["id_projeto_investimento"] for x in results]
    if any(not x for x in ids) or len(ids) != len(set(ids)):
        raise ValueError("Projetos com ID ausente ou duplicado")
    counts = {}
    for r in results:
        counts[r["status_territorial"]] = counts.get(r["status_territorial"], 0) + 1
    out = {
        "metadata": {
            "qa": "triagem_geografica_sem_homologacao",
            "universe": "RMRP_34",
            "source_index": str(input_path),
            "source_polygons": str(polygons_path),
            "crs_input": "EPSG:4326",
            "note": "Qualidade maxima API IBGE pode conter generalizacao; coordenada de obra pode ser administrativa",
            "money_policy": "nenhuma soma ou distribuicao monetaria efetuada",
            "counts": counts,
        },
        "items": results,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    csv_path = output.with_suffix(".csv")
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, delimiter=";", fieldnames=[
            "id_projeto_investimento", "titulo", "situacao", "pontos_validos",
            "municipios_ibge_intersecao", "status_territorial",
            "em_fronteira", "qa_status", "origem_pagina",
        ])
        writer.writeheader()
        for row in results:
            writer.writerow({**row, "municipios_ibge_intersecao": "|".join(row["municipios_ibge_intersecao"])})
    print(json.dumps({"items": len(results), "counts": counts, "json": str(output),
                      "csv": str(csv_path)}, ensure_ascii=False))
    return 0


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--index", required=True, type=Path)
    p.add_argument("--polygons", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    a = p.parse_args()
    raise SystemExit(execute(a.index, a.polygons, a.output))


if __name__ == "__main__":
    main()
