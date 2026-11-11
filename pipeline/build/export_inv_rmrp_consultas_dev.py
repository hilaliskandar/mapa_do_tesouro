#!/usr/bin/env python3
"""Gera consultas estáticas INV-RMRP a partir de SQLite de DESENVOLVIMENTO.

Os registros do piloto são candidatos; valores previstos não são agregados como
investimentos executados. Nunca exporta pagamentos não homologados.
Não altera o banco de entrada. Impede saída sobre pasta existente.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import sqlite3

SCHEMA = "inv-rmrp-sqlite-preview-v1"
STATES = ("candidato", "em_revisao", "homologado", "rejeitado")


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    path.write_text(text, encoding="utf-8")
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def ensure_parent(path):
    if path.exists():
        raise ValueError(f"Saída já existe: {path}")
    path.mkdir(parents=True)


def load_roster(path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f, delimiter=";"))
    ids = [r["codigo_ibge"] for r in rows]
    if len(rows) != 34 or len(set(ids)) != 34:
        raise ValueError("Universo da RMRP exige 34 códigos distintos")
    return sorted(rows, key=lambda r: r["codigo_ibge"])


def fetch_all(conn, sql, args=()):
    return [dict(row) for row in conn.execute(sql, args)]


def build(db, roster_path, output):
    rows = load_roster(roster_path)
    codes = {r["codigo_ibge"] for r in rows}
    if not db.is_file():
        raise FileNotFoundError(db)
    conn = sqlite3.connect(f"file:{db.resolve()}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    try:
        check = conn.execute("PRAGMA integrity_check").fetchone()[0]
        fk = list(conn.execute("PRAGMA foreign_key_check"))
        if check != "ok" or fk:
            raise RuntimeError("Banco de desenvolvimento com falhas de integridade")
        actual = {
            r[0] for r in conn.execute(
                "SELECT codigo_ibge FROM municipio WHERE codigo_ibge IN (%s)" %
                ",".join("?" for _ in codes), tuple(sorted(codes))
            )
        }
        if actual != codes:
            raise RuntimeError("RMRP/SQLite: falta código municipal na origem")
        projects = fetch_all(conn, """
            SELECT p.projeto_id, p.titulo, p.descricao, p.situacao_cadastral,
                   p.setor, p.natureza_intervencao, p.qa_status,
                   ie.identificador AS id_obrasgov, ie.sistema AS sistema_id,
                   a.url AS fonte_documental
            FROM inv_projeto p
            LEFT JOIN inv_identificador_externo ie ON ie.projeto_id=p.projeto_id
            LEFT JOIN artefato_fonte a ON a.artefato_id=ie.artefato_id
            ORDER BY p.projeto_id
        """)
        source_ids = [p["projeto_id"] for p in projects]
        if len(source_ids) != len(set(source_ids)):
            raise RuntimeError("Mais de um identificador externo por projeto: contrato exige ajuste")
        link_rows = fetch_all(conn, """
            SELECT projeto_id, codigo_ibge, papel, qualidade
            FROM inv_projeto_municipio
            WHERE papel='local_execucao'
            ORDER BY projeto_id,codigo_ibge
        """)
        geo_rows = fetch_all(conn, """
            SELECT projeto_id, sequencia, latitude, longitude, precisao, crs_origem
            FROM inv_localizacao
            ORDER BY projeto_id, sequencia
        """)
        events = fetch_all(conn, """
            SELECT evento_id, projeto_id, estagio, natureza_fluxo, natureza_despesa,
                   valor_centavos, qa_status, fonte_sistema, documento_origem
            FROM inv_evento_financeiro ORDER BY projeto_id,evento_id
        """)
        if any(e["qa_status"] not in STATES for e in events):
            raise RuntimeError("Estado de QA desconhecido em evento")
        unknown_projects = set(x["projeto_id"] for x in link_rows + geo_rows + events) - set(source_ids)
        if unknown_projects:
            raise RuntimeError(f"Referência a projetos desconhecidos: {unknown_projects}")
        # Política da primeira prévia: sem eventos pagos até homologação completa.
        forbidden = [e for e in events
                     if e["estagio"] in {"pago", "transferido", "liquidado"}
                     and e["qa_status"] != "homologado"]
        if forbidden:
            raise RuntimeError("Evento pago/transferido/liquidado sem homologação não pode ser exportado")
        rejected = [e for e in events if e["qa_status"] == "rejeitado"]
        if rejected:
            raise RuntimeError("Eventos rejeitados não devem alimentar a prévia")
        ensure_parent(output)
        hashes = {}
        by_project = {p["projeto_id"]: {
            **p, "localizacao": [], "municipios_intersecao": [],
            "eventos_candidatos": [], "valores_publicaveis_centavos": None,
            "nota": "Valores previstos não são investimento liquidado/pago; localização por ponto é candidata."
        } for p in projects}
        for v in link_rows:
            by_project[v["projeto_id"]]["municipios_intersecao"].append({
                "codigo_ibge": v["codigo_ibge"], "papel": v["papel"],
                "qualidade": v["qualidade"]})
        for v in geo_rows:
            by_project[v["projeto_id"]]["localizacao"].append({
                "latitude": v["latitude"], "longitude": v["longitude"],
                "precisao": v["precisao"], "crs_origem": v["crs_origem"]})
        for e in events:
            by_project[e["projeto_id"]]["eventos_candidatos"].append({
                "evento_id": e["evento_id"], "estagio": e["estagio"],
                "natureza_fluxo": e["natureza_fluxo"],
                "natureza_despesa": e["natureza_despesa"],
                "valor_centavos": e["valor_centavos"],
                "qa_status": e["qa_status"],
                "fonte_sistema": e["fonte_sistema"],
                "documento_origem": e["documento_origem"]})
        for project in projects:
            pid = project["projeto_id"]
            safeid = hashlib.sha256(pid.encode("utf-8")).hexdigest()[:24]
            path = Path("projetos") / f"{safeid}.json"
            hashes[str(path)] = dump(output / path, by_project[pid])
            by_project[pid]["arquivo_detalhe"] = str(path)
        municipio_summaries = []
        for city in rows:
            ibge = city["codigo_ibge"]
            local_projects = [p for p in by_project.values() if any(
                m["codigo_ibge"] == ibge for m in p["municipios_intersecao"])]
            items = [
                {"projeto_id": p["projeto_id"], "titulo": p["titulo"],
                 "qa_status": p["qa_status"], "situacao": p["situacao_cadastral"],
                 "arquivo_detalhe": p["arquivo_detalhe"]}
                for p in local_projects
            ]
            info = {
                "codigo_ibge": ibge,
                "municipio": city["municipio"],
                "sub_regiao": city["sub_regiao"],
                "qa_status": "consulta_exploratoria_nao_homologada",
                "cobertura": {"obrasgov": "amostra_224_projetos_busca_nominal",
                              "transferegov": "nao_integrado_sqlite",
                              "sistema_estadual": "nao_integrado_sqlite"},
                "metricas_candidatas": {
                    "projetos_com_ponto_no_municipio": len(local_projects),
                    "investimento_publico_executado_centavos": None,
                    "transferencias_federais_pagas_centavos": None,
                    "transferencias_estaduais_pagas_centavos": None},
                "projetos": items
            }
            path = Path("municipios") / f"{ibge}.json"
            hashes[str(path)] = dump(output / path, info)
            municipio_summaries.append({
                "codigo_ibge": ibge, "municipio": city["municipio"],
                "sub_regiao": city["sub_regiao"],
                "projetos_com_ponto_no_municipio": len(items),
                "arquivo": str(path)})
        hashes["municipios.json"] = dump(output / "municipios.json", municipio_summaries)
        summary = {
            "schema": SCHEMA,
            "qa_status": "dev_only_non_published_candidates",
            "universo": "RMRP_34",
            "municípios": 34,
            "projetos_candidatos": len(projects),
            "projetos_com_ao_menos_um_municipio": sum(
                bool(p["municipios_intersecao"]) for p in by_project.values()),
            "relacoes_municipais": len(link_rows),
            "pontos": len(geo_rows),
            "eventos_candidatos": len(events),
            "eventos_pagos_homologados": sum(
                e["estagio"] == "pago" and e["qa_status"] == "homologado" for e in events),
            "consultas_individuais": len(rows),
            "arquivos_sha256": hashes,
            "limits": [
                "Valores de previsão não representam investimentos executados",
                "Projetos são candidatos obtidos por busca nominal, não censo da RMRP",
                "A localização por coordenadas ainda não foi validada documentalmente",
                "Municípios sem projetos na amostra não são municípios sem investimentos",
                "Não há atribuição monetária ou rateio a projetos plurimunicipais",
            ]}
        dump(output / "manifest.json", summary)
        return summary
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", type=Path, required=True)
    parser.add_argument("--roster", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    res = build(args.db, args.roster, args.out)
    print(json.dumps({k: v for k, v in res.items() if k != "arquivos_sha256"},
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
