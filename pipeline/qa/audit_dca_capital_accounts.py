"""Classify exact DCA account availability directly from archived Siconfi annexes.

Read-only audit: does not change canonical CSV, SQLite or editorial builds.
Run: python -m pipeline.qa.audit_dca_capital_accounts --raw-root PATH --year 2025 --output-prefix PATH
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

from pipeline.acquire.siconfi_dca import annex_slug
from pipeline.normalize.dca import load_mapping, resolve_rule_for_year, _match
from pipeline.sources.siconfi import read_raw_dca

VARIABLES = (
    "dca_inversoes_financeiras_liquidada",
    "dca_operacoes_credito",
    "dca_alienacao_bens",
)
FIELDS = ("codigo_ibge", "ano", "variavel_id", "anexo", "categoria", "valor",
          "linhas_exatas", "linhas_mesmo_codigo", "linhas_anexo",
          "codigo_conta_esperado", "coluna_esperada", "rotulo_esperado",
          "arquivo_bruto", "sha256_arquivo")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def classify(payload: dict | None, rule: dict) -> tuple[str, float | None, int, int, int]:
    if payload is None:
        return "anexo_ausente", None, 0, 0, 0
    items = payload.get("items")
    if not isinstance(items, list):
        return "anexo_invalido", None, 0, 0, 0
    candidates = [x for x in items if x.get("cod_conta") == rule.get("cod_conta")]
    matches = [x for x in items if _match(x, rule)]
    if len(matches) > 1:
        return "correspondencia_ambigua", None, len(matches), len(candidates), len(items)
    if not matches:
        category = "rubrica_ausente" if not candidates else "codigo_presente_filtro_divergente"
        return category, None, 0, len(candidates), len(items)
    original = matches[0].get("valor")
    if original is None or (isinstance(original, str) and not original.strip()):
        return "valor_nulo", None, 1, len(candidates), len(items)
    try:
        value = float(original)
    except (ValueError, TypeError):
        return "valor_invalido", None, 1, len(candidates), len(items)
    return ("zero_explicito" if value == 0 else "valor_observado"), value, 1, len(candidates), len(items)


def audit(root: Path, year: int, prefix: Path, mapping_path: Path | None = None) -> dict:
    mapping = load_mapping(mapping_path) if mapping_path else load_mapping()
    rules = {name: resolve_rule_for_year(mapping["variables"][name], year) for name in VARIABLES}
    annexes = sorted({r["annex"] for r in rules.values()})
    paths_by_annex = {
        annex: {p.name.removesuffix(".json.gz"): p
                for p in (root / annex_slug(annex) / str(year)).glob("*.json.gz")}
        for annex in annexes
    }
    codes = sorted(set().union(*(set(d) for d in paths_by_annex.values())))
    if not codes:
        raise ValueError("No raw DCA .json.gz files found for requested year.")
    rows = []
    totals = {name: Counter() for name in VARIABLES}
    for code in codes:
        for name, rule in rules.items():
            annex = rule["annex"]
            path = paths_by_annex[annex].get(code)
            payload = read_raw_dca(path) if path else None
            if payload and (str(payload.get("entity_id")) != code or int(payload.get("year")) != year):
                raise ValueError(f"Source key mismatch: {path}")
            cat, val, exact, same, total = classify(payload, rule)
            totals[name][cat] += 1
            rows.append({
                "codigo_ibge": code, "ano": year, "variavel_id": name,
                "anexo": annex, "categoria": cat, "valor": val if val is not None else "",
                "linhas_exatas": exact, "linhas_mesmo_codigo": same, "linhas_anexo": total,
                "codigo_conta_esperado": rule.get("cod_conta", ""),
                "coluna_esperada": rule.get("column", ""), "rotulo_esperado": rule.get("rotulo", ""),
                "arquivo_bruto": str(path) if path else "",
                "sha256_arquivo": sha256(path) if path else "",
            })
    prefix.parent.mkdir(parents=True, exist_ok=True)
    csv_path = prefix.with_suffix(".csv")
    json_path = prefix.with_suffix(".json")
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    report = {
        "year": year, "municipalities_with_any_annex": len(codes),
        "scope_note": "Coverage denominator is municipalities having at least one target annex archive.",
        "classifications": {name: dict(totals[name]) for name in VARIABLES},
        "csv_path": str(csv_path), "csv_sha256": sha256(csv_path),
        "limitations": "A missing exact row is not a declared zero. No canonical values changed.",
    }
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-root", type=Path, required=True)
    parser.add_argument("--year", type=int, default=2025)
    parser.add_argument("--output-prefix", type=Path, required=True)
    parser.add_argument("--mapping", type=Path)
    args = parser.parse_args()
    print(json.dumps(audit(args.raw_root, args.year, args.output_prefix, args.mapping), ensure_ascii=False))


if __name__ == "__main__":
    main()
