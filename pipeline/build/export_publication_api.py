from __future__ import annotations

import argparse
import json
import math
import sqlite3
import statistics
from pathlib import Path

import yaml

from pipeline.build.export_static_data import build_metadata, write_json


def _load_yaml(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Catalogo YAML invalido: {path}")
    return data


def _median(values: list[float]) -> float | None:
    return statistics.median(values) if values else None


def _quartiles(values: list[float]) -> tuple[float | None, float | None]:
    ordered = sorted(values)
    n = len(ordered)
    if n < 2:
        return (ordered[0], ordered[0]) if ordered else (None, None)
    mid = n // 2
    lower = ordered[:mid]
    upper = ordered[mid + (n % 2):]
    q1 = statistics.median(lower) if lower else ordered[0]
    q3 = statistics.median(upper) if upper else ordered[-1]
    return q1, q3


def _relative_position(value: float, values: list[float], median: float | None) -> dict:
    if not values:
        return {}
    less = sum(1 for item in values if item < value)
    equal = sum(1 for item in values if item == value)
    percentile = 100.0 * (less + 0.5 * equal) / len(values)
    if percentile <= 25:
        quartile = 1
    elif percentile <= 50:
        quartile = 2
    elif percentile <= 75:
        quartile = 3
    else:
        quartile = 4
    rank_desc = 1 + sum(1 for item in values if item > value)
    diff = None if median is None else value - median
    diff_pct = None
    if median not in (None, 0):
        diff_pct = 100.0 * diff / abs(median)
    return {
        "percentile": round(percentile, 4),
        "quartile": quartile,
        "rank_desc": rank_desc,
        "difference_from_median": diff,
        "difference_from_median_pct": diff_pct,
    }


def _members(
    con: sqlite3.Connection,
    source_universe_id: str,
    excluded_codes: set[str],
) -> list[dict]:
    rows = con.execute(
        """
        SELECT m.codigo_ibge,m.nome,m.uf
        FROM universo_municipio u
        JOIN municipio m USING(codigo_ibge)
        WHERE u.universo_id=?
        ORDER BY m.nome,m.codigo_ibge
        """,
        (source_universe_id,),
    ).fetchall()
    return [
        dict(row)
        for row in rows
        if row["codigo_ibge"] not in excluded_codes
    ]


def _variable_metadata(
    con: sqlite3.Connection,
    variable_ids: list[str],
) -> dict[str, dict]:
    placeholders = ",".join("?" for _ in variable_ids)
    rows = con.execute(
        f"""
        SELECT variavel_id,nome,grupo,tipo,natureza,unidade,definicao,
               formula,como_ler,cautelas,fonte_preferencial_id,periodicidade
        FROM variavel
        WHERE variavel_id IN ({placeholders})
        """,
        tuple(variable_ids),
    ).fetchall()
    return {row["variavel_id"]: dict(row) for row in rows}


def _observations(
    con: sqlite3.Connection,
    member_codes: list[str],
    variable_ids: list[str],
) -> list[dict]:
    if not member_codes or not variable_ids:
        return []
    member_ph = ",".join("?" for _ in member_codes)
    variable_ph = ",".join("?" for _ in variable_ids)
    rows = con.execute(
        f"""
        SELECT o.codigo_ibge,m.nome AS municipio,o.ano,o.variavel_id,
               o.valor_num,o.valor_texto,o.status,o.fonte_id,o.referencia_origem
        FROM observacao o
        JOIN municipio m USING(codigo_ibge)
        WHERE o.codigo_ibge IN ({member_ph})
          AND o.variavel_id IN ({variable_ph})
        ORDER BY o.variavel_id,o.ano,m.nome
        """,
        tuple(member_codes) + tuple(variable_ids),
    ).fetchall()
    return [dict(row) for row in rows]


def _stats_for_rows(rows: list[dict], expected: int) -> dict:
    status_counts = {
        "observado": 0,
        "ausente": 0,
        "nao_aplicavel": 0,
        "em_revisao": 0,
    }
    numeric_rows = []
    categories: dict[str, int] = {}
    for row in rows:
        status = row["status"]
        status_counts[status] = status_counts.get(status, 0) + 1
        if status != "observado":
            continue
        if row["valor_num"] is not None:
            numeric_rows.append(row)
        elif row["valor_texto"] is not None:
            key = str(row["valor_texto"])
            categories[key] = categories.get(key, 0) + 1

    observed = status_counts.get("observado", 0)
    payload = {
        "expected": expected,
        "observed": observed,
        "coverage_pct": round(100.0 * observed / expected, 4) if expected else None,
        "status_counts": status_counts,
    }

    if numeric_rows:
        values = [float(row["valor_num"]) for row in numeric_rows]
        med = _median(values)
        q1, q3 = _quartiles(values)
        min_row = min(numeric_rows, key=lambda row: row["valor_num"])
        max_row = max(numeric_rows, key=lambda row: row["valor_num"])
        payload["numeric"] = {
            "sum": sum(values),
            "mean": statistics.fmean(values),
            "median": med,
            "q1": q1,
            "q3": q3,
            "min": {
                "value": min_row["valor_num"],
                "codigo_ibge": min_row["codigo_ibge"],
                "municipio": min_row["municipio"],
            },
            "max": {
                "value": max_row["valor_num"],
                "codigo_ibge": max_row["codigo_ibge"],
                "municipio": max_row["municipio"],
            },
        }
    if categories:
        payload["categorical"] = {
            "counts": dict(sorted(categories.items())),
        }
    return payload


def export_publication_api(
    database: Path,
    output: Path,
    *,
    universes_catalog: Path,
    variables_catalog: Path,
) -> dict:
    output.mkdir(parents=True, exist_ok=True)
    universes_doc = _load_yaml(universes_catalog)
    variables_doc = _load_yaml(variables_catalog)
    publication_universes = universes_doc.get("publication_universes", [])
    groups = variables_doc.get("groups", {})
    variable_ids = list(dict.fromkeys(
        variable_id
        for group_ids in groups.values()
        for variable_id in group_ids
    ))

    con = sqlite3.connect(database)
    con.row_factory = sqlite3.Row
    try:
        metadata = build_metadata(con)
        variable_meta = _variable_metadata(con, variable_ids)
        missing_variables = [
            variable_id for variable_id in variable_ids
            if variable_id not in variable_meta
        ]
        if missing_variables:
            raise ValueError(
                "Variaveis editoriais ausentes do banco: "
                + ", ".join(missing_variables)
            )

        index = []
        total_contexts = 0
        total_municipality_contexts = 0

        for universe in publication_universes:
            publication_id = universe["publication_id"]
            source_universe_id = universe["source_universe_id"]
            excluded = {
                str(item["codigo_ibge"])
                for item in universe.get("exclude_members", [])
            }
            members = _members(con, source_universe_id, excluded)
            member_codes = [item["codigo_ibge"] for item in members]
            rows = _observations(con, member_codes, variable_ids)
            years = sorted({row["ano"] for row in rows})
            latest_year = years[-1] if years else None

            rows_by_variable_year: dict[tuple[str, int], list[dict]] = {}
            rows_by_municipality_variable: dict[tuple[str, str], list[dict]] = {}
            for row in rows:
                rows_by_variable_year.setdefault(
                    (row["variavel_id"], row["ano"]), []
                ).append(row)
                rows_by_municipality_variable.setdefault(
                    (row["codigo_ibge"], row["variavel_id"]), []
                ).append(row)

            variable_contexts = {}
            for variable_id in variable_ids:
                meta = variable_meta[variable_id]
                yearly = []
                for year in years:
                    year_rows = rows_by_variable_year.get((variable_id, year), [])
                    if not year_rows:
                        continue
                    yearly.append({
                        "year": year,
                        **_stats_for_rows(year_rows, len(members)),
                    })
                variable_contexts[variable_id] = {
                    "metadata": meta,
                    "editorial_group": next(
                        (
                            group_name
                            for group_name, group_ids in groups.items()
                            if variable_id in group_ids
                        ),
                        None,
                    ),
                    "yearly": yearly,
                    "latest": next(
                        (
                            item for item in reversed(yearly)
                            if item["year"] == latest_year
                        ),
                        None,
                    ),
                }

            universe_payload = {
                "api_version": "v1",
                "publication_id": publication_id,
                "name": universe["name"],
                "type": universe["type"],
                "source_universe_id": source_universe_id,
                "excluded_members": universe.get("exclude_members", []),
                "member_count": len(members),
                "members": members,
                "years": years,
                "latest_year": latest_year,
                "build": metadata,
                "rules": variables_doc.get("rules", {}),
                "variable_groups": groups,
                "variables": variable_contexts,
            }

            universe_dir = output / "publication" / "universes" / publication_id
            write_json(universe_dir / "context.json", universe_payload)
            write_json(universe_dir / "municipalities.json", members)
            total_contexts += 1

            for member in members:
                code = member["codigo_ibge"]
                municipality_variables = {}
                for variable_id in variable_ids:
                    series_rows = rows_by_municipality_variable.get(
                        (code, variable_id), []
                    )
                    series = [
                        {
                            "year": row["ano"],
                            "status": row["status"],
                            "value": (
                                row["valor_num"]
                                if row["valor_num"] is not None
                                else row["valor_texto"]
                            ),
                            "fonte_id": row["fonte_id"],
                            "referencia_origem": row["referencia_origem"],
                        }
                        for row in series_rows
                    ]
                    latest = next(
                        (
                            row for row in reversed(series_rows)
                            if row["ano"] == latest_year
                        ),
                        None,
                    )
                    relative = None
                    if (
                        latest is not None
                        and latest["status"] == "observado"
                        and latest["valor_num"] is not None
                    ):
                        group_rows = [
                            row for row in rows_by_variable_year.get(
                                (variable_id, latest_year), []
                            )
                            if row["status"] == "observado"
                            and row["valor_num"] is not None
                        ]
                        values = [float(row["valor_num"]) for row in group_rows]
                        relative = _relative_position(
                            float(latest["valor_num"]),
                            values,
                            _median(values),
                        )
                    municipality_variables[variable_id] = {
                        "metadata": variable_meta[variable_id],
                        "editorial_group": next(
                            (
                                group_name
                                for group_name, group_ids in groups.items()
                                if variable_id in group_ids
                            ),
                            None,
                        ),
                        "series": series,
                        "latest": (
                            {
                                "year": latest["ano"],
                                "status": latest["status"],
                                "value": (
                                    latest["valor_num"]
                                    if latest["valor_num"] is not None
                                    else latest["valor_texto"]
                                ),
                                "fonte_id": latest["fonte_id"],
                                "referencia_origem": latest["referencia_origem"],
                            }
                            if latest is not None
                            else None
                        ),
                        "relative_latest": relative,
                        "group_latest": variable_contexts[variable_id]["latest"],
                    }

                municipality_payload = {
                    "api_version": "v1",
                    "publication_universe": {
                        "publication_id": publication_id,
                        "name": universe["name"],
                        "type": universe["type"],
                        "member_count": len(members),
                    },
                    "municipality": member,
                    "years": years,
                    "latest_year": latest_year,
                    "build": metadata,
                    "rules": variables_doc.get("rules", {}),
                    "variables": municipality_variables,
                }
                write_json(
                    universe_dir / "municipalities" / f"{code}.json",
                    municipality_payload,
                )
                total_municipality_contexts += 1

            index.append({
                "publication_id": publication_id,
                "name": universe["name"],
                "type": universe["type"],
                "source_universe_id": source_universe_id,
                "member_count": len(members),
                "excluded_members": universe.get("exclude_members", []),
                "latest_year": latest_year,
                "context_path": (
                    f"publication/universes/{publication_id}/context.json"
                ),
                "municipalities_path": (
                    f"publication/universes/{publication_id}/municipalities.json"
                ),
            })

        write_json(output / "publication" / "universes.json", index)
        contract = {
            "api_version": "v1",
            "publication_universe_count": len(index),
            "municipality_context_count": total_municipality_contexts,
            "contracts": {
                "universe_index": "/data/api/v1/publication/universes.json",
                "universe_context": (
                    "/data/api/v1/publication/universes/{publication_id}/context.json"
                ),
                "universe_municipalities": (
                    "/data/api/v1/publication/universes/{publication_id}/municipalities.json"
                ),
                "municipality_context": (
                    "/data/api/v1/publication/universes/{publication_id}/"
                    "municipalities/{codigo_ibge}.json"
                ),
            },
            "rules": variables_doc.get("rules", {}),
            "build": metadata,
        }
        write_json(output / "publication" / "contract.json", contract)

    finally:
        con.close()

    return {
        "publication_universes": total_contexts,
        "municipality_contexts": total_municipality_contexts,
        "variables": len(variable_ids),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Exporta a API estatica de contextos editoriais."
    )
    parser.add_argument("database", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--universes-catalog", type=Path, required=True)
    parser.add_argument("--variables-catalog", type=Path, required=True)
    args = parser.parse_args()
    result = export_publication_api(
        args.database,
        args.output,
        universes_catalog=args.universes_catalog,
        variables_catalog=args.variables_catalog,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
