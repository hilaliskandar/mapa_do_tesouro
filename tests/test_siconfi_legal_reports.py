from pathlib import Path

from pipeline.acquire.siconfi_legal_reports import acquire_legal_reports, read_raw, valid_raw, write_raw
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



class FakeClient:
    def __init__(self, min_interval):
        self.min_interval = min_interval

    def fetch_rgf(self, **kwargs):
        return FetchResult(
            items=[{"cod_conta": "RGF_TESTE", "valor": 10}],
            pages=1,
            request_count=1,
        )


def test_generic_rgf_acquisition_cli_core(tmp_path, monkeypatch):
    import pipeline.acquire.siconfi_legal_reports as module

    monkeypatch.setattr(module, "SiconfiClient", FakeClient)
    result = acquire_legal_reports(
        endpoint="rgf",
        entity_id="3501608",
        years=[2025],
        annexes=["RGF-Anexo 01", "RGF-Anexo 05"],
        output=tmp_path / "raw",
        min_interval=0,
        period=3,
        report_type="RGF",
        sphere="M",
        periodicity="Q",
        branch="E",
    )
    assert result["completed_now"] == 2
    assert result["request_count"] == 2
    assert result["failed"] == []
    assert len(result["artifacts"]) == 2
