from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
from pathlib import Path

from pipeline.build.export_documentation import export_documentation


def write_json(path: Path, payload) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    content = json.dumps(
        payload,
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
        separators=(",", ": "),
    ) + "\n"
    path.write_text(content, encoding="utf-8")
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def build_metadata(con: sqlite3.Connection) -> dict:
    con.row_factory = sqlite3.Row
    row = con.execute(
        """
        SELECT build_id,build_timestamp,data_version,methodology_version,
               app_version,schema_version,data_sha256,qa_status,notes
        FROM build
        ORDER BY build_timestamp DESC
        LIMIT 1
        """
    ).fetchone()
    if row is None:
        return {}
    return dict(row)


def export_static_data(
    database: Path,
    output: Path,
    universe_id: str = "TIC_TIM_30",
) -> dict:
    output.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(database)
    con.row_factory = sqlite3.Row

    try:
        metadata = build_metadata(con)
        universe = con.execute(
            """
            SELECT universo_id,nome,descricao,tipo
            FROM universo
            WHERE universo_id=?
            """,
            (universe_id,),
        ).fetchone()
        if universe is None:
            raise ValueError(f"Universo inexistente: {universe_id}")

        municipalities = [
            dict(row)
            for row in con.execute(
                """
                SELECT m.codigo_ibge,m.nome,m.uf
                FROM universo_municipio u
                JOIN municipio m USING(codigo_ibge)
                WHERE u.universo_id=?
                ORDER BY m.nome,m.codigo_ibge
                """,
                (universe_id,),
            )
        ]

        years = [
            row[0]
            for row in con.execute(
                """
                SELECT DISTINCT o.ano
                FROM observacao o
                JOIN universo_municipio u USING(codigo_ibge)
                WHERE u.universo_id=?
                ORDER BY o.ano
                """,
                (universe_id,),
            )
        ]

        variable_ids = [
            row[0]
            for row in con.execute(
                """
                SELECT variavel_id
                FROM variavel
                WHERE publicavel=1 AND ativo=1
                ORDER BY variavel_id
                """
            )
        ]

        manifest = {
            "universe": dict(universe),
            "build": metadata,
            "years": years,
            "municipality_count": len(municipalities),
            "variable_count": len(variable_ids),
            "contracts": {
                "annual_snapshot": "/data/annual/{year}.json",
                "municipality": "/data/municipalities/{codigo_ibge}.json",
                "catalog": "/data/catalog/variables/{variavel_id}.json",
                "methodology": "/data/methodology/{secao_id}.json",
                "crosswalk": "/data/crosswalk.json",
                "coverage": "/data/coverage.json",
            },
        }

        hashes = {}
        hashes["metadata.json"] = write_json(output / "metadata.json", manifest)
        hashes["municipalities.json"] = write_json(
            output / "municipalities.json", municipalities
        )

        # Um snapshot por ano: suficiente para mapa, ranking e comparação.
        for year in years:
            rows = con.execute(
                """
                SELECT
                    o.codigo_ibge,
                    m.nome AS municipio,
                    o.variavel_id,
                    o.valor_num,
                    o.valor_texto,
                    o.status
                FROM observacao o
                JOIN municipio m USING(codigo_ibge)
                JOIN universo_municipio u USING(codigo_ibge)
                JOIN variavel v USING(variavel_id)
                WHERE u.universo_id=?
                  AND o.ano=?
                  AND v.publicavel=1
                  AND v.ativo=1
                ORDER BY m.nome,o.variavel_id
                """,
                (universe_id, year),
            ).fetchall()

            by_municipality = {
                item["codigo_ibge"]: {
                    "codigo_ibge": item["codigo_ibge"],
                    "municipio": item["nome"],
                    "values": {},
                }
                for item in municipalities
            }
            for row in rows:
                entry = {
                    "status": row["status"],
                    "value": (
                        row["valor_num"]
                        if row["valor_num"] is not None
                        else row["valor_texto"]
                    ),
                }
                by_municipality[row["codigo_ibge"]]["values"][
                    row["variavel_id"]
                ] = entry

            rel = f"annual/{year}.json"
            hashes[rel] = write_json(
                output / rel,
                {
                    "year": year,
                    "universe_id": universe_id,
                    "municipalities": list(by_municipality.values()),
                },
            )

        # Um arquivo por município: séries, tipologias, marcadores e pares.
        for municipality in municipalities:
            code = municipality["codigo_ibge"]
            observations = [
                dict(row)
                for row in con.execute(
                    """
                    SELECT ano,variavel_id,valor_num,valor_texto,status
                    FROM observacao
                    WHERE codigo_ibge=?
                    ORDER BY variavel_id,ano
                    """,
                    (code,),
                )
            ]
            series = {}
            for row in observations:
                series.setdefault(row["variavel_id"], []).append(
                    {
                        "year": row["ano"],
                        "status": row["status"],
                        "value": (
                            row["valor_num"]
                            if row["valor_num"] is not None
                            else row["valor_texto"]
                        ),
                    }
                )

            typologies = [
                dict(row)
                for row in con.execute(
                    """
                    SELECT dimensao_id,janela_id,media,cv,n_anos,
                           mediana_nivel,mediana_cv,nivel_relativo,
                           estabilidade,quadrante,status
                    FROM classificacao_relativa
                    WHERE codigo_ibge=? AND universo_id=?
                    ORDER BY dimensao_id,janela_id
                    """,
                    (code, universe_id),
                )
            ]

            markers = [
                dict(row)
                for row in con.execute(
                    """
                    SELECT janela_id,marcador_id,valor_texto,status
                    FROM marcador_comparavel
                    WHERE codigo_ibge=? AND universo_id=?
                    ORDER BY janela_id,marcador_id
                    """,
                    (code, universe_id),
                )
            ]

            pairs = [
                dict(row)
                for row in con.execute(
                    """
                    SELECT
                        p.codigo_ibge_comparado,
                        m.nome AS municipio_comparado,
                        p.janela_id,
                        p.dimensoes_comparaveis,
                        p.dimensoes_coincidentes,
                        p.proporcao_coincidencia,
                        p.ordem_prioritaria,
                        p.reciproco,
                        p.dimensoes_coincidentes_lista,
                        p.observacao
                    FROM par_municipal p
                    JOIN municipio m
                      ON m.codigo_ibge=p.codigo_ibge_comparado
                    WHERE p.codigo_ibge_referencia=?
                      AND p.universo_id=?
                    ORDER BY
                        CASE WHEN p.ordem_prioritaria IS NULL THEN 999 ELSE p.ordem_prioritaria END,
                        p.proporcao_coincidencia DESC,
                        m.nome
                    """,
                    (code, universe_id),
                )
            ]

            payload = {
                **municipality,
                "universe_id": universe_id,
                "series": series,
                "typologies": typologies,
                "markers": markers,
                "pairs": pairs,
            }
            rel = f"municipalities/{code}.json"
            hashes[rel] = write_json(output / rel, payload)

        crosswalk = [
            dict(row)
            for row in con.execute(
                """
                SELECT
                    c.crosswalk_id,c.variavel_id,v.nome AS variavel,
                    c.ano_inicio,c.ano_fim,c.fonte_id,c.demonstrativo,
                    c.estagio,c.codigo_conta,c.descricao_conta,c.campo_bruto,
                    c.finalidade,c.regra_harmonizacao,c.prioridade,c.confianca
                FROM crosswalk_variavel c
                JOIN variavel v USING(variavel_id)
                ORDER BY c.variavel_id,c.ano_inicio,c.prioridade
                """
            )
        ]
        hashes["crosswalk.json"] = write_json(
            output / "crosswalk.json", crosswalk
        )

        coverage = [
            dict(row)
            for row in con.execute(
                """
                SELECT variavel_id,ano,universo_id,esperado,observado,
                       ausente,nao_aplicavel
                FROM cobertura
                WHERE universo_id=?
                ORDER BY variavel_id,ano
                """,
                (universe_id,),
            )
        ]
        hashes["coverage.json"] = write_json(
            output / "coverage.json", coverage
        )

    finally:
        con.close()

    doc_result = export_documentation(database, output)

    file_manifest = {
        "build": metadata,
        "universe_id": universe_id,
        "files": hashes,
        "documentation": doc_result,
    }
    manifest_hash = write_json(output / "manifest.json", file_manifest)

    return {
        "universe_id": universe_id,
        "municipalities": len(municipalities),
        "years": len(years),
        "annual_snapshots": len(years),
        "municipality_files": len(municipalities),
        "manifest_sha256": manifest_hash,
        **doc_result,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Gera artefatos static-first para o frontend."
    )
    parser.add_argument("database", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--universe", default="TIC_TIM_30")
    args = parser.parse_args()
    result = export_static_data(
        args.database,
        args.output,
        universe_id=args.universe,
    )
    for key, value in result.items():
        print(f"{key}={value}")


if __name__ == "__main__":
    main()
