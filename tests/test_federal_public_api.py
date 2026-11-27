"""Testes isolados do contrato GET; nenhuma requisicao de rede externa."""

import io
import json
from urllib.error import HTTPError

import pytest

from pipeline.acquire.federal_public_api import PublicFederalClient


class Response:
    def __init__(self, data):
        self.data = data

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def read(self):
        return json.dumps(self.data).encode("utf-8")


def payload(rows, *, total=2, pages=2, page=1):
    return {
        "data": rows, "total_items": total, "total_pages": pages,
        "page_number": page, "page_size": len(rows),
    }


def test_obrasgov_get_preserva_id_e_empenho():
    calls = []

    def opener(request, timeout):
        calls.append((request.get_method(), request.full_url, timeout))
        return Response(payload([{
            "id_projeto_investimento": "32435.15-23", "valor_empenho": 2500000,
            "nr_empenho": "2026NE000003",
        }], total=1, pages=1))

    page = PublicFederalClient(opener=opener, sleep=lambda _: None).fetch_page(
        "obrasgov", "empenho",
        filters={"id_projeto_investimento": "32435.15-23"}, page_size=2,
    )
    assert page.data[0]["id_projeto_investimento"] == "32435.15-23"
    assert page.data[0]["valor_empenho"] == 2500000
    assert calls[0][0] == "GET"
    assert "id_projeto_investimento=32435.15-23" in calls[0][1]
    assert "tamanho_da_pagina=2" in calls[0][1]


def test_transferegov_paginacao_interrompe_no_total():
    seen = []

    def opener(request, timeout):
        query = request.full_url
        seen.append(query)
        number = len(seen)
        return Response(payload([{"id_parceria": 38059 + number}], total=2, pages=2, page=number))

    pages = PublicFederalClient(opener=opener, sleep=lambda _: None).fetch_pages(
        "parcerias", "empenho-parceria", page_size=1, max_pages=5,
    )
    assert len(pages) == 2
    assert len(seen) == 2
    assert pages[0].data[0]["id_parceria"] == 38060
    assert pages[1].data[0]["id_parceria"] == 38061


def test_api_vazia_nao_equivale_a_zero_financeiro():
    client = PublicFederalClient(opener=lambda *_a, **_k: Response(
        payload([], total=0, pages=0)
    ))
    pages = client.fetch_pages("especiais", "empenhos-especiais")
    assert len(pages) == 1
    assert pages[0].data == []


@pytest.mark.parametrize("source,endpoint", [
    ("siop", "empenho"),
    ("obrasgov", "alterar-projeto"),
    ("parcerias", "proposta/123"),
])
def test_impede_servicos_fora_da_allowlist(source, endpoint):
    with pytest.raises(ValueError, match="allowlist"):
        PublicFederalClient().fetch_page(source, endpoint)


def test_rejeita_paginacao_excessiva_e_filtros_reservados():
    client = PublicFederalClient()
    with pytest.raises(ValueError, match="Limites"):
        client.fetch_page("obrasgov", "empenho", page_size=1000)
    with pytest.raises(ValueError, match="max_pages"):
        client.fetch_pages("obrasgov", "empenho", max_pages=30)
    with pytest.raises(ValueError, match="reservado"):
        client.fetch_page("obrasgov", "empenho", filters={"pagina": 3})


def test_rejeita_resposta_malformada():
    client = PublicFederalClient(opener=lambda *_a, **_k: Response({"records": []}))
    with pytest.raises(ValueError, match="contrato"):
        client.fetch_page("parcerias", "proposta")


def test_retry_somente_transiente():
    count = []
    sleeps = []

    def opener(request, timeout):
        count.append(1)
        if len(count) == 1:
            raise HTTPError(request.full_url, 503, "temporario", {}, io.BytesIO(b""))
        return Response(payload([{"id_projeto_investimento": "123"}], total=1, pages=1))

    result = PublicFederalClient(opener=opener, sleep=sleeps.append).fetch_page(
        "obrasgov", "projeto-investimento"
    )
    assert result.total_items == 1
    assert len(count) == 2
    assert sleeps == [1]


def test_erro_http_permanente_nao_tenta_novamente():
    count = []

    def opener(request, timeout):
        count.append(1)
        raise HTTPError(request.full_url, 403, "bloqueado", {}, io.BytesIO(b""))

    client = PublicFederalClient(opener=opener, sleep=lambda _: None)
    with pytest.raises(HTTPError):
        client.fetch_page("parcerias", "programa")
    assert len(count) == 1
