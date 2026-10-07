from __future__ import annotations

import base64
import gzip
import hashlib
from pathlib import Path

import yaml

from deployment.fetch_r2_snapshot import validate_csv

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "catalogs" / "sp_645_pilot_2020_2023.yml"


def test_sp645_pilot_manifest_contract():
    manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["universe"]["id"] == "SP_645"
    assert manifest["universe"]["municipalities"] == 645
    assert manifest["rows"] == 2580
    assert manifest["period"] == {"start": 2020, "end": 2023}
    assert len(manifest["r2"]["parts"]) == 8
    assert sum(part["chars"] for part in manifest["r2"]["parts"]) == 77136
    assert manifest["compressed"]["sha256"] == (
        "3f5ebf5a6482b7627cd2c1bd121c722e53e2632fed2340ae5ccae7e02290088a"
    )
    assert manifest["csv"]["sha256"] == (
        "1bc6b7a32585c111aa2d25f2cabe794ce6bf6550c2ba1e26ab136806b7a94626"
    )


def test_validate_csv_accepts_645_by_four_grid():
    manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    header = [
        "cod_ibge",
        "municipio",
        "ano",
        *manifest["variables"],
    ]
    lines = [",".join(header)]
    for municipality in range(645):
        code = f"35{municipality:05d}"
        for year in range(2020, 2024):
            row = [
                code,
                f"Municipio {municipality}",
                str(year),
                "1",
                "2",
                "3",
                "4",
                "5",
            ]
            lines.append(",".join(row))
    payload = ("\n".join(lines) + "\n").encode()
    result = validate_csv(payload, manifest)
    assert result == {
        "rows": 2580,
        "municipalities": 645,
        "years": [2020, 2021, 2022, 2023],
        "variables": 5,
    }
