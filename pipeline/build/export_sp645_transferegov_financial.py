"""Exporta fluxos financeiros agregados do Transferegov para o site SP645.

A saída é agregada por município proponente, exercício e etapa. Não exporta
linhas, identificadores, números de convênio ou dados de favorecidos.
"""
from __future__ import annotations

import argparse
import csv
import json
import sqlite3
import tarfile
import tempfile
from collections import defaultdict
from pathlib import Path

STAGES = ("desembolso", "pagamento")
ARCHIVE_SHA256 = "d7c0d8758fca9434e5c348e8f2be8905d443b1737ecc31b6aaffa33ddeaf77cc"


def _copy_database(archive_path: Path, destination: Path) -> None:
    with tarfile.open(archive_path, "r:gz") as archive:
        matches = [m for m in archive.getmembers()
                   if m.name == "financial.sqlite" and m.isfile()]
        if len(matches) != 1:
            raise ValueError("staging archive must contain one financial.sqlite")
        source = archive.extractfile(matches[0])
        if source is None:
            raise ValueError("cannot read financial.sqlite from staging archive")
        with source, destination.open("wb") as target:
            while chunk := source.read(1024 * 1024):
                target.write(chunk)


def _municipalities(path: Path) -> dict[str, str]:
    result = {}
    with path.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle, delimiter=";"):
            code = row["codigo_ibge"].strip()
            if code in result:
                raise ValueError("duplicate municipality code in SP645 dimension")
            result[code] = row["municipio"].strip()
    if len(result) != 645:
        raise ValueError(f"SP645 dimension has {len(result)} municipalities, expected 645")
    return result


def build(archive_path: Path, geo_path: Path, output_path: Path,
          expected_sha256: str) -> dict:
    import hashlib
    digest = hashlib.sha256(archive_path.read_bytes()).hexdigest()
    if digest != expected_sha256 or digest != ARCHIVE_SHA256:
        raise ValueError("financial staging archive hash differs from approved snapshot")

    municipalities = _municipalities(geo_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="sp645-financial-export-") as temp:
        db_path = Path(temp) / "financial.sqlite"
        _copy_database(archive_path, db_path)
        con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        con.row_factory = sqlite3.Row
        try:
            if con.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
                raise ValueError("financial staging SQLite integrity check failed")
            db_municipalities = {
                row[0] for row in con.execute(
                    "SELECT DISTINCT ibge FROM convenio WHERE ibge IS NOT NULL"
                )
            }
            unknown = sorted(db_municipalities - municipalities.keys())
            if unknown:
                raise ValueError("staging contains municipalities outside SP645 dimension")

            records = []
            for row in con.execute("""
                SELECT c.ibge AS codigo_ibge, e.stage AS stage,
                       CAST(substr(e.date, 1, 4) AS INTEGER) AS year,
                       COUNT(*) AS event_count,
                       COUNT(DISTINCT e.convenio) AS instrument_count,
                       SUM(e.cents) AS net_cents,
                       SUM(CASE WHEN e.cents < 0 THEN 1 ELSE 0 END) AS negative_events,
                       SUM(CASE WHEN e.cents = 0 THEN 1 ELSE 0 END) AS zero_events
                FROM event e
                JOIN convenio c ON c.numero=e.convenio
                GROUP BY c.ibge,e.stage,CAST(substr(e.date, 1, 4) AS INTEGER)
                ORDER BY year,stage,c.ibge
            """):
                if row["stage"] not in STAGES:
                    raise ValueError("unexpected financial stage in staging database")
                code = str(row["codigo_ibge"])
                if code not in municipalities:
                    raise ValueError("financial event cannot be matched to SP645 municipality")
                records.append({
                    "codigo_ibge": code,
                    "municipio": municipalities[code],
                    "year": row["year"],
                    "stage": row["stage"],
                    "event_count": row["event_count"],
                    "instrument_count": row["instrument_count"],
                    "net_amount_brl": row["net_cents"] / 100,
                    "negative_events": row["negative_events"],
                    "zero_events": row["zero_events"],
                })
        finally:
            con.close()

    years = sorted({item["year"] for item in records})
    coverage = []
    for year in years:
        for stage in STAGES:
            subset = [item for item in records
                      if item["year"] == year and item["stage"] == stage]
            coverage.append({
                "year": year,
                "stage": stage,
                "expected_municipalities": 645,
                "municipalities_with_events": len({x["codigo_ibge"] for x in subset}),
                "event_count": sum(x["event_count"] for x in subset),
            })

    document = {
        "schema_version": "1.0.0",
        "universe": "SP_645",
        "title": "Fluxos financeiros federais registrados no Transferegov",
        "geographic_basis": "municipio proponente do convenio; nao representa local da execucao",
        "period_basis": "ano da data do evento financeiro",
        "value_basis": "valores nominais; pagamentos negativos e zerados permanecem nas agregacoes",
        "stage_policy": "desembolso e pagamento sao etapas distintas e nao aditivas; nao somar as etapas",
        "interpretation": [
            "os registros nao comprovam natureza de capital nem investimento executado",
            "o municipio proponente nao identifica necessariamente o local fisico da obra, bem ou servico",
            "municipio sem evento na tabela significa sem registro selecionado, nao valor igual a zero",
            "valores agregados por municipio, etapa e ano; nenhuma linha ou identificador transacional e exposto",
        ],
        "source": {
            "name": "Transferegov — arquivos financeiros oficiais",
            "snapshot_archive_sha256": digest,
            "staging_run": 46006854691,
        },
        "municipality_count": 645,
        "years": years,
        "coverage": coverage,
        "records": records,
    }
    output_path.write_text(json.dumps(document, ensure_ascii=False, separators=(",", ":")) + "\n",
                           encoding="utf-8")
    return {
        "municipalities": 645,
        "years": years,
        "records": len(records),
        "coverage_rows": len(coverage),
        "source_sha256": digest,
        "output_bytes": output_path.stat().st_size,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--geo", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--expected-sha256", required=True)
    args = parser.parse_args()
    result = build(args.archive, args.geo, args.output, args.expected_sha256)
    print("SP645_TRANSFEREGOV_FINANCIAL_EXPORT " +
          json.dumps(result, ensure_ascii=False, separators=(",", ":")))


if __name__ == "__main__":
    main()
