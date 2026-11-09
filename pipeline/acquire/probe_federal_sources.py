#!/usr/bin/env python3
"""FED00: read-only smoke probes for federal public APIs, without modifying canonical data.

Only retrieves bounded metadata or a few latest observations. Uses no credentials.
No municipio-wide enumeration, no R2 write, no SQLite migrations and no deployment.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

USER_AGENT = "mapa-do-tesouro-FED00-source-probe/1.0 (public-data)"
PROBES = (
    ("bcb_sgs_ipca_433", "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados/ultimos/3?formato=json", "sgs"),
    ("bcb_sgs_selic_meta_432", "https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados/ultimos/3?formato=json", "sgs"),
    ("transferegov_parcerias_openapi", "https://api-publica.transferegov.gestao.gov.br/parcerias/openapi.json", "openapi"),
    ("transferegov_discricionarias_openapi", "https://api-publica.transferegov.gestao.gov.br/discricionarias/openapi.json", "openapi"),
    ("stn_transferencias_ckan", "https://www.tesourotransparente.gov.br/ckan/api/3/action/package_show?id=transferencias-constitucionais-para-municipios", "ckan"),
)

def request_json(url: str, *, timeout: int = 25, max_bytes: int = 3_000_000) -> tuple[object, bytes]:
    request = Request(url, headers={"Accept": "application/json", "User-Agent": USER_AGENT})
    with urlopen(request, timeout=timeout) as response:
        if response.status != 200:
            raise ValueError(f"unexpected_http_status={response.status}")
        raw = response.read(max_bytes + 1)
        if len(raw) > max_bytes:
            raise ValueError(f"response_exceeded_limit={max_bytes}")
        return json.loads(raw.decode("utf-8-sig")), raw

def inspect(kind: str, data: object) -> dict:
    if kind == "sgs":
        if not isinstance(data, list) or not data:
            raise ValueError("empty_or_invalid_sgs_array")
        if any(not isinstance(item, dict) or not {"data", "valor"}.issubset(item) for item in data):
            raise ValueError("unexpected_sgs_schema")
        return {"records": len(data), "first_date": data[0]["data"], "last_date": data[-1]["data"],
                "schema_fields": ["data", "valor"], "value_semantics": "source_specific_no_reinterpretation"}
    if kind == "openapi":
        if not isinstance(data, dict) or not isinstance(data.get("paths"), dict):
            raise ValueError("unexpected_openapi_schema")
        return {"paths_count": len(data["paths"]), "openapi_version": str(data.get("openapi", "")),
                "sample_paths": sorted(data["paths"])[:8]}
    if kind == "ckan":
        if not isinstance(data, dict) or data.get("success") is not True or not isinstance(data.get("result"), dict):
            raise ValueError("unexpected_ckan_response")
        rs = data["result"].get("resources") or []
        return {"resources": len(rs), "formats": sorted({str(x.get("format", "")).upper() for x in rs if isinstance(x, dict)}),
                "sample_resource_names": [str(x.get("name", "")) for x in rs[:5] if isinstance(x, dict)]}
    raise ValueError("unknown_kind")

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="build/fed00_api_probes/QA_FED00_API_PROBES.json")
    args = parser.parse_args()
    rows = []
    for name, url, kind in PROBES:
        record = {"id": name, "url": url, "kind": kind}
        try:
            data, raw = request_json(url)
            record.update({"status": "qa_pass", "sha256_response": hashlib.sha256(raw).hexdigest(),
                           "bytes": len(raw), "evidence": inspect(kind, data)})
        except (HTTPError, URLError, TimeoutError, ValueError, UnicodeError, json.JSONDecodeError) as exc:
            record.update({"status": "failed_or_unavailable",
                           "error": f"{type(exc).__name__}: {str(exc)[:220]}"})
        rows.append(record)
        print(json.dumps({"id": name, "status": record["status"]}, ensure_ascii=False), flush=True)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    obj = {"run_time_utc": datetime.now(timezone.utc).isoformat(),
           "scope": "FED00 public API smoke tests; not statewide ingestion",
           "successful": sum(r["status"] == "qa_pass" for r in rows),
           "total": len(rows),
           "status": "pass" if all(r["status"] == "qa_pass" for r in rows) else "partial",
           "results": rows,
           "restrictions": ["No source response indicates municipal completeness",
                            "No observation is written to canonical SQLite or R2",
                            "No missing response is interpreted as zero",
                            "IPCA from BCB SGS mirrors IBGE source and is not a separate price index"]}
    output.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("QA_FILE=" + str(output))
    return 0 if obj["status"] == "pass" else 2

if __name__ == "__main__":
    sys.exit(main())
