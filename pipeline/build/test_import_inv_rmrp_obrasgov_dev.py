#!/usr/bin/env python3
"""QA offline de ingestão INV Obrasgov usando fonte SQLite sintética baseada no esquema real."""
import csv
import importlib.util
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
SRC = Path(__file__).with_name("import_inv_rmrp_obrasgov_dev.py")
spec = importlib.util.spec_from_file_location("rmrp_inv_dev", SRC)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
ROSTER = ROOT / "governance/INV_RMRP_34_MUNICIPIOS_PILOTO_IBGE_VERIFICADO_2026_11_11.csv"
CANDIDATES = ROOT / "app/static/data/api/v3/investimentos/rmrp/obrasgov-triagem-espacial.json"
SCHEMA = ROOT / "governance/proposals/INV_RMRP_SCHEMA_EXTENSAO_SQLITE_2026_11_11.sql"


def create_base(path):
    with sqlite3.connect(path) as conn:
        for p in ("data/schema/001_initial.sql", "data/schema/004_provenance.sql"):
            conn.executescript((ROOT / p).read_text(encoding="utf-8"))
        with ROSTER.open(encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f, delimiter=";"))
        for r in rows:
            conn.execute("INSERT INTO municipio(codigo_ibge,nome,uf) VALUES(?,?,?)",
                         (r["codigo_ibge"], r["municipio"], "SP"))
        conn.commit()


class ImportDevTest(unittest.TestCase):
    def test_cents_decimal(self):
        self.assertEqual(mod.centavos(0.01), 1)
        self.assertEqual(mod.centavos("100.335"), 10034)
        self.assertIsNone(mod.centavos(None))
        self.assertIsNone(mod.centavos("n.d."))

    def test_copy_preserves_source_and_loads_only_candidates(self):
        with tempfile.TemporaryDirectory() as d:
            base = Path(d) / "canonical-test.sqlite"
            output = Path(d) / "rmrp-dev.sqlite"
            create_base(base)
            stats = mod.import_to_dev(base, output, ROSTER, CANDIDATES, SCHEMA)
            self.assertEqual(stats["counts"]["municipalities_validated"], 34)
            self.assertEqual(stats["counts"]["project_candidates"], 224)
            self.assertEqual(stats["counts"]["approved_projects"], 0)
            self.assertEqual(stats["counts"]["paid_events"], 0)
            self.assertGreaterEqual(stats["counts"]["municipality_links"], 131)
            self.assertTrue(output.with_suffix(".qa.json").exists())
            with sqlite3.connect(output) as conn:
                self.assertEqual(conn.execute("PRAGMA integrity_check").fetchone()[0], "ok")
                self.assertEqual(conn.execute("PRAGMA foreign_key_check").fetchall(), [])
                self.assertEqual(conn.execute("SELECT COUNT(*) FROM inv_projeto").fetchone()[0], 224)
                self.assertEqual(conn.execute(
                    "SELECT COUNT(*) FROM inv_evento_financeiro WHERE estagio!='previsto'"
                ).fetchone()[0], 0)
                query = conn.execute(
                    "SELECT COUNT(*) FROM inv_projeto_municipio WHERE codigo_ibge='3543402'"
                ).fetchone()[0]
                self.assertGreater(query, 0)
            with sqlite3.connect(base) as conn:
                self.assertIsNone(conn.execute(
                    "SELECT name FROM sqlite_master WHERE name='inv_projeto'"
                ).fetchone())
            with self.assertRaises(ValueError):
                mod.import_to_dev(base, output, ROSTER, CANDIDATES, SCHEMA)

    def test_reject_wrong_ibge_set(self):
        with tempfile.TemporaryDirectory() as d:
            base = Path(d) / "canonical-test.sqlite"
            output = Path(d) / "rmrp-dev.sqlite"
            create_base(base)
            with sqlite3.connect(base) as conn:
                conn.execute("DELETE FROM municipio WHERE codigo_ibge='3543402'")
            with self.assertRaises(RuntimeError):
                mod.import_to_dev(base, output, ROSTER, CANDIDATES, SCHEMA)
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
