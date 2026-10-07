import json
from pathlib import Path

import pipeline.acquire.siconfi_dca_state as module


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


def test_state_year_orchestrates_three_annexes_and_hashes_output(
    tmp_path, monkeypatch
):
    geo = tmp_path / "sp.geojson"
    make_geojson(geo)
    output = tmp_path / "raw"
    normalized = tmp_path / "normalized.csv"
    calls = []

    def fake_acquire(
        geojson,
        years,
        raw_output,
        *,
        annex,
        limit_codes,
        min_interval,
    ):
        calls.append((annex, tuple(years), limit_codes, min_interval))
        manifest_path = raw_output / "manifests" / f"{len(calls)}.json"
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text("{}\n", encoding="utf-8")
        return {
            "completed_now": 2,
            "reused": 0,
            "request_count": 2,
            "failed": [],
            "manifest_path": str(manifest_path),
        }

    def fake_normalize_tree(raw_root, output_csv):
        output_csv.parent.mkdir(parents=True, exist_ok=True)
        output_csv.write_text(
            "cod_ibge,ano,dca_receita_corrente_bruta\n"
            "3500105,2025,1\n"
            "3500204,2025,2\n",
            encoding="utf-8",
        )
        return {
            "rows": 2,
            "variables": 1,
            "issues": 0,
            "output": str(output_csv),
        }

    monkeypatch.setattr(module, "acquire", fake_acquire)
    monkeypatch.setattr(module, "normalize_tree", fake_normalize_tree)

    result = module.acquire_state_year(
        geo,
        2025,
        output,
        normalized,
        min_interval=0,
        expected_municipalities=2,
    )

    assert [call[0] for call in calls] == list(module.ANNEXES)
    assert result["municipalities_requested"] == 2
    assert result["normalization"]["rows"] == 2
    assert result["failed"] == []
    assert len(result["normalized_sha256"]) == 64
    assert len(result["raw_tree_sha256"]) == 64
    assert Path(result["manifest_path"]).exists()


def test_state_year_rejects_wrong_municipality_universe(tmp_path):
    geo = tmp_path / "sp.geojson"
    make_geojson(geo)

    try:
        module.acquire_state_year(
            geo,
            2025,
            tmp_path / "raw",
            tmp_path / "normalized.csv",
            expected_municipalities=645,
        )
    except ValueError as exc:
        assert "Unexpected municipality count" in str(exc)
    else:
        raise AssertionError("Expected municipality-universe validation failure.")
