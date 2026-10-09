from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_release_v0_3_1_is_qa_only_patch():
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    manifest = (ROOT / "data" / "catalogs" / "release_v0_3_1.yml").read_text(encoding="utf-8")
    qa = (ROOT / "deployment" / "qa_sp645_pages.py").read_text(encoding="utf-8")

    assert version == "0.3.1"
    assert "release_universe: SP_645" in manifest
    assert "data_unchanged_from: 0.3.0" in manifest
    assert "remote_json_propagation_retry: true" in manifest
    assert "except (json.JSONDecodeError, UnicodeDecodeError)" in qa
    assert "time.sleep(delay)" in qa
