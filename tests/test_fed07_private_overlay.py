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
        self.zip_path = Path("/home/user/RMRP_FED07_PREVIA_API_V3_PRIVADA_2026-11-16.zip")
        self.repo = Path("/home/user/mapa_do_tesouro_fed07")
    def tearDown(self):
        self.tmp.cleanup()
    def test_no_marker(self):
        with self.assertRaisesRegex(RuntimeError, "Private preview marker"):
            materialize(self.site, self.zip_path, self.repo)
    def test_private_overlay(self):
        (self.site / ".rmrp-fed07-private-preview").write_text("private")
        report=materialize(self.site, self.zip_path, self.repo)
        self.assertFalse(report["publication_authorized"])
        self.assertEqual(report["json_count"], 279)
        self.assertEqual(report["qa"]["municipios"],34)
        self.assertEqual(report["qa"]["projetos"],218)
        self.assertGreaterEqual(report["qa"]["technical_checks_passed"],1603)
    def test_no_overwrite(self):
        (self.site / ".rmrp-fed07-private-preview").write_text("private")
        materialize(self.site, self.zip_path, self.repo)
        with self.assertRaisesRegex(RuntimeError, "Destination already exists"):
            materialize(self.site, self.zip_path, self.repo)
if __name__ == "__main__":
    unittest.main()
