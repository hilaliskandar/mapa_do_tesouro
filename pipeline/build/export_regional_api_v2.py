"""Exportador regional v2: universos, cobertura anual e contextos municipais.

Os estados de cobertura incluem sem_registro como categoria distinta de
ausente declarado. Nao infere valores nem altera a API editorial v1.
"""
from __future__ import annotations

import argparse
import json
import math
import sqlite3
from collections import Counter, defaultdict
from pathlib import Path

from pipeline.build.export_static_data import build_metadata, write_json


STATUSES = ("observado", "ausente", "nao_aplicavel", "em_revisao", "sem_registro")


def export_regional_api(database: Path, output: Path) -> dict:
    con = sqlite3.connect(database)
    con.row_factory = sqlite3.Row
    try:
        universes = [dict(r) for r in con.execute(
            "SELECT universo_id,nome,tipo FROM universo WHERE ativo=1 ORDER BY universo_id"
        )]
        variables = [dict(r) for r in con.execute(
            """SELECT variavel_id,nome,tipo,unidade,formula,definicao,
                      como_ler,cautelas,fonte_preferencial_id
               FROM variavel WHERE ativo=1 AND publicavel=1
               ORDER BY variavel_id"""
        )]
        metadata = build_metadata(con)
        years = [r[0] for r in con.execute("SELECT DISTINCT ano FROM observacao ORDER BY ano")]
        var_ids = [v["variavel_id"] for v in variables]
        result = []
        for universe in universes:
            uid = universe["universo_id"]
            members = [dict(r) for r in con.execute(
                """SELECT m.codigo_ibge,m.nome,m.uf
                   FROM universo_municipio um
                   JOIN municipio m ON m.codigo_ibge=um.codigo_ibge
                   WHERE um.universo_id=? ORDER BY m.codigo_ibge""",
                (uid,),
            )]
            codes = {m["codigo_ibge"] for m in members}
            if not codes:
                continue
            observations = [dict(r) for r in con.execute(
                """SELECT o.codigo_ibge,o.ano,o.variavel_id,o.status,o.valor_num,
                          o.valor_texto,o.fonte_id,o.referencia_origem
                   FROM observacao o
                   JOIN universo_municipio um ON o.codigo_ibge=um.codigo_ibge
                   JOIN variavel v ON v.variavel_id=o.variavel_id
                   WHERE um.universo_id=? AND v.ativo=1 AND v.publicavel=1
                   ORDER BY o.ano,o.variavel_id,o.codigo_ibge""",
                (uid,),
            )]
            observed_lookup = {(r["codigo_ibge"], r["ano"], r["variavel_id"]): r
                               for r in observations}
            coverage = []
            for year in years:
                for vid in var_ids:
                    counter = Counter()
                    nums = []
                    categories = Counter()
                    sources = Counter()
                    for code in codes:
                        row = observed_lookup.get((code, year, vid))
                        status = row["status"] if row else "sem_registro"
                        if status not in STATUSES:
                            raise ValueError(f"Estado invalido: {status}")
                        counter[status] += 1
                        if row and status == "observado":
                            if row["valor_num"] is not None:
                                if not math.isfinite(row["valor_num"]):
                                    raise ValueError(f"Numero nao finito: {uid}/{vid}/{year}/{code}")
                                nums.append(row["valor_num"])
                            elif row["valor_texto"] is not None:
                                categories[row["valor_texto"]] += 1
                        if row and row["fonte_id"]:
                            sources[row["fonte_id"]] += 1
                    entry = {
                        "year": year,
                        "variable_id": vid,
                        "expected": len(codes),
                        "observed": counter["observado"],
                        "coverage_pct": round(100 * counter["observado"] / len(codes), 4),
                        "status_counts": {s: counter[s] for s in STATUSES},
                        "source_counts": dict(sorted(sources.items())),
                    }
                    if nums:
                        entry["observed_numeric"] = {
                            "count": len(nums),
                            "mean": sum(nums) / len(nums),
                            "min": min(nums),
                            "max": max(nums),
                        }
                        unit = next(v["unidade"] for v in variables if v["variavel_id"] == vid)
                        kind = next(v["tipo"] for v in variables if v["variavel_id"] == vid)
                        if unit == "BRL" and kind in ("conta_oficial", "agregado_analitico"):
                            entry["observed_numeric"]["sum"] = sum(nums)
                        else:
                            entry["observed_numeric"]["sum"] = None
                            entry["observed_numeric"]["sum_policy"] = "not_additive"
                    if categories:
                        entry["observed_categories"] = dict(sorted(categories.items()))
                    coverage.append(entry)

            base = output / "universes" / uid
            write_json(base / "members.json", members)
            write_json(base / "coverage.json", {
                "universe": universe, "member_count": len(members),
                "years": years, "coverage": coverage, "build": metadata,
            })
            write_json(base / "context.json", {
                "universe": universe, "member_count": len(members),
                "members_path": f"/data/api/v2/universes/{uid}/members.json",
                "coverage_path": f"/data/api/v2/universes/{uid}/coverage.json",
                "years": years, "variable_ids": var_ids, "build": metadata,
            })
            for member in members:
                code = member["codigo_ibge"]
                entries = [r for r in observations if r["codigo_ibge"] == code]
                by_variable = defaultdict(list)
                for r in entries:
                    by_variable[r["variavel_id"]].append({
                        "year": r["ano"], "status": r["status"],
                        "value": (r["valor_num"] if r["valor_num"] is not None
                                  else r["valor_texto"]) if r["status"] == "observado" else None,
                        "source_id": r["fonte_id"],
                        "source_reference": r["referencia_origem"],
                    })
                write_json(base / "municipalities" / f"{code}.json", {
                    "municipality": member, "universe": universe,
                    "variables": dict(by_variable), "years": years,
                    "missing_record_policy": "sem_registro; nao equivale a ausente",
                    "build": metadata,
                })
            result.append({**universe, "member_count": len(members),
                           "coverage_path": f"universes/{uid}/coverage.json"})
        write_json(output / "catalog" / "universes.json", result)
        return {"universes": len(result),
                "municipality_universe_contexts": sum(x["member_count"] for x in result),
                "years": len(years), "variables": len(variables)}
    finally:
        con.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("database", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    print(json.dumps(export_regional_api(args.database, args.output),
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
