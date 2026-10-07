from pathlib import Path

from pipeline.acquire.siconfi_legal_reports import read_raw, valid_raw, write_raw
from pipeline.sources.siconfi import FetchResult


def test_legal_raw_artifact_roundtrip(tmp_path):
    path = tmp_path / "rreo" / "2025" / "3501608.json.gz"
    result = FetchResult(
        items=[{"conta": "Teste", "valor": 10}],
        pages=1,
        request_count=1,
    )

    write_raw(
        path,
        endpoint="rreo",
        year=2025,
        entity_id="3501608",
        params={"nr_periodo": 6},
        result=result,
    )

    payload = read_raw(path)
    assert payload["status"] == "observado"
    assert payload["items"][0]["valor"] == 10
    assert valid_raw(
        path,
        endpoint="rreo",
        year=2025,
        entity_id="3501608",
    )


def test_empty_legal_report_is_absent_not_zero(tmp_path):
    path = tmp_path / "rgf" / "2025" / "3501608.json.gz"
    result = FetchResult(items=[], pages=1, request_count=1)

    write_raw(
        path,
        endpoint="rgf",
        year=2025,
        entity_id="3501608",
        params={"nr_periodo": 3},
        result=result,
    )

    payload = read_raw(path)
    assert payload["status"] == "ausente"
    assert payload["items"] == []
