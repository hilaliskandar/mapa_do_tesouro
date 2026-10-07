from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
from urllib.request import Request, urlopen


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def upload_r2_object(
    *,
    account_id: str,
    api_token: str,
    bucket: str,
    object_key: str,
    source: Path,
    content_type: str,
) -> None:
    url = (
        "https://api.cloudflare.com/client/v4/accounts/"
        f"{account_id}/r2/buckets/{bucket}/objects/{object_key}"
    )
    data = source.read_bytes()
    request = Request(
        url,
        data=data,
        method="PUT",
        headers={
            "Authorization": f"Bearer {api_token}",
            "Content-Type": content_type,
            "User-Agent": "financas-municipais-sp-ci/1",
        },
    )
    with urlopen(request, timeout=180) as response:
        if response.status not in (200, 201):
            raise SystemExit(
                f"R2 upload failed for {object_key}: HTTP {response.status}"
            )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Upload one approved canonical source object to private R2."
    )
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--object-key", required=True)
    parser.add_argument("--content-type", default="application/octet-stream")
    parser.add_argument("--expected-sha256")
    args = parser.parse_args()

    required = {
        "CLOUDFLARE_ACCOUNT_ID": os.environ.get("CLOUDFLARE_ACCOUNT_ID"),
        "CLOUDFLARE_API_TOKEN": os.environ.get("CLOUDFLARE_API_TOKEN"),
        "CLOUDFLARE_R2_BUCKET": os.environ.get("CLOUDFLARE_R2_BUCKET"),
    }
    missing = [name for name, value in required.items() if not value]
    if missing:
        raise SystemExit("Missing configuration: " + ", ".join(missing))

    if not args.source.is_file():
        raise SystemExit(f"Source does not exist: {args.source}")

    actual = sha256(args.source)
    if args.expected_sha256 and actual != args.expected_sha256.lower():
        raise SystemExit(
            f"SHA-256 mismatch before upload: {actual} != "
            f"{args.expected_sha256.lower()}"
        )

    upload_r2_object(
        account_id=required["CLOUDFLARE_ACCOUNT_ID"],
        api_token=required["CLOUDFLARE_API_TOKEN"],
        bucket=required["CLOUDFLARE_R2_BUCKET"],
        object_key=args.object_key,
        source=args.source,
        content_type=args.content_type,
    )

    print(f"R2 object uploaded: {args.object_key}")
    print(f"sha256={actual}")
    print(f"bytes={args.source.stat().st_size}")


if __name__ == "__main__":
    main()
