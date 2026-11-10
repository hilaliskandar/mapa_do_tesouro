"""FED04: regression for non-public candidate catalog variables.

Runs only against a disposable SQLite database; no production writes.
"""
from __future__ import annotations

import sqlite3
import tempfile
import unittest
from pathlib import Path

import yaml

from pipeline.build.load_catalog import load_catalog


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "data" / "schema" / "001_initial.sql"


class CatalogVisibilityTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.db = Path(self.tmp.name) / "qa.sqlite"
        self.catalog = Path(self.tmp.name) / "catalog.yml"
        with sqlite3.connect(self.db) as con:
            con.executescript(SCHEMA.read_text(encoding="utf-8"))

    def _load(self, **kwargs):
        name = kwargs.pop("nome", "ITR teste")
        item = {
            "variavel_id": "dca_itr_cota_parte_bruta",
            "nome": name,
            "grupo": "transferencias",
            "tipo": "conta_oficial",
            "unidade": "BRL",
            "fonte_preferencial_id": "SICONFI_DCA",
            "definicao": "QA de categoria anual, sem publicacao",
            **kwargs,
        }
        payload = {"fontes": [
            {"fonte_id": "SICONFI_DCA", "nome": "SICONFI DCA", "orgao": "STN"}
        ], "variaveis": [item]}
        self.catalog.write_text(yaml.safe_dump(payload, allow_unicode=True), encoding="utf-8")
        load_catalog(self.db, [self.catalog])

    def _flags(self):
        with sqlite3.connect(self.db) as con:
            return con.execute(
                "SELECT publicavel, ativo, nome FROM variavel "
                "WHERE variavel_id='dca_itr_cota_parte_bruta'"
            ).fetchone()

    def test_explicit_zero_flags_prevent_automatic_publication(self):
        self._load(publicavel=0, ativo=0)
        self.assertEqual(self._flags()[:2], (0, 0))
        with sqlite3.connect(self.db) as con:
            visible = con.execute(
                "SELECT COUNT(*) FROM v_observacao_publicavel "
                "WHERE variavel_id='dca_itr_cota_parte_bruta'"
            ).fetchone()[0]
        self.assertEqual(visible, 0)

    def test_omitted_flags_keep_backward_compatible_defaults(self):
        self._load()
        self.assertEqual(self._flags()[:2], (1, 1))

    def test_omitted_flags_do_not_reenable_blocked_existing_variable(self):
        self._load(publicavel=0, ativo=0)
        self._load(nome="Atualizacao documental")
        self.assertEqual(self._flags(), (0, 0, "Atualizacao documental"))

    def test_explicit_flag_updates_only_the_target_status(self):
        self._load(publicavel=0, ativo=0)
        self._load(publicavel=1)
        self.assertEqual(self._flags()[:2], (1, 0))

    def test_invalid_flag_type_is_rejected(self):
        with self.assertRaises(ValueError):
            self._load(publicavel="false", ativo=0)

    def test_repeated_load_is_idempotent(self):
        self._load(publicavel=0, ativo=0)
        self._load(publicavel=0, ativo=0)
        with sqlite3.connect(self.db) as con:
            count = con.execute(
                "SELECT COUNT(*) FROM variavel "
                "WHERE variavel_id='dca_itr_cota_parte_bruta'"
            ).fetchone()[0]
        self.assertEqual(count, 1)
        self.assertEqual(self._flags()[:2], (0, 0))


if __name__ == "__main__":
    unittest.main()
