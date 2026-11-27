"""Aggregate QA of the already-staged SP645 Transferegov financial archive.

This emits only aggregate counts and movement categories. It never writes
transaction identifiers, instrument numbers, row numbers, or exact amounts.
"""
from __future__ import annotations

import argparse
import collections
import csv
import decimal
import datetime
import json
import sqlite3
import tarfile
import tempfile
import zipfile
from pathlib import Path

from pipeline.acquire.inv_sp645_transferegov_new_source_layout import acquire
from pipeline.acquire.inv_sp645_proponent_obrasgov_regional_coverage import read

ARCHIVE_MEMBERS = {"financial.sqlite", "qa.json", "municipio_ano.csv"}


def copy_member(archive: tarfile.TarFile, name: str, destination: Path) -> None:
    matches = [m for m in archive.getmembers() if m.name == name]
    if len(matches) != 1 or not matches[0].isfile():
        raise ValueError(f"expected one regular archive member: {name}")
    source = archive.extractfile(matches[0])
    if source is None:
        raise ValueError(f"could not read archive member: {name}")
    with source, destination.open("wb") as target:
        while chunk := source.read(1024 * 1024):
            target.write(chunk)


def load_archive(archive_path: Path, work: Path) -> tuple[Path, dict]:
    with tarfile.open(archive_path, "r:gz") as tar:
        names = [m.name for m in tar.getmembers() if m.isfile()]
        if set(names) != ARCHIVE_MEMBERS or len(names) != len(ARCHIVE_MEMBERS):
            raise ValueError("staging archive members differ from the expected set")
        db_path = work / "financial.sqlite"
        qa_path = work / "source_qa.json"
        copy_member(tar, "financial.sqlite", db_path)
        copy_member(tar, "qa.json", qa_path)
    return db_path, json.loads(qa_path.read_text(encoding="utf-8"))



def payment_source_schema(work: Path) -> dict:
    path, metadata = acquire(work, "siconv_pagamento", 650)
    with zipfile.ZipFile(path) as archive:
        members = [item for item in archive.infolist()
                   if not item.is_dir() and item.filename.lower().endswith(".csv")]
        if len(members) != 1:
            raise ValueError("expected one payment CSV in the official ZIP")
        with archive.open(members[0], "r") as binary:
            header_bytes = binary.readline(262145)
            if len(header_bytes) > 262144:
                raise ValueError("payment CSV header exceeds 256 KiB")
        columns = None
        for encoding in ("utf-8-sig", "cp1252"):
            try:
                header = header_bytes.decode(encoding, errors="strict")
                delimiter = ";" if header.count(";") >= header.count(",") else ","
                columns = next(csv.reader([header], delimiter=delimiter))
                break
            except UnicodeDecodeError:
                continue
        if columns is None or any(not column.strip() for column in columns):
            raise ValueError("payment CSV header encoding or fields are invalid")
        if len(columns) != len(set(columns)):
            raise ValueError("duplicate payment CSV column names")
        if archive.testzip() is not None:
            raise ValueError("payment ZIP CRC verification failed")
    return {
        "source_sha256_zip": metadata["sha256_zip"],
        "source_zip_bytes": metadata["zip_bytes"],
        "csv_columns": columns,
        "rows_read": 0,
        "purpose": "schema only; no payment rows or values exported",
    }


def payment_document_linkage(db_path: Path, payment_zip: Path,
                            source_qa: dict, expected_source_hash: str) -> dict:
    db = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    db.row_factory = sqlite3.Row
    negatives = {
        row["id"]: {
            "convenio": row["convenio"],
            "date": row["date"],
            "cents": row["cents"],
        }
        for row in db.execute("""
            SELECT id, convenio, date, cents
            FROM event WHERE stage='pagamento' AND cents < 0
        """)
    }
    db.close()

    required = {"NR_MOV_FIN", "NR_CONVENIO", "TP_MOV_FINANCEIRA",
                "DATA_PAG", "VL_PAGO", "NR_DL", "ID_DL"}
    expected_payment_meta = source_qa["sources"]["siconv_pagamento"]
    actual_hash = expected_payment_meta["sha256_zip"]
    if actual_hash != expected_source_hash:
        raise ValueError("payment source archive hash differs from staged QA")
    found = {}

    def cents(value: str) -> int:
        value = value.strip()
        if "," in value:
            value = value.replace(".", "").replace(",", ".")
        amount = decimal.Decimal(value)
        if not amount.is_finite() or amount * 100 != (amount * 100).to_integral_value():
            raise ValueError("non-finite or sub-cent payment value in selected row")
        return int(amount * 100)

    def normalized_date(value: str) -> str:
        value = value.strip()
        for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d/%m/%Y %H:%M:%S"):
            try:
                return datetime.datetime.strptime(value, fmt).date().isoformat()
            except ValueError:
                continue
        raise ValueError("unrecognized date in selected source payment")

    for row in read(payment_zip, required):
        event_id = row["NR_MOV_FIN"].strip()
        if event_id not in negatives:
            continue
        expected = negatives[event_id]
        if row["NR_CONVENIO"].strip() != expected["convenio"]:
            raise ValueError("selected negative-payment instrument linkage mismatch")
        if normalized_date(row["DATA_PAG"]) != expected["date"]:
            raise ValueError("selected negative-payment date linkage mismatch")
        parsed = cents(row["VL_PAGO"])
        if parsed != expected["cents"]:
            raise ValueError("selected negative-payment amount mismatch")
        found[event_id] = {
            "convenio": row["NR_CONVENIO"].strip(),
            "nr_dl": row["NR_DL"].strip(),
            "id_dl": row["ID_DL"].strip(),
        }

    if len(found) != len(negatives):
        raise ValueError("not all staged negative payments matched the source snapshot")

    stats = {
        event_id: {
            "nr_dl_positive_same_instrument": False,
            "id_dl_positive_same_instrument": False,
            "equal_opposite_positive_same_id_dl_same_instrument": False,
        }
        for event_id in negatives
    }

    for row in read(payment_zip, required):
        event_id = row["NR_MOV_FIN"].strip()
        if event_id in negatives:
            continue
        value = cents(row["VL_PAGO"])
        if value <= 0:
            continue
        convention = row["NR_CONVENIO"].strip()
        nr_dl = row["NR_DL"].strip()
        id_dl = row["ID_DL"].strip()
        for negative_id, detail in found.items():
            same_convenio = convention == detail["convenio"]
            same_nr_dl = bool(detail["nr_dl"]) and nr_dl == detail["nr_dl"]
            same_id_dl = bool(detail["id_dl"]) and id_dl == detail["id_dl"]
            if not same_convenio:
                continue
            if same_nr_dl:
                stats[negative_id]["nr_dl_positive_same_instrument"] = True
            if same_id_dl:
                stats[negative_id]["id_dl_positive_same_instrument"] = True
                if value == -negatives[negative_id]["cents"]:
                    stats[negative_id][
                        "equal_opposite_positive_same_id_dl_same_instrument"
                    ] = True

    output = {
        "source_sha256_matches_staged_snapshot": True,
        "negative_events_matched_back_to_source": len(found),
        "negative_events_with_nr_dl": sum(bool(x["nr_dl"]) for x in found.values()),
        "negative_events_with_id_dl": sum(bool(x["id_dl"]) for x in found.values()),
    }
    for key in next(iter(stats.values()), {}):
        output[key] = sum(item[key] for item in stats.values())
    output["negative_events_without_positive_same_doc_instrument"] = sum(
        not (item["nr_dl_positive_same_instrument"] or
             item["id_dl_positive_same_instrument"])
        for item in stats.values()
    )
    output["interpretation"] = (
        "document linkage is descriptive and does not by itself establish a reversal"
    )
    return output


def audit(db_path: Path, geo_csv: Path, source_qa: dict) -> dict:
    municipalities = {}
    with geo_csv.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle, delimiter=";"):
            code = row["codigo_ibge"].strip()
            if code in municipalities:
                raise ValueError(f"duplicate IBGE code in territorial dimension: {code}")
            municipalities[code] = row["municipio"].strip()
    if len(municipalities) != 645:
        raise ValueError(f"expected 645 municipalities, got {len(municipalities)}")

    db = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    db.row_factory = sqlite3.Row
    integrity = db.execute("PRAGMA integrity_check").fetchone()[0]
    fk_issues = db.execute("PRAGMA foreign_key_check").fetchall()
    if integrity != "ok" or fk_issues:
        raise ValueError("staged SQLite integrity check failed")

    stages = {}
    for row in db.execute("""
        SELECT stage, COUNT(*) events, COUNT(DISTINCT c.ibge) municipalities,
               COUNT(DISTINCT e.convenio) instruments,
               SUM(CASE WHEN e.cents < 0 THEN 1 ELSE 0 END) negatives,
               SUM(CASE WHEN e.cents = 0 THEN 1 ELSE 0 END) zeros
        FROM event e JOIN convenio c ON c.numero=e.convenio
        GROUP BY stage ORDER BY stage
    """):
        stages[row["stage"]] = {k: row[k] for k in
                                ("events", "municipalities", "instruments",
                                 "negatives", "zeros")}

    negative_types = {}
    for row in db.execute("""
        SELECT COALESCE(NULLIF(TRIM(kind), ''), '[vazio]') kind, COUNT(*) events
        FROM event
        WHERE stage='pagamento' AND cents < 0
        GROUP BY 1 ORDER BY 1
    """):
        label = row["kind"]
        lower = label.casefold()
        reversal_hint = any(term in lower for term in
                            ("estorn", "anula", "cancel", "revers", "devol"))
        negative_types[label] = {"events": row["events"],
                                 "type_name_suggests_reversal": reversal_hint}

    zero_types = {}
    for row in db.execute("""
        SELECT COALESCE(NULLIF(TRIM(kind), ''), '[vazio]') kind, COUNT(*) events
        FROM event
        WHERE stage='pagamento' AND cents = 0
        GROUP BY 1 ORDER BY 1
    """):
        zero_types[row["kind"]] = row["events"]

    municipality_payment_counts = {
        row["ibge"]: row["events"]
        for row in db.execute("""
            SELECT c.ibge, COUNT(*) events
            FROM event e JOIN convenio c ON c.numero=e.convenio
            WHERE e.stage='pagamento'
            GROUP BY c.ibge
        """)
    }
    missing_payment = [
        {"codigo_ibge": code, "municipio": name}
        for code, name in sorted(municipalities.items())
        if code not in municipality_payment_counts
    ]

    missing_payment_coverage = []
    for item in missing_payment:
        code = item["codigo_ibge"]
        row = db.execute("""
            SELECT c.ibge, COUNT(DISTINCT c.numero) instruments,
                   SUM(CASE WHEN e.stage='desembolso' THEN 1 ELSE 0 END) desembolso_events
            FROM convenio c
            LEFT JOIN event e ON e.convenio=c.numero
            WHERE c.ibge=?
            GROUP BY c.ibge
        """, (code,)).fetchone()
        missing_payment_coverage.append({
            **item,
            "convenios_in_staging": row["instruments"] if row else 0,
            "desembolso_events": row["desembolso_events"] if row else 0,
        })

    instrument_counts = {
        row["stage"]: row["n"]
        for row in db.execute("""
            SELECT stage, COUNT(DISTINCT convenio) n
            FROM event GROUP BY stage
        """)
    }
    overlap = db.execute("""
        WITH by_instrument AS (
            SELECT convenio,
                   MAX(stage='pagamento') has_pagamento,
                   MAX(stage='desembolso') has_desembolso
            FROM event GROUP BY convenio
        )
        SELECT SUM(has_pagamento=1 AND has_desembolso=1) both,
               SUM(has_pagamento=1 AND has_desembolso=0) pagamento_only,
               SUM(has_pagamento=0 AND has_desembolso=1) desembolso_only
        FROM by_instrument
    """).fetchone()

    negative_counterparts = collections.Counter()
    negative_rows = list(db.execute("""
        SELECT convenio, date, cents
        FROM event
        WHERE stage='pagamento' AND cents < 0
    """))
    for negative in negative_rows:
        matches = [
            row["date"]
            for row in db.execute("""
                SELECT date FROM event
                WHERE stage='pagamento' AND convenio=? AND cents=?
            """, (negative["convenio"], -negative["cents"]))
        ]
        if not matches:
            category = "no_equal_opposite_payment_same_instrument"
        else:
            before = any(day < negative["date"] for day in matches)
            after = any(day > negative["date"] for day in matches)
            same_day = any(day == negative["date"] for day in matches)
            if before and after:
                category = "equal_opposite_payments_before_and_after"
            elif before:
                category = "equal_opposite_payment_before"
            elif after:
                category = "equal_opposite_payment_after"
            elif same_day:
                category = "equal_opposite_payment_same_day"
            else:
                category = "equal_opposite_payment_date_unclassified"
        negative_counterparts[category] += 1

    chronology = db.execute("""
        WITH date_ranges AS (
            SELECT convenio, stage, MIN(date) first_date, MAX(date) last_date
            FROM event GROUP BY convenio, stage
        )
        SELECT COUNT(*) matched_instruments,
               SUM(p.last_date < d.first_date) payments_entirely_before_disbursement,
               SUM(d.last_date < p.first_date) disbursements_entirely_before_payment,
               SUM(NOT (p.last_date < d.first_date OR d.last_date < p.first_date))
                   date_ranges_interleaved_or_touching
        FROM date_ranges p
        JOIN date_ranges d ON d.convenio=p.convenio
        WHERE p.stage='pagamento' AND d.stage='desembolso'
    """).fetchone()

    db.close()
    baseline = {
        item["stage"]: item["events"]
        for item in source_qa.get("summary", [])
    }
    database_events = {stage: item["events"] for stage, item in stages.items()}
    baseline_matches = all(database_events.get(stage) == count
                           for stage, count in baseline.items())

    return {
        "scope": "SP645 financial staging, by proponent municipality",
        "territorial_universe": len(municipalities),
        "database_integrity": integrity,
        "source_qa_event_counts_match": baseline_matches,
        "stages": stages,
        "negative_payment_type_counts": negative_types,
        "zero_payment_type_counts": zero_types,
        "payment_municipalities_without_selected_events": missing_payment_coverage,
        "negative_same_instrument_equal_opposite_match_counts": dict(negative_counterparts),
        "instruments_by_stage": instrument_counts,
        "instrument_overlap": dict(overlap),
        "chronology": {
            "instruments_with_both_stages": chronology["matched_instruments"],
            "payments_entirely_before_disbursement":
                chronology["payments_entirely_before_disbursement"],
            "disbursements_entirely_before_payment":
                chronology["disbursements_entirely_before_payment"],
            "date_ranges_interleaved_or_touching":
                chronology["date_ranges_interleaved_or_touching"],
            "interpretation": "descriptive only; stages are not additive",
        },
        "source_qa_publication_authorized":
            source_qa.get("publication_authorized", False),
        "privacy": {
            "transaction_ids_in_output": False,
            "instrument_numbers_in_output": False,
            "row_numbers_in_output": False,
            "exact_transaction_amounts_in_output": False,
        },
        "classification_status":
            "movement-type labels are screening clues, not final adjudication",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--geo", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="sp645-financial-audit-") as temp:
        work = Path(temp)
        db_path, source_qa = load_archive(args.archive, work)
        payment_schema = payment_source_schema(work)
        result = audit(db_path, args.geo, source_qa)
        result["current_payment_source_schema"] = payment_schema
        result["negative_payment_document_linkage"] = payment_document_linkage(
            db_path, work / "siconv_pagamento.zip", source_qa,
            payment_schema["source_sha256_zip"])
    if not result["source_qa_event_counts_match"]:
        raise SystemExit("database event counts differ from source QA")
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8")
    print("SP645_FINANCIAL_AUDIT_SUMMARY " +
          json.dumps(result, ensure_ascii=False, separators=(",", ":")),
          flush=True)


if __name__ == "__main__":
    main()
