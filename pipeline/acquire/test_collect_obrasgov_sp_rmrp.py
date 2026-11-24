#!/usr/bin/env python3
"""Testes offline do coletor Obrasgov; não acessa API ou bases produtivas."""
import gzip
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

MODULE_PATH = Path(__file__).with_name("collect_obrasgov_sp_rmrp.py")
SPEC = importlib.util.spec_from_file_location("obrasgov_collector", MODULE_PATH)
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)


def response(page, id_, total=2, pages=2):
    return {
        "data": [{
            "id_projeto_investimento": id_,
            "desc_nome": f"Projeto {id_}",
            "uf_principal": "SP",
            "situacao": "Cadastrada",
            "pins": [{"latitude": "-21.1", "longitude": "-47.9"}],
            "investimentos_previstos": [
                {"vl_investimento_previsto": 900, "desc_nome_fonte_recurso": "Federal"}
            ],
        }],
        "total_items": total,
        "total_pages": pages,
        "page_number": page,
        "page_size": 200,
    }


class TestObrasgov(unittest.TestCase):
    def test_check_missing_page(self):
        rows = {1: {"rows": 1, "total_items": 2, "total_pages": 2}}
        r = mod.check(rows)
        self.assertFalse(r["complete"])
        self.assertEqual(r["missing_pages"], [2])

    def test_check_inconsistent_source_count(self):
        rows = {
            1: {"rows": 1, "total_items": 2, "total_pages": 2},
            2: {"rows": 1, "total_items": 3, "total_pages": 2},
        }
        self.assertFalse(mod.check(rows)["complete"])

    def test_resume_and_mark_not_full_on_smoke(self):
        seen = []

        def fake_request(page):
            seen.append(page)
            payload = json.dumps(response(page, "p"+str(page))).encode()
            return "https://api.oficial/obras", payload, response(page, "p"+str(page))

        with tempfile.TemporaryDirectory() as folder, patch.object(mod, "request_page", fake_request):
            root = Path(folder)
            status = mod.run(root, max_pages=1, pause=0)
            self.assertEqual(status, 0)
            report = json.loads((root / "manifest.json").read_text())
            self.assertEqual(report["qa"]["status"], "incompleto")
            self.assertEqual(len(report["pages"]), 1)
            self.assertEqual(seen, [1])
            status = mod.run(root, max_pages=0, pause=0)
            self.assertEqual(status, 0)
            self.assertEqual(seen, [1, 2])
            report = json.loads((root / "manifest.json").read_text())
            self.assertTrue(report["qa"]["complete"])
            self.assertEqual(report["qa"]["unique_project_ids"], 2)
            self.assertEqual(report["qa"]["retrieved_rows"], 2)
            self.assertEqual(len(mod.inspect(root)), 2)
            pages = sorted((root / "pages").glob("*.gz"))
            self.assertEqual(len(pages), 2)
            self.assertEqual(len(json.loads(gzip.decompress(
                (root / "index.json.gz").read_bytes()
            ))), 2)

    def test_duplicate_ids_block_homologation(self):
        def fake_request(page):
            payload = json.dumps(response(page, "same")).encode()
            return "https://api.oficial/obras", payload, response(page, "same")

        with tempfile.TemporaryDirectory() as folder, patch.object(mod, "request_page", fake_request):
            status = mod.run(Path(folder), max_pages=0, pause=0)
            self.assertEqual(status, 2)
            qa = json.loads((Path(folder) / "manifest.json").read_text())["qa"]
            self.assertFalse(qa["complete"])
            self.assertEqual(qa["duplicate_project_ids"], ["same"])

    def test_inconsistent_pagination_prevents_snapshot(self):
        def fake_request(page):
            altered = response(page, "p"+str(page), total=2 if page == 1 else 3)
            return "https://api.oficial/obras", json.dumps(altered).encode(), altered

        with tempfile.TemporaryDirectory() as folder, patch.object(mod, "request_page", fake_request):
            status = mod.run(Path(folder), max_pages=0, pause=0)
            self.assertEqual(status, 2)
            qa = json.loads((Path(folder) / "manifest.json").read_text())["qa"]
            self.assertFalse(qa["complete"])
            self.assertTrue(qa["errors"])

    def test_missing_id_fails_index(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            data = response(1, "dummy", total=1, pages=1)
            del data["data"][0]["id_projeto_investimento"]
            path = root / "pages" / "page-00001.json.gz"
            mod.put_atomic(path, gzip.compress(json.dumps(data).encode(), mtime=0))
            with self.assertRaises(ValueError):
                mod.extract_index(root, mod.inspect(root))


if __name__ == "__main__":
    unittest.main()
