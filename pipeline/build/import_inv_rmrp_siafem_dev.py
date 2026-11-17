#!/usr/bin/env python3
"""Importação SIAFEM para CÓPIA de SQLite; jamais escreve no banco de origem.

A tabela de convênio-ano NÃO representa pagamento individual.
Data do pagamento e origem estatal específica permanecem indeterminadas.
"""
from __future__ import annotations

import argparse
import csv
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import sqlite3

SOURCE = "siafem_sp_transferencias_voluntarias"
ARTIFACT = "inv_rmrp_siafem_conv_ano_20261112"
URL = "https://www.fazenda.sp.gov.br/TransferenciaVoluntaria/Sistema/Novo/PesquisaComposta.aspx"


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter=";"))


def brl_to_cents(s):
    return int(Decimal(s.replace(".", "").replace(",", ".")) * 100)


def safe_backup(source: Path, target: Path):
    if source.resolve() == target.resolve() or target.exists() or not source.is_file():
        raise ValueError("A origem deve existir e a saída deve ser nova e diferente da origem")
    target.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(f"file:{source.resolve()}?mode=ro", uri=True) as src:
        with sqlite3.connect(target) as dst:
            src.backup(dst)


def import_dev(source, target, root):
    gov = root / "governance"
    roster = read_csv(gov / "INV_RMRP_34_MUNICIPIOS_PILOTO_IBGE_VERIFICADO_2026_11_11.csv")
    base = []
    for n in (1, 2):
        base += read_csv(gov / f"INV_RMRP_SIAFEM_INVESTIMENTO_2020_LOTE_0{n}_2026_11_12.csv")
    year = read_csv(gov / "INV_RMRP_SIAFEM_889_CONVENIO_ANO_EXATO_2026_11_12.csv")
    monthly = read_csv(gov / "INV_RMRP_SIAFEM_34_MUNICIPIOS_2020_2026_ANUAL_EXATO_2026_11_12.csv")
    roster_ids = {r["codigo_ibge"] for r in roster}
    if len(roster_ids) != len(roster) or len(roster) != 34:
        raise ValueError("Cadastro não possui 34 municípios IBGE7 únicos")
    if len(base) != 752 or len(year) != 889 or len(monthly) != 238:
        raise ValueError("Universo documental divergente")
    primary = {(r["codigo_ibge"], r["numero_convenio_siafem"]): r for r in base}
    if len(primary) != 752:
        raise ValueError("Identificador de instrumento duplicado")
    if {r["codigo_ibge"] for r in base} != roster_ids:
        raise ValueError("Cobertura RMRP divergente")
    if len({(r["codigo_ibge"], r["numero_convenio_siafem"], r["ano"]) for r in year}) != 889:
        raise ValueError("Identificador convênio-ano duplicado")
    if len({(r["codigo_ibge"], r["ano"]) for r in monthly}) != 238:
        raise ValueError("Município-ano duplicado")
    summary = {}
    count = {}
    for r in year:
        key = (r["codigo_ibge"], r["ano"])
        if (r["codigo_ibge"], r["numero_convenio_siafem"]) not in primary:
            raise ValueError("Instrumento anual sem cadastro")
        summary[key] = summary.get(key, 0) + int(r["valor_liberado_estornado_ano_centavos"])
        count[key] = count.get(key, 0) + int(r["pagamentos_ano"])
    for r in monthly:
        key = (r["codigo_ibge"], r["ano"])
        if summary.get(key, 0) != int(r["valor_liberado_estornado_exato_centavos"]):
            raise ValueError("Valor convênio-ano diverge do município-ano")
        if count.get(key, 0) != int(r["quantidade_pagamentos"]):
            raise ValueError("Contagem convênio-ano diverge do município-ano")
    if sum(summary.values()) != 30552102920 or sum(count.values()) != 1017:
        raise ValueError("Série regional diverge do controle oficial")

    input_file = gov / "INV_RMRP_SIAFEM_889_CONVENIO_ANO_EXATO_2026_11_12.csv"
    sha = hashlib.sha256(input_file.read_bytes()).hexdigest()
    safe_backup(source, target)
    conn = sqlite3.connect(target)
    conn.execute("PRAGMA foreign_keys=ON")
    try:
        db_ids = {x[0] for x in conn.execute("SELECT codigo_ibge FROM municipio")}
        if roster_ids - db_ids:
            raise ValueError("O banco não possui todos os municípios do cadastro RMRP")
        schema = gov / "proposals/INV_RMRP_SCHEMA_EXTENSAO_SQLITE_2026_11_11.sql"
        conn.executescript(schema.read_text(encoding="utf-8"))
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS inv_siafem_convenio_ano (
              instrumento_id TEXT NOT NULL REFERENCES inv_instrumento(instrumento_id),
              codigo_ibge TEXT NOT NULL REFERENCES municipio(codigo_ibge),
              ano INTEGER NOT NULL CHECK(ano BETWEEN 2020 AND 2026),
              quantidade_pagamentos INTEGER NOT NULL CHECK(quantidade_pagamentos >= 0),
              valor_liberado_estornado_centavos INTEGER NOT NULL,
              artefato_id TEXT NOT NULL REFERENCES artefato_fonte(artefato_id),
              qa_status TEXT NOT NULL CHECK(qa_status IN
                  ('candidato','em_revisao','homologado','rejeitado')),
              PRIMARY KEY(instrumento_id, ano)
            );
            CREATE INDEX IF NOT EXISTS idx_inv_siafem_ano_municipio
              ON inv_siafem_convenio_ano(codigo_ibge, ano);
        """)
        conn.execute("BEGIN")
        conn.execute(
            "INSERT OR IGNORE INTO fonte(fonte_id,nome,orgao,sistema,url_publica) VALUES(?,?,?,?,?)",
            (SOURCE, "SIAFEM/SP Transferências Voluntárias", "SEFAZ/SP", "SIAFEM", URL)
        )
        conn.execute("""INSERT INTO artefato_fonte
          (artefato_id,fonte_id,nome,source_version,url,retrieved_at,sha256,mime_type,observacao)
          VALUES(?,?,?,?,?,?,?,?,?)""",
          (ARTIFACT, SOURCE, "RMRP - 889 convênio-ano exatos", "2026-11-12",
           URL, "2026-11-12", sha, "text/csv",
           "Série anual líquida, não representa pagamento individual ou gasto final"))
        cnpj_by_mun = {}
        for r in base:
            key = r["codigo_ibge"]
            cnpj = r["cnpj_convenente"]
            if len(cnpj) != 14 or not cnpj.isdigit():
                raise ValueError("CNPJ de convenente inválido")
            if key in cnpj_by_mun and cnpj_by_mun[key] != cnpj:
                raise ValueError("CNPJ municipal inconsistente")
            cnpj_by_mun[key] = cnpj
        names = {r["codigo_ibge"]: r["municipio"] for r in roster}
        for code in sorted(roster_ids):
            conn.execute("""INSERT INTO inv_ator
              (ator_id,nome,tipo_ente,cnpj,codigo_ibge_sede) VALUES(?,?,?,?,?)""",
              (f"prefeitura:{code}", f"Prefeitura Municipal de {names[code]}",
               "municipio", cnpj_by_mun[code], code))
        for (ibge, number), r in primary.items():
            instrument = f"siafem_sp:{ibge}:{number}"
            conn.execute("""INSERT INTO inv_instrumento
                (instrumento_id,fonte_sistema,fonte_modulo,id_origem,numero_publico,
                 tipo_juridico,beneficiario_ator_id,valor_global_centavos,qa_status)
                 VALUES(?,?,?,?,?,?,?,?,?)""",
                (instrument, "siafem_sp", "transferencias_voluntarias", f"{ibge}|{number}",
                 number, "convenio", f"prefeitura:{ibge}",
                 brl_to_cents(r["valor_convenio_brl"]), "em_revisao"))
        for r in year:
            instrument = f"siafem_sp:{r['codigo_ibge']}:{r['numero_convenio_siafem']}"
            conn.execute("""INSERT INTO inv_siafem_convenio_ano
                (instrumento_id,codigo_ibge,ano,quantidade_pagamentos,
                 valor_liberado_estornado_centavos,artefato_id,qa_status)
                VALUES(?,?,?,?,?,?,?)""",
                (instrument, r["codigo_ibge"], int(r["ano"]), int(r["pagamentos_ano"]),
                 int(r["valor_liberado_estornado_ano_centavos"]), ARTIFACT, "em_revisao"))
        if list(conn.execute("PRAGMA foreign_key_check")):
            raise ValueError("Falha de integridade referencial")
        if conn.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
            raise ValueError("Falha de integridade SQLite")
        values = conn.execute("""SELECT COUNT(*),SUM(valor_liberado_estornado_centavos),
                         SUM(quantidade_pagamentos) FROM inv_siafem_convenio_ano
                         WHERE artefato_id=?""", (ARTIFACT,)).fetchone()
        if values != (889, 30552102920, 1017):
            raise ValueError(f"Totais incorretos no SQLite de desenvolvimento: {values}")
        assert conn.execute("SELECT COUNT(*) FROM inv_instrumento WHERE fonte_sistema='siafem_sp'").fetchone()[0] == 752
        assert conn.execute("SELECT COUNT(*) FROM inv_ator WHERE ator_id LIKE 'prefeitura:%'").fetchone()[0] == 34
        conn.commit()
    except Exception:
        conn.rollback()
        conn.close()
        target.unlink(missing_ok=True)
        raise
    conn.close()
    qa = {
        "status": "COPIA_DEV_QA", "source_unchanged": True,
        "source_db": str(source), "target_db": str(target),
        "instruments": 752, "instrument_year_rows": 889, "municipalities": 34,
        "payments_count": 1017, "amount_cents": 30552102920,
        "financial_event_rows_added": 0, "approved_projects_added": 0,
        "data_sha256": sha,
        "limitations": [
          "Conênio-ano é agregado e não pagamento individual",
          "Montante transferido não é gasto municipal realizado",
          "Não há vínculo documental comprovado a projetos Obrasgov"
        ]
    }
    target.with_suffix(".siafem.qa.json").write_text(
        json.dumps(qa, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(qa, ensure_ascii=False))
    return qa


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--source-db", required=True, type=Path)
    p.add_argument("--output-db", required=True, type=Path)
    p.add_argument("--repo-root", type=Path, default=Path("."))
    args = p.parse_args()
    import_dev(args.source_db, args.output_db, args.repo_root.resolve())


if __name__ == "__main__":
    main()
