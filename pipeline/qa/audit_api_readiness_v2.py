"""Relatorio auditavel de prontidao da API v2; nao altera base ou arquivos publicados."""
from __future__ import annotations

import argparse
import json
import sqlite3
from collections import Counter
from pathlib import Path

from pipeline.build.export_static_data import write_json


REQUIRED_FIELDS = ("nome", "grupo", "tipo", "unidade", "definicao",
                   "periodicidade", "como_ler", "cautelas")


def audit_readiness(database: Path, output: Path, universe_id: str = "SP_645") -> dict:
    con = sqlite3.connect(database)
    con.row_factory = sqlite3.Row
    try:
        codes = [r[0] for r in con.execute(
            "SELECT codigo_ibge FROM universo_municipio WHERE universo_id=?",
            (universe_id,),
        )]
        if not codes:
            raise ValueError("Universo sem municipios: " + universe_id)
        variables = [dict(r) for r in con.execute(
            "SELECT * FROM variavel ORDER BY variavel_id"
        )]
        if not variables:
            raise ValueError("Catalogo de variaveis vazio")
        has_editorial = con.execute(
            "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='variavel_documentacao'"
        ).fetchone()[0] > 0
        editorial = {}
        if has_editorial:
            editorial = {
                r["variavel_id"]: dict(r) for r in con.execute(
                    """SELECT variavel_id,formula_publica,como_ler,limitacoes,
                              fonte_publica,documentation_version
                       FROM variavel_documentacao"""
                )
            }
        years = [r[0] for r in con.execute(
            """SELECT DISTINCT o.ano FROM observacao o
               JOIN universo_municipio um USING(codigo_ibge)
               WHERE um.universo_id=? ORDER BY o.ano""",
            (universe_id,),
        )]
        stats = {
            (r["variavel_id"], r["ano"], r["status"]): r["n"]
            for r in con.execute(
                """SELECT o.variavel_id,o.ano,o.status,COUNT(*) AS n
                   FROM observacao o
                   JOIN universo_municipio um USING(codigo_ibge)
                   WHERE um.universo_id=?
                   GROUP BY o.variavel_id,o.ano,o.status""",
                (universe_id,),
            )
        }
        entries = []
        for v in variables:
            doc = editorial.get(v["variavel_id"], {})
            def documented(field):
                if v.get(field) is not None and str(v[field]).strip():
                    return True
                mapping = {"formula": "formula_publica", "como_ler": "como_ler",
                           "cautelas": "limitacoes"}
                key = mapping.get(field)
                return bool(key and doc.get(key) is not None and str(doc[key]).strip())
            missing = [field for field in REQUIRED_FIELDS if not documented(field)]
            if v["tipo"] == "indicador_derivado" and not documented("formula"):
                missing.append("formula")
            series = []
            for year in years:
                counts = {s: stats.get((v["variavel_id"], year, s), 0)
                          for s in ("observado", "ausente", "nao_aplicavel", "em_revisao")}
                total = sum(counts.values())
                if total > len(codes):
                    raise ValueError(f"Observacoes excedem membros: {v['variavel_id']} {year}")
                counts["sem_registro"] = len(codes) - total
                series.append({"year": year, "expected": len(codes),
                               "states": counts, "coverage_pct":
                               round(100 * counts["observado"] / len(codes), 4)})
            entries.append({
                "variable_id": v["variavel_id"],
                "type": v["tipo"],
                "publishable": bool(v["publicavel"] and v["ativo"]),
                "missing_methodology_fields": missing,
                "editorial_documentation_version": doc.get("documentation_version"),
                "methodology_checked_in": "variavel + variavel_documentacao",
                "scale_verified": False if v["unidade"] == "percentual" else None,
                "years": series,
            })
        report = {
            "universe_id": universe_id, "municipality_count": len(codes),
            "variable_count": len(variables),
            "years": years, "variables": entries,
            "summary": {
                "publishable_variables": sum(x["publishable"] for x in entries),
                "variables_missing_methodology": sum(bool(x["missing_methodology_fields"])
                                                      for x in entries),
                "percentage_scale_audit_required": sum(x["scale_verified"] is False
                                                        for x in entries),
            },
            "methodology": "Diagnostico de prontidao, sem aprovacao automatica de dados.",
        }
        write_json(output, report)
        return report
    finally:
        con.close()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("database", type=Path)
    p.add_argument("output", type=Path)
    p.add_argument("--universe-id", default="SP_645")
    a = p.parse_args()
    report = audit_readiness(a.database, a.output, a.universe_id)
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
