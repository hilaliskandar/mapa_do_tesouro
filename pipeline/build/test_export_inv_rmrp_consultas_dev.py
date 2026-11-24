#!/usr/bin/env python3
"""QA da exportação INV-RMRP em SQLite sintético isolado, sem rede."""
import csv
import importlib.util
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


def load(name):
    spec = importlib.util.spec_from_file_location(name, HERE / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ingest = load("import_inv_rmrp_obrasgov_dev")
export = load("export_inv_rmrp_consultas_dev")
ROSTER = ROOT / "governance/INV_RMRP_34_MUNICIPIOS_PILOTO_IBGE_VERIFICADO_2026_11_11.csv"
CANDIDATES = ROOT / "app/static/data/api/v3/investimentos/rmrp/obrasgov-triagem-espacial.json"
SCHEMA = ROOT / "governance/proposals/INV_RMRP_SCHEMA_EXTENSAO_SQLITE_2026_11_11.sql"


def create_base(path):
    with sqlite3.connect(path) as c:
        for p in ["data/schema/001_initial.sql", "data/schema/004_provenance.sql"]:
            c.executescript((ROOT / p).read_text(encoding="utf-8"))
        with ROSTER.open(encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f, delimiter=";"):
                c.execute("INSERT INTO municipio(codigo_ibge,nome,uf) VALUES(?,?,?)",
                          (row["codigo_ibge"], row["municipio"], "SP"))
        c.commit()


class ExportDevTest(unittest.TestCase):
    def test_full_isolated_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            original = root / "canonical-synthetic.sqlite"
            stage = root / "candidate.sqlite"
            out = root / "json-v3"
            create_base(original)
            ingest.import_to_dev(original, stage, ROSTER, CANDIDATES, SCHEMA)
            result = export.build(stage, ROSTER, out)
            self.assertEqual(result["municípios"], 34)
            self.assertEqual(result["projetos_candidatos"], 224)
            self.assertEqual(result["relacoes_municipais"], 132)
            self.assertEqual(result["consultas_individuais"], 34)
            self.assertEqual(result["eventos_pagos_homologados"], 0)
            self.assertEqual(result["eventos_candidatos"], 226)
            self.assertEqual(len(list((out / "municipios").glob("*.json"))), 34)
            self.assertEqual(len(list((out / "projetos").glob("*.json"))), 224)
            self.assertEqual(len(result["arquivos_sha256"]), 259)
            for path in (out / "municipios").glob("*.json"):
                data = json.loads(path.read_text(encoding="utf-8"))
                self.assertIsNone(data["metricas_candidatas"]["investimento_publico_executado_centavos"])
                self.assertIsNone(data["metricas_candidatas"]["transferencias_federais_pagas_centavos"])
                self.assertEqual(data["qa_status"], "consulta_exploratoria_nao_homologada")
            self.assertEqual(json.loads((out / "manifest.json").read_text())["schema"],
                             "inv-rmrp-sqlite-preview-v1")
            with self.assertRaises(ValueError):
                export.build(stage, ROSTER, out)
            with sqlite3.connect(original) as c:
                self.assertIsNone(c.execute(
                    "SELECT 1 FROM sqlite_master WHERE name='inv_projeto'").fetchone())

    def test_reject_unapproved_paid_event(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            original = root / "canonical.sqlite"
            stage = root / "stage.sqlite"
            create_base(original)
            ingest.import_to_dev(original, stage, ROSTER, CANDIDATES, SCHEMA)
            with sqlite3.connect(stage) as c:
                c.execute("UPDATE inv_evento_financeiro SET estagio='pago' WHERE evento_id=("
                          "SELECT evento_id FROM inv_evento_financeiro LIMIT 1)")
            with self.assertRaises(RuntimeError):
                export.build(stage, ROSTER, root / "publish")
            self.assertFalse((root / "publish").exists())


if __name__ == "__main__":
    unittest.main()
