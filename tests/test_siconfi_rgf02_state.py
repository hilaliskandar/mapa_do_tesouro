import csv
import json

import pipeline.acquire.siconfi_rgf02_state as module
from pipeline.sources.siconfi import FetchResult


class FakeClient:
    def __init__(self, min_interval):
        self.min_interval = min_interval

    def fetch_rgf(self, **kwargs):
        return FetchResult(
            items=[
                {
                    "cod_conta": "DividaConsolidada",
                    "conta": "DÍVIDA CONSOLIDADA - DC (I)",
                    "coluna": "Até o 3º Quadrimestre",
                    "valor": 10,
                    "populacao": 100,
                },
                {
                    "cod_conta": "RGF2ReceitaCorrenteLiquida",
                    "conta": "RECEITA CORRENTE LÍQUIDA - RCL",
                    "coluna": "Até o 3º Quadrimestre",
                    "valor": 20,
                    "populacao": 100,
                },
            ],
            pages=1,
            request_count=1,
        )


def test_rgf02_state_preserves_long_taxonomy(tmp_path, monkeypatch):
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

    output = tmp_path / "rgf02.csv"
    result = module.acquire_state_year(
        geo,
        2025,
        tmp_path / "raw",
        output,
        min_interval=0,
        expected_municipalities=2,
    )

    rows = list(csv.DictReader(output.open(encoding="utf-8")))
    assert result["municipalities_requested"] == 2
    assert result["observed_municipalities"] == 2
    assert result["long_rows"] == 4
    assert result["distinct_account_codes"] == 2
    assert result["failed"] == []
    assert rows[0]["coluna"] == "Até o 3º Quadrimestre"
    assert rows[0]["fonte"] == "SICONFI_API"
