from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import os
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import yaml


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def list_buckets(account_id: str, token: str) -> list[str]:
    url = (
        "https://api.cloudflare.com/client/v4/accounts/"
        f"{account_id}/r2/buckets"
    )
    request = Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "User-Agent": "financas-municipais-sp-r2-fetch/1",
        },
    )
    with urlopen(request, timeout=60) as response:
        payload = yaml.safe_load(response.read().decode("utf-8"))
    if not payload.get("success"):
        raise RuntimeError("Cloudflare R2 bucket listing failed")
    return [item["name"] for item in payload.get("result", {}).get("buckets", [])]


def fetch_object(account_id: str, token: str, bucket: str, key: str) -> bytes:
    url = (
        "https://api.cloudflare.com/client/v4/accounts/"
        f"{account_id}/r2/buckets/{bucket}/objects/{key}"
    )
    request = Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "User-Agent": "financas-municipais-sp-r2-fetch/1",
        },
    )
    with urlopen(request, timeout=60) as response:
        if response.status != 200:
            raise RuntimeError(f"HTTP {response.status}: {key}")
        return response.read()


def discover_bucket(
    account_id: str,
    token: str,
    key: str,
    expected_size: int,
    expected_sha256: str,
) -> tuple[str, bytes]:
    matches: list[tuple[str, bytes]] = []
    for bucket in list_buckets(account_id, token):
        try:
            payload = fetch_object(account_id, token, bucket, key)
        except HTTPError as exc:
            if exc.code == 404:
                continue
            raise
        if len(payload) != expected_size:
            continue
        if sha256_bytes(payload) != expected_sha256:
            continue
        matches.append((bucket, payload))

    if len(matches) != 1:
        raise RuntimeError(
            "Expected exactly one private R2 bucket containing the "
            f"manifested object; found {len(matches)}."
        )
    return matches[0]


def validate_csv(csv_bytes: bytes, manifest: dict) -> dict:
    text = csv_bytes.decode("utf-8-sig")
    rows = list(csv.DictReader(text.splitlines()))
    if len(rows) != int(manifest["rows"]):
        raise ValueError(f"rows={len(rows)} != {manifest['rows']}")

    municipalities = {row["cod_ibge"] for row in rows}
    years = sorted({int(row["ano"]) for row in rows})
    expected_years = list(
        range(
            int(manifest["period"]["start"]),
            int(manifest["period"]["end"]) + 1,
        )
    )
    if len(municipalities) != int(manifest["universe"]["municipalities"]):
        raise ValueError(
            f"municipalities={len(municipalities)} "
            f"!= {manifest['universe']['municipalities']}"
        )
    if years != expected_years:
        raise ValueError(f"years={years} != {expected_years}")

    expected_columns = {
        "cod_ibge",
        "municipio",
        "ano",
        *manifest["variables"],
    }
    actual_columns = set(rows[0]) if rows else set()
    if actual_columns != expected_columns:
        raise ValueError(
            f"columns={sorted(actual_columns)} != {sorted(expected_columns)}"
        )

    pairs = {(row["cod_ibge"], int(row["ano"])) for row in rows}
    if len(pairs) != len(rows):
        raise ValueError("duplicate municipality-year pairs")

    return {
        "rows": len(rows),
        "municipalities": len(municipalities),
        "years": years,
        "variables": len(manifest["variables"]),
    }


def csv_to_xlsx(csv_bytes: bytes, output: Path, sheet_name: str) -> None:
    import openpyxl

    text = csv_bytes.decode("utf-8-sig")
    workbook = openpyxl.Workbook(write_only=True)
    worksheet = workbook.create_sheet(title=sheet_name)
    for row in csv.reader(text.splitlines()):
        worksheet.append(row)
    output.parent.mkdir(parents=True, exist_ok=True)
    workbook.save(output)


def fetch_snapshot(
    manifest_path: Path,
    *,
    account_id: str,
    token: str,
    bucket: str | None,
    csv_output: Path,
    xlsx_output: Path | None = None,
    sheet_name: str = "Base multifuentes",
) -> dict:
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    key = manifest["r2"]["object"]
    expected_size = int(manifest["compressed"]["size_bytes"])
    expected_sha = manifest["compressed"]["sha256"]

    if bucket:
        compressed = fetch_object(account_id, token, bucket, key)
    else:
        _, compressed = discover_bucket(
            account_id,
            token,
            key,
            expected_size,
            expected_sha,
        )
    if len(compressed) != expected_size:
        raise ValueError(
            f"compressed size={len(compressed)} "
            f"!= {manifest['compressed']['size_bytes']}"
        )
    compressed_sha = sha256_bytes(compressed)
    if compressed_sha != manifest["compressed"]["sha256"]:
        raise ValueError(
            f"compressed sha256={compressed_sha} "
            f"!= {manifest['compressed']['sha256']}"
        )

    csv_bytes = gzip.decompress(compressed)
    if len(csv_bytes) != int(manifest["csv"]["size_bytes"]):
        raise ValueError("csv size mismatch")
    csv_sha = sha256_bytes(csv_bytes)
    if csv_sha != manifest["csv"]["sha256"]:
        raise ValueError("csv sha256 mismatch")

    validation = validate_csv(csv_bytes, manifest)
    csv_output.parent.mkdir(parents=True, exist_ok=True)
    csv_output.write_bytes(csv_bytes)

    if xlsx_output is not None:
        csv_to_xlsx(csv_bytes, xlsx_output, sheet_name)

    return {
        **validation,
        "object": key,
        "compressed_sha256": compressed_sha,
        "csv_sha256": csv_sha,
        "csv_output": str(csv_output),
        "xlsx_output": str(xlsx_output) if xlsx_output else None,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Reconstrói e valida snapshot privado versionado no Cloudflare R2."
    )
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument(
        "--bucket",
        default=os.getenv("CLOUDFLARE_R2_BUCKET"),
        help="Optional. If omitted, the reader discovers the unique bucket containing the manifested object.",
    )
    parser.add_argument("--account-id", default=os.getenv("CLOUDFLARE_ACCOUNT_ID"))
    parser.add_argument("--token", default=os.getenv("CLOUDFLARE_API_TOKEN"))
    parser.add_argument("--csv-output", type=Path, required=True)
    parser.add_argument("--xlsx-output", type=Path)
    parser.add_argument("--sheet-name", default="Base multifuentes")
    args = parser.parse_args()

    if not args.account_id:
        raise SystemExit("CLOUDFLARE_ACCOUNT_ID/--account-id is required")
    if not args.token:
        raise SystemExit("CLOUDFLARE_API_TOKEN/--token is required")

    result = fetch_snapshot(
        args.manifest,
        account_id=args.account_id,
        token=args.token,
        bucket=args.bucket,
        csv_output=args.csv_output,
        xlsx_output=args.xlsx_output,
        sheet_name=args.sheet_name,
    )
    for key, value in result.items():
        print(f"{key}={value}")


if __name__ == "__main__":
    main()
