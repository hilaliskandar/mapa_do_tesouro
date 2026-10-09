#!/usr/bin/env python3
import json
import sys
from pathlib import Path


def fail(msg: str) -> None:
    raise SystemExit(msg)


def main() -> None:
    if len(sys.argv) != 3:
        fail("uso: validate_context.py universe <arquivo.json>")
    kind, path = sys.argv[1], Path(sys.argv[2])
    if kind != "universe":
        fail("tipo esperado: universe")
    data = json.loads(path.read_text(encoding="utf-8"))
    for key in ("api_version", "publication_id", "member_count", "variables", "rules"):
        if key not in data:
            fail(f"campo ausente: {key}")
    if data["api_version"] != "v1":
        fail("api_version incompatível")
    if data["rules"].get("absence_is_not_zero") is not True:
        fail("regra absence_is_not_zero ausente")
    print("OK")


if __name__ == "__main__":
    main()
