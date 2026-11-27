from __future__ import annotations

import argparse
import json
import math
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


EXPECTED_YEARS = [2021, 2022, 2023, 2024, 2025]
EXPECTED_MUNICIPALITIES = 645
EXPECTED_CAPAG_OBSERVED = 645
EXPECTED_PUBLICATION_UNIVERSES = {
    "RM_SAO_PAULO": 38,
    "RM_BAIXADA_SANTISTA": 9,
    "RM_CAMPINAS": 20,
    "RM_VALE_PARAIBA_LITORAL_NORTE": 39,
    "RM_SOROCABA": 27,
    "RM_RIBEIRAO_PRETO": 34,
    "RM_SAO_JOSE_RIO_PRETO": 37,
    "RM_JUNDIAI": 7,
    "RM_PIRACICABA": 24,
    "AU_FRANCA": 19,
    "CIDADES_MEDIAS": 33,
}

def expected_administrative_universes() -> dict[str, int]:
    """Derive RA/RG counts from the versioned municipal direct-source dimension."""
    import csv
    from collections import Counter
    source = (
        Path(__file__).resolve().parents[1]
        / "governance"
        / "DIM_SP645_IBGE_RA_RG_SEMIL_SEADE_2026_11_14.csv"
    )
    with source.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter=";"))
    if len(rows) != 645 or len({r["codigo_ibge"] for r in rows}) != 645:
        raise ValueError("Invalid official municipality source; expected 645 IBGE7")
    ra = Counter(r["ra_codigo"] for r in rows)
    rg = Counter(r["rg_codigo"] for r in rows)
    if len(ra) != 16 or len(rg) != 43:
        raise ValueError("Unexpected RA/RG source cardinality")
    expected = {
        **{f"RA_SEADE_{int(code):02d}": number for code, number in ra.items()},
        **{f"RG_SEADE_{int(code):02d}": number for code, number in rg.items()},
    }
    if len(expected) != 59 or sum(expected.values()) != 1290:
        raise ValueError("RA/RG municipality membership conservation error")
    return expected


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

EXPECTED_UNIVERSES.update(expected_administrative_universes())


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


TRANSFEREGOV_ALLOWED_STAGES = {"desembolso", "pagamento"}
TRANSFEREGOV_RECORD_FIELDS = {
    "codigo_ibge", "municipio", "year", "stage", "event_count",
    "instrument_count", "net_amount_brl", "negative_events", "zero_events",
}
TRANSFEREGOV_FORBIDDEN_FIELDS = {
    "nr_mov_fin", "nr_convenio", "convenio", "id_dl", "nr_dl",
    "fornecedor", "nome_fornecedor", "identif_fornecedor", "row_number",
}


def validate_transferegov_financial(document: dict) -> None:
    if document.get("schema_version") != "1.0.0":
        fail("Transferegov aggregate schema_version mismatch")
    if document.get("universe") != "SP_645" or document.get("municipality_count") != 645:
        fail("Transferegov aggregate universe mismatch")

    municipality_rows = document.get("municipalities")
    if not isinstance(municipality_rows, list) or len(municipality_rows) != 645:
        fail("Transferegov municipality dimension must contain 645 rows")
    municipalities = {}
    for item in municipality_rows:
        if not isinstance(item, dict) or set(item) != {"codigo_ibge", "municipio"}:
            fail("Transferegov municipality dimension contains unexpected fields")
        code = item["codigo_ibge"]
        name = item["municipio"]
        if not isinstance(code, str) or len(code) != 7 or not code.isdigit():
            fail("Transferegov municipality code is invalid")
        if not isinstance(name, str) or not name.strip() or code in municipalities:
            fail("Transferegov municipality dimension has invalid or duplicate rows")
        municipalities[code] = name

    years = document.get("years")
    if (not isinstance(years, list) or not years or
            any(not isinstance(year, int) or year < 2000 or year > 2100 for year in years) or
            years != sorted(set(years))):
        fail("Transferegov aggregate years are invalid")

    records = document.get("records")
    if not isinstance(records, list) or not records:
        fail("Transferegov aggregate records are missing")
    seen = set()
    sums = {stage: 0 for stage in TRANSFEREGOV_ALLOWED_STAGES}
    municipality_coverage = {stage: set() for stage in TRANSFEREGOV_ALLOWED_STAGES}
    issue_counts = {"negative_events": 0, "zero_events": 0}
    per_year_stage = {}
    for row in records:
        if not isinstance(row, dict) or set(row) != TRANSFEREGOV_RECORD_FIELDS:
            fail("Transferegov record is not a municipality-year-stage aggregate")
        if set(key.casefold() for key in row).intersection(TRANSFEREGOV_FORBIDDEN_FIELDS):
            fail("Transferegov aggregate contains a forbidden identifying field")
        code = row["codigo_ibge"]
        year = row["year"]
        stage = row["stage"]
        if code not in municipalities or row["municipio"] != municipalities[code]:
            fail("Transferegov aggregate municipality does not match the dimension")
        if year not in years or stage not in TRANSFEREGOV_ALLOWED_STAGES:
            fail("Transferegov aggregate has an unexpected year or stage")
        key = (code, year, stage)
        if key in seen:
            fail("Transferegov aggregate contains duplicate municipality-year-stage keys")
        seen.add(key)
        for field in ("event_count", "instrument_count", "negative_events", "zero_events"):
            value = row[field]
            if not isinstance(value, int) or value < 0:
                fail(f"Transferegov aggregate field {field} is invalid")
        if row["event_count"] < 1 or row["instrument_count"] > row["event_count"]:
            fail("Transferegov aggregate counts are inconsistent")
        amount = row["net_amount_brl"]
        if not isinstance(amount, (int, float)) or not math.isfinite(amount):
            fail("Transferegov aggregate amount is invalid")
        sums[stage] += row["event_count"]
        municipality_coverage[stage].add(code)
        issue_counts["negative_events"] += row["negative_events"]
        issue_counts["zero_events"] += row["zero_events"]
        metric = (year, stage)
        current = per_year_stage.setdefault(metric, {"events": 0, "municipalities": set()})
        current["events"] += row["event_count"]
        current["municipalities"].add(code)

    if sums != {"desembolso": 47392, "pagamento": 945970}:
        fail("Transferegov aggregate event totals differ from the audited snapshot")
    if {stage: len(codes) for stage, codes in municipality_coverage.items()} != {
        "desembolso": 645, "pagamento": 644
    }:
        fail("Transferegov aggregate municipal coverage differs from the audited snapshot")
    if issue_counts != {"negative_events": 5, "zero_events": 2194}:
        fail("Transferegov aggregate negative/zero payment counts differ from QA")

    coverage = document.get("coverage")
    if not isinstance(coverage, list) or len(coverage) != len(years) * len(TRANSFEREGOV_ALLOWED_STAGES):
        fail("Transferegov aggregate coverage table is incomplete")
    coverage_seen = set()
    for item in coverage:
        if not isinstance(item, dict) or set(item) != {
            "year", "stage", "expected_municipalities",
            "municipalities_with_events", "event_count",
        }:
            fail("Transferegov coverage contains unexpected fields")
        key = (item["year"], item["stage"])
        if key in coverage_seen or key not in per_year_stage:
            fail("Transferegov coverage has duplicate or unsupported year-stage rows")
        coverage_seen.add(key)
        actual = per_year_stage[key]
        if (item["expected_municipalities"] != 645 or
                item["municipalities_with_events"] != len(actual["municipalities"]) or
                item["event_count"] != actual["events"]):
            fail("Transferegov coverage does not reconcile to aggregate records")
    if coverage_seen != set(per_year_stage):
        fail("Transferegov coverage does not reconcile to all year-stage pairs")

    source = document.get("source")
    if not isinstance(source, dict) or source.get("snapshot_archive_sha256") != (
        "d7c0d8758fca9434e5c348e8f2be8905d443b1737ecc31b6aaffa33ddeaf77cc"
    ):
        fail("Transferegov aggregate source snapshot hash mismatch")
    if not isinstance(document.get("interpretation"), list):
        fail("Transferegov interpretation notes are missing")
    if "municipio proponente" not in document.get("geographic_basis", ""):
        fail("Transferegov geographic basis must identify the proponent municipality")
    if "nao aditivas" not in document.get("stage_policy", ""):
        fail("Transferegov stage policy must prohibit summing stages")


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
        site / "data" / "api" / "v1" / "publication" / "contract.json",
        site / "data" / "api" / "v1" / "publication" / "universes.json",
        site / "data" / "transferegov" / "financial_sp645.json",
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
    validate_transferegov_financial(read_json(site / "data" / "transferegov" / "financial_sp645.json"))

    universes = read_json(site / "data" / "universes.json")
    _validate_universe_catalog(universes)

    publication = read_json(
        site / "data" / "api" / "v1" / "publication" / "universes.json"
    )
    publication_counts = {
        item["publication_id"]: item["member_count"] for item in publication
    }
    if publication_counts != EXPECTED_PUBLICATION_UNIVERSES:
        fail(f"publication_universes={publication_counts}")
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

    validate_transferegov_financial(fetch_json(base_url, "/data/transferegov/financial_sp645.json"))

    universes = fetch_json(base_url, "/data/universes.json")
    _validate_universe_catalog(universes)

    publication = fetch_json(
        base_url, "/data/api/v1/publication/universes.json"
    )
    publication_counts = {
        item["publication_id"]: item["member_count"] for item in publication
    }
    if publication_counts != EXPECTED_PUBLICATION_UNIVERSES:
        fail(f"remote publication_universes={publication_counts}")
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
