from __future__ import annotations

import csv
import json
import re
from pathlib import Path

import yaml

from pipeline.acquire.siconfi_dca import annex_slug
from pipeline.sources.siconfi import read_raw_dca

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MAPPING = ROOT / "data" / "mappings" / "dca_canonical_v1.yml"


def load_mapping(path: Path = DEFAULT_MAPPING) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def resolve_rule_for_year(rule: dict, year: int | None) -> dict:
    resolved = {key: value for key, value in rule.items() if key != "variants"}
    if year is None:
        return resolved

    matches = []
    for variant in rule.get("variants", []):
        from_year = variant.get("from_year")
        to_year = variant.get("to_year")
        if from_year is not None and year < int(from_year):
            continue
        if to_year is not None and year > int(to_year):
            continue
        matches.append(variant)

    if len(matches) > 1:
        raise ValueError(
            f"Overlapping temporal variants for year {year}: {matches!r}"
        )
    if matches:
        resolved.update(
            {
                key: value
                for key, value in matches[0].items()
                if key not in {"from_year", "to_year"}
            }
        )
    return resolved


def _match(item: dict, rule: dict) -> bool:
    if rule.get("column") is not None and item.get("coluna") != rule["column"]:
        return False
    if rule.get("rotulo") is not None and item.get("rotulo") != rule["rotulo"]:
        return False
    if rule.get("cod_conta") is not None and item.get("cod_conta") != rule["cod_conta"]:
        return False
    pattern = rule.get("conta_regex")
    if pattern and not re.search(pattern, str(item.get("conta") or "")):
        return False
    return True


def normalize_bundle(
    payloads: dict[str, dict],
    *,
    mapping: dict,
) -> dict:
    variables: dict[str, dict] = {}
    issues: list[dict] = []

    entity_ids = {
        str(payload.get("entity_id"))
        for payload in payloads.values()
        if payload.get("entity_id") is not None
    }
    years = {
        int(payload.get("year"))
        for payload in payloads.values()
        if payload.get("year") is not None
    }
    bundle_year = next(iter(years)) if len(years) == 1 else None

    for variable_id, base_rule in mapping["variables"].items():
        rule = resolve_rule_for_year(base_rule, bundle_year)

        if rule.get("special") == "population_consensus":
            values = {
                int(item["populacao"])
                for payload in payloads.values()
                for item in payload.get("items", [])
                if item.get("populacao") is not None
            }
            if len(values) == 1:
                value = float(next(iter(values)))
                variables[variable_id] = {
                    "status": "observado",
                    "value": value,
                    "source": {"rule": "population_consensus"},
                }
            elif not values:
                variables[variable_id] = {
                    "status": "ausente",
                    "value": None,
                    "source": {"rule": "population_consensus"},
                }
            else:
                variables[variable_id] = {
                    "status": "em_revisao",
                    "value": None,
                    "source": {"rule": "population_consensus"},
                }
                issues.append(
                    {
                        "variable_id": variable_id,
                        "type": "population_conflict",
                        "values": sorted(values),
                    }
                )
            continue

        annex = rule["annex"]
        payload = payloads.get(annex)
        if payload is None:
            variables[variable_id] = {
                "status": "ausente",
                "value": None,
                "source": {"annex": annex, "rule": "missing_annex"},
            }
            issues.append(
                {
                    "variable_id": variable_id,
                    "type": "missing_annex",
                    "annex": annex,
                }
            )
            continue

        matches = [item for item in payload.get("items", []) if _match(item, rule)]
        if len(matches) == 1:
            item = matches[0]
            raw_value = item.get("valor")
            if raw_value is None:
                status = "ausente"
                value = None
            else:
                status = "observado"
                value = float(raw_value)
            variables[variable_id] = {
                "status": status,
                "value": value,
                "source": {
                    "annex": annex,
                    "rotulo": item.get("rotulo"),
                    "column": item.get("coluna"),
                    "cod_conta": item.get("cod_conta"),
                    "conta": item.get("conta"),
                },
            }
        elif len(matches) == 0:
            variables[variable_id] = {
                "status": "ausente",
                "value": None,
                "source": {
                    "annex": annex,
                    "column": rule.get("column"),
                    "cod_conta": rule.get("cod_conta"),
                    "conta_regex": rule.get("conta_regex"),
                },
            }
        else:
            variables[variable_id] = {
                "status": "em_revisao",
                "value": None,
                "source": {
                    "annex": annex,
                    "column": rule.get("column"),
                    "cod_conta": rule.get("cod_conta"),
                },
            }
            issues.append(
                {
                    "variable_id": variable_id,
                    "type": "ambiguous_match",
                    "match_count": len(matches),
                }
            )

    if len(entity_ids) != 1 or len(years) != 1:
        issues.append(
            {
                "type": "bundle_key_conflict",
                "entity_ids": sorted(entity_ids),
                "years": sorted(years),
            }
        )

    return {
        "codigo_ibge": next(iter(entity_ids)) if len(entity_ids) == 1 else None,
        "ano": next(iter(years)) if len(years) == 1 else None,
        "variables": variables,
        "issues": issues,
    }


def load_bundle(raw_root: Path, code: str, year: int, annexes: list[str]) -> dict[str, dict]:
    payloads = {}
    for annex in annexes:
        path = raw_root / annex_slug(annex) / str(year) / f"{code}.json.gz"
        if path.exists():
            payloads[annex] = read_raw_dca(path)
    return payloads


def normalize_tree(
    raw_root: Path,
    output_csv: Path,
    *,
    mapping_path: Path = DEFAULT_MAPPING,
) -> dict:
    mapping = load_mapping(mapping_path)
    annexes = sorted(
        {
            rule["annex"]
            for rule in mapping["variables"].values()
            if "annex" in rule
        }
    )

    keys: set[tuple[str, int]] = set()
    for annex in annexes:
        annex_dir = raw_root / annex_slug(annex)
        if not annex_dir.exists():
            continue
        for year_dir in annex_dir.iterdir():
            if not year_dir.is_dir() or not year_dir.name.isdigit():
                continue
            for path in year_dir.glob("*.json.gz"):
                keys.add((path.name.removesuffix(".json.gz"), int(year_dir.name)))

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    variable_ids = list(mapping["variables"])
    issue_count = 0
    with output_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["cod_ibge", "ano", *variable_ids, "qa_issue_count"],
        )
        writer.writeheader()
        for code, year in sorted(keys):
            normalized = normalize_bundle(
                load_bundle(raw_root, code, year, annexes),
                mapping=mapping,
            )
            issue_count += len(normalized["issues"])
            row = {
                "cod_ibge": code,
                "ano": year,
                "qa_issue_count": len(normalized["issues"]),
            }
            for variable_id in variable_ids:
                entry = normalized["variables"][variable_id]
                row[variable_id] = (
                    entry["value"] if entry["status"] == "observado" else ""
                )
            writer.writerow(row)

    return {
        "rows": len(keys),
        "variables": len(variable_ids),
        "issues": issue_count,
        "output": str(output_csv),
    }
