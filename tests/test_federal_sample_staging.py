"""Amostragem ponta a ponta sem rede: cliente injetado, staging e hash."""

from pathlib import Path

import pytest

from pipeline.acquire.federal_public_api import PublicPage
from pipeline.acquire.federal_sample_staging import run_sample
from pipeline.acquire.federal_staging import verify_manifest


class FakeClient:
    def __init__(self, *, empty_source=None):
        self.calls = []
        self.empty_source = empty_source

    def fetch_page(self, source, endpoint, *, filters, page, page_size):
        self.calls.append((source, endpoint, filters, page, page_size))
        bases = {
            "obrasgov": "https://api-publica.obrasgov.gestao.gov.br/obras",
            "parcerias": "https://api-publica.transferegov.gestao.gov.br/parcerias",
            "especiais": "https://api-publica.transferegov.gestao.gov.br/especiais",
        }
        records = [] if source == self.empty_source else [{"id": source, "valor": None}]
        return PublicPage(
            source=source,
            endpoint=endpoint,
            request_url=f"{bases[source]}/{endpoint}?pagina=1&tamanho_da_pagina=2",
            page_number=page,
            page_size=page_size,
            total_items=len(records),
            total_pages=1 if records else 0,
            data=records,
        )


def test_amostragem_de_tres_fontes_cria_manifesto_verificavel(tmp_path):
    client = FakeClient()
    output = tmp_path / "privado"
    result = run_sample(output=output, client=client)
    assert result["status"] == "staging_verified_local_only"
    assert result["artifact_count"] == 3
    assert result["row_count"] == 3
    assert len(client.calls) == 3
    assert {source for source, *_ in client.calls} == {"obrasgov", "parcerias", "especiais"}
    assert all(page == 1 and size == 2 for *_prefix, page, size in client.calls)
    assert verify_manifest(output_dir=output, manifest_id=result["manifest_id"])["row_count"] == 3

    repeated = run_sample(output=output, client=FakeClient())
    assert repeated["manifest_id"] == result["manifest_id"]
    assert len(list((output / "manifests").glob("*.json"))) == 1


def test_amostra_incompleta_nao_persiste_lote(tmp_path):
    output = tmp_path / "privado"
    with pytest.raises(RuntimeError, match="incompleta"):
        run_sample(output=output, client=FakeClient(empty_source="parcerias"))
    assert not output.exists()


def test_diretorio_relativo_rejeitado(tmp_path):
    with pytest.raises(ValueError, match="absoluto"):
        run_sample(output=Path("data/snapshots/federal"), client=FakeClient())
