from __future__ import annotations

import argparse
import hashlib
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = ROOT / "data" / "schema" / "001_initial.sql"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def initialize_database(output: Path, schema: Path = SCHEMA) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    sql = schema.read_text(encoding="utf-8")
    connection = sqlite3.connect(output)
    try:
        connection.executescript(sql)
        connection.commit()
    finally:
        connection.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Inicializa o SQLite canônico.")
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "data" / "financas_municipais_sp.sqlite",
    )
    args = parser.parse_args()
    initialize_database(args.output)
    print(f"Banco criado: {args.output}")
    print(f"schema_sha256={sha256(SCHEMA)}")


if __name__ == "__main__":
    main()
