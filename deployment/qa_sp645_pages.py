from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


EXPECTED_YEARS = [2021, 2022, 2023, 2024, 2025]
EXPECTED_MUNICIPALITIES = 645
EXPECTED_CAPAG_OBSERVED = 645


def fail(message: str) -> None:
    raise SystemExit(message)


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate_payloads(metadata: dict, municipalities: list, annual_2025: dict, geo: dict) -> None:
    if metadata.get("municipality_count") != EXPECTED_MUNICIPALITIES:
        fail(f"municipality_count={metadata.get('municipality_count')}")
    if metadata.get("years") != EXPECTED_YEARS:
        fail(f"years={metadata.get('years')}")
    if len(municipalities) != EXPECTED_MUNICIPALITIES:
        fail(f"municipalities={len(municipalities)}")
    if len(geo.get("features", [])) != EXPECTED_MUNICIPALITIES:
        fail(f"map_features={len(geo.get('features', []))}")

    rows = annual_2025.get("municipalities", [])
    if len(rows) != EXPECTED_MUNICIPALITIES:
        fail(f"annual_2025_municipalities={len(rows)}")

    capag_observed = 0
    for row in rows:
        entry = row.get("values", {}).get("capag", {})
        if entry.get("status") == "observado":
            capag_observed += 1
    if capag_observed != EXPECTED_CAPAG_OBSERVED:
        fail(f"capag_observed={capag_observed}")


def validate_local(site: Path) -> None:
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
        site / "data" / "coverage.json",
        site / "data" / "coverage_sources.json",
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        fail("Missing files: " + ", ".join(missing))

    validate_payloads(
        read_json(site / "data" / "metadata.json"),
        read_json(site / "data" / "municipalities.json"),
        read_json(site / "data" / "annual" / "2025.json"),
        read_json(site / "data" / "maps" / "municipalities.geojson"),
    )

    headers = (site / "_headers").read_text(encoding="utf-8")
    for required_header in (
        "X-Frame-Options: DENY",
        "X-Content-Type-Options: nosniff",
        "Content-Security-Policy:",
    ):
        if required_header not in headers:
            fail(f"Missing header policy: {required_header}")

    app_js = (site / "app.js").read_text(encoding="utf-8")
    if "exportCurrentSliceCsv" not in app_js:
        fail("F116 export function missing")
    lowered = app_js.lower()
    for forbidden in ("workers.dev", "api.github.com"):
        if forbidden in lowered:
            fail(f"Unexpected runtime dependency: {forbidden}")

    print("SP645 local static-site QA: OK")


def fetch(url: str, *, attempts: int = 8, delay: float = 4.0):
    last_error = None
    for attempt in range(attempts):
        try:
            request = Request(url, headers={"User-Agent": "financas-municipais-sp-sp645-qa/1"})
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


def validate_remote(base_url: str) -> None:
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
    )

    print(f"SP645 remote deployment QA: OK ({base_url})")


def main() -> None:
    parser = argparse.ArgumentParser(description="QA for SP645 static preview deployments.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--site", type=Path)
    group.add_argument("--url")
    args = parser.parse_args()

    if args.site is not None:
        validate_local(args.site)
    else:
        validate_remote(args.url)


if __name__ == "__main__":
    main()
