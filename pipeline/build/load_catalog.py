from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
CATALOG_DIR = ROOT / "data" / "catalogs"
DEFAULT_CATALOGS = [
    CATALOG_DIR / "variables_core.yml",
    CATALOG_DIR / "variables_v7_extension.yml",
]


def read_catalogs(catalogs: list[Path]) -> dict:
    merged = {"fontes": [], "variaveis": []}
    seen_sources: set[str] = set()
    seen_variables: set[str] = set()

    for catalog in catalogs:
        payload = yaml.safe_load(catalog.read_text(encoding="utf-8")) or {}
        for item in payload.get("fontes", []):
            source_id = item["fonte_id"]
            if source_id in seen_sources:
                raise ValueError(f"Fonte duplicada nos catalogos: {source_id}")
            seen_sources.add(source_id)
            merged["fontes"].append(item)

        for item in payload.get("variaveis", []):
            variable_id = item["variavel_id"]
            if variable_id in seen_variables:
                raise ValueError(f"Variavel duplicada nos catalogos: {variable_id}")
            seen_variables.add(variable_id)
            merged["variaveis"].append(item)

    return merged


def load_catalog(database: Path, catalogs: list[Path] | None = None) -> None:
    catalogs = catalogs or DEFAULT_CATALOGS
    payload = read_catalogs(catalogs)

    connection = sqlite3.connect(database)
    connection.execute("PRAGMA foreign_keys = ON")
    try:
        for item in payload.get("fontes", []):
            connection.execute(
                """
                INSERT INTO fonte(fonte_id,nome,orgao,sistema,observacao)
                VALUES (?,?,?,?,?)
                ON CONFLICT(fonte_id) DO UPDATE SET
                    nome=excluded.nome,
                    orgao=excluded.orgao,
                    sistema=excluded.sistema,
                    observacao=excluded.observacao
                """,
                (
                    item["fonte_id"],
                    item["nome"],
                    item.get("orgao"),
                    item.get("sistema"),
                    item.get("finalidade"),
                ),
            )

        for item in payload.get("variaveis", []):
            connection.execute(
                """
                INSERT INTO variavel(
                    variavel_id,nome,grupo,tipo,natureza,unidade,definicao,
                    formula,como_ler,cautelas,fonte_preferencial_id
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?)
                ON CONFLICT(variavel_id) DO UPDATE SET
                    nome=excluded.nome,
                    grupo=excluded.grupo,
                    tipo=excluded.tipo,
                    natureza=excluded.natureza,
                    unidade=excluded.unidade,
                    definicao=excluded.definicao,
                    formula=excluded.formula,
                    como_ler=excluded.como_ler,
                    cautelas=excluded.cautelas,
                    fonte_preferencial_id=excluded.fonte_preferencial_id
                """,
                (
                    item["variavel_id"],
                    item["nome"],
                    item["grupo"],
                    item["tipo"],
                    item.get("natureza"),
                    item["unidade"],
                    item["definicao"],
                    item.get("formula"),
                    item.get("como_ler"),
                    item.get("cautelas"),
                    item.get("fonte_preferencial_id"),
                ),
            )
        connection.commit()
    finally:
        connection.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Carrega catálogos canônicos no SQLite.")
    parser.add_argument("database", type=Path)
    parser.add_argument(
        "--catalog",
        action="append",
        type=Path,
        dest="catalogs",
        help="Pode ser repetido. Sem uso, carrega core + extensão v7.",
    )
    args = parser.parse_args()
    load_catalog(args.database, args.catalogs)
    print(f"Catálogo carregado em {args.database}")


if __name__ == "__main__":
    main()
