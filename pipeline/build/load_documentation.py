from __future__ import annotations

import argparse
import re
import sqlite3
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
CATALOG_DIR = ROOT / "data" / "catalogs"
DOC_VERSION = "panel-v7-baseline"


def read_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def slug(text: str) -> str:
    value = text.lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")


def load_documentation(database: Path, *, strict: bool = True) -> dict:
    indicators = read_yaml(CATALOG_DIR / "indicators_documentation_v7.yml") or []
    accounts = []
    for path in sorted(CATALOG_DIR.glob("accounts_documentation_v7_*.yml")):
        accounts.extend(read_yaml(path) or [])
    methodology = read_yaml(CATALOG_DIR / "methodology_sections_v7.yml") or {}
    sources = read_yaml(CATALOG_DIR / "sources_documentation_v7.yml") or []
    priorities = {
        item["id"]: int(item["ordem"])
        for item in (read_yaml(CATALOG_DIR / "priority_variables_v7.yml") or [])
    }

    connection = sqlite3.connect(database)
    connection.execute("PRAGMA foreign_keys = ON")
    loaded = 0
    skipped = []

    try:
        known = {
            row[0]
            for row in connection.execute("SELECT variavel_id FROM variavel")
        }

        for item, origin, kind in [
            *[(x, "painel_v7:Indicadores", "indicador") for x in indicators],
            *[(x, "painel_v7:Contas e agregações", "conta") for x in accounts],
        ]:
            variable_id = item["id"]
            if variable_id not in known:
                skipped.append(variable_id)
                continue

            connection.execute(
                """
                INSERT INTO variavel_documentacao(
                    variavel_id,titulo_publico,unidade_publica,formula_publica,
                    componentes_publicos,fonte_publica,periodo_publico,como_ler,
                    limitacoes,regra_ausencia,url_fonte,grupo_publico,
                    natureza_publica,ordem_prioridade,origem_documental,
                    documentation_version
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                ON CONFLICT(variavel_id) DO UPDATE SET
                    titulo_publico=excluded.titulo_publico,
                    unidade_publica=excluded.unidade_publica,
                    formula_publica=excluded.formula_publica,
                    componentes_publicos=excluded.componentes_publicos,
                    fonte_publica=excluded.fonte_publica,
                    periodo_publico=excluded.periodo_publico,
                    como_ler=excluded.como_ler,
                    limitacoes=excluded.limitacoes,
                    regra_ausencia=excluded.regra_ausencia,
                    url_fonte=excluded.url_fonte,
                    grupo_publico=excluded.grupo_publico,
                    natureza_publica=excluded.natureza_publica,
                    ordem_prioridade=excluded.ordem_prioridade,
                    origem_documental=excluded.origem_documental,
                    documentation_version=excluded.documentation_version
                """,
                (
                    variable_id,
                    item["label"],
                    item.get("unit"),
                    item.get("formula"),
                    item.get("inputs"),
                    item.get("source"),
                    str(item.get("period")) if item.get("period") is not None else None,
                    item.get("read") or "",
                    item.get("limits"),
                    item.get("na_rule"),
                    item.get("source_url"),
                    item.get("group"),
                    item.get("kind") or kind,
                    priorities.get(variable_id),
                    origin,
                    DOC_VERSION,
                ),
            )
            loaded += 1

        for section in methodology.get("sections", []):
            connection.execute(
                """
                INSERT INTO documentacao_secao(
                    secao_id,titulo,resumo,corpo_markdown,ordem,
                    origem_documental,documentation_version
                ) VALUES (?,?,?,?,?,?,?)
                ON CONFLICT(secao_id) DO UPDATE SET
                    titulo=excluded.titulo,
                    resumo=excluded.resumo,
                    corpo_markdown=excluded.corpo_markdown,
                    ordem=excluded.ordem,
                    origem_documental=excluded.origem_documental,
                    documentation_version=excluded.documentation_version
                """,
                (
                    section["secao_id"],
                    section["titulo"],
                    section.get("resumo"),
                    section["corpo_markdown"],
                    int(section.get("ordem", 100)),
                    "painel_v7:Regras de leitura",
                    methodology.get("documentation_version", DOC_VERSION),
                ),
            )

        for source in sources:
            reference_id = "v7_" + slug(source["label"])
            connection.execute(
                """
                INSERT INTO referencia_documental(
                    referencia_id,titulo,url,descricao,tipo,
                    origem_documental,documentation_version
                ) VALUES (?,?,?,?,?,?,?)
                ON CONFLICT(referencia_id) DO UPDATE SET
                    titulo=excluded.titulo,
                    url=excluded.url,
                    descricao=excluded.descricao,
                    origem_documental=excluded.origem_documental,
                    documentation_version=excluded.documentation_version
                """,
                (
                    reference_id,
                    source["label"],
                    source.get("url"),
                    source.get("desc"),
                    "fonte",
                    "painel_v7:Fontes",
                    DOC_VERSION,
                ),
            )

        if strict and skipped:
            raise ValueError(
                "Variaveis documentadas ausentes do catalogo tecnico: "
                + ", ".join(sorted(set(skipped)))
            )

        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()

    return {
        "loaded_variable_documentation": loaded,
        "skipped_variables": sorted(set(skipped)),
        "methodology_sections": len(methodology.get("sections", [])),
        "references": len(sources),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Carrega a documentação canônica preservada do painel v7."
    )
    parser.add_argument("database", type=Path)
    parser.add_argument(
        "--allow-missing-variables",
        action="store_true",
        help="Permite carga parcial durante a migração do catálogo técnico.",
    )
    args = parser.parse_args()
    result = load_documentation(
        args.database,
        strict=not args.allow_missing_variables,
    )
    for key, value in result.items():
        print(f"{key}={value}")


if __name__ == "__main__":
    main()
