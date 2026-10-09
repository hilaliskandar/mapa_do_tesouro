from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_public_preview_skips_sp645_releases():
    workflow = (ROOT / ".github" / "workflows" / "pages-preview.yml").read_text(
        encoding="utf-8"
    )
    assert "release_universe: SP_645" in workflow
    assert "github.event_name != 'release'" in workflow


def test_sp645_candidate_workflow_remains_manual():
    workflow = (ROOT / ".github" / "workflows" / "pages-sp645-candidate.yml").read_text(
        encoding="utf-8"
    )
    assert "workflow_dispatch:" in workflow
    assert "release:" not in workflow
    assert "push:" not in workflow
