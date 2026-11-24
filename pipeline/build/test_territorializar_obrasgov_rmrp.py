#!/usr/bin/env python3
"""QA offline da atribuição de pontos a malhas RMRP sem simplificação."""
import gzip
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SRC = Path(__file__).with_name("territorializar_obrasgov_rmrp.py")
spec = importlib.util.spec_from_file_location("territorializar", SRC)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def square(x, y, dx=0.8):
    return [[x, y], [x+dx, y], [x+dx, y+dx], [x, y+dx], [x, y]]


def polygons():
    out = []
    for i in range(34):
        geo = {"type": "Polygon", "coordinates": [square(i*2, 0)]}
        out.append({"type": "Feature", "properties": {"codarea": str(3500000+i),
                   "name": f"Cidade {i}"}, "geometry": geo})
    out[0]["geometry"]["coordinates"].append(square(0.2, 0.2, 0.3))
    out[1]["geometry"] = {"type": "MultiPolygon",
                            "coordinates": [[square(2, 0)], [square(2, 2)]]}
    return {"type": "FeatureCollection", "features": out}


class TerritorializacaoTest(unittest.TestCase):
    def setUp(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "m.geojson"
            p.write_text(json.dumps(polygons()))
            self.polys = mod.load_polygons(p)

    def test_boundary(self):
        r = mod.candidate_record({"id_projeto_investimento": "i1",
                   "pins": [{"lat": 0, "lon": 0}]}, self.polys)
        self.assertEqual(r["status_territorial"], "FRONTEIRA_REVISAR")

    def test_hole(self):
        r = mod.candidate_record({"id_projeto_investimento": "i2",
                    "pins": [{"lat": 0.3, "lon": 0.3}]}, self.polys)
        self.assertEqual(r["status_territorial"], "PONTOS_FORA_DA_RMRP")

    def test_multipolygon(self):
        r = mod.candidate_record({"id_projeto_investimento": "i3",
                    "pins": [{"lat": 2.3, "lon": 2.3}]}, self.polys)
        self.assertEqual(r["municipios_ibge_intersecao"], ["3500001"])

    def test_multiple_municipalities(self):
        r = mod.candidate_record({"id_projeto_investimento": "i4",
                   "pins": [{"lat": 0.6, "lon": 0.6},
                            {"lat": 0.6, "lon": 2.5}]}, self.polys)
        self.assertEqual(r["status_territorial"], "VARIOS_MUNICIPIOS")

    def test_invalid_point_not_zero(self):
        r = mod.candidate_record({"id_projeto_investimento": "i5",
                  "pins": [{"lat": None, "lon": "x"}]}, self.polys)
        self.assertEqual(r["status_territorial"], "SEM_COORDENADAS_VALIDAS")

    def test_json_csv_materialization(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            geom = root / "polygons.geojson"
            geom.write_text(json.dumps(polygons()), encoding="utf-8")
            items = [
                {"id_projeto_investimento": "p1", "desc_nome": "Obra A",
                 "pins": [{"lat": -0.3, "lon": -0.3}]},
                {"id_projeto_investimento": "p2", "desc_nome": "Obra B",
                 "pins": [{"lat": 0.6, "lon": 2.6}]},
                {"id_projeto_investimento": "p3", "desc_nome": "Obra C", "pins": []},
            ]
            index = root / "index.json.gz"
            index.write_bytes(gzip.compress(json.dumps(items).encode(), mtime=0))
            result = root / "out" / "qa.json"
            self.assertEqual(mod.execute(index, geom, result), 0)
            self.assertTrue(result.with_suffix(".csv").exists())
            obj = json.loads(result.read_text())
            self.assertEqual(len(obj["items"]), 3)
            self.assertEqual(obj["items"][0]["status_territorial"], "PONTOS_FORA_DA_RMRP")
            self.assertEqual(obj["items"][1]["status_territorial"], "INTERSECAO_UNICA_CANDIDATA")
            self.assertEqual(obj["items"][2]["status_territorial"], "SEM_COORDENADAS_VALIDAS")


if __name__ == "__main__":
    unittest.main()
