from pathlib import Path


def test_sp645_build_materializes_v2_without_replacing_v1():
    root = Path(__file__).resolve().parents[1]
    source = (root / "pipeline/build/build_sp645_private_site.py").read_text(encoding="utf-8")
    assert 'result["publication_api"] = export_publication_api(' in source
    assert 'result["api_v2_state"] = export_state_api(' in source
    assert 'result["api_v2_regional"] = export_regional_api(' in source
    assert 'result["api_v2_readiness"] = audit_readiness(' in source
    assert 'site_output / "data" / "api" / "v2"' in source
