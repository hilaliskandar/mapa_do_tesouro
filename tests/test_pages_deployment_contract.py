from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_pages_preview_workflow_contract():
    workflow = (ROOT / ".github" / "workflows" / "pages-preview.yml").read_text(encoding="utf-8")
    assert "pull_request:" in workflow
    assert "release:" in workflow
    assert "workflow_dispatch:" in workflow
    assert "deployment/qa_pages.py --site build/site" in workflow
    assert "deployment/qa_pages.py" in workflow
    assert "--branch=\"$DEPLOY_ALIAS\"" in workflow
    assert "CLOUDFLARE_API_TOKEN" in workflow
    assert "CLOUDFLARE_ACCOUNT_ID" in workflow
    assert "CLOUDFLARE_PAGES_PROJECT" in workflow


def test_pages_production_is_explicit_and_release_scoped():
    workflow = (ROOT / ".github" / "workflows" / "pages-production.yml").read_text(encoding="utf-8")
    assert "workflow_dispatch:" in workflow
    assert "release_tag:" in workflow
    assert 'gh release view "$RELEASE_TAG"' in workflow
    assert "--branch=main" in workflow
    assert "environment: production" in workflow
    assert "pull_request:" not in workflow
    assert "release:\n" not in workflow


def test_importer_reads_application_version():
    importer = (ROOT / "pipeline" / "ingest" / "import_multifuentes.py").read_text(encoding="utf-8")
    assert "VERSION_FILE = ROOT / \"VERSION\"" in importer
    assert "read_app_version()" in importer


def test_pages_qa_has_expected_sentinels_and_source_hash():
    qa = (ROOT / "deployment" / "qa_pages.py").read_text(encoding="utf-8")
    assert "f51d8615f3742b1d414f1edff67805cac1a10cbc18764b454aab518de9c9e3f1" in qa
    assert '"dc_pct_rcl": 0.9322' in qa
    assert '"dcl_pct_rcl": 0.8368' in qa
    assert '"dtp_pct_rcl": 0.3669' in qa
