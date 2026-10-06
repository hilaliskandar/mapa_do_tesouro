from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CATALOG = ROOT / "data" / "catalogs" / "variables_core.yml"


def load_catalog(database: Path, catalog: Path = DEFAULT_CATALOG) -> None:
    payload = yaml.safe_load(catalog.read_text(encoding="utf-8"))
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
    parser = argparse.ArgumentParser(description="Carrega catálogo canônico no SQLite.")
    parser.add_argument("database", type=Path)
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    args = parser.parse_args()
    load_catalog(args.database, args.catalog)
    print(f"Catálogo carregado em {args.database}")


if __name__ == "__main__":
    main()
