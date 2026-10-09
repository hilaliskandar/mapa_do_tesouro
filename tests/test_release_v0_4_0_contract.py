from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_release_v0_4_0_publication_api_contract():
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    manifest = (ROOT / "data" / "catalogs" / "release_v0_4_0.yml").read_text(encoding="utf-8")
    notes = (ROOT / "governance" / "RELEASE_NOTES_V0_4_0.md").read_text(encoding="utf-8")

    assert version == "0.4.0"
    assert "release_universe: SP_645" in manifest
    assert "publication_universe_count: 11" in manifest
    assert "municipality_context_count: 287" in manifest
    assert "RM_SAO_PAULO: 38" in manifest
    assert "CIDADES_MEDIAS: 33" in manifest
    assert "rmsp_excludes_sao_paulo: true" in manifest
    assert "cidades_medias_overlap_intentional: true" in manifest
    assert "/data/api/v1" in notes
