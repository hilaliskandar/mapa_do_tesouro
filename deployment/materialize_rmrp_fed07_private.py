#!/usr/bin/env python3
"""Overlay vetted FED07 JSON onto a private site build only.

Usage:
python deployment/materialize_rmrp_fed07_private.py --site PRIVATE_SITE --source-zip FED07.zip
Requires PRIVATE_SITE/.rmrp-fed07-private-preview and PRIVATE_SITE/index.html.
Refuses writing into repository or public build roots.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import shutil
import tempfile
import zipfile
from pathlib import Path
from pipeline.qa.validate_rmrp_api_v3_fed07 import validate

PREFIX = Path("data/api/v3/investimentos/rmrp")
MARKER = ".rmrp-fed07-private-preview"

def materialize(site: Path, source_zip: Path, repo_root: Path | None = None) -> dict:
    site = site.resolve()
    if not (site / "index.html").is_file() or not (site / MARKER).is_file():
        raise RuntimeError("Private preview marker and site/index.html are mandatory")
    repo_root = (repo_root or Path(__file__).resolve().parents[1]).resolve()
    forbidden = [repo_root / "app" / "static", repo_root / "data",
                 repo_root / "deployment", repo_root]
    if any(site == x.resolve() or x.resolve() in site.parents for x in forbidden):
        raise RuntimeError("Refusing to write private source into repository/public build paths")
    with zipfile.ZipFile(source_zip) as z:
        if z.testzip() is not None:
            raise RuntimeError("ZIP CRC failure")
        members = [n for n in z.namelist()
                   if n.startswith(PREFIX.as_posix() + "/") and n.endswith(".json")]
        # 1 manifest + 1 municipality index + 34 municipalities + 19 years
        # + 218 projects + 1 pending + 1 subregions index + 4 subregions = 279.
        if len(members) != 279:
            raise RuntimeError("Incorrect number of JSON endpoints for FED07")
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            for name in members:
                target_file = (tmp / name).resolve()
                if not target_file.is_relative_to(tmp.resolve()):
                    raise RuntimeError("ZIP path escape")
                target_file.parent.mkdir(parents=True, exist_ok=True)
                with z.open(name) as src, target_file.open("wb") as dst:
                    shutil.copyfileobj(src, dst)
            stats = validate(tmp / PREFIX)
            if stats["public_release_authorized"]:
                raise RuntimeError("Unexpected publication authorization")
            target = site / PREFIX
            if target.exists():
                colliding = [f.relative_to(tmp / PREFIX) for f in (tmp / PREFIX).rglob("*.json")
                             if (target / f.relative_to(tmp / PREFIX)).exists()]
                if colliding:
                    raise RuntimeError(f"Destination contains FED07 file(s); refuse overwrite: {colliding[:3]}")
                for file in (tmp / PREFIX).rglob("*.json"):
                    dest = target / file.relative_to(tmp / PREFIX)
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(file, dest)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copytree(tmp / PREFIX, target)
    h = hashlib.sha256()
    with source_zip.open("rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b)
    report = {"private_preview": True, "source_sha256": h.hexdigest(),
              "json_count": len(members), "qa": stats,
              "publication_authorized": False}
    (site / "QA_FED07_PRIVATE_OVERLAY.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", type=Path, required=True)
    parser.add_argument("--source-zip", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(materialize(args.site, args.source_zip), ensure_ascii=False))
