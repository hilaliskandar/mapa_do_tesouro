"""QA isolado do staging de dados federais; sem rede, R2 ou SQLite."""

from dataclasses import replace
from pathlib import Path

import pytest

from pipeline.acquire.federal_public_api import PublicPage
from pipeline.acquire.federal_staging import persist_staging, verify_manifest


def sample(*, value=100, page=1):
    return PublicPage(
        source="obrasgov", endpoint="empenho",
        request_url=(
            "https://api-publica.obrasgov.gestao.gov.br/obras/empenho?"
            f"pagina={page}&tamanho_da_pagina=2"
        ),
        page_number=page, page_size=2, total_items=2, total_pages=1,
        data=[{"id_projeto_investimento": "32435.15-23", "valor_empenho": value}],
    )


def test_staging_hash_roundtrip_e_idempotencia(tmp_path):
    root = tmp_path / "snapshots"
    first = persist_staging([sample()], output_dir=root)
    assert first["status"] == "experimental_unvalidated"
    assert first["row_count"] == 1
    assert first["artifact_count"] == 1
    artifact = root / first["artifacts"][0]["relative_path"]
    assert artifact.exists()
    assert verify_manifest(output_dir=root, manifest_id=first["manifest_id"]) == first

    # Mesmo lote nao cria uma segunda versao nem modifica o timestamp.
    assert persist_staging([sample()], output_dir=root) == first
    assert len(list((root / "manifests").glob("*.json"))) == 1
    assert len(list((root / "obrasgov" / "empenho").glob("*.json"))) == 1


def test_mudanca_de_valor_gera_novo_snapshot(tmp_path):
    root = tmp_path / "snapshots"
    first = persist_staging([sample(value=100)], output_dir=root)
    second = persist_staging([sample(value=110)], output_dir=root)
    assert first["manifest_id"] != second["manifest_id"]
    assert first["artifacts"][0]["sha256"] != second["artifacts"][0]["sha256"]
    assert len(list((root / "obrasgov" / "empenho").glob("*.json"))) == 2


def test_hash_divergente_bloqueia_leitura(tmp_path):
    root = tmp_path / "snapshots"
    manifest = persist_staging([sample()], output_dir=root)
    artifact = root / manifest["artifacts"][0]["relative_path"]
    artifact.write_text('{"dados":"alterados"}', encoding="utf-8")
    with pytest.raises(ValueError, match="Hash divergente"):
        verify_manifest(output_dir=root, manifest_id=manifest["manifest_id"])


def test_identificador_invalidado_e_lote_vazio(tmp_path):
    with pytest.raises(ValueError, match="Lote vazio"):
        persist_staging([], output_dir=tmp_path.resolve())
    with pytest.raises(ValueError, match="Identificador invalido"):
        verify_manifest(output_dir=tmp_path, manifest_id="../../etc/passwd")
    with pytest.raises(ValueError, match="absoluto"):
        persist_staging([sample()], output_dir=Path("data/snapshots"))


def test_rejeita_fonte_ou_url_estranha(tmp_path):
    bad = replace(sample(), request_url="https://example.org/obras/empenho?pagina=1")
    with pytest.raises(ValueError, match="dominio oficial"):
        persist_staging([bad], output_dir=tmp_path.resolve())


def test_rejeita_pagina_duplicada_e_preserva_zero_ou_nulo(tmp_path):
    with pytest.raises(ValueError, match="repetida"):
        persist_staging([sample(), sample()], output_dir=tmp_path.resolve())
    root = tmp_path / "snapshots"
    zero = sample(value=0)
    null = sample(value=None)
    m0 = persist_staging([zero], output_dir=root)
    mn = persist_staging([null], output_dir=root)
    assert m0["manifest_id"] != mn["manifest_id"]
