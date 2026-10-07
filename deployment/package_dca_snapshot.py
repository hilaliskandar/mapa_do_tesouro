from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import io
import json
import tarfile
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def gzip_deterministic(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    with source.open("rb") as src, target.open("wb") as raw:
        with gzip.GzipFile(
            filename="",
            mode="wb",
            fileobj=raw,
            mtime=0,
        ) as gz:
            for chunk in iter(lambda: src.read(1024 * 1024), b""):
                gz.write(chunk)


def tar_gzip_deterministic(source_dir: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    tar_buffer = io.BytesIO()
    with tarfile.open(fileobj=tar_buffer, mode="w") as tar:
        for path in sorted(
            p for p in source_dir.rglob("*") if p.is_file()
        ):
            relative = path.relative_to(source_dir).as_posix()
            info = tar.gettarinfo(str(path), arcname=relative)
            info.mtime = 0
            info.uid = 0
            info.gid = 0
            info.uname = ""
            info.gname = ""
            info.mode = 0o644
            with path.open("rb") as handle:
                tar.addfile(info, handle)

    tar_buffer.seek(0)
    with target.open("wb") as raw:
        with gzip.GzipFile(
            filename="",
            mode="wb",
            fileobj=raw,
            mtime=0,
        ) as gz:
            gz.write(tar_buffer.getvalue())


def validate_inputs(
    *,
    year: int,
    normalized_csv: Path,
    raw_root: Path,
    state_manifest: Path,
) -> dict:
    manifest = json.loads(state_manifest.read_text(encoding="utf-8"))
    if manifest["year"] != year:
        raise ValueError(f"Manifest year mismatch: {manifest['year']} != {year}")
    if manifest["municipalities_in_geojson"] != 645:
        raise ValueError("Manifest does not describe 645 municipalities")
    if manifest["municipalities_requested"] != 645:
        raise ValueError("Manifest did not request all 645 municipalities")
    if manifest["failed"]:
        raise ValueError(f"Acquisition failures present: {manifest['failed'][:10]}")

    with normalized_csv.open(
        encoding="utf-8-sig",
        newline="",
    ) as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 645:
        raise ValueError(f"Normalized rows mismatch: {len(rows)} != 645")
    codes = [row["cod_ibge"] for row in rows]
    if len(set(codes)) != 645:
        raise ValueError("Normalized CSV does not contain 645 unique codes")

    raw_files = list(raw_root.glob("**/*.json.gz"))
    if len(raw_files) != 1935:
        raise ValueError(f"Raw response count mismatch: {len(raw_files)} != 1935")

    actual_normalized = sha256(normalized_csv)
    if actual_normalized != manifest["normalized_sha256"]:
        raise ValueError(
            "Normalized SHA-256 mismatch: "
            f"{actual_normalized} != {manifest['normalized_sha256']}"
        )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Package an approved SP 645 DCA year for private R2 storage."
    )
    parser.add_argument("--year", type=int, required=True)
    parser.add_argument("--normalized-csv", type=Path, required=True)
    parser.add_argument("--raw-root", type=Path, required=True)
    parser.add_argument("--state-manifest", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    manifest = validate_inputs(
        year=args.year,
        normalized_csv=args.normalized_csv,
        raw_root=args.raw_root,
        state_manifest=args.state_manifest,
    )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    normalized_gz = args.output_dir / "normalized.csv.gz"
    raw_tgz = args.output_dir / "raw.tar.gz"
    public_manifest = args.output_dir / "manifest.json"

    gzip_deterministic(args.normalized_csv, normalized_gz)
    tar_gzip_deterministic(args.raw_root, raw_tgz)

    payload = {
        "snapshot_id": f"sp_645_dca_{args.year}",
        "status": "approved_gate_a_candidate",
        "universe_id": "SP_645",
        "year": args.year,
        "municipalities": 645,
        "annexes": manifest["annexes"],
        "normalized": {
            "object": f"sp_645/dca/{args.year}/normalized.csv.gz",
            "sha256": sha256(normalized_gz),
            "size_bytes": normalized_gz.stat().st_size,
            "uncompressed_sha256": sha256(args.normalized_csv),
        },
        "raw": {
            "object": f"sp_645/dca/{args.year}/raw.tar.gz",
            "sha256": sha256(raw_tgz),
            "size_bytes": raw_tgz.stat().st_size,
            "tree_sha256": manifest["raw_tree_sha256"],
            "files": 1935,
        },
        "source_manifest_sha256": sha256(args.state_manifest),
        "semantic_contract": "data/mappings/dca_canonical_v1.yml",
        "notes": [
            "Snapshot privado de aquisicao DCA estadual.",
            "Nao constitui, sozinho, release estadual publica.",
            "Ausencia permanece ausencia; nenhum vazio e promovido a zero.",
        ],
    }
    public_manifest.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
