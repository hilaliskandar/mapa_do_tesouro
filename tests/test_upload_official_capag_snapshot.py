"""Contract tests: only exact official bytes can be sent to private R2."""
from pathlib import Path
from unittest.mock import patch
import pytest
from deployment.upload_official_capag_snapshot import upload,DEFAULT_KEY,EXPECTED_SHA

def test_reject_source_before_network(tmp_path):
    bad=tmp_path/"unverified.xlsx"
    bad.write_bytes(b"unverified")
    with patch("deployment.upload_official_capag_snapshot.urlopen") as transport:
        with pytest.raises(ValueError,match="SHA-256"):
            upload(bad,"account","secret","private",DEFAULT_KEY)
        transport.assert_not_called()

def test_source_key_is_versioned_and_private():
    assert DEFAULT_KEY.startswith("sp_645/official_snapshots/capag/2026-09/")
    assert len(EXPECTED_SHA)==64
