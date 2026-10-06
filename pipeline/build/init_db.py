from __future__ import annotations

import argparse
import hashlib
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_DIR = ROOT / "data" / "schema"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def discover_migrations(schema_dir: Path = SCHEMA_DIR) -> list[Path]:
    migrations = sorted(schema_dir.glob("[0-9][0-9][0-9]_*.sql"))
    if not migrations:
        raise FileNotFoundError(f"Nenhuma migration SQL em {schema_dir}")
    return migrations


def initialize_database(
    output: Path,
    schema: Path | None = None,
    schema_dir: Path = SCHEMA_DIR,
) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    migrations = [schema] if schema is not None else discover_migrations(schema_dir)

    connection = sqlite3.connect(output)
    try:
        connection.execute("PRAGMA foreign_keys = ON")
        for migration in migrations:
            connection.executescript(migration.read_text(encoding="utf-8"))
        connection.commit()
    finally:
        connection.close()


def schema_fingerprint(schema_dir: Path = SCHEMA_DIR) -> str:
    digest = hashlib.sha256()
    for path in discover_migrations(schema_dir):
        digest.update(path.name.encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


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
    print(f"schema_sha256={schema_fingerprint()}")


if __name__ == "__main__":
    main()
