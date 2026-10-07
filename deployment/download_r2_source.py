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


def download_r2_object(
    *,
    account_id: str,
    api_token: str,
    bucket: str,
    object_key: str,
    output: Path,
) -> None:
    url = (
        "https://api.cloudflare.com/client/v4/accounts/"
        f"{account_id}/r2/buckets/{bucket}/objects/{object_key}"
    )
    request = Request(
        url,
        headers={
            "Authorization": f"Bearer {api_token}",
            "User-Agent": "financas-municipais-sp-ci/1",
        },
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    with urlopen(request, timeout=120) as response, output.open("wb") as target:
        if response.status != 200:
            raise SystemExit(f"R2 download failed: HTTP {response.status}")
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            target.write(chunk)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download a private canonical source object from Cloudflare R2."
    )
    parser.add_argument("--object-key", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--expected-sha256", required=True)
    args = parser.parse_args()

    required = {
        "CLOUDFLARE_ACCOUNT_ID": os.environ.get("CLOUDFLARE_ACCOUNT_ID"),
        "CLOUDFLARE_API_TOKEN": os.environ.get("CLOUDFLARE_API_TOKEN"),
        "CLOUDFLARE_R2_BUCKET": os.environ.get("CLOUDFLARE_R2_BUCKET"),
    }
    missing = [name for name, value in required.items() if not value]
    if missing:
        raise SystemExit("Missing configuration: " + ", ".join(missing))

    download_r2_object(
        account_id=required["CLOUDFLARE_ACCOUNT_ID"],
        api_token=required["CLOUDFLARE_API_TOKEN"],
        bucket=required["CLOUDFLARE_R2_BUCKET"],
        object_key=args.object_key,
        output=args.output,
    )

    actual = sha256(args.output)
    expected = args.expected_sha256.lower()
    if actual != expected:
        args.output.unlink(missing_ok=True)
        raise SystemExit(
            f"SHA-256 mismatch for {args.object_key}: {actual} != {expected}"
        )

    print(f"R2 canonical source verified: {args.object_key}")
    print(f"sha256={actual}")
    print(f"bytes={args.output.stat().st_size}")


if __name__ == "__main__":
    main()
