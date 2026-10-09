from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_release_v0_3_0_manifest_remains_historically_valid():
    notes = (ROOT / "governance" / "RELEASE_NOTES_V0_3_0.md").read_text(encoding="utf-8")
    manifest = (ROOT / "data" / "catalogs" / "release_v0_3_0.yml").read_text(encoding="utf-8")

    assert "version: 0.3.0" in manifest
    assert "release_universe: SP_645" in notes
    assert "release_universe: SP_645" in manifest
    assert "universe_count: 13" in manifest
    assert "CIDADES_MEDIAS: 33" in manifest
    assert "TIC_TIM_30: 30" in manifest
    assert "relative_statistics_recomputed_per_universe: true" in manifest
    assert "production_promoted: false" in manifest
