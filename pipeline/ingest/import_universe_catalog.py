from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path

import yaml


def _member_code(member) -> str:
    if isinstance(member, dict):
        return str(member["codigo_ibge"])
    return str(member)


def read_universe_catalog(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    universes = data.get("universes") if isinstance(data, dict) else None
    if not isinstance(universes, list) or not universes:
        raise ValueError("Catalogo de universos invalido: universes ausente.")

    ids = [item.get("id") for item in universes]
    if any(not value for value in ids) or len(ids) != len(set(ids)):
        raise ValueError("Catalogo de universos invalido: ids vazios ou duplicados.")

    for item in universes:
        members = item.get("members")
        if not isinstance(members, list):
            raise ValueError(f"Universo sem members: {item['id']}")
        codes = [_member_code(member) for member in members]
        if len(codes) != int(item["municipality_count"]):
            raise ValueError(
                f"Contagem divergente em {item['id']}: "
                f"catalogo={item['municipality_count']} members={len(codes)}"
            )
        if len(codes) != len(set(codes)):
            raise ValueError(f"Municipio duplicado em {item['id']}.")
        invalid = [code for code in codes if len(code) != 7 or not code.isdigit()]
        if invalid:
            raise ValueError(f"Codigos IBGE invalidos em {item['id']}: {invalid[:5]}")
    return data


def import_universe_catalog(
    connection: sqlite3.Connection,
    catalog_path: Path,
) -> dict[str, int]:
    catalog = read_universe_catalog(catalog_path)
    universes = catalog["universes"]
    all_members = {
        _member_code(member)
        for item in universes
        for member in item["members"]
    }

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
            f"Municipios do catalogo ausentes da base ({len(missing)}): "
            + ", ".join(missing[:5])
        )

    source_title = catalog.get("source", {}).get("title", "catalogo de universos")
    reference_date = catalog.get("reference_date", "nao informada")

    for item in universes:
        description = item.get("description") or (
            f"Universo com composicao de referencia {reference_date}; "
            f"fonte {source_title}."
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
        for member in item["members"]:
            code = _member_code(member)
            connection.execute(
                """
                INSERT INTO universo_municipio(
                    universo_id,codigo_ibge,vigencia_inicio,vigencia_fim
                ) VALUES (?,?,NULL,NULL)
                ON CONFLICT(universo_id,codigo_ibge) DO UPDATE SET
                    vigencia_fim=NULL
                """,
                (item["id"], code),
            )

    connection.commit()
    return {
        "universes": len(universes),
        "memberships": sum(len(item["members"]) for item in universes),
        "municipalities": len(all_members),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Importa um catalogo de universos no SQLite canonico."
    )
    parser.add_argument("--database", type=Path, required=True)
    parser.add_argument("--catalog", type=Path, required=True)
    args = parser.parse_args()

    with sqlite3.connect(args.database) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        stats = import_universe_catalog(connection, args.catalog)
    print(stats)


if __name__ == "__main__":
    main()
