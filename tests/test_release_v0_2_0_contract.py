from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_sp645_release_has_routing_marker_and_manifest():
    notes = (ROOT / "governance" / "RELEASE_NOTES_V0_2_0.md").read_text(encoding="utf-8")
    manifest = (ROOT / "data" / "catalogs" / "release_v0_2_0.yml").read_text(encoding="utf-8")
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()

    assert version == "0.2.0"
    assert "release_universe: SP_645" in notes
    assert "release_universe: SP_645" in manifest
    assert "production_promoted: false" in manifest
    assert "sp645-candidate.finbra-tic-tim-referencia.pages.dev" in notes
