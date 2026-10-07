import json

from pipeline.sources.siconfi import SiconfiClient


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self):
        return json.dumps(self.payload).encode("utf-8")


def test_rreo_builds_expected_query():
    calls = []

    def opener(request, timeout):
        calls.append(request.full_url)
        return FakeResponse({"items": [{"valor": 1}], "hasMore": False})

    client = SiconfiClient(
        base_url="https://example.test",
        min_interval=0,
        opener=opener,
    )
    result = client.fetch_rreo(
        year=2025,
        period=6,
        entity_id="3501608",
        annex="RREO-Anexo 03",
    )

    assert result.items == [{"valor": 1}]
    url = calls[0]
    assert "/rreo?" in url
    assert "an_exercicio=2025" in url
    assert "nr_periodo=6" in url
    assert "co_tipo_demonstrativo=RREO" in url
    assert "co_esfera=M" in url
    assert "id_ente=3501608" in url


def test_rgf_builds_expected_query():
    calls = []

    def opener(request, timeout):
        calls.append(request.full_url)
        return FakeResponse({"items": [{"valor": 2}], "hasMore": False})

    client = SiconfiClient(
        base_url="https://example.test",
        min_interval=0,
        opener=opener,
    )
    result = client.fetch_rgf(
        year=2025,
        periodicity="Q",
        period=3,
        entity_id="3501608",
        annex="RGF-Anexo 01",
    )

    assert result.items == [{"valor": 2}]
    url = calls[0]
    assert "/rgf?" in url
    assert "an_exercicio=2025" in url
    assert "in_periodicidade=Q" in url
    assert "nr_periodo=3" in url
    assert "co_tipo_demonstrativo=RGF" in url
    assert "co_esfera=M" in url
    assert "co_poder=E" in url
    assert "id_ente=3501608" in url
