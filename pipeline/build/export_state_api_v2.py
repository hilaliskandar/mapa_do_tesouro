"""Exportacao estatica estadual da API v2, independente da API editorial v1.

Etapa inicial: catalogo integral, fichas municipais e manifesto.
Nao publica automaticamente. Estados sem linha sao 'sem_registro',
nao se confundindo com o estado 'ausente' declarado pela fonte.
"""
from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

from pipeline.build.export_static_data import build_metadata, write_json


def _dicts(con, sql, params=()):
    return [dict(row) for row in con.execute(sql, params)]


def export_state_api(database: Path, output: Path, *, universe_id: str = "SP_645") -> dict:
    """Materializa endpoints estaduais sem alterar o SQLite nem a API v1."""
    con = sqlite3.connect(database)
    con.row_factory = sqlite3.Row
    try:
        universe = con.execute(
            "SELECT universo_id,nome,tipo FROM universo WHERE universo_id=?",
            (universe_id,),
        ).fetchone()
        if universe is None:
            raise ValueError(f"Universo nao encontrado: {universe_id}")
        members = _dicts(
            con,
            """SELECT m.codigo_ibge,m.nome,m.uf
               FROM universo_municipio um
               JOIN municipio m ON m.codigo_ibge=um.codigo_ibge
               WHERE um.universo_id=?
               ORDER BY m.codigo_ibge""",
            (universe_id,),
        )
        codes = [m["codigo_ibge"] for m in members]
        if len(codes) != len(set(codes)):
            raise ValueError("Codigo IBGE duplicado")
        variables = _dicts(
            con,
            """SELECT variavel_id,nome,grupo,tipo,natureza,unidade,definicao,
                      formula,como_ler,cautelas,fonte_preferencial_id,
                      periodicidade,publicavel,ativo
               FROM variavel ORDER BY variavel_id""",
        )
        variables_by_id = {v["variavel_id"]: v for v in variables}
        years = [r[0] for r in con.execute(
            """SELECT DISTINCT o.ano FROM observacao o
               JOIN universo_municipio um ON um.codigo_ibge=o.codigo_ibge
               WHERE um.universo_id=? ORDER BY o.ano""", (universe_id,)
        )]
        crosswalk = _dicts(
            con, "SELECT * FROM crosswalk_variavel ORDER BY variavel_id,ano_inicio,prioridade"
        )
        crosswalk_by_variable = {}
        for entry in crosswalk:
            crosswalk_by_variable.setdefault(entry["variavel_id"], []).append(entry)
        # Nao incluir valores em revisao nem variaveis bloqueadas pelo catalogo.
        allowed = {v["variavel_id"] for v in variables if v["publicavel"] and v["ativo"]}
        observations = _dicts(
            con,
            """SELECT o.codigo_ibge,o.ano,o.variavel_id,o.valor_num,
                      o.valor_texto,o.status,o.fonte_id,o.referencia_origem
               FROM observacao o JOIN universo_municipio um
               ON um.codigo_ibge=o.codigo_ibge
               WHERE um.universo_id=? ORDER BY o.codigo_ibge,o.ano,o.variavel_id""",
            (universe_id,),
        )
        by_code = {code: [] for code in codes}
        for row in observations:
            if row["variavel_id"] not in allowed:
                continue
            if row["status"] == "em_revisao":
                row["valor_num"] = None
                row["valor_texto"] = None
            by_code[row["codigo_ibge"]].append(row)

        root = output
        root.mkdir(parents=True, exist_ok=True)
        write_json(root / "catalog" / "variables.json", {
            "catalog_count": len(variables),
            "variables": [{
                **v,
                "api_available": v["variavel_id"] in allowed,
                "crosswalk": crosswalk_by_variable.get(v["variavel_id"], []),
                "storage_scale": "nao_documentada",
                "display_multiplier": None,
            } for v in variables],
        })
        write_json(root / "catalog" / "municipalities.json", members)
        for member in members:
            code = member["codigo_ibge"]
            grouped = {}
            for row in by_code[code]:
                var_id = row["variavel_id"]
                grouped.setdefault(var_id, []).append({
                    "year": row["ano"],
                    "status": row["status"],
                    "value": (row["valor_num"] if row["valor_num"] is not None
                              else row["valor_texto"]),
                    "source_id": row["fonte_id"],
                    "source_reference": row["referencia_origem"],
                })
            write_json(root / "municipalities" / f"{code}.json", {
                "api_version": "v2-candidate",
                "municipality": member,
                "universe_id": universe_id,
                "years_in_universe": years,
                "variables": grouped,
                "missing_record_policy": "sem_registro; nunca inferir zero ou ausente",
                "catalog_path": "/data/api/v2/catalog/variables.json",
                "build": build_metadata(con),
            })
        manifest = {
            "api_version": "v2-candidate",
            "universe_id": universe_id,
            "municipality_count": len(members),
            "variable_catalog_count": len(variables),
            "exposed_variable_count": len(allowed),
            "observation_count": sum(map(len, by_code.values())),
            "years_with_observations": years,
            "build": build_metadata(con),
            "source_snapshot_qa": build_metadata(con).get("qa_status"),
            "publication_qa": "not_evaluated",
            "contracts": {
                "municipality": "/data/api/v2/municipalities/{codigo_ibge}.json",
                "variables": "/data/api/v2/catalog/variables.json",
                "municipalities": "/data/api/v2/catalog/municipalities.json",
            },
        }
        write_json(root / "manifest.json", manifest)
        return {
            "municipalities": len(members),
            "variables": len(variables),
            "observations": manifest["observation_count"],
        }
    finally:
        con.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("database", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--universe-id", default="SP_645")
    args = parser.parse_args()
    print(json.dumps(export_state_api(args.database, args.output,
                                      universe_id=args.universe_id),
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
