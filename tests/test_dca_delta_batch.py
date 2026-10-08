from pathlib import Path

import yaml

from pipeline.acquire.dca_delta_batch import run_batch


def test_batch_stops_when_recovered_data_requires_review(tmp_path, monkeypatch):
    queue = {
        "policy": {"max_codes_per_run": 100},
        "years": {
            2013: {
                "priority": 1,
                "codes": [3514106],
                "missing_by_annex": {"i_c": [3514106], "i_d": [], "i_e": []},
            },
            2014: {
                "priority": 2,
                "codes": [3500550],
                "missing_by_annex": {"i_c": [3500550], "i_d": [], "i_e": []},
            },
        },
    }
    queue_path = tmp_path / "queue.yml"
    queue_path.write_text(yaml.safe_dump(queue), encoding="utf-8")
    geojson = tmp_path / "sp.geojson"
    geojson.write_text('{"features":[]}', encoding="utf-8")

    calls = []

    def fake_acquire(geojson, year, plan, output, normalized_csv, **kwargs):
        calls.append(year)
        output.mkdir(parents=True, exist_ok=True)
        normalized_csv.parent.mkdir(parents=True, exist_ok=True)
        normalized_csv.write_text("cod_ibge,ano\n", encoding="utf-8")
        requested = sum(len(v) for v in plan.values())
        empty = requested if year == 2013 else 0
        return {
            "year": year,
            "failed": [],
            "codes": [str(c) for values in plan.values() for c in values],
            "municipalities_requested": 1,
            "municipality_annex_pairs_requested": requested,
            "empty_source_pair_count": empty,
            "normalized_sha256": f"sha-{year}",
        }

    monkeypatch.setattr(
        "pipeline.acquire.dca_delta_batch.acquire_delta_plan",
        fake_acquire,
    )

    result = run_batch(
        queue_path,
        geojson,
        tmp_path / "raw",
        tmp_path / "normalized",
        tmp_path / "qa",
        run_id="1",
        max_cycles=10,
    )

    assert calls == [2013, 2014]
    assert result["stopped_for_review"] is True
    updated = yaml.safe_load(queue_path.read_text(encoding="utf-8"))
    assert updated["years"][2013]["status"] == "source_confirmed_absence"
    assert updated["years"][2014]["status"] == "delta_recovered_pending_merge"
