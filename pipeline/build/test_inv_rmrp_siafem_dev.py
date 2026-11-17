#!/usr/bin/env python3
"""QA de importação SIAFEM em cópia de SQLite estritamente sintética."""
from __future__ import annotations
import csv
from pathlib import Path
import sqlite3
import tempfile
import unittest
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "pipeline" / "build"))
from import_inv_rmrp_siafem_dev import import_dev  # noqa: E402


class SiafemStagingTest(unittest.TestCase):
    def test_copy_and_safeguards(self):
        with tempfile.TemporaryDirectory() as dir_:
            directory = Path(dir_)
            source = directory / "source-synthetic.sqlite"
            target = directory / "target-staging.sqlite"
            roster = ROOT / "governance/INV_RMRP_34_MUNICIPIOS_PILOTO_IBGE_VERIFICADO_2026_11_11.csv"
            with roster.open(encoding="utf-8-sig", newline="") as f:
                municipalities = list(csv.DictReader(f, delimiter=";"))
            with sqlite3.connect(source) as db:
                db.executescript("""
                    PRAGMA foreign_keys=ON;
                    CREATE TABLE municipio(codigo_ibge TEXT PRIMARY KEY);
                    CREATE TABLE fonte(
                        fonte_id TEXT PRIMARY KEY, nome TEXT, orgao TEXT,
                        sistema TEXT, url_publica TEXT
                    );
                    CREATE TABLE artefato_fonte(
                        artefato_id TEXT PRIMARY KEY,
                        fonte_id TEXT REFERENCES fonte(fonte_id),
                        nome TEXT, source_version TEXT, url TEXT,
                        retrieved_at TEXT, sha256 TEXT, mime_type TEXT, observacao TEXT
                    );
                """)
                db.executemany("INSERT INTO municipio(codigo_ibge) VALUES(?)",
                               [(r["codigo_ibge"],) for r in municipalities])
                db.commit()
            meta = import_dev(source, target, ROOT)
            self.assertTrue(meta["source_unchanged"])
            self.assertEqual(meta["instruments"], 752)
            self.assertEqual(meta["instrument_year_rows"], 889)
            self.assertEqual(meta["payments_count"], 1017)
            self.assertEqual(meta["financial_event_rows_added"], 0)
            with sqlite3.connect(source) as src:
                self.assertFalse(src.execute(
                    "SELECT 1 FROM sqlite_master WHERE name='inv_siafem_convenio_ano'"
                ).fetchone())
                self.assertEqual(src.execute(
                    "SELECT COUNT(*) FROM municipio"
                ).fetchone()[0], 34)
            with sqlite3.connect(target) as dst:
                self.assertEqual(dst.execute("PRAGMA integrity_check").fetchone()[0], "ok")
                self.assertFalse(dst.execute("PRAGMA foreign_key_check").fetchall())
                self.assertEqual(dst.execute(
                    "SELECT COUNT(*) FROM inv_evento_financeiro"
                ).fetchone()[0], 0)
                self.assertEqual(dst.execute("""
                    SELECT COUNT(*), SUM(valor_liberado_estornado_centavos),
                      SUM(quantidade_pagamentos)
                    FROM inv_siafem_convenio_ano
                """).fetchone(), (889, 30552102920, 1017))
                self.assertEqual(dst.execute(
                    "SELECT COUNT(*) FROM inv_instrumento"
                ).fetchone()[0], 752)
            with self.assertRaises(ValueError):
                import_dev(source, target, ROOT)
            self.assertTrue(target.exists())


if __name__ == "__main__":
    unittest.main()
