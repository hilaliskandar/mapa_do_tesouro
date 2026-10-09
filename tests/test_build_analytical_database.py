from pathlib import Path

import pipeline.build.build_analytical_database as module


def test_build_propagates_active_universe(monkeypatch, tmp_path):
    calls = []

    def fake_import(workbook, database, **kwargs):
        calls.append(("ingest", kwargs.get("universe_id")))
        return {"universe_id": "SP_TESTE"}

    monkeypatch.setattr(module, "import_multifuentes", fake_import)
    monkeypatch.setattr(
        module,
        "load_documentation",
        lambda database, strict=True: calls.append(("documentation", strict)),
    )
    monkeypatch.setattr(
        module,
        "calculate_annual",
        lambda database: calls.append(("annual", None)) or {},
    )
    monkeypatch.setattr(
        module,
        "refresh_coverage",
        lambda database, universe_id: calls.append(("coverage", universe_id)) or {},
    )
    monkeypatch.setattr(
        module,
        "calculate_window_statistics",
        lambda database, universe_id: calls.append(("window", universe_id)) or {},
    )
    monkeypatch.setattr(
        module,
        "calculate_typologies",
        lambda database, universe_id: calls.append(("typologies", universe_id)) or {},
    )
    monkeypatch.setattr(
        module,
        "calculate_markers",
        lambda database, universe_id: calls.append(("markers", universe_id)) or {},
    )
    monkeypatch.setattr(
        module,
        "calculate_pairs",
        lambda database, universe_id: calls.append(("pairs", universe_id)) or {},
    )
    monkeypatch.setattr(
        module,
        "export_static_data",
        lambda database, output, universe_id: calls.append(("static", universe_id)) or {},
    )
    monkeypatch.setattr(
        module,
        "build_static_site",
        lambda database, output, source_geojson=None, universe_id=None:
            calls.append(("site", universe_id)) or {},
    )

    module.build_analytical_database(
        Path("input.xlsx"),
        tmp_path / "db.sqlite",
        overwrite=True,
        static_output=tmp_path / "static",
        site_output=tmp_path / "site",
        source_geojson=Path("map.geojson"),
        universe_id="SP_OVERRIDE",
    )

    assert ("ingest", "SP_OVERRIDE") in calls
    for stage in ("coverage", "window", "typologies", "markers", "pairs", "static", "site"):
        assert (stage, "SP_TESTE") in calls
