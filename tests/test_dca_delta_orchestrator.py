import json
from pathlib import Path

import yaml

from pipeline.acquire.dca_delta_orchestrator import (
    classify_manifest,
    next_pending_year,
    update_queue_for_manifest,
)


def test_next_pending_year_uses_priority_then_year():
    queue = {
        "years": {
            2013: {
                "priority": 6,
                "codes": [1],
                "missing_by_annex": {"i_c": [1], "i_d": [], "i_e": []},
            },
            2016: {
                "priority": 3,
                "codes": [2, 3],
                "missing_by_annex": {"i_c": [3], "i_d": [2], "i_e": [2]},
            },
            2018: {
                "priority": None,
                "codes": [],
                "status": "source_confirmed_absence",
            },
        }
    }
    item = next_pending_year(queue)
    assert item["year"] == 2016
    assert item["pair_count"] == 3


def test_classify_all_empty_as_confirmed_absence():
    manifest = {
        "failed": [],
        "municipality_annex_pairs_requested": 3,
        "empty_source_pair_count": 3,
    }
    assert classify_manifest(manifest) == "source_confirmed_absence"


def test_classify_partial_recovery_as_pending_merge():
    manifest = {
        "failed": [],
        "municipality_annex_pairs_requested": 3,
        "empty_source_pair_count": 2,
    }
    assert classify_manifest(manifest) == "delta_recovered_pending_merge"


def test_update_queue_removes_year_from_automatic_queue():
    queue = {
        "years": {
            2016: {
                "priority": 3,
                "codes": [3543238, 3554607],
                "missing_by_annex": {
                    "i_c": [3554607],
                    "i_d": [3543238],
                    "i_e": [3543238],
                },
            }
        }
    }
    manifest = {
        "year": 2016,
        "failed": [],
        "codes": ["3543238", "3554607"],
        "municipality_annex_pairs_requested": 3,
        "empty_source_pair_count": 3,
        "normalized_sha256": "abc",
    }
    updated, classification = update_queue_for_manifest(
        queue,
        manifest,
        run_id="123",
    )
    entry = updated["years"][2016]
    assert classification == "source_confirmed_absence"
    assert entry["priority"] is None
    assert entry["codes"] == []
    assert entry["status"] == "source_confirmed_absence"
    assert entry["source_check"]["run_id"] == 123
