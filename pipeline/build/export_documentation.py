from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path


def write_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def export_documentation(database: Path, output: Path) -> dict:
    con = sqlite3.connect(database)
    con.row_factory = sqlite3.Row
    try:
        variables = [
            dict(row)
            for row in con.execute(
                """
                SELECT *
                FROM v_catalogo_publico
                WHERE titulo_publico IS NOT NULL
                ORDER BY COALESCE(ordem_prioridade, 9999), titulo_publico
                """
            )
        ]
        sections = [
            dict(row)
            for row in con.execute(
                """
                SELECT secao_id,titulo,resumo,corpo_markdown,ordem,documentation_version
                FROM documentacao_secao
                WHERE publico=1
                ORDER BY ordem, titulo
                """
            )
        ]
        refs = [
            dict(row)
            for row in con.execute(
                """
                SELECT referencia_id,titulo,url,descricao,tipo,documentation_version
                FROM referencia_documental
                ORDER BY titulo
                """
            )
        ]
    finally:
        con.close()

    write_json(output / "catalog" / "variables.json", variables)
    write_json(output / "methodology" / "index.json", sections)
    write_json(output / "references.json", refs)

    for item in variables:
        write_json(
            output / "catalog" / "variables" / f"{item['variavel_id']}.json",
            item,
        )

    for section in sections:
        write_json(
            output / "methodology" / f"{section['secao_id']}.json",
            section,
        )

    return {
        "variables": len(variables),
        "methodology_sections": len(sections),
        "references": len(refs),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Exporta dicionário e metodologia para consumo static-first."
    )
    parser.add_argument("database", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    result = export_documentation(args.database, args.output)
    for key, value in result.items():
        print(f"{key}={value}")


if __name__ == "__main__":
    main()
