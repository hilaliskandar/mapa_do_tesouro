from pathlib import Path
import hashlib

from deployment.download_r2_source import sha256


def test_sha256_matches_known_content(tmp_path):
    path = tmp_path / "sample.bin"
    content = b"financas-municipais-sp\n"
    path.write_bytes(content)
    assert sha256(path) == hashlib.sha256(content).hexdigest()


def test_snapshot_manifest_declares_pilot_scope():
    root = Path(__file__).resolve().parents[1]
    text = (
        root
        / "data"
        / "snapshots"
        / "sp_645_receitas_piloto_2020_2023.yml"
    ).read_text(encoding="utf-8")
    assert "status: local_qa_only" in text
    assert "municipalities: 645" in text
    assert "rows: 2580" in text
    assert "despesas_empenhadas_reconstruidas" in text
    assert "populacao_fixa_2024" in text
