from __future__ import annotations

import gzip
import json
from pathlib import Path

from pipeline.sources.siconfi import FetchResult


def slug(value: str) -> str:
    return value.lower().replace(" ", "-").replace("/", "-")


def write_raw(
    path: Path,
    *,
    endpoint: str,
    year: int,
    entity_id: str,
    params: dict,
    result: FetchResult,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "source": "SICONFI",
        "endpoint": endpoint,
        "year": int(year),
        "entity_id": str(entity_id),
        "parameters": params,
        "status": "observado" if result.items else "ausente",
        "pages": result.pages,
        "requests": result.request_count,
        "items": result.items,
    }
    with gzip.open(path, "wt", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, separators=(",", ":"))


def read_raw(path: Path) -> dict:
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        return json.load(handle)


def valid_raw(path: Path, *, endpoint: str, year: int, entity_id: str) -> bool:
    try:
        payload = read_raw(path)
    except Exception:
        return False
    return (
        payload.get("endpoint") == endpoint
        and int(payload.get("year")) == int(year)
        and str(payload.get("entity_id")) == str(entity_id)
        and payload.get("status") in {"observado", "ausente"}
        and isinstance(payload.get("items"), list)
    )
