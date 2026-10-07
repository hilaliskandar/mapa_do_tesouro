from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

EXPECTED_SOURCE_SHA256 = "f51d8615f3742b1d414f1edff67805cac1a10cbc18764b454aab518de9c9e3f1"
EXPECTED_YEARS = list(range(2013, 2026))
EXPECTED_MUNICIPALITIES = 30
EXPECTED_VARIABLES = 75

SENTINELS_2025 = {
    "dc_pct_rcl": 0.9322,
    "dcl_pct_rcl": 0.8368,
    "dtp_pct_rcl": 0.3669,
}


def fail(message: str) -> None:
    raise SystemExit(message)


def validate_payloads(
    metadata: dict,
    municipalities: list,
    annual_2025: dict,
    geo: dict,
    *,
    expected_app_version: str | None = None,
) -> None:
    build = metadata.get("build", {})
    if expected_app_version is not None and build.get("app_version") != expected_app_version:
        fail(
            f"app_version={build.get('app_version')}, expected={expected_app_version}"
        )
    if build.get("data_sha256") != EXPECTED_SOURCE_SHA256:
        fail(f"Unexpected source hash: {build.get('data_sha256')}")
    if metadata.get("municipality_count") != EXPECTED_MUNICIPALITIES:
        fail(f"municipality_count={metadata.get('municipality_count')}")
    if metadata.get("variable_count") != EXPECTED_VARIABLES:
        fail(f"variable_count={metadata.get('variable_count')}")
    if metadata.get("years") != EXPECTED_YEARS:
        fail(f"years={metadata.get('years')}")
    if len(municipalities) != EXPECTED_MUNICIPALITIES:
        fail(f"municipalities={len(municipalities)}")
    if len(geo.get("features", [])) != EXPECTED_MUNICIPALITIES:
        fail(f"map_features={len(geo.get('features', []))}")

    americana = next(
        (item for item in annual_2025.get("municipalities", [])
         if item.get("codigo_ibge") == "3501608"),
        None,
    )
    if americana is None:
        fail("Americana 2025 not found")

    values = americana.get("values", {})
    for variable_id, expected in SENTINELS_2025.items():
        entry = values.get(variable_id, {})
        actual = entry.get("value")
        if entry.get("status") != "observado":
            fail(f"{variable_id} status={entry.get('status')}")
        if actual is None or abs(float(actual) - expected) > 1e-9:
            fail(f"{variable_id}={actual}, expected={expected}")


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate_local(site: Path, expected_app_version: str | None = None) -> None:
    required = [
        site / "index.html",
        site / "styles.css",
        site / "app.js",
        site / "_headers",
        site / "data" / "metadata.json",
        site / "data" / "manifest.json",
        site / "data" / "municipalities.json",
        site / "data" / "annual" / "2025.json",
        site / "data" / "maps" / "municipalities.geojson",
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        fail("Missing files: " + ", ".join(missing))

    validate_payloads(
        read_json(site / "data" / "metadata.json"),
        read_json(site / "data" / "municipalities.json"),
        read_json(site / "data" / "annual" / "2025.json"),
        read_json(site / "data" / "maps" / "municipalities.geojson"),
        expected_app_version=expected_app_version,
    )

    headers = (site / "_headers").read_text(encoding="utf-8")
    for required_header in (
        "X-Frame-Options: DENY",
        "X-Content-Type-Options: nosniff",
        "Content-Security-Policy:",
    ):
        if required_header not in headers:
            fail(f"Missing header policy: {required_header}")

    app_js = (site / "app.js").read_text(encoding="utf-8").lower()
    for forbidden in ("workers.dev", "api.github.com"):
        if forbidden in app_js:
            fail(f"Unexpected runtime dependency: {forbidden}")

    print("Local static-site QA: OK")


def fetch(url: str, *, attempts: int = 8, delay: float = 4.0):
    last_error = None
    for attempt in range(attempts):
        try:
            request = Request(url, headers={"User-Agent": "financas-municipais-sp-qa/1"})
            with urlopen(request, timeout=30) as response:
                return response.status, response.headers, response.read()
        except (HTTPError, URLError, TimeoutError) as exc:
            last_error = exc
            if attempt + 1 < attempts:
                time.sleep(delay)
    fail(f"Unable to fetch {url}: {last_error}")


def fetch_json(base_url: str, path: str):
    status, _, body = fetch(base_url.rstrip("/") + path)
    if status != 200:
        fail(f"{path}: HTTP {status}")
    return json.loads(body.decode("utf-8"))


def validate_remote(base_url: str, expected_app_version: str | None = None) -> None:
    status, headers, html = fetch(base_url.rstrip("/") + "/")
    if status != 200:
        fail(f"root: HTTP {status}")
    if b"Painel fiscal municipal" not in html:
        fail("root HTML does not contain expected title")

    normalized = {key.lower(): value for key, value in headers.items()}
    if normalized.get("x-frame-options", "").upper() != "DENY":
        fail("X-Frame-Options is not DENY")
    if normalized.get("x-content-type-options", "").lower() != "nosniff":
        fail("X-Content-Type-Options is not nosniff")
    if "default-src 'self'" not in normalized.get("content-security-policy", ""):
        fail("Content-Security-Policy missing expected default-src")

    validate_payloads(
        fetch_json(base_url, "/data/metadata.json"),
        fetch_json(base_url, "/data/municipalities.json"),
        fetch_json(base_url, "/data/annual/2025.json"),
        fetch_json(base_url, "/data/maps/municipalities.geojson"),
        expected_app_version=expected_app_version,
    )

    print(f"Remote deployment QA: OK ({base_url})")


def main() -> None:
    parser = argparse.ArgumentParser(description="QA for static Pages deployments.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--site", type=Path)
    group.add_argument("--url")
    parser.add_argument("--expected-app-version")
    args = parser.parse_args()

    if args.site is not None:
        validate_local(args.site, args.expected_app_version)
    else:
        validate_remote(args.url, args.expected_app_version)


if __name__ == "__main__":
    main()
