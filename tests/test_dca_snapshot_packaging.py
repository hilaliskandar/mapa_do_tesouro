import gzip
import json
import tarfile
from pathlib import Path

from deployment.package_dca_snapshot import (
    gzip_deterministic,
    sha256,
    tar_gzip_deterministic,
)


def test_deterministic_gzip(tmp_path):
    source = tmp_path / "source.csv"
    source.write_text("a,b\n1,2\n", encoding="utf-8")
    first = tmp_path / "first.gz"
    second = tmp_path / "second.gz"
    gzip_deterministic(source, first)
    gzip_deterministic(source, second)
    assert sha256(first) == sha256(second)
    with gzip.open(first, "rt", encoding="utf-8") as handle:
        assert handle.read() == "a,b\n1,2\n"


def test_deterministic_tar_gzip(tmp_path):
    source = tmp_path / "raw"
    source.mkdir()
    (source / "b.txt").write_text("b", encoding="utf-8")
    (source / "a.txt").write_text("a", encoding="utf-8")
    first = tmp_path / "first.tar.gz"
    second = tmp_path / "second.tar.gz"
    tar_gzip_deterministic(source, first)
    tar_gzip_deterministic(source, second)
    assert sha256(first) == sha256(second)
    with tarfile.open(first, "r:gz") as tar:
        assert tar.getnames() == ["a.txt", "b.txt"]
