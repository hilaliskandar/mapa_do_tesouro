import json
from pathlib import Path

import pipeline.acquire.siconfi_dca as module
from pipeline.sources.siconfi import FetchResult


def make_geojson(path: Path):
    path.write_text(
        json.dumps(
            {
                "type": "FeatureCollection",
                "features": [
                    {"type": "Feature", "properties": {"id": "3500105", "name": "A"}},
                    {"type": "Feature", "properties": {"id": "3500204", "name": "B"}},
                ],
            }
        ),
        encoding="utf-8",
    )


class FakeClient:
    request_count = 0

    def __init__(self, min_interval):
        self.request_count = 0

    def fetch_dca(self, *, year, entity_id, annex=None):
        self.request_count += 1
        return FetchResult(
            items=[{"cod_ibge": int(entity_id), "exercicio": year}],
            pages=1,
            request_count=1,
        )


def test_acquisition_reuses_valid_existing_artifacts(tmp_path, monkeypatch):
    geo = tmp_path / "mun.json"
    make_geojson(geo)
    output = tmp_path / "raw"
    monkeypatch.setattr(module, "SiconfiClient", FakeClient)

    first = module.acquire(
        geo,
        [2025],
        output,
        limit_codes=1,
        min_interval=0,
    )
    assert first["completed_now"] == 1
    assert first["reused"] == 0
    assert first["failed"] == []

    second = module.acquire(
        geo,
        [2025],
        output,
        limit_codes=1,
        min_interval=0,
    )
    assert second["completed_now"] == 0
    assert second["reused"] == 1
    assert second["request_count"] == 0
