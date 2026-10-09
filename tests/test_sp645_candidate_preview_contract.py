from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_sp645_candidate_preview_is_manual_and_isolated():
    workflow = (ROOT / ".github" / "workflows" / "pages-sp645-candidate.yml").read_text(
        encoding="utf-8"
    )
    assert "workflow_dispatch:" in workflow
    assert "pull_request:" not in workflow
    assert "release:" not in workflow
    assert "push:" not in workflow
    assert 'default: "sp645-candidate"' in workflow
    assert "--branch=\"$DEPLOY_ALIAS\"" in workflow
    assert "pages-production.yml" not in workflow


def test_sp645_pages_qa_keeps_statewide_contract():
    qa = (ROOT / "deployment" / "qa_sp645_pages.py").read_text(encoding="utf-8")
    assert "EXPECTED_MUNICIPALITIES = 645" in qa
    assert "EXPECTED_YEARS = [2021, 2022, 2023, 2024, 2025]" in qa
    assert "EXPECTED_CAPAG_OBSERVED = 645" in qa
    assert "exportCurrentSliceCsv" in qa
