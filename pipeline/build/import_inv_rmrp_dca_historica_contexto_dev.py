#!/usr/bin/env python3
"""Acopla DCA histórica RMRP como CONTEXTO em CÓPIA NOVA de staging SIAFEM.

Não cria observacoes fiscais oficiais 2013–2025; não transforma DCA em execução
de convênio; não confunde valor ausente com zero; não modifica o banco de origem.
"""
from __future__ import annotations

import argparse
import csv
from decimal import Decimal, InvalidOperation
import hashlib
import json
from pathlib import Path
import sqlite3

EXPECTED_SHA = "67a94313e0f0557bc23f48c78a1396fd02ae10ad7923ea2ac2e5c9f2726f65d5"
SOURCE = "dca_sp645_historica_2013_2025"
ARTIFACT = "inv_rmrp_dca_historica_contexto_20261112"


def read(path, sep):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter=sep))


def cents(raw):
    if raw is None or raw.strip() == "":
        return None
    try:
        x = Decimal(raw) * 100
    except InvalidOperation as exc:
        raise ValueError(f"Valor DCA inválido: {raw!r}") from exc
    if not x.is_finite() or x != x.to_integral_value():
        raise ValueError("DCA não possui precisão de centavos válida")
    return int(x)


def status(v):
    return "AUSENTE_NAO_ZERO" if v is None else "ZERO_EXPLICITO" if v == 0 else "OBSERVADO"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--source-db", type=Path, required=True)
    p.add_argument("--output-db", type=Path, required=True)
    p.add_argument("--dca", type=Path, required=True)
    p.add_argument("--roster", type=Path, required=True)
    a = p.parse_args()

    if a.source_db.resolve() == a.output_db.resolve() or a.output_db.exists():
        raise ValueError("A saída deve ser uma cópia inédita, distinta da origem")
    if not a.source_db.is_file():
        raise ValueError("Banco de origem não existe")
    digest = hashlib.sha256(a.dca.read_bytes()).hexdigest()
    if digest != EXPECTED_SHA:
        raise ValueError("SHA256 DCA histórico inesperado")
    records = read(a.dca, ",")
    if len(records) != 8385:
        raise ValueError("DCA histórico incompleto")
    roster = {x["codigo_ibge"]: x for x in read(a.roster, ";")}
    if len(roster) != 34:
        raise ValueError("Cadastro RMRP inválido")
    selected = [x for x in records if x["cod_ibge"] in roster]
    if len(selected) != 442 or len({(x["cod_ibge"], x["ano"]) for x in selected}) != 442:
        raise ValueError("Série histórica DCA da RMRP incompleta")
    if {int(x["ano"]) for x in selected} != set(range(2013, 2026)):
        raise ValueError("Exercícios DCA inconsistentes")
    a.output_db.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(f"file:{a.source_db.resolve()}?mode=ro", uri=True) as original:
        with sqlite3.connect(a.output_db) as clone:
            original.backup(clone)
    db = sqlite3.connect(a.output_db)
    db.execute("PRAGMA foreign_keys=ON")
    try:
        values = db.execute(
            "SELECT COUNT(*), SUM(valor_liberado_estornado_centavos), "
            "SUM(quantidade_pagamentos) FROM inv_siafem_convenio_ano"
        ).fetchone()
        if values != (889, 30552102920, 1017):
            raise ValueError("Staging de entrada não tem SIAFEM reconciliado")
        existing = {r[0] for r in db.execute("SELECT codigo_ibge FROM municipio")}
        if set(roster) - existing:
            raise ValueError("Faltam municípios na origem")
        db.executescript("""
        CREATE TABLE inv_rmrp_dca_contexto_ano (
            codigo_ibge TEXT NOT NULL REFERENCES municipio(codigo_ibge),
            ano INTEGER NOT NULL CHECK (ano BETWEEN 2013 AND 2025),
            investimento_liquidado_centavos INTEGER,
            investimento_liquidado_status TEXT NOT NULL CHECK(
                investimento_liquidado_status IN ('OBSERVADO','ZERO_EXPLICITO','AUSENTE_NAO_ZERO')),
            transferencia_capital_centavos INTEGER,
            transferencia_capital_status TEXT NOT NULL CHECK(
                transferencia_capital_status IN ('OBSERVADO','ZERO_EXPLICITO','AUSENTE_NAO_ZERO')),
            fonte_sha256 TEXT NOT NULL,
            classificacao TEXT NOT NULL CHECK(classificacao='CONTEXTO_DCA_NAO_ADITIVO'),
            PRIMARY KEY (codigo_ibge,ano),
            CHECK ((investimento_liquidado_status='AUSENTE_NAO_ZERO')=(investimento_liquidado_centavos IS NULL)),
            CHECK ((transferencia_capital_status='AUSENTE_NAO_ZERO')=(transferencia_capital_centavos IS NULL))
        );
        CREATE INDEX idx_inv_rmrp_dca_ano ON inv_rmrp_dca_contexto_ano(ano,codigo_ibge);
        """)
        payload = []
        for row in selected:
            inv, cap = cents(row["dca_investimentos_liquidada"]), cents(row["dca_transferencias_capital"])
            payload.append((row["cod_ibge"], int(row["ano"]), inv, status(inv),
                            cap, status(cap), digest, "CONTEXTO_DCA_NAO_ADITIVO"))
        db.executemany("""INSERT INTO inv_rmrp_dca_contexto_ano
            (codigo_ibge,ano,investimento_liquidado_centavos,investimento_liquidado_status,
             transferencia_capital_centavos,transferencia_capital_status,fonte_sha256,classificacao)
            VALUES(?,?,?,?,?,?,?,?)""", payload)
        check = db.execute("""
            SELECT COUNT(*),COUNT(DISTINCT codigo_ibge),
              SUM(investimento_liquidado_status='AUSENTE_NAO_ZERO'),
              SUM(transferencia_capital_status='AUSENTE_NAO_ZERO')
            FROM inv_rmrp_dca_contexto_ano
        """).fetchone()
        if check != (442, 34, 2, 10):
            raise ValueError(f"DCA histórico staging divergente {check}")
        if db.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
            raise ValueError("SQLite danificado")
        if list(db.execute("PRAGMA foreign_key_check")):
            raise ValueError("FK inválida")
        db.commit()
    except Exception:
        db.rollback()
        db.close()
        a.output_db.unlink(missing_ok=True)
        raise
    db.close()
    print(json.dumps({"status":"QA_PASS_STAGING_HISTORICO_SEPARADO",
                      "dca_contexto_rows":442,"municipios":34,
                      "exercicios":13,"ausentes_investimento":2,
                      "ausentes_transferencia_capital":10,
                      "siafem_convenio_ano_preservados":889,
                      "siafem_valor_preservado_centavos":30552102920,
                      "source_unchanged":True}, ensure_ascii=False))


if __name__ == "__main__":
    main()
