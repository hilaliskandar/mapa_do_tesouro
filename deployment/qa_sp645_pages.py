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
EXPECTED_UNIVERSES = {
    "SP_645": 645,
    "TIC_TIM_30": 30,
    "CIDADES_MEDIAS": 33,
    "AU_FRANCA": 19,
    "RM_BAIXADA_SANTISTA": 9,
    "RM_CAMPINAS": 20,
    "RM_JUNDIAI": 7,
    "RM_PIRACICABA": 24,
    "RM_RIBEIRAO_PRETO": 34,
    "RM_SOROCABA": 27,
    "RM_SAO_JOSE_RIO_PRETO": 37,
    "RM_SAO_PAULO": 39,
    "RM_VALE_PARAIBA_LITORAL_NORTE": 39,
}


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


def _validate_universe_catalog(universes: list) -> None:
    actual = {
        item.get("universo_id"): item.get("municipality_count")
        for item in universes
    }
    if actual != EXPECTED_UNIVERSES:
        fail(f"universes={actual}")
    defaults = [item["universo_id"] for item in universes if item.get("default")]
    if defaults != ["SP_645"]:
        fail(f"default_universe={defaults}")


def _universe_path(item: dict) -> str:
    data_path = item.get("data_path")
    if data_path == ".":
        return "/data"
    return f"/data/{data_path}"


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
        site / "data" / "universes.json",
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

    universes = read_json(site / "data" / "universes.json")
    _validate_universe_catalog(universes)
    for item in universes:
        base = site / "data"
        if item["data_path"] != ".":
            base = base / item["data_path"]
        metadata = read_json(base / "metadata.json")
        municipalities = read_json(base / "municipalities.json")
        geo = read_json(base / "maps" / "municipalities.geojson")
        expected = EXPECTED_UNIVERSES[item["universo_id"]]
        if metadata.get("universe", {}).get("universo_id") != item["universo_id"]:
            fail(f"metadata universe mismatch: {item['universo_id']}")
        if metadata.get("municipality_count") != expected:
            fail(f"{item['universo_id']} municipality_count={metadata.get('municipality_count')}")
        if len(municipalities) != expected:
            fail(f"{item['universo_id']} municipalities={len(municipalities)}")
        if len(geo.get("features", [])) != expected:
            fail(f"{item['universo_id']} map_features={len(geo.get('features', []))}")

    headers = (site / "_headers").read_text(encoding="utf-8")
    for required_header in (
        "X-Frame-Options: DENY",
        "X-Content-Type-Options: nosniff",
        "Content-Security-Policy:",
    ):
        if required_header not in headers:
            fail(f"Missing header policy: {required_header}")

    html = (site / "index.html").read_text(encoding="utf-8")
    app_js = (site / "app.js").read_text(encoding="utf-8")
    if 'id="universe-select"' not in html:
        fail("Universe selector missing")
    if "loadUniverse" not in app_js or "./data/universes.json" not in app_js:
        fail("Multi-universe frontend contract missing")
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


def fetch_json(base_url: str, path: str, *, attempts: int = 8, delay: float = 4.0):
    url = base_url.rstrip("/") + path
    last_error = None
    for attempt in range(attempts):
        status, _, body = fetch(url, attempts=1)
        if status != 200:
            last_error = f"HTTP {status}"
        else:
            try:
                return json.loads(body.decode("utf-8"))
            except (json.JSONDecodeError, UnicodeDecodeError) as exc:
                last_error = exc
        if attempt + 1 < attempts:
            time.sleep(delay)
    fail(f"Unable to decode JSON from {path}: {last_error}")


def validate_remote(base_url: str) -> None:
    status, headers, html = fetch(base_url.rstrip("/") + "/")
    if status != 200:
        fail(f"root: HTTP {status}")
    if b"Painel fiscal municipal" not in html:
        fail("root HTML does not contain expected title")
    if b'id="universe-select"' not in html:
        fail("root HTML does not expose universe selector")

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

    universes = fetch_json(base_url, "/data/universes.json")
    _validate_universe_catalog(universes)
    for item in universes:
        base = _universe_path(item)
        metadata = fetch_json(base_url, base + "/metadata.json")
        municipalities = fetch_json(base_url, base + "/municipalities.json")
        geo = fetch_json(base_url, base + "/maps/municipalities.geojson")
        expected = EXPECTED_UNIVERSES[item["universo_id"]]
        if metadata.get("universe", {}).get("universo_id") != item["universo_id"]:
            fail(f"remote metadata universe mismatch: {item['universo_id']}")
        if metadata.get("municipality_count") != expected:
            fail(f"remote {item['universo_id']} municipality_count={metadata.get('municipality_count')}")
        if len(municipalities) != expected:
            fail(f"remote {item['universo_id']} municipalities={len(municipalities)}")
        if len(geo.get("features", [])) != expected:
            fail(f"remote {item['universo_id']} map_features={len(geo.get('features', []))}")

    status, _, app_js = fetch(base_url.rstrip("/") + "/app.js")
    if status != 200 or b"loadUniverse" not in app_js:
        fail("remote app.js missing multi-universe loader")

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
