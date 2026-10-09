from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path

import yaml


def read_territorial_catalog(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    universes = data.get("universes") if isinstance(data, dict) else None
    if not isinstance(universes, list) or not universes:
        raise ValueError("Catalogo territorial invalido: universes ausente.")

    ids = [item.get("id") for item in universes]
    if any(not value for value in ids) or len(ids) != len(set(ids)):
        raise ValueError("Catalogo territorial invalido: ids vazios ou duplicados.")

    for item in universes:
        members = item.get("members")
        if not isinstance(members, list):
            raise ValueError(f"Universo sem members: {item['id']}")
        if len(members) != int(item["municipality_count"]):
            raise ValueError(
                f"Contagem divergente em {item['id']}: "
                f"catalogo={item['municipality_count']} members={len(members)}"
            )
        if len(members) != len(set(members)):
            raise ValueError(f"Municipio duplicado em {item['id']}.")
        invalid = [code for code in members if len(str(code)) != 7 or not str(code).isdigit()]
        if invalid:
            raise ValueError(f"Codigos IBGE invalidos em {item['id']}: {invalid[:5]}")
    return data


def import_territorial_universes(
    connection: sqlite3.Connection,
    catalog_path: Path,
) -> dict[str, int]:
    catalog = read_territorial_catalog(catalog_path)
    universes = catalog["universes"]
    all_members = {str(code) for item in universes for code in item["members"]}

    missing = [
        code
        for code in sorted(all_members)
        if connection.execute(
            "SELECT 1 FROM municipio WHERE codigo_ibge=?", (code,)
        ).fetchone()
        is None
    ]
    if missing:
        raise ValueError(
            f"Municipios do catalogo territorial ausentes da base ({len(missing)}): "
            + ", ".join(missing[:5])
        )

    for item in universes:
        description = (
            f"Recorte territorial com composicao de referencia {catalog['reference_date']}; "
            f"fonte {catalog['source']['title']}; "
            f"codigo de categoria {item['source_category_code']}."
        )
        connection.execute(
            """
            INSERT INTO universo(universo_id,nome,descricao,tipo,ativo)
            VALUES (?,?,?,?,1)
            ON CONFLICT(universo_id) DO UPDATE SET
                nome=excluded.nome,
                descricao=excluded.descricao,
                tipo=excluded.tipo,
                ativo=1
            """,
            (item["id"], item["name"], description, item["type"].lower()),
        )
        for code in item["members"]:
            connection.execute(
                """
                INSERT INTO universo_municipio(
                    universo_id,codigo_ibge,vigencia_inicio,vigencia_fim
                ) VALUES (?,?,NULL,NULL)
                ON CONFLICT(universo_id,codigo_ibge) DO UPDATE SET
                    vigencia_fim=NULL
                """,
                (item["id"], str(code)),
            )

    connection.commit()
    return {
        "universes": len(universes),
        "memberships": sum(len(item["members"]) for item in universes),
        "municipalities": len(all_members),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Importa universos territoriais paulistas no SQLite canonico."
    )
    parser.add_argument("--database", type=Path, required=True)
    parser.add_argument("--catalog", type=Path, required=True)
    args = parser.parse_args()

    with sqlite3.connect(args.database) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        stats = import_territorial_universes(connection, args.catalog)
    print(stats)


if __name__ == "__main__":
    main()
