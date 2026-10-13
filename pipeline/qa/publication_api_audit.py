"""Audita a consistencia interna da API editorial estaticamente exportada."""
import argparse
import json
from pathlib import Path


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def audit(root):
    errors = []
    base = root / "publication"
    idx = read(base / "universes.json")
    for item in idx:
        uid = item["publication_id"]
        folder = base / "universes" / uid
        ctx = read(folder / "context.json")
        members = read(folder / "municipalities.json")
        codes = [str(m["codigo_ibge"]) for m in members]
        if len(set(codes)) != len(codes) or len(codes) != item["member_count"]:
            errors.append(f"{uid}: membros divergentes ou duplicados")
        if len(codes) != ctx["member_count"]:
            errors.append(f"{uid}: contexto com contagem divergente")
        fichas = {}
        for code in codes:
            file = folder / "municipalities" / f"{code}.json"
            if not file.exists():
                errors.append(f"{uid}/{code}: ficha ausente")
                continue
            ficha = read(file)
            fichas[code] = ficha
            if str(ficha["municipality"]["codigo_ibge"]) != code:
                errors.append(f"{uid}/{code}: codigo divergente")
            if ficha["build"]["build_id"] != ctx["build"]["build_id"]:
                errors.append(f"{uid}/{code}: build divergente")
        for vid, var in ctx["variables"].items():
            latest = var.get("latest")
            if not latest:
                continue
            if sum(latest["status_counts"].values()) != len(codes):
                errors.append(f"{uid}/{vid}: estados nao fecham")
            found = 0
            for code, ficha in fichas.items():
                x = ficha["variables"].get(vid)
                if x is None:
                    errors.append(f"{uid}/{code}/{vid}: nao consta")
                    continue
                year = latest["year"]
                r = next((s for s in x["series"] if s["year"] == year), None)
                if r and r["status"] == "observado":
                    found += 1
                    if r["value"] is None:
                        errors.append(f"{uid}/{code}/{vid}: observado sem valor")
            if found != latest["observed"]:
                errors.append(f"{uid}/{vid}: cobertura {found} vs {latest['observed']}")
    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    args = parser.parse_args()
    errors = audit(args.root)
    if errors:
        print("\n".join(errors))
        raise SystemExit(1)
    print("QA estrutural aprovado (nao substitui QA de cobertura estadual).")


if __name__ == "__main__":
    main()
