#!/usr/bin/env python3
"""FED04: safety gate on a disposable SQLite rebuilt from pinned R2 XLSX.

Never runs on production. The repository workflow creates the database under
build/fed04-real-qa/, never writes to R2 and never publishes data.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from pipeline.build.load_catalog import load_catalog

ROOT = Path(__file__).resolve().parents[2]
CANDIDATES = {
    "dca_itr_cota_parte_bruta",
    "dca_itr_deducao_fundeb",
    "dca_fundeb_recebido_bruto",
    "dca_fundeb_complementacao_uniao_bruta",
}


def _query_snapshot(db: sqlite3.Connection, sql: str) -> tuple[int, str]:
    sha = hashlib.sha256()
    count = 0
    for row in db.execute(sql):
        sha.update(json.dumps(row, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))
        sha.update(b"\n")
        count += 1
    return count, sha.hexdigest()


BASELINE = """SELECT codigo_ibge,ano,variavel_id,fonte_id,valor_num,valor_texto,
                      status,referencia_origem,build_id
               FROM observacao ORDER BY codigo_ibge,ano,variavel_id"""
PUBLISHED = """SELECT codigo_ibge,ano,variavel_id,valor_num,valor_texto,status
                FROM v_observacao_publicavel
                ORDER BY codigo_ibge,ano,variavel_id"""
VAR_BASELINE = """SELECT variavel_id,nome,grupo,tipo,natureza,unidade,definicao,
                         formula,como_ler,cautelas,fonte_preferencial_id,
                         periodicidade,publicavel,ativo
                  FROM variavel
                  WHERE variavel_id NOT IN
                  ('dca_itr_cota_parte_bruta','dca_itr_deducao_fundeb',
                   'dca_fundeb_recebido_bruto','dca_fundeb_complementacao_uniao_bruta')
                  ORDER BY variavel_id"""


def audit(dbfile: Path, proposal: Path, outfile: Path) -> dict:
    root = dbfile.resolve()
    # A destructive operation is never permitted: only disposable DB paths in build.
    build = (ROOT / "build" / "fed04-real-qa").resolve()
    if not root.is_relative_to(build):
        raise ValueError("FED04 real-data QA accepts only files under build/fed04-real-qa/")
    if not root.is_file() or not proposal.is_file():
        raise FileNotFoundError("Isolated DB or proposal unavailable")

    with sqlite3.connect(root) as conn:
        conn.execute("PRAGMA foreign_keys=ON")
        if conn.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
            raise AssertionError("Baseline SQLite integrity_check failed")
        sp = conn.execute("SELECT count(*) FROM municipio WHERE uf='SP'").fetchone()[0]
        if sp != 645:
            raise AssertionError(f"Expected 645 municipalities, got {sp}")
        before_obs = _query_snapshot(conn, BASELINE)
        before_public = _query_snapshot(conn, PUBLISHED)
        before_vars = _query_snapshot(conn, VAR_BASELINE)
        if any(conn.execute("SELECT 1 FROM variavel WHERE variavel_id=?", (id,)).fetchone()
               for id in CANDIDATES):
            raise AssertionError("Candidate variable already exists in baseline")
        if not conn.execute("SELECT 1 FROM fonte WHERE fonte_id='SICONFI_DCA'").fetchone():
            raise AssertionError("SICONFI_DCA source missing in baseline")
        before_sources = conn.execute("SELECT count(*) FROM fonte").fetchone()[0]

    # Performs only the four metadata inserts on the **disposable copy**.
    load_catalog(root, [proposal])
    with sqlite3.connect(root) as conn:
        conn.execute("PRAGMA foreign_keys=ON")
        rows = conn.execute(
            "SELECT variavel_id,publicavel,ativo FROM variavel "
            "WHERE variavel_id IN (?,?,?,?) ORDER BY variavel_id",
            tuple(sorted(CANDIDATES)),
        ).fetchall()
        if len(rows) != 4 or any((p, a) != (0, 0) for _, p, a in rows):
            raise AssertionError(f"Candidate flags not private: {rows}")
        if _query_snapshot(conn, BASELINE) != before_obs:
            raise AssertionError("Loading candidates modified an existing observation")
        if _query_snapshot(conn, VAR_BASELINE) != before_vars:
            raise AssertionError("Loading candidates modified an existing variable")
        if conn.execute("SELECT count(*) FROM fonte").fetchone()[0] != before_sources:
            raise AssertionError("Loading candidates changed source count")
        if _query_snapshot(conn, PUBLISHED) != before_public:
            raise AssertionError("Loading candidate metadata changed public view")

        # A few explicitly synthetic values test that even inserted observations
        # are not exposed. They are never copied to production nor R2.
        example = conn.execute(
            "SELECT codigo_ibge FROM municipio WHERE uf='SP' ORDER BY codigo_ibge LIMIT 1"
        ).fetchone()[0]
        for idx, variable in enumerate(sorted(CANDIDATES), start=1):
            conn.execute(
                "INSERT INTO observacao(codigo_ibge,ano,variavel_id,fonte_id,"
                "valor_num,status,referencia_origem) "
                "VALUES(?,2025,?,'SICONFI_DCA',?,'observado','FED04_SYNTHETIC_QA_ONLY')",
                (example, variable, float(idx)),
            )
        if _query_snapshot(conn, PUBLISHED) != before_public:
            raise AssertionError("Synthetic private values leaked into public view")
        if conn.execute("PRAGMA foreign_key_check").fetchall():
            raise AssertionError("Foreign key check failed after candidate insertions")
        if conn.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
            raise AssertionError("Integrity check failed after candidate insertions")
        out = {
            "qa": "passed_disposable_real_2025_source_only",
            "at_utc": datetime.now(timezone.utc).isoformat(),
            "source_scope": "isolated SQLite rebuilt from pinned 2025 canonical XLSX; not historical 2013-2025 DB",
            "municipalities_sp": sp,
            "baseline_observation_count": before_obs[0],
            "baseline_observations_sha256": before_obs[1],
            "baseline_public_view_count": before_public[0],
            "baseline_public_view_sha256": before_public[1],
            "baseline_existing_variable_count": before_vars[0],
            "baseline_existing_variables_sha256": before_vars[1],
            "candidate_variable_count": len(rows),
            "candidate_flags": {name: {"publicavel": p, "ativo": a} for name, p, a in rows},
            "synthetic_candidate_observations": 4,
            "existing_observations_unchanged": True,
            "existing_variables_unchanged": True,
            "public_view_unchanged_even_with_synthetic_values": True,
            "foreign_key_check": "ok",
            "integrity_check": "ok",
            "database_published": False,
            "r2_written": False,
        }

    outfile.parent.mkdir(parents=True, exist_ok=True)
    outfile.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False))
    return out


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--database", type=Path, required=True)
    p.add_argument("--proposal", type=Path, default=ROOT / "governance/proposals/FED04_VARIAVEIS_DCA_ITR_FUNDEB_CANDIDATAS.yml")
    p.add_argument("--qa", type=Path, required=True)
    args = p.parse_args()
    audit(args.database, args.proposal, args.qa)
