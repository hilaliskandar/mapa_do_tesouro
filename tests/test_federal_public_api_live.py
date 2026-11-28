"""Smoke real de APIs federais abertas; opt-in e sem escrita.

Ativar apenas em workflow isolado: FEDERAL_API_LIVE_SMOKE=1.
Executa tres GETs, pagina unica com dois registros; nao salva dados brutos.
"""
import os

import pytest

from pipeline.acquire.federal_public_api import PublicFederalClient


pytestmark = pytest.mark.skipif(
    os.environ.get("FEDERAL_API_LIVE_SMOKE") != "1",
    reason="Teste HTTP real reservado ao workflow isolado, explicitamente ativado.",
)


@pytest.mark.parametrize(
    "source,endpoint,filters,required_key",
    [
        ("obrasgov", "projeto-investimento", {"uf_principal": "SP"}, "id_projeto_investimento"),
        ("parcerias", "proposta", {"sg_uf_recebedor": "SP"}, "id_proposta"),
        ("especiais", "programas-especiais", {}, "id_programa"),
    ],
)
def test_api_federal_get_real(source, endpoint, filters, required_key):
    page = PublicFederalClient(timeout=30, retries=2).fetch_page(
        source, endpoint, filters=filters, page=1, page_size=2
    )
    assert page.page_number == 1
    assert page.total_items >= len(page.data) > 0
    assert 0 < page.total_pages
    assert all(record.get(required_key) is not None for record in page.data)
    # Nao imprimir nem persistir nomes, documentos ou valores dos beneficiarios.
    print(
        f" fonte={source} rota={endpoint} total_informado={page.total_items}"
        f" amostra={len(page.data)} contrato=OK"
    )
