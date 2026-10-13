"""Validate a materialized SP645 API v2 tree before preview publication."""
import argparse
import json
from pathlib import Path

EXPECTED_MUNICIPALITIES = 645
EXPECTED_UNIVERSE_MEMBERS = {
    "SP_645": 645, "TIC_TIM_30": 30, "CIDADES_MEDIAS": 33,
    "AU_FRANCA": 19, "RM_BAIXADA_SANTISTA": 9,
    "RM_CAMPINAS": 20, "RM_JUNDIAI": 7,
    "RM_PIRACICABA": 24, "RM_RIBEIRAO_PRETO": 34,
    "RM_SOROCABA": 27, "RM_SAO_JOSE_RIO_PRETO": 37,
    "RM_SAO_PAULO": 39, "RM_VALE_PARAIBA_LITORAL_NORTE": 39,
}
STATES = ("observado", "ausente", "nao_aplicavel", "em_revisao", "sem_registro")


def load(path):
    if not path.is_file():
        raise ValueError(f"Missing: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def validate_v2(site):
    root = site / "data" / "api" / "v2"
    manifest = load(root / "manifest.json")
    municipalities = load(root / "catalog" / "municipalities.json")
    catalog = load(root / "catalog" / "variables.json")
    universes = load(root / "catalog" / "universes.json")
    readiness = load(root / "qa" / "readiness.json")
    if manifest["municipality_count"] != EXPECTED_MUNICIPALITIES:
        raise ValueError("Manifest municipality count != 645")
    codes = {x["codigo_ibge"] for x in municipalities}
    if len(codes) != EXPECTED_MUNICIPALITIES:
        raise ValueError("Municipality catalog is incomplete or duplicated")
    if readiness["municipality_count"] != EXPECTED_MUNICIPALITIES:
        raise ValueError("Readiness municipality count != 645")
    if manifest["variable_catalog_count"] != len(catalog["variables"]):
        raise ValueError("Variable catalog count mismatch")
    for code in codes:
        ficha = load(root / "municipalities" / f"{code}.json")
        if ficha["municipality"]["codigo_ibge"] != code:
            raise ValueError(f"Wrong municipality content: {code}")
    groups = {x["universo_id"]: x["member_count"] for x in universes}
    if groups != EXPECTED_UNIVERSE_MEMBERS:
        raise ValueError(f"Wrong regional universe composition: {groups}")
    for universe_id, size in groups.items():
        folder = root / "universes" / universe_id
        members = load(folder / "members.json")
        ctx = load(folder / "context.json")
        cov = load(folder / "coverage.json")
        if len(members) != size or ctx["member_count"] != size or cov["member_count"] != size:
            raise ValueError(f"Member count mismatch in {universe_id}")
        for m in members:
            load(folder / "municipalities" / f'{m["codigo_ibge"]}.json')
        for row in cov["coverage"]:
            states = row["status_counts"]
            if row["expected"] != size or sum(states.get(k, 0) for k in STATES) != size:
                raise ValueError(f"Coverage does not reconcile: {universe_id}/{row['variable_id']}/{row['year']}")
            if row["observed"] != states["observado"]:
                raise ValueError("Observed count mismatch")
    return {"municipalities": len(codes), "universes": len(groups),
            "variables": len(catalog["variables"]), "publication_qa": manifest["publication_qa"]}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--site", required=True, type=Path)
    args = p.parse_args()
    print(json.dumps(validate_v2(args.site), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
