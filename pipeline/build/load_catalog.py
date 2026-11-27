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



def _catalog_flag(item: dict, name: str) -> tuple[int, int]:
    """Value and explicitness: omitted flags preserve existing SQLite states."""
    if name not in item:
        return 1, 0
    value = item[name]
    if type(value) not in (bool, int) or value not in (0, 1):
        raise ValueError(f"Catalogo: {name} deve ser 0 ou 1: {item.get('variavel_id')}")
    return int(value), 1


def load_catalog(
    database: Path,
    catalogs: Path | list[Path] | None = None,
) -> None:
    if catalogs is None:
        catalogs = DEFAULT_CATALOGS
    elif isinstance(catalogs, Path):
        # Compatibilidade com chamadas anteriores que informavam um único catálogo.
        # O core informado é complementado automaticamente pela extensão v7 padrão.
        if catalogs == DEFAULT_CATALOGS[0]:
            catalogs = DEFAULT_CATALOGS
        else:
            catalogs = [catalogs]
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
            publicavel, publicavel_explicito = _catalog_flag(item, "publicavel")
            ativo, ativo_explicito = _catalog_flag(item, "ativo")
            connection.execute(
                """
                INSERT INTO variavel(
                    variavel_id,nome,grupo,tipo,natureza,unidade,definicao,
                    formula,como_ler,cautelas,fonte_preferencial_id,
                    publicavel,ativo
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
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
                    fonte_preferencial_id=excluded.fonte_preferencial_id,
                    publicavel=CASE WHEN ?=1 THEN excluded.publicavel ELSE variavel.publicavel END,
                    ativo=CASE WHEN ?=1 THEN excluded.ativo ELSE variavel.ativo END
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
                    publicavel,
                    ativo,
                    publicavel_explicito,
                    ativo_explicito,
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
