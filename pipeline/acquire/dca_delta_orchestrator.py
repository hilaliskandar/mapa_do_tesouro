from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import yaml


DEFAULT_QUEUE = Path("data/catalogs/dca_sp_delta_queue.yml")


def load_queue(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def next_pending_year(queue: dict) -> dict | None:
    candidates = []
    for raw_year, entry in (queue.get("years") or {}).items():
        year = int(raw_year)
        codes = [str(code) for code in (entry.get("codes") or [])]
        missing = entry.get("missing_by_annex") or {}
        pair_count = sum(len(missing.get(key) or []) for key in ("i_c", "i_d", "i_e"))
        priority = entry.get("priority")
        if not codes or pair_count == 0 or priority is None:
            continue
        candidates.append(
            {
                "year": year,
                "priority": int(priority),
                "codes": codes,
                "pair_count": pair_count,
                "plan": {
                    key: [str(code) for code in (missing.get(key) or [])]
                    for key in ("i_c", "i_d", "i_e")
                },
            }
        )
    if not candidates:
        return None
    return sorted(candidates, key=lambda item: (item["priority"], item["year"]))[0]


def classify_manifest(manifest: dict) -> str:
    if manifest.get("failed"):
        return "failed"
    requested = int(manifest.get("municipality_annex_pairs_requested") or 0)
    empty = int(manifest.get("empty_source_pair_count") or 0)
    if requested <= 0:
        raise ValueError("Manifest does not contain requested municipality-annex pairs.")
    if empty == requested:
        return "source_confirmed_absence"
    return "delta_recovered_pending_merge"


def update_queue_for_manifest(
    queue: dict,
    manifest: dict,
    *,
    run_id: str | None = None,
) -> tuple[dict, str]:
    year = int(manifest["year"])
    entry = (queue.get("years") or {}).get(year)
    if entry is None:
        raise ValueError(f"Year {year} is not present in queue.")

    classification = classify_manifest(manifest)
    if classification == "failed":
        raise ValueError("Cannot update queue from failed manifest.")

    original_missing = entry.get("missing_by_annex") or {}
    entry["priority"] = None
    entry["codes"] = []
    entry["status"] = classification
    entry["original_missing_by_annex"] = original_missing
    entry.pop("missing_by_annex", None)
    entry["source_check"] = {
        "run_id": int(run_id) if run_id and str(run_id).isdigit() else run_id,
        "normalized_sha256": manifest.get("normalized_sha256"),
        "codes": manifest.get("codes") or [],
        "municipality_annex_pairs_requested": manifest.get(
            "municipality_annex_pairs_requested"
        ),
        "empty_source_pairs": manifest.get("empty_source_pair_count"),
        "result": classification,
    }
    if classification == "delta_recovered_pending_merge":
        entry["source_check"]["recovered_pairs"] = (
            int(manifest["municipality_annex_pairs_requested"])
            - int(manifest["empty_source_pair_count"])
        )
    return queue, classification


def write_qa_markdown(manifest: dict, classification: str, output: Path) -> None:
    year = int(manifest["year"])
    lines = [
        f"# QA automático — delta seletivo DCA {year}",
        "",
        f"Run ID: `{os.environ.get('GITHUB_RUN_ID', 'n/a')}`",
        "",
        f"- municípios: {manifest['municipalities_requested']};",
        f"- pares município–anexo: {manifest['municipality_annex_pairs_requested']};",
        f"- pares com `items=[]`: {manifest['empty_source_pair_count']};",
        f"- falhas: {len(manifest.get('failed') or [])};",
        f"- SHA-256 normalizado: `{manifest['normalized_sha256']}`;",
        f"- classificação: `{classification}`.",
        "",
    ]
    if classification == "source_confirmed_absence":
        lines += [
            "## Decisão",
            "",
            "Todos os pares consultados retornaram fonte vazia. As lacunas permanecem como ausência confirmada da fonte atual, não são convertidas em zero e saem da fila automática.",
            "",
        ]
    else:
        lines += [
            "## Decisão",
            "",
            "Ao menos um par município–anexo retornou observações. O delta sai da fila automática e fica classificado como `delta_recovered_pending_merge`. A composição fill-only e qualquer conflito exigem QA antes de promoção.",
            "",
        ]

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Orchestrate Gate B selective DCA deltas.")
    sub = parser.add_subparsers(dest="command", required=True)

    next_cmd = sub.add_parser("next")
    next_cmd.add_argument("--queue", type=Path, default=DEFAULT_QUEUE)
    next_cmd.add_argument("--github-output", type=Path)
    next_cmd.add_argument("--plan-output", type=Path)

    apply_cmd = sub.add_parser("apply")
    apply_cmd.add_argument("--queue", type=Path, default=DEFAULT_QUEUE)
    apply_cmd.add_argument("--manifest", type=Path, required=True)
    apply_cmd.add_argument("--qa-output", type=Path, required=True)
    apply_cmd.add_argument("--run-id")

    args = parser.parse_args()

    if args.command == "next":
        queue = load_queue(args.queue)
        item = next_pending_year(queue)
        if item is None:
            if args.github_output:
                with args.github_output.open("a", encoding="utf-8") as out:
                    out.write("has_work=false\n")
            print(json.dumps({"has_work": False}))
            return

        if args.plan_output:
            args.plan_output.parent.mkdir(parents=True, exist_ok=True)
            args.plan_output.write_text(
                json.dumps(item["plan"], ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
        if args.github_output:
            with args.github_output.open("a", encoding="utf-8") as out:
                out.write("has_work=true\n")
                out.write(f"year={item['year']}\n")
                out.write(f"priority={item['priority']}\n")
                out.write(f"pair_count={item['pair_count']}\n")
                out.write(f"code_count={len(item['codes'])}\n")
        print(json.dumps({"has_work": True, **item}, ensure_ascii=False, indent=2))
        return

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    queue = load_queue(args.queue)
    queue, classification = update_queue_for_manifest(
        queue,
        manifest,
        run_id=args.run_id,
    )
    args.queue.write_text(
        yaml.safe_dump(queue, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    write_qa_markdown(manifest, classification, args.qa_output)
    print(json.dumps({"classification": classification}, ensure_ascii=False))


if __name__ == "__main__":
    main()
