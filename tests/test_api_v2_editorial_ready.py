from pathlib import Path
import json
import tempfile
import unittest
from editorial.audit_v2_editorial_ready import audit


class ReadinessTests(unittest.TestCase):
    def test_missing_files_block(self):
        with tempfile.TemporaryDirectory() as d:
            result = audit(Path(d))
            self.assertEqual(result["status"], "blocked")
            self.assertIn("manifest.json", result["missing"])

    def test_uncertified_percentage_cannot_promote(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / "data" / "api" / "v2"
            (root / "catalog").mkdir(parents=True)
            (root / "qa").mkdir()
            inputs = {
                "manifest.json": {"municipality_count": 645},
                "catalog/variables.json": {"variables": [
                    {"variable_id": "test_ratio", "unidade": "percentual",
                     "scale_verified": False, "cautelas": ""},
                    {"variable_id": "test_money", "unidade": "BRL",
                     "cautelas": "Careful comparison"},
                ]},
                "catalog/universes.json": [],
                "qa/readiness.json": {"publication_qa": "not_evaluated"},
            }
            for path, payload in inputs.items():
                (root / path).write_text(json.dumps(payload), encoding="utf-8")
            result = audit(Path(d))
            self.assertEqual(result["status"], "candidate_only")
            self.assertIn("test_ratio", result["checks"]["uncertified_percentages"])
            self.assertFalse(result["publication_authorized"])


if __name__ == "__main__":
    unittest.main()
