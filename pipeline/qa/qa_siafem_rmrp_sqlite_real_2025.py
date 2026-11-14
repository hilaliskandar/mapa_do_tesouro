#!/usr/bin/env python3
"""Verificar imutabilidade de conteúdo fiscal em SQLite SP645 real reconstruído.

Compara conteúdo ordenado e schema do núcleo municipal entre banco origem 2025
e cópia de staging SIAFEM; saída JSON contém exclusivamente contagens e hashes.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sqlite3

CORE = ["municipio", "universo", "universo_municipio", "fonte", "variavel",
        "crosswalk_variavel", "observacao", "cobertura", "build", "build_source"]
NEW_SOURCE = "siafem_sp_transferencias_voluntarias"
EXPECTED = (889, 30552102920, 1017)


def stable_table(conn, name):
    cols = [r[1] for r in conn.execute(f'PRAGMA table_info("{name}")')]
    if not cols:
        raise RuntimeError(f'Tabela fiscal ausente: {name}')
    hash_value = hashlib.sha256()
    count = 0
    rows = conn.execute(f'SELECT * FROM "{name}" ORDER BY ' +
                        ', '.join(f'"{col}"' for col in cols))
    for row in rows:
        hash_value.update(json.dumps(list(row), sort_keys=True, ensure_ascii=False,
                                     separators=(',', ':'), default=str).encode('utf-8'))
        hash_value.update(b'\n')
        count += 1
    return {"n": count, "sha256": hash_value.hexdigest()}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--original", type=Path, required=True)
    p.add_argument("--staging", type=Path, required=True)
    p.add_argument("--qa", type=Path, required=True)
    args = p.parse_args()
    if args.original.resolve() == args.staging.resolve():
        raise ValueError("Origem e staging precisam ser distintos")

    old = sqlite3.connect(f"file:{args.original.resolve()}?mode=ro", uri=True)
    new = sqlite3.connect(f"file:{args.staging.resolve()}?mode=ro", uri=True)
    try:
        statuses = {"origin_integrity": old.execute("PRAGMA integrity_check").fetchone()[0],
                    "staging_integrity": new.execute("PRAGMA integrity_check").fetchone()[0],
                    "origin_fks": len(old.execute("PRAGMA foreign_key_check").fetchall()),
                    "staging_fks": len(new.execute("PRAGMA foreign_key_check").fetchall())}
        if statuses != {"origin_integrity": "ok", "staging_integrity": "ok",
                        "origin_fks": 0, "staging_fks": 0}:
            raise RuntimeError(f"Integridade fiscal: {statuses}")
        core = {}
        for table in CORE:
            # Fonte ganha UMA linha de metadados SIAFEM; conteúdo anterior deve permanecer.
            if table == "fonte":
                prev = list(old.execute("SELECT fonte_id FROM fonte ORDER BY fonte_id"))
                current = list(new.execute(
                    "SELECT fonte_id FROM fonte WHERE fonte_id != ? ORDER BY fonte_id",
                    (NEW_SOURCE,)))
                if prev != current:
                    raise RuntimeError("IDs de fontes fiscais originais alterados")
                old_rows = list(old.execute("SELECT * FROM fonte ORDER BY fonte_id"))
                new_rows = list(new.execute(
                    "SELECT * FROM fonte WHERE fonte_id != ? ORDER BY fonte_id", (NEW_SOURCE,)))
                if old_rows != new_rows:
                    raise RuntimeError("Conteúdo pré-existente de fonte alterado")
                core[table] = {"n_original": len(old_rows), "n_staging_anteriores": len(new_rows),
                               "status": "identico"}
            else:
                a, b = stable_table(old, table), stable_table(new, table)
                if a != b:
                    raise RuntimeError(f"Tabela fiscal alterada: {table}: {a} != {b}")
                core[table] = {"n": a["n"], "sha256": a["sha256"]}
        view_name = "v_observacao_publicavel"
        view_sql = (
            "SELECT codigo_ibge, municipio, ano, variavel_id, variavel, grupo, tipo, "
            "unidade, valor_num, valor_texto, status, fonte_id, referencia_origem "
            f"FROM {view_name} ORDER BY codigo_ibge, ano, variavel_id"
        )
        obs_old = old.execute(view_sql).fetchall()
        obs_new = new.execute(view_sql).fetchall()
        if obs_old != obs_new:
            raise RuntimeError("Regressão da visão pública observacao")
        source_only = new.execute(
            "SELECT COUNT(*) FROM fonte WHERE fonte_id=?", (NEW_SOURCE,)).fetchone()[0]
        if source_only != 1:
            raise RuntimeError("Fonte nova não encontrada")
        metrics = new.execute(
            "SELECT COUNT(*), SUM(valor_liberado_estornado_centavos), "
            "SUM(quantidade_pagamentos) FROM inv_siafem_convenio_ano"
        ).fetchone()
        if metrics != EXPECTED:
            raise RuntimeError(f"Valores estaduais divergentes: {metrics}")
        ins = new.execute(
            "SELECT COUNT(*) FROM inv_instrumento WHERE fonte_sistema='siafem_sp'"
        ).fetchone()[0]
        if ins != 752:
            raise RuntimeError(f"Instrumentos estaduais divergentes: {ins}")
        if new.execute("SELECT COUNT(*) FROM inv_evento_financeiro").fetchone()[0] != 0:
            raise RuntimeError("Não devem existir pagamentos individuais sintéticos")
        if new.execute("SELECT COUNT(*) FROM inv_projeto WHERE qa_status='homologado'").fetchone()[0]:
            raise RuntimeError("Projetos não homologados")
        report = {
            "status": "qa_pass_real_2025_reconstructed_source_only",
            "scope": "Reconstrução canônica 2025 com inputs R2, NÃO materialização histórica 2013-2025",
            "original_schema_unchanged": True, "original_fiscal_content_unchanged": True,
            "public_view_unchanged": True, "original_public_rows": len(obs_old),
            "core": core, "sqlite": statuses,
            "siafem": {"instruments": ins, "instrument_year": metrics[0],
                       "value_centavos": metrics[1], "payments_count": metrics[2],
                       "status": "em_revisao"},
            "restrictions": [
                "Não substitui QA sobre materialização histórica real",
                "Não representa pagamentos individuais ou investimento executado",
                "Não publicar nem escrever snapshots R2 a partir deste QA"
            ]
        }
        args.qa.parent.mkdir(parents=True, exist_ok=True)
        args.qa.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
        print(json.dumps({"status": report["status"], "fiscal_rows": len(obs_old),
                          "instruments": ins, "transfers_cents": metrics[1]}))
    finally:
        old.close()
        new.close()


if __name__ == "__main__":
    main()
