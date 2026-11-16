#!/usr/bin/env python3
"""Stage SP official Convenios ZIP to local SQLite without assuming financial field meanings."""
from __future__ import annotations
import argparse
import csv
import hashlib
import io
import json
import sqlite3
from collections import Counter
from pathlib import Path
from zipfile import ZipFile

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def stage(zip_path: Path, sqlite_path: Path) -> dict:
    source_sha = sha256(zip_path)
    years = Counter()
    sqlite_path.parent.mkdir(parents=True, exist_ok=True)
    cols = ", ".join(f"col_{n:02} TEXT NOT NULL" for n in range(1, 11))
    with sqlite3.connect(sqlite_path) as conn:
        conn.execute("PRAGMA foreign_keys=ON")
        conn.execute(f"""CREATE TABLE IF NOT EXISTS sp_convenios_raw (
            source_sha256 TEXT NOT NULL, row_num INTEGER NOT NULL, year INTEGER NOT NULL,
            {cols}, PRIMARY KEY(source_sha256,row_num))""")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_sp_convenios_raw_year ON sp_convenios_raw(year)")
        with ZipFile(zip_path) as archive:
            if archive.testzip() is not None:
                raise ValueError("ZIP CRC invalid")
            csv_names = [n for n in archive.namelist() if n.lower().endswith(".csv")]
            if len(csv_names) != 1:
                raise ValueError(f"expected one CSV, found {len(csv_names)}")
            reader = csv.reader(io.StringIO(archive.read(csv_names[0]).decode("utf-8-sig")),delimiter=";")
            first = next(reader, None)
            if first is None or len(first) != 10 or not first[0].strip().isdigit():
                raise ValueError("unexpected CSV shape or headers: investigate schema drift")
            rows = [first, *reader]
            conn.execute("DELETE FROM sp_convenios_raw WHERE source_sha256=?", (source_sha,))
            placeholders = ",".join("?" for _ in range(13))
            for row_num, row in enumerate(rows, 1):
                if len(row) != 10:
                    raise ValueError(f"row {row_num}: {len(row)} fields")
                year = int(row[0])
                if not 1900 <= year <= 2100:
                    raise ValueError(f"row {row_num}: invalid year")
                conn.execute(f"INSERT INTO sp_convenios_raw VALUES ({placeholders})",
                             (source_sha,row_num,year,*(str(v) for v in row)))
                years[year] += 1
        count = conn.execute("SELECT COUNT(*) FROM sp_convenios_raw WHERE source_sha256=?", (source_sha,)).fetchone()[0]
        assert count == sum(years.values())
        return {"source_sha256":source_sha, "table":"sp_convenios_raw",
                "rows":count,"years":dict(sorted(years.items())),
                "financial_schema_homologated":False,
                "physical_location_homologated":False}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--zip",type=Path,required=True)
    parser.add_argument("--db",type=Path,required=True)
    a = parser.parse_args()
    print(json.dumps(stage(a.zip,a.db),ensure_ascii=False))

if __name__ == "__main__":
    main()
