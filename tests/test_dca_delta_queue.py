from pathlib import Path

import pytest

from pipeline.acquire.dca_delta_queue import resolve_year


def test_resolve_year_returns_versioned_codes(tmp_path: Path):
    queue = tmp_path / "queue.yml"
    queue.write_text(
        """
policy:
  max_codes_per_run: 100
years:
  2018:
    priority: 1
    codes: [3502408, 3531407]
    missing_by_annex:
      i_c: [3502408, 3531407]
      i_d: [3502408, 3531407]
      i_e: [3502408, 3531407]
""".strip(),
        encoding="utf-8",
    )
    result = resolve_year(queue, 2018)
    assert result["codes"] == ["3502408", "3531407"]
    assert result["codes_arg"] == "3502408 3531407"
    assert result["priority"] == 1
    assert result["pair_count"] == 6
    assert result["plan"] == {
        "i_c": ["3502408", "3531407"],
        "i_d": ["3502408", "3531407"],
        "i_e": ["3502408", "3531407"],
    }


def test_resolve_year_rejects_resolved_year(tmp_path: Path):
    queue = tmp_path / "queue.yml"
    queue.write_text(
        """
years:
  2022:
    codes: []
    status: resolved_by_local_revenue_supplement
""".strip(),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="no queued external delta codes"):
        resolve_year(queue, 2022)



def test_resolve_year_preserves_annex_specific_missing_pairs(tmp_path: Path):
    queue = tmp_path / "queue.yml"
    queue.write_text(
        """
policy:
  max_codes_per_run: 100
years:
  2016:
    priority: 3
    codes: [3543238, 3554607]
    missing_by_annex:
      i_c: [3554607]
      i_d: [3543238]
      i_e: [3543238]
""".strip(),
        encoding="utf-8",
    )
    result = resolve_year(queue, 2016)
    assert result["pair_count"] == 3
    assert result["plan"] == {
        "i_c": ["3554607"],
        "i_d": ["3543238"],
        "i_e": ["3543238"],
    }
