import csv
import json

import pytest

from pipeline.build.export_dca_historical_v2 import EXPECTED_VARIABLES, export_history
from pipeline.build import stage_dca_history_v2 as bridge


def _history(tmp_path):
    source = tmp_path / "canonical.csv"
    with source.open("w", newline="", encoding="utf-8") as fp:
        writer = csv.DictWriter(fp, fieldnames=["cod_ibge", "ano", *EXPECTED_VARIABLES, "qa_issue_count"])
        writer.writeheader()
        for year in range(2013, 2026):
            for code in ("3500001", "3500002"):
                row = {"cod_ibge": code, "ano": year, "qa_issue_count": "0"}
                row.update({key: "0" for key in EXPECTED_VARIABLES})
                if year == 2013 and code == "3500001":
                    row["dca_iptu_principal"] = ""
                writer.writerow(row)
    history = tmp_path / "history"
    manifest = export_history(source, history, expected_municipalities=2)
    return history, manifest


def test_stage_historical_discovery_and_preserve_core_manifest(tmp_path, monkeypatch):
    history, manifest = _history(tmp_path)
    monkeypatch.setattr(bridge, "EXPECTED_SOURCE_SHA", manifest["source_sha256"])
    v2 = tmp_path / "site" / "data" / "api" / "v2"
    v2.mkdir(parents=True)
    (v2 / "manifest.json").write_text('{"existing":true}', encoding="utf-8")
    report = bridge.stage(history, v2, expected_municipalities=2)
    assert report["cells_verified"] == 2 * 13 * 26
    assert json.loads((v2 / "manifest.json").read_text()) == {"existing": True}
    sources = json.loads((v2 / "catalog" / "historical_sources.json").read_text())
    assert sources["publication_authorized"] is False
    assert sources["sources"][0]["years"] == list(range(2013, 2026))
    assert len(list((v2 / "history" / "dca" / "municipalities").glob("*.json"))) == 2


def test_stage_rejects_corrupt_content_before_writing(tmp_path, monkeypatch):
    history, manifest = _history(tmp_path)
    monkeypatch.setattr(bridge, "EXPECTED_SOURCE_SHA", manifest["source_sha256"])
    target = tmp_path / "site" / "data" / "api" / "v2"
    p = history / "municipalities" / "3500001.json"
    payload = json.loads(p.read_text())
    payload["years"]["2013"]["dca_iptu_principal"] = {"status": "observado", "value_decimal": "999"}
    p.write_text(json.dumps(payload))
    with pytest.raises(ValueError, match="Coverage mismatch"):
        bridge.stage(history, target, expected_municipalities=2)
    assert not target.exists()


def test_stage_rejects_existing_destination(tmp_path, monkeypatch):
    history, manifest = _history(tmp_path)
    monkeypatch.setattr(bridge, "EXPECTED_SOURCE_SHA", manifest["source_sha256"])
    target = tmp_path / "v2"
    (target / "history" / "dca").mkdir(parents=True)
    with pytest.raises(FileExistsError, match="overwrite"):
        bridge.stage(history, target, expected_municipalities=2)
