from pathlib import Path

from pipeline.acquire.siconfi_dca_state import ANNEXES, raw_tree_sha256


def test_state_annex_contract():
    assert ANNEXES == (
        "DCA-Anexo I-C",
        "DCA-Anexo I-D",
        "DCA-Anexo I-E",
    )


def test_raw_tree_sha256_is_order_stable(tmp_path):
    import gzip

    first = tmp_path / "z" / "2025" / "2.json.gz"
    second = tmp_path / "a" / "2025" / "1.json.gz"
    first.parent.mkdir(parents=True)
    second.parent.mkdir(parents=True)

    with first.open("wb") as raw:
        with gzip.GzipFile(fileobj=raw, mode="wb", mtime=0) as handle:
            handle.write(b"two")
    with second.open("wb") as raw:
        with gzip.GzipFile(fileobj=raw, mode="wb", mtime=0) as handle:
            handle.write(b"one")

    digest_a = raw_tree_sha256(tmp_path)
    digest_b = raw_tree_sha256(tmp_path)
    assert len(digest_a) == 64
    assert digest_a == digest_b
