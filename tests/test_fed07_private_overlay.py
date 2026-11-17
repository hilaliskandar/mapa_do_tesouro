import os
import tempfile
import unittest
from pathlib import Path
from deployment.materialize_rmrp_fed07_private import materialize

class TestFed07Preview(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.site = Path(self.tmp.name) / "private_preview"
        self.site.mkdir()
        (self.site / "index.html").write_text("<!doctype html>")
        self.repo = Path(__file__).resolve().parents[1]
        source = os.getenv("RMRP_FED07_SOURCE_ZIP")
        self.zip_path = Path(source) if source else None

    def tearDown(self):
        self.tmp.cleanup()

    def require_private_artifact(self):
        if not self.zip_path or not self.zip_path.is_file():
            self.skipTest("RMRP_FED07_SOURCE_ZIP not available in runner")

    def test_no_marker(self):
        with self.assertRaisesRegex(RuntimeError, "Private preview marker"):
            materialize(self.site, self.zip_path or Path("unavailable"), self.repo)

    def test_private_overlay(self):
        self.require_private_artifact()
        (self.site / ".rmrp-fed07-private-preview").write_text("private")
        report = materialize(self.site, self.zip_path, self.repo)
        self.assertFalse(report["publication_authorized"])
        self.assertEqual(report["json_count"], 279)
        self.assertEqual(report["qa"]["municipios"], 34)
        self.assertEqual(report["qa"]["projetos"], 218)
        self.assertGreaterEqual(report["qa"]["technical_checks_passed"], 1603)

    def test_preserves_other_rmrp_previews(self):
        self.require_private_artifact()
        preexisting = self.site / "data/api/v3/investimentos/rmrp/preview-amostras.json"
        preexisting.parent.mkdir(parents=True, exist_ok=True)
        preexisting.write_text('{"source":"other-preview"}', encoding="utf-8")
        (self.site / ".rmrp-fed07-private-preview").write_text("private")
        result = materialize(self.site, self.zip_path, self.repo)
        self.assertEqual(result["json_count"], 279)
        self.assertEqual(preexisting.read_text(), '{"source":"other-preview"}')

    def test_no_overwrite(self):
        self.require_private_artifact()
        (self.site / ".rmrp-fed07-private-preview").write_text("private")
        materialize(self.site, self.zip_path, self.repo)
        with self.assertRaisesRegex(RuntimeError, "Destination contains FED07 file"):
            materialize(self.site, self.zip_path, self.repo)
if __name__ == "__main__":
    unittest.main()
