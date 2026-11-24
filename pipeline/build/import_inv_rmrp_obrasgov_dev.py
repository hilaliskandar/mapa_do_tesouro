#!/usr/bin/env python3
"""Importador read-only da base canônica -> CÓPIA SQLite INV RMRP para QA.

NUNCA altera a origem. Carrega somente projetos exploratórios como qa_status=candidato.
Valores previstos são eventos 'previsto' e NÃO entram nas despesas de investimento executado.
"""
from __future__ import annotations

import argparse
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import hashlib
import json
from pathlib import Path
import sqlite3


SOURCE_ID = "obrasgov_api"
ARTEFACT_ID = "obrasgov_rmrp_triagem_espacial_20261111"


def centavos(value):
    if value is None:
        return None
    try:
        dec = Decimal(str(value))
        if not dec.is_finite():
            return None
        return int((dec * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
    except (InvalidOperation, ValueError):
        return None


def read_roster(path):
    import csv
    with path.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f, delimiter=";"))
    codes = {r["codigo_ibge"] for r in rows}
    if len(rows) != 34 or len(codes) != 34:
        raise ValueError("RMRP deve conter 34 codigos IBGE7 unicos")
    return codes


def copy_sqlite(source, target):
    if source.resolve() == target.resolve() or target.exists():
        raise ValueError("Saída já existe ou é idêntica à origem; não sobrescrever")
    target.parent.mkdir(parents=True, exist_ok=True)
    src = sqlite3.connect(f"file:{source.resolve()}?mode=ro", uri=True)
    dst = sqlite3.connect(target)
    try:
        src.backup(dst)
        dst.commit()
    finally:
        src.close()
        dst.close()


def import_to_dev(source, target, roster, candidates, schema):
    codes = read_roster(roster)
    blob = candidates.read_bytes()
    dataset = json.loads(blob)
    if dataset["meta"]["qa_status"] != "triagem_espacial_nao_validacao_financeira":
        raise ValueError("Entrada não qualificada como triagem")
    ids = [x["id"] for x in dataset["items"]]
    if len(ids) != len(set(ids)):
        raise ValueError("IDs Obrasgov repetidos")
    if {m["codigo_ibge"] for m in dataset["municipios"]} != codes:
        raise ValueError("Cadastro de municípios da fonte diverge do roster")

    copy_sqlite(source, target)
    conn = sqlite3.connect(target)
    conn.execute("PRAGMA foreign_keys=ON")
    try:
        valid = {x[0] for x in conn.execute("SELECT codigo_ibge FROM municipio")}
        absent = sorted(codes - valid)
        if absent:
            raise RuntimeError(f"Municípios não encontrados no SQLite canônico: {absent}")
        conn.executescript(schema.read_text(encoding="utf-8"))
        conn.execute("BEGIN")
        conn.execute("INSERT OR IGNORE INTO fonte(fonte_id,nome,orgao,sistema,url_publica) VALUES(?,?,?,?,?)",
                     (SOURCE_ID, "Obrasgov API pública", "Governo Federal", "Obrasgov",
                      "https://api-publica.obrasgov.gestao.gov.br/obras/"))
        conn.execute(
            "INSERT INTO artefato_fonte(artefato_id,fonte_id,nome,source_version,url,retrieved_at,sha256,mime_type,observacao) VALUES(?,?,?,?,?,?,?,?,?)",
            (ARTEFACT_ID, SOURCE_ID, "RMRP Obrasgov - triagem espacial candidatos",
             "2026-11-11", "https://github.com/hilaliskandar/mapa_do_tesouro/blob/"
             "investimentos-territoriais-sp645-20261111/app/static/data/api/v3/investimentos/"
             "rmrp/obrasgov-triagem-espacial.json",
             "2026-11-11", hashlib.sha256(blob).hexdigest(), "application/json",
             "Amostra textual e QA ponto-poligono; NAO e censo Obrasgov nem pagamentos"))
        financial = links = points = 0
        for rec in dataset["items"]:
            pid = "obrasgov:" + rec["id"]
            title = rec.get("nome") or rec["id"]
            conn.execute(
                "INSERT INTO inv_projeto(projeto_id,titulo,descricao,situacao_cadastral,"
                "id_fonte_preferencial,qa_status) VALUES(?,?,?,?,?,?)",
                (pid, title, rec.get("descricao"), rec.get("situacao"), SOURCE_ID, "candidato"))
            conn.execute(
                "INSERT INTO inv_identificador_externo(sistema,modulo,identificador,projeto_id,artefato_id)"
                " VALUES(?,?,?,?,?)",
                ("obrasgov", "projeto-investimento", rec["id"], pid, ARTEFACT_ID))
            for m in rec.get("municipios_intersecao", []):
                if m["code"] not in codes:
                    raise ValueError("Localização fora do cadastro RMRP: " + m["code"])
                conn.execute(
                    "INSERT INTO inv_projeto_municipio(projeto_id,codigo_ibge,papel,qualidade,artefato_id)"
                    " VALUES(?,?,?,?,?)",
                    (pid, m["code"], "local_execucao", "intersecao_geometrica", ARTEFACT_ID))
                links += 1
            for order, point in enumerate(rec.get("coordenadas") or [], 1):
                try:
                    lat, lon = float(point["lat"]), float(point["lon"])
                except (TypeError, ValueError, KeyError):
                    continue
                if not (-90 <= lat <= 90 and -180 <= lon <= 180):
                    continue
                conn.execute(
                    "INSERT INTO inv_localizacao(projeto_id,sequencia,latitude,longitude,"
                    "precisao,crs_origem,artefato_id) VALUES(?,?,?,?,?,?,?)",
                    (pid, order, lat, lon, "coordenada_fonte", "EPSG:4326", ARTEFACT_ID))
                points += 1
            for n, f in enumerate(rec.get("fontes_previstas") or [], 1):
                cents = centavos(f.get("valor"))
                if cents is None:
                    continue
                conn.execute(
                    "INSERT INTO inv_evento_financeiro(evento_id,fonte_sistema,fonte_modulo,"
                    "documento_origem,linha_origem,projeto_id,estagio,natureza_fluxo,"
                    "natureza_despesa,valor_centavos,artefato_id,qa_status)"
                    " VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                    ("obrasgov:" + rec["id"] + ":previsto:" + str(n),
                     "obrasgov", "projeto-investimento", rec["id"], str(n), pid,
                     "previsto", "outro", "nao_classificado", cents, ARTEFACT_ID,
                     "candidato"))
                financial += 1
        violations = list(conn.execute("PRAGMA foreign_key_check"))
        if violations:
            raise RuntimeError(f"Violação FK em staging: {violations[:5]}")
        conn.commit()
        counts = {
            "project_candidates": conn.execute(
                "SELECT COUNT(*) FROM inv_projeto WHERE qa_status='candidato'"
            ).fetchone()[0],
            "municipality_links": links,
            "location_points": points,
            "planned_events": financial,
            "paid_events": conn.execute(
                "SELECT COUNT(*) FROM inv_evento_financeiro WHERE estagio='pago'"
            ).fetchone()[0],
            "approved_projects": conn.execute(
                "SELECT COUNT(*) FROM inv_projeto WHERE qa_status='homologado'"
            ).fetchone()[0],
            "municipalities_validated": len(codes),
        }
        if counts["project_candidates"] != len(ids) or counts["paid_events"] or counts["approved_projects"]:
            raise RuntimeError("Falha QA contagem e/ou segregação de candidatos")
    except Exception:
        conn.rollback()
        conn.close()
        # Target é descartável; remover cópia para impedir leitura parcial.
        target.unlink(missing_ok=True)
        raise
    conn.close()
    meta = {"state": "dev_only_qa_candidates", "canonical_untouched": True,
            "source": str(source), "destination": str(target),
            "input_sha256": hashlib.sha256(blob).hexdigest(),
            "counts": counts, "limits": [
                "Municipio no ponto nao confirma local juridico da obra",
                "Previsto nao equivale a pago ou investido",
                "Propostas Transferegov, instrumentos e pagamentos ainda nao vinculados"
            ]}
    target.with_suffix(".qa.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(meta, ensure_ascii=False))
    return meta


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-db", required=True, type=Path)
    parser.add_argument("--output-db", required=True, type=Path)
    parser.add_argument("--roster", required=True, type=Path)
    parser.add_argument("--candidates", required=True, type=Path)
    parser.add_argument("--schema", type=Path, default=Path(
        "governance/proposals/INV_RMRP_SCHEMA_EXTENSAO_SQLITE_2026_11_11.sql"))
    args = parser.parse_args()
    import_to_dev(args.source_db, args.output_db, args.roster, args.candidates, args.schema)


if __name__ == "__main__":
    main()
