#!/usr/bin/env python3
"""Testes sem rede de cobertura, minimização e QA do coletor de extratos TE."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SRC = Path(__file__).with_name("collect_especiais_movimentacoes_rmrp.py")
spec = importlib.util.spec_from_file_location("te_ledger", SRC)
collector = importlib.util.module_from_spec(spec)
spec.loader.exec_module(collector)


def beneficiaries(path):
    data = {"items": [
        {"codigo_ibge": str(3500000+i), "municipio": f"Cidade {i}",
         "beneficiarios": [{"cnpj": str(10000000000000+i)}]}
        for i in range(34)
    ]}
    path.write_text(json.dumps(data), encoding="utf-8")
    return data


def example(cnpj, page):
    record = {
        "id_lancamento_gestao_financeira": f"synthetic-id-{cnpj[-4:]}-{page}",
        "origem_solicitacao_gestao_financeira": "TE",
        "descricao_gestao_financeira": "APL FUNDO" if page == 2 else "CRED TED",
        "data_lancamento_gestao_financeira": "2025-04-10",
        "tipo_operacao_gestao_financeira": "D" if page == 2 else "C",
        "valor_gestao_financeira": "10.15",
        "codigo_categoria_despesa_lancamento_gestao_financeira": 4,
        "quantidade_subtransacoes_lancamento_gestao_financeira": 0,
        "codigo_conta_gestao_financeira": "TOP_SECRET_ACCOUNT",
        "doc_favorecido_gestao_financeira": "SENSITIVE_PERSON_ID",
        "nome_favorecido_gestao_financeira": "SENSITIVE_NAME",
    }
    return {"data": [record], "page_number": page, "total_items": 2,
            "total_pages": 2}


class LedgerTest(unittest.TestCase):
    def test_centavos_precisao(self):
        self.assertEqual(collector.cents("0.015"), 2)
        self.assertEqual(collector.cents("100.33"), 10033)
        self.assertIsNone(collector.cents("n.d."))

    def test_minimization(self):
        raw = example("12345678901234", 1)["data"][0]
        cleaned = collector.sanitize(raw)
        self.assertEqual(cleaned["valor_centavos"], 1015)
        self.assertNotIn("codigo_conta_gestao_financeira", cleaned)
        self.assertNotIn("doc_favorecido_gestao_financeira", cleaned)
        self.assertNotIn("nome_favorecido_gestao_financeira", cleaned)

    def test_complete_34_and_no_personal_data_in_outputs(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            input_file = root / "beneficiarios.json"
            beneficiaries(input_file)
            output = root / "out"
            with patch.object(collector, "get_page",
                              side_effect=lambda cnpj, page: (b"raw", example(cnpj, page))):
                with contextlib.redirect_stdout(io.StringIO()):
                    status = collector.run(input_file, output, pause=0)
            self.assertEqual(status, 0)
            manifest = json.loads((output / "manifest.json").read_text())
            self.assertTrue(manifest["snapshot_complete"])
            self.assertEqual(manifest["lancamentos"], 68)
            self.assertEqual(manifest["municipios"], 34)
            self.assertEqual(manifest["pages"], 68)
            all_text = "".join(p.read_text() for p in output.rglob("*.json"))
            self.assertNotIn("TOP_SECRET_ACCOUNT", all_text)
            self.assertNotIn("SENSITIVE_PERSON_ID", all_text)
            self.assertNotIn("SENSITIVE_NAME", all_text)
            self.assertNotIn("10000000000000", all_text)

    def test_limit_is_not_full_qa(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            input_file = root / "beneficiarios.json"
            beneficiaries(input_file)
            with patch.object(collector, "get_page",
                              side_effect=lambda cnpj, page: (b"raw", example(cnpj, page))):
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(collector.run(input_file, root / "out", limit=1, pause=0), 0)
            manifest = json.loads((root / "out" / "manifest.json").read_text())
            self.assertFalse(manifest["snapshot_complete"])
            self.assertEqual(manifest["qa_status"], "incomplete")

    def test_cnpj_redacted_from_errors(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            input_file = root / "beneficiarios.json"
            beneficiaries(input_file)
            with patch.object(collector, "get_page",
                              side_effect=lambda cnpj, page: (_ for _ in ()).throw(
                                  RuntimeError("Request to https://host/?cnpj=" + cnpj))):
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(collector.run(input_file, root / "out", limit=1, pause=0), 2)
            manifest = (root / "out" / "manifest.json").read_text()
            self.assertNotIn("10000000000000", manifest)
            self.assertIn("[CNPJ_SUPRIMIDO]", manifest)


if __name__ == "__main__":
    unittest.main()
