from __future__ import annotations

import gzip
import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable
from urllib.parse import urlencode
from urllib.request import Request, urlopen

BASE_URL = "https://apidatalake.tesouro.gov.br/ords/siconfi/tt"


@dataclass
class FetchResult:
    items: list[dict]
    pages: int
    request_count: int


class SiconfiClient:
    def __init__(
        self,
        *,
        base_url: str = BASE_URL,
        min_interval: float = 1.05,
        timeout: int = 90,
        sleep: Callable[[float], None] = time.sleep,
        opener=urlopen,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.min_interval = max(0.0, float(min_interval))
        self.timeout = timeout
        self.sleep = sleep
        self.opener = opener
        self._last_request_at: float | None = None
        self.request_count = 0

    def _throttle(self) -> None:
        if self._last_request_at is None or self.min_interval <= 0:
            return
        elapsed = time.monotonic() - self._last_request_at
        remaining = self.min_interval - elapsed
        if remaining > 0:
            self.sleep(remaining)

    def _request_json(self, url: str) -> dict:
        self._throttle()
        request = Request(
            url,
            headers={
                "Accept": "application/json",
                "User-Agent": "financas-municipais-sp/0.1 (+GitHub)",
            },
        )
        try:
            with self.opener(request, timeout=self.timeout) as response:
                payload = json.loads(response.read().decode("utf-8"))
        finally:
            self._last_request_at = time.monotonic()
            self.request_count += 1
        if not isinstance(payload, dict):
            raise ValueError(f"Unexpected SICONFI payload type: {type(payload)!r}")
        return payload

    @staticmethod
    def _next_link(payload: dict) -> str | None:
        for link in payload.get("links", []) or []:
            rel = str(link.get("rel", "")).lower()
            href = link.get("href")
            if rel == "next" and href:
                return str(href)
        return None

    def fetch_all(self, endpoint: str, params: dict[str, object]) -> FetchResult:
        query = urlencode(
            [(key, value) for key, value in params.items() if value is not None]
        )
        url = f"{self.base_url}/{endpoint.lstrip('/')}?{query}"
        items: list[dict] = []
        pages = 0
        initial_requests = self.request_count
        seen_urls: set[str] = set()

        while url:
            if url in seen_urls:
                raise RuntimeError(f"Pagination loop detected: {url}")
            seen_urls.add(url)

            payload = self._request_json(url)
            page_items = payload.get("items", [])
            if not isinstance(page_items, list):
                raise ValueError("SICONFI payload 'items' is not a list.")
            items.extend(page_items)
            pages += 1

            next_url = self._next_link(payload)
            if next_url:
                url = next_url
                continue

            if payload.get("hasMore"):
                raise RuntimeError(
                    "SICONFI response indicates hasMore=true without a next link."
                )
            url = None

        return FetchResult(
            items=items,
            pages=pages,
            request_count=self.request_count - initial_requests,
        )

    def fetch_dca(
        self,
        *,
        year: int,
        entity_id: str | int,
        annex: str | None = None,
    ) -> FetchResult:
        return self.fetch_all(
            "dca",
            {
                "an_exercicio": int(year),
                "id_ente": str(entity_id),
                "no_anexo": annex,
            },
        )


def write_raw_dca(
    output: Path,
    *,
    year: int,
    entity_id: str,
    result: FetchResult,
    annex: str | None,
) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "source": "SICONFI",
        "endpoint": "dca",
        "year": int(year),
        "entity_id": str(entity_id),
        "annex": annex,
        "pages": result.pages,
        "requests": result.request_count,
        "items": result.items,
    }
    with gzip.open(output, "wt", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, separators=(",", ":"))


def read_raw_dca(path: Path) -> dict:
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        return json.load(handle)
