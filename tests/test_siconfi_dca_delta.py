import json
from pathlib import Path

import pipeline.acquire.siconfi_dca as module
from pipeline.acquire.siconfi_dca_delta import parse_codes
from pipeline.sources.siconfi import FetchResult


def make_geojson(path: Path):
    path.write_text(
        json.dumps(
            {
                "type": "FeatureCollection",
                "features": [
                    {"type": "Feature", "properties": {"id": "3500105", "name": "A"}},
                    {"type": "Feature", "properties": {"id": "3500204", "name": "B"}},
                    {"type": "Feature", "properties": {"id": "3500303", "name": "C"}},
                ],
            }
        ),
        encoding="utf-8",
    )


class FakeClient:
    def __init__(self, min_interval):
        self.request_count = 0

    def fetch_dca(self, *, year, entity_id, annex=None):
        self.request_count += 1
        return FetchResult(
            items=[{"cod_ibge": int(entity_id), "exercicio": year}],
            pages=1,
            request_count=1,
        )


def test_parse_codes_deduplicates_and_preserves_order():
    assert parse_codes("3500204, 3500105 3500204") == [
        "3500204",
        "3500105",
    ]


def test_parse_codes_accepts_labeled_workflow_paste():
    assert parse_codes(
        "year = 2018 codes = 3502408 3531407 min_interval = 1.05"
    ) == ["3502408", "3531407"]


def test_acquire_can_target_explicit_codes(tmp_path, monkeypatch):
    geo = tmp_path / "mun.json"
    make_geojson(geo)
    output = tmp_path / "raw"
    monkeypatch.setattr(module, "SiconfiClient", FakeClient)

    manifest = module.acquire(
        geo,
        [2022],
        output,
        annex="DCA-Anexo I-C",
        only_codes={"3500204"},
        min_interval=0,
    )

    assert manifest["municipalities_requested"] == 1
    assert manifest["completed_now"] == 1
    assert manifest["request_count"] == 1
    assert (output / "i-c" / "2022" / "3500204.json.gz").exists()
    assert not (output / "i-c" / "2022" / "3500105.json.gz").exists()


def test_acquire_rejects_unknown_explicit_code(tmp_path, monkeypatch):
    geo = tmp_path / "mun.json"
    make_geojson(geo)
    monkeypatch.setattr(module, "SiconfiClient", FakeClient)

    try:
        module.acquire(
            geo,
            [2022],
            tmp_path / "raw",
            only_codes={"3599999"},
            min_interval=0,
        )
    except ValueError as exc:
        assert "Unknown municipality codes" in str(exc)
    else:
        raise AssertionError("Expected ValueError for unknown municipality code")
