import json
from pathlib import Path
from unittest.mock import patch
import pytest
from deployment.stage_tcesp_api_v2 import merge_tcesp_preview

def setup(tmp_path):
    preview=tmp_path/"preview"; site=tmp_path/"site"
    source=preview/"data/api/v2/tcesp"
    source.mkdir(parents=True)
    (source/"manifest.json").write_text('{"status":"preview_not_published"}')
    dest=site/"data/api/v2"
    dest.mkdir(parents=True)
    (dest/"manifest.json").write_text('{"canonical":"unchanged"}')
    return preview,site

def test_disabled_by_default(tmp_path):
    preview,site=setup(tmp_path)
    with pytest.raises(ValueError,match="disabled"):
        merge_tcesp_preview(preview=preview,site=site)
    assert not (site/"data/api/v2/tcesp").exists()

def test_opt_in_preserves_canonical_manifest(tmp_path):
    preview,site=setup(tmp_path)
    original=(site/"data/api/v2/manifest.json").read_bytes()
    with patch("deployment.stage_tcesp_api_v2.subprocess.run") as run:
        result=merge_tcesp_preview(preview=preview,site=site,enabled=True)
        run.assert_called_once()
    assert result["status"]=="staged_not_published"
    assert (site/"data/api/v2/tcesp/manifest.json").is_file()
    assert (site/"data/api/v2/manifest.json").read_bytes()==original
    with patch("deployment.stage_tcesp_api_v2.subprocess.run"):
        with pytest.raises(FileExistsError):
            merge_tcesp_preview(preview=preview,site=site,enabled=True)

def test_missing_canonical_manifest_denied(tmp_path):
    preview,site=setup(tmp_path)
    (site/"data/api/v2/manifest.json").unlink()
    with patch("deployment.stage_tcesp_api_v2.subprocess.run"):
        with pytest.raises(ValueError,match="Main API v2"):
            merge_tcesp_preview(preview=preview,site=site,enabled=True)

def test_staging_adds_link_only_to_preview_index(tmp_path):
    preview,site=setup(tmp_path)
    index=site/"index.html"
    before='<main><nav class="tabs" aria-label="Seções"></nav></main>'
    index.write_text(before,encoding="utf-8")
    with patch("deployment.stage_tcesp_api_v2.subprocess.run"):
        result=merge_tcesp_preview(preview=preview,site=site,enabled=True)
    result_html=index.read_text(encoding="utf-8")
    assert result["status"]=="staged_not_published"
    assert '<a href="./tcesp-investimentos.html">' in result_html
    assert 'href="./tcesp-investimentos.html"' not in before
    assert (site/"data/api/v2/manifest.json").read_text()=='{"canonical":"unchanged"}'
