import json

import pipeline.acquire.siconfi_rreo_state as module
from pipeline.sources.siconfi import FetchResult


class FakeClient:
    def __init__(self, min_interval):
        self.min_interval = min_interval

    def fetch_rreo(self, **kwargs):
        return FetchResult(
            items=[
                {
                    "cod_conta": "ReceitaCorrenteLiquida",
                    "conta": "RECEITA CORRENTE LÍQUIDA (III) = (I - II)",
                    "coluna": "TOTAL (ÚLTIMOS 12 MESES)",
                    "valor": 10.0,
                    "populacao": 100,
                }
            ],
            pages=1,
            request_count=1,
        )


def test_rreo_state_acquisition(tmp_path, monkeypatch):
    geo = tmp_path / "sp.json"
    geo.write_text(
        json.dumps(
            {
                "features": [
                    {"properties": {"id": "3500105", "name": "A"}},
                    {"properties": {"id": "3500204", "name": "B"}},
                ]
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(module, "SiconfiClient", FakeClient)

    result = module.acquire_state_year(
        geo,
        2025,
        tmp_path / "raw",
        tmp_path / "normalized.csv",
        min_interval=0,
        expected_municipalities=2,
    )

    assert result["municipalities_requested"] == 2
    assert result["completed_now"] == 2
    assert result["failed"] == []
    assert result["normalization"]["rows"] == 2
    assert result["normalization"]["observed_rcl_rows"] == 2



def test_rreo_state_can_target_explicit_codes(tmp_path, monkeypatch):
    geo = tmp_path / "sp.json"
    geo.write_text(
        json.dumps(
            {
                "features": [
                    {"properties": {"id": "3500105", "name": "A"}},
                    {"properties": {"id": "3500204", "name": "B"}},
                    {"properties": {"id": "3500303", "name": "C"}},
                ]
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(module, "SiconfiClient", FakeClient)

    result = module.acquire_state_year(
        geo,
        2025,
        tmp_path / "raw",
        tmp_path / "normalized.csv",
        min_interval=0,
        only_codes={"3500204"},
        expected_municipalities=3,
    )

    assert result["municipalities_requested"] == 1
    assert result["normalization"]["rows"] == 1
    assert result["normalization"]["observed_rcl_rows"] == 1
