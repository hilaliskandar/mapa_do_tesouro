import gzip
import io
import json
from pathlib import Path
from urllib.error import HTTPError, URLError

from pipeline.sources.siconfi import SiconfiClient, read_raw_dca, write_raw_dca


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self):
        return json.dumps(self.payload).encode("utf-8")


def test_siconfi_follows_next_link_and_aggregates_items():
    calls = []
    pages = [
        {
            "items": [{"valor": 1}],
            "hasMore": True,
            "limit": 1,
            "offset": 0,
            "links": [],
        },
        {
            "items": [{"valor": 2}],
            "hasMore": False,
            "links": [],
        },
    ]

    def opener(request, timeout):
        calls.append((request.full_url, timeout))
        return FakeResponse(pages[len(calls) - 1])

    client = SiconfiClient(
        base_url="https://example.test",
        min_interval=0,
        opener=opener,
    )
    result = client.fetch_all(
        "dca",
        {"an_exercicio": 2025, "id_ente": "3501608"},
        page_limit=1,
    )

    assert result.items == [{"valor": 1}, {"valor": 2}]
    assert result.pages == 2
    assert result.request_count == 2
    assert calls[0][0].startswith("https://example.test/dca?")
    assert "offset=0" in calls[0][0]
    assert calls[1][0].startswith("https://example.test/dca?")
    assert "offset=1" in calls[1][0]


def test_siconfi_rejects_has_more_without_usable_offset():
    def opener(request, timeout):
        return FakeResponse({"items": [], "hasMore": True, "links": []})

    client = SiconfiClient(
        base_url="https://example.test",
        min_interval=0,
        opener=opener,
    )
    try:
        client.fetch_dca(year=2025, entity_id="3501608")
    except RuntimeError as exc:
        assert "usable offset" in str(exc)
    else:
        raise AssertionError("Expected pagination failure.")


def test_raw_dca_roundtrip(tmp_path):
    path = tmp_path / "2025" / "3501608.json.gz"
    client = SiconfiClient(
        min_interval=0,
        opener=lambda request, timeout: FakeResponse(
            {"items": [{"cod_ibge": 3501608, "valor": 10}], "hasMore": False}
        ),
    )
    result = client.fetch_dca(year=2025, entity_id="3501608")
    write_raw_dca(
        path,
        year=2025,
        entity_id="3501608",
        result=result,
        annex=None,
    )

    payload = read_raw_dca(path)
    assert payload["source"] == "SICONFI"
    assert payload["year"] == 2025
    assert payload["entity_id"] == "3501608"
    assert payload["items"][0]["valor"] == 10
    assert gzip.open(path, "rt", encoding="utf-8").read().startswith("{")


def test_siconfi_retries_transient_http_error():
    attempts = []
    sleeps = []

    def opener(request, timeout):
        attempts.append(request.full_url)
        if len(attempts) < 3:
            raise HTTPError(
                request.full_url,
                503,
                "Service Unavailable",
                hdrs=None,
                fp=io.BytesIO(b""),
            )
        return FakeResponse({"items": [{"valor": 1}], "hasMore": False})

    client = SiconfiClient(
        base_url="https://example.test",
        min_interval=0,
        opener=opener,
        max_retries=3,
        retry_backoff=0.25,
        sleep=sleeps.append,
    )
    result = client.fetch_dca(year=2025, entity_id="3501608")

    assert result.items == [{"valor": 1}]
    assert len(attempts) == 3
    assert client.request_count == 3
    assert sleeps == [0.25, 0.5]


def test_siconfi_does_not_retry_non_transient_http_error():
    attempts = []

    def opener(request, timeout):
        attempts.append(request.full_url)
        raise HTTPError(
            request.full_url,
            404,
            "Not Found",
            hdrs=None,
            fp=io.BytesIO(b""),
        )

    client = SiconfiClient(
        base_url="https://example.test",
        min_interval=0,
        opener=opener,
        max_retries=3,
        retry_backoff=0,
    )
    try:
        client.fetch_dca(year=2025, entity_id="3501608")
    except HTTPError as exc:
        assert exc.code == 404
    else:
        raise AssertionError("Expected HTTPError.")
    assert len(attempts) == 1


def test_siconfi_retries_url_error_until_limit():
    attempts = []
    sleeps = []

    def opener(request, timeout):
        attempts.append(request.full_url)
        raise URLError("temporary network failure")

    client = SiconfiClient(
        base_url="https://example.test",
        min_interval=0,
        opener=opener,
        max_retries=2,
        retry_backoff=0.1,
        sleep=sleeps.append,
    )
    try:
        client.fetch_dca(year=2025, entity_id="3501608")
    except URLError:
        pass
    else:
        raise AssertionError("Expected URLError.")
    assert len(attempts) == 3
    assert client.request_count == 3
    assert sleeps == [0.1, 0.2]
