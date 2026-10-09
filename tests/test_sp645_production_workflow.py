from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_sp645_production_workflow_is_manual_and_release_bound():
    workflow = (ROOT / ".github" / "workflows" / "pages-sp645-production.yml").read_text(
        encoding="utf-8"
    )
    assert "workflow_dispatch:" in workflow
    assert "release_tag:" in workflow
    assert "release_universe: SP_645" in workflow
    assert "environment: production" in workflow
    assert "--branch=main" in workflow
    assert "qa_sp645_pages.py --site build/site-sp645" in workflow
    assert "qa_sp645_pages.py" in workflow
    assert "pull_request:" not in workflow
    assert "push:" not in workflow
    assert "release:" not in workflow


def test_legacy_production_workflow_remains_separate():
    legacy = (ROOT / ".github" / "workflows" / "pages-production.yml").read_text(
        encoding="utf-8"
    )
    statewide = (ROOT / ".github" / "workflows" / "pages-sp645-production.yml").read_text(
        encoding="utf-8"
    )
    assert "materialize_preview.py" in legacy
    assert "build_sp645_private_site" in statewide
