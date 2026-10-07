from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
FRONTEND = ROOT / "app" / "static"

HEADERS = """/*
  X-Frame-Options: DENY
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=()
  Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'none'; form-action 'self'

/data/*
  Cache-Control: public, max-age=3600, must-revalidate

/*.js
  Cache-Control: public, max-age=3600, must-revalidate

/*.css
  Cache-Control: public, max-age=3600, must-revalidate
"""


def fetch(base_url: str, relative: str, *, attempts: int = 6) -> bytes:
    url = base_url.rstrip("/") + "/" + relative.lstrip("/")
    last_error = None
    for attempt in range(attempts):
        try:
            request = Request(url, headers={"User-Agent": "financas-municipais-sp-materializer/1"})
            with urlopen(request, timeout=30) as response:
                if response.status != 200:
                    raise RuntimeError(f"HTTP {response.status}: {url}")
                return response.read()
        except (HTTPError, URLError, TimeoutError, RuntimeError) as exc:
            last_error = exc
            if attempt + 1 < attempts:
                time.sleep(3)
    raise SystemExit(f"Unable to fetch {url}: {last_error}")


def write_bytes(output: Path, relative: str, content: bytes) -> None:
    target = output / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(content)


def fetch_json(base_url: str, relative: str):
    return json.loads(fetch(base_url, relative).decode("utf-8"))


def write_json(path: Path, payload) -> str:
    content = json.dumps(
        payload,
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
        separators=(",", ": "),
    ) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def materialize(base_url: str, output: Path, app_version: str) -> None:
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)

    municipalities = fetch_json(base_url, "data/municipalities.json")
    metadata = fetch_json(base_url, "data/metadata.json")
    manifest = fetch_json(base_url, "data/manifest.json")
    variables = fetch_json(base_url, "data/catalog/variables.json")
    methodology = fetch_json(base_url, "data/methodology/index.json")

    fixed = [
        "data/municipalities.json",
        "data/crosswalk.json",
        "data/coverage.json",
        "data/references.json",
        "data/catalog/variables.json",
        "data/methodology/index.json",
        "data/maps/municipalities.geojson",
    ]
    for relative in fixed:
        write_bytes(output, relative, fetch(base_url, relative))

    for year in metadata["years"]:
        relative = f"data/annual/{year}.json"
        write_bytes(output, relative, fetch(base_url, relative))

    for municipality in municipalities:
        relative = f"data/municipalities/{municipality['codigo_ibge']}.json"
        write_bytes(output, relative, fetch(base_url, relative))

    for variable in variables:
        relative = f"data/catalog/variables/{variable['variavel_id']}.json"
        write_bytes(output, relative, fetch(base_url, relative))

    for section in methodology:
        relative = f"data/methodology/{section['secao_id']}.json"
        write_bytes(output, relative, fetch(base_url, relative))

    metadata.setdefault("build", {})["app_version"] = app_version
    metadata_hash = write_json(output / "data" / "metadata.json", metadata)

    manifest.setdefault("build", {})["app_version"] = app_version
    manifest.setdefault("files", {})["metadata.json"] = metadata_hash
    write_json(output / "data" / "manifest.json", manifest)

    for filename in ("index.html", "styles.css", "app.js"):
        shutil.copy2(FRONTEND / filename, output / filename)
    (output / "_headers").write_text(HEADERS, encoding="utf-8")

    print(
        {
            "source": base_url,
            "app_version": app_version,
            "municipalities": len(municipalities),
            "variables": len(variables),
            "methodology_sections": len(methodology),
            "output": str(output),
        }
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Materialize an existing static Pages snapshot and overlay the checked-out frontend."
    )
    parser.add_argument("--url", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--app-version", required=True)
    args = parser.parse_args()
    materialize(args.url, args.output, args.app_version)


if __name__ == "__main__":
    main()
