#!/usr/bin/env python3
"""Testes offline da aquisição Transferegov; sem requisições reais."""
import contextlib
import csv
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit

SRC = Path(__file__).with_name("collect_investimentos_rmrp.py")
spec = importlib.util.spec_from_file_location("transferegov_acquire", SRC)
collector = importlib.util.module_from_spec(spec)
spec.loader.exec_module(collector)


def create_roster(path):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["codigo_ibge", "municipio"], delimiter=";")
        writer.writeheader()
        for k in range(34):
            writer.writerow({"codigo_ibge": str(3500000 + k), "municipio": f"Cidade {k}"})


class TransferegovAcquisitionTest(unittest.TestCase):
    def test_rmrp_roster_enforced(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "roster.csv"
            f.write_text("codigo_ibge;municipio\n3500000;Incompleta\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                collector.roster_read(f)

    def test_pagination_checkpoint_resume(self):
        calls = []

        def fake_fetch(url):
            q = parse_qs(urlsplit(url).query)
            page = int(q["pagina"][0])
            code = q.get("cd_ibge_recebedor", q.get("cod_munic_ibge"))[0]
            key = "cd_ibge_recebedor" if "cd_ibge_recebedor" in q else "cod_munic_ibge"
            calls.append((code, key, page))
            item = {key: int(code), "id_proposta": int(code) * 10 + page}
            j = {"data": [item], "page_number": page, "page_size": 200,
                 "total_items": 2, "total_pages": 2}
            return j, json.dumps(j).encode()

        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            roster = root / "rmrp.csv"
            create_roster(roster)
            with patch.object(collector, "fetch_json", fake_fetch):
                with contextlib.redirect_stdout(io.StringIO()):
                    code = collector.run(roster, root / "snapshot", limit_pages=1, delay=0)
                self.assertEqual(code, 0)
                manifest = json.loads((root / "snapshot" / "manifest.json").read_text())
                self.assertFalse(manifest["snapshot_complete"])
                self.assertEqual(len(manifest["sources"]), 68)
                self.assertEqual(len(calls), 68)

                with contextlib.redirect_stdout(io.StringIO()):
                    code = collector.run(roster, root / "snapshot", limit_pages=0, delay=0)
                self.assertEqual(code, 0)
                manifest = json.loads((root / "snapshot" / "manifest.json").read_text())
                self.assertTrue(manifest["snapshot_complete"])
                self.assertEqual(manifest["qa_status"], "pass")
                self.assertEqual(len(manifest["sources"]), 136)
                self.assertEqual(sum(x["checkpoint_reused"] for x in manifest["sources"]), 68)
                self.assertEqual(len(calls), 136)
                self.assertTrue(all(x["all_pages"] for x in manifest["coverage"]))

    def test_http_error_blocks_even_smoke(self):
        def broken_fetch(url):
            raise RuntimeError("429 repetido")

        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            roster = root / "rmrp.csv"
            create_roster(roster)
            with patch.object(collector, "fetch_json", broken_fetch):
                with contextlib.redirect_stdout(io.StringIO()):
                    code = collector.run(roster, root / "snapshot", limit_pages=1, delay=0)
            self.assertEqual(code, 2)
            manifest = json.loads((root / "snapshot" / "manifest.json").read_text())
            self.assertFalse(manifest["snapshot_complete"])
            self.assertEqual(len(manifest["errors"]), 68)


if __name__ == "__main__":
    unittest.main()
