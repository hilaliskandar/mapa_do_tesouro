from __future__ import annotations

import gzip
import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable
from urllib.parse import parse_qsl, urlencode, urlparse
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
    def _next_offset(payload: dict) -> int | None:
        if not payload.get("hasMore"):
            return None

        try:
            offset = int(payload.get("offset", 0))
            limit = int(payload["limit"])
        except (KeyError, TypeError, ValueError):
            offset = None
            limit = None

        if offset is not None and limit is not None and limit > 0:
            return offset + limit

        for link in payload.get("links", []) or []:
            if str(link.get("rel", "")).lower() != "next":
                continue
            href = link.get("href")
            if not href:
                continue
            query = dict(parse_qsl(urlparse(str(href)).query))
            try:
                return int(query["offset"])
            except (KeyError, TypeError, ValueError):
                continue

        raise RuntimeError(
            "SICONFI response indicates hasMore=true without a usable offset."
        )

    def fetch_all(
        self,
        endpoint: str,
        params: dict[str, object],
        *,
        page_limit: int = 5000,
    ) -> FetchResult:
        base_params = {
            key: value
            for key, value in params.items()
            if value is not None
        }
        if page_limit <= 0:
            raise ValueError("page_limit must be greater than zero.")

        items: list[dict] = []
        pages = 0
        initial_requests = self.request_count
        seen_offsets: set[int] = set()
        offset = 0

        while True:
            if offset in seen_offsets:
                raise RuntimeError(f"Pagination loop detected at offset={offset}.")
            seen_offsets.add(offset)

            query_params = dict(base_params)
            query_params["limit"] = int(page_limit)
            query_params["offset"] = int(offset)
            query = urlencode(list(query_params.items()))
            url = f"{self.base_url}/{endpoint.lstrip('/')}?{query}"

            payload = self._request_json(url)
            page_items = payload.get("items", [])
            if not isinstance(page_items, list):
                raise ValueError("SICONFI payload 'items' is not a list.")
            items.extend(page_items)
            pages += 1

            next_offset = self._next_offset(payload)
            if next_offset is None:
                break
            if next_offset <= offset:
                raise RuntimeError(
                    f"Invalid SICONFI next offset: {next_offset} <= {offset}."
                )
            offset = next_offset

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


    def fetch_entities(self) -> FetchResult:
        return self.fetch_all("entes", {})

    def fetch_rreo(
        self,
        *,
        year: int,
        period: int,
        entity_id: str | int,
        annex: str,
        report_type: str = "RREO",
        sphere: str = "M",
    ) -> FetchResult:
        return self.fetch_all(
            "rreo",
            {
                "an_exercicio": int(year),
                "nr_periodo": int(period),
                "co_tipo_demonstrativo": report_type,
                "no_anexo": annex,
                "co_esfera": sphere,
                "id_ente": str(entity_id),
            },
        )

    def fetch_rgf(
        self,
        *,
        year: int,
        periodicity: str,
        period: int,
        entity_id: str | int,
        annex: str,
        report_type: str = "RGF",
        sphere: str = "M",
        branch: str = "E",
    ) -> FetchResult:
        return self.fetch_all(
            "rgf",
            {
                "an_exercicio": int(year),
                "in_periodicidade": periodicity,
                "nr_periodo": int(period),
                "co_tipo_demonstrativo": report_type,
                "no_anexo": annex,
                "co_esfera": sphere,
                "co_poder": branch,
                "id_ente": str(entity_id),
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
