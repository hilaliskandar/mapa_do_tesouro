"""Cliente público GET para Obrasgov e Transferegov, sem efeitos sobre a produção.

Paginação explícita e limitada; nenhum método de escrita é exposto.
Os registros brutos são retornados sem presumir enquadramento Novo PAC.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from typing import Any, Callable, Mapping
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlsplit
from urllib.request import Request, urlopen


BASE_URLS = {
    "obrasgov": "https://api-publica.obrasgov.gestao.gov.br/obras",
    "parcerias": "https://api-publica.transferegov.gestao.gov.br/parcerias",
    "especiais": "https://api-publica.transferegov.gestao.gov.br/especiais",
}
# Allowlist restritiva: impedir consultas acidentais a endpoints privados,
# operacoes de alteracao ou hosts arbitrarios.
ENDPOINTS = {
    "obrasgov": frozenset({
        "projeto-investimento", "empenho", "execucao-fisica",
        "contrato", "geometria", "estudo-viabilidade",
        "historico-situacao-cancelada-paralisada",
    }),
    "parcerias": frozenset({
        "programa", "proposta", "parceria", "empenho-parceria",
        "ordem-pagamento", "cronograma-desembolso",
    }),
    "especiais": frozenset({
        "programas-especiais", "planos-acao-especiais",
        "beneficiarios-especiais", "empenhos-especiais",
        "ordens-pagamentos-ordens-bancarias-especiais",
    }),
}
TRANSIENT_HTTP = frozenset({429, 500, 502, 503, 504})


@dataclass(frozen=True)
class PublicPage:
    source: str
    endpoint: str
    request_url: str
    page_number: int
    page_size: int
    total_items: int
    total_pages: int
    data: list[dict[str, Any]]


class PublicFederalClient:
    """API GET pública, com limites para evitar varredura involuntária."""

    def __init__(
        self,
        *,
        opener: Callable[..., Any] = urlopen,
        timeout: float = 20.0,
        retries: int = 2,
        sleep: Callable[[float], Any] = time.sleep,
        base_urls: Mapping[str, str] | None = None,
    ) -> None:
        if timeout <= 0 or retries < 0:
            raise ValueError("timeout deve ser positivo e retries nao negativo")
        self.opener = opener
        self.timeout = timeout
        self.retries = retries
        self.sleep = sleep
        self.base_urls = dict(BASE_URLS if base_urls is None else base_urls)

    def fetch_page(
        self,
        source: str,
        endpoint: str,
        *,
        filters: Mapping[str, str | int] | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> PublicPage:
        if source not in ENDPOINTS or endpoint not in ENDPOINTS[source]:
            raise ValueError("Fonte ou endpoint fora da allowlist publica GET")
        if not 1 <= page <= 10_000 or not 1 <= page_size <= 100:
            raise ValueError("Limites de pagina devem estar entre 1 e 100")
        base = self.base_urls[source].rstrip("/")
        parsed = urlsplit(base)
        if parsed.scheme != "https" or not parsed.hostname:
            raise ValueError("Base URL deve ser HTTPS")
        query: dict[str, str | int] = {}
        for key, value in (filters or {}).items():
            if not key.isidentifier() or key in {"pagina", "tamanho_da_pagina"}:
                raise ValueError("Filtro invalido ou reservado")
            if not isinstance(value, (str, int)) or len(str(value)) > 256:
                raise ValueError("Valor de filtro invalido")
            query[key] = value
        query.update({"pagina": page, "tamanho_da_pagina": page_size})
        url = f"{base}/{endpoint}?{urlencode(query)}"
        request = Request(url, headers={"Accept": "application/json", "User-Agent": "MapaDoTesouro/experimental"})
        for attempt in range(self.retries + 1):
            try:
                with self.opener(request, timeout=self.timeout) as response:
                    payload = json.loads(response.read().decode("utf-8"))
                break
            except HTTPError as exc:
                if exc.code not in TRANSIENT_HTTP or attempt == self.retries:
                    raise
            except (URLError, TimeoutError):
                if attempt == self.retries:
                    raise
            self.sleep(min(2**attempt, 8))
        if not isinstance(payload, dict) or not isinstance(payload.get("data"), list):
            raise ValueError("Resposta fora do contrato paginado")
        rows = payload["data"]
        if not all(isinstance(row, dict) for row in rows):
            raise ValueError("Registros retornados nao sao objetos")
        total = payload.get("total_items")
        total_pages = payload.get("total_pages")
        if type(total) is not int or type(total_pages) is not int:
            raise ValueError("Contadores de paginacao ausentes")
        returned_page = payload.get("page_number")
        if returned_page is not None and returned_page != page:
            raise ValueError("Pagina retornada diverge da solicitada")
        if total < 0 or total_pages < 0 or len(rows) > page_size:
            raise ValueError("Contagem ou pagina excede os limites")
        return PublicPage(
            source=source, endpoint=endpoint, request_url=url,
            page_number=page, page_size=page_size,
            total_items=total, total_pages=total_pages, data=rows,
        )

    def fetch_pages(
        self,
        source: str,
        endpoint: str,
        *,
        filters: Mapping[str, str | int] | None = None,
        page_size: int = 10,
        max_pages: int = 2,
    ) -> list[PublicPage]:
        if not 1 <= max_pages <= 20:
            raise ValueError("max_pages deve estar entre 1 e 20")
        result = []
        for number in range(1, max_pages + 1):
            page = self.fetch_page(source, endpoint, filters=filters, page=number, page_size=page_size)
            result.append(page)
            if not page.data or number >= page.total_pages:
                break
        return result
