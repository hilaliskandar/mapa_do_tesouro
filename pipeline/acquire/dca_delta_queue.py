from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml


DEFAULT_QUEUE = Path("data/catalogs/dca_sp_delta_queue.yml")


def resolve_year(queue_path: Path, year: int) -> dict:
    payload = yaml.safe_load(queue_path.read_text(encoding="utf-8"))
    entry = (payload.get("years") or {}).get(int(year))
    if entry is None:
        raise ValueError(f"Year {year} is not present in the delta queue.")

    codes = [str(code) for code in (entry.get("codes") or [])]
    if not codes:
        status = entry.get("status")
        raise ValueError(
            f"Year {year} has no queued external delta codes"
            + (f" (status={status})" if status else "")
            + "."
        )

    max_codes = int((payload.get("policy") or {}).get("max_codes_per_run", 100))
    if len(codes) > max_codes:
        raise ValueError(f"Year {year} exceeds queue maximum.")

    missing = entry.get("missing_by_annex") or {}
    plan = {
        annex: [str(code) for code in (missing.get(annex) or [])]
        for annex in ("i_c", "i_d", "i_e")
    }
    if not any(plan.values()):
        raise ValueError(
            f"Year {year} has queued codes but no municipality-annex pairs."
        )

    return {
        "year": int(year),
        "codes": codes,
        "codes_arg": " ".join(codes),
        "priority": entry.get("priority"),
        "missing_by_annex": plan,
        "plan": plan,
        "pair_count": sum(len(values) for values in plan.values()),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Resolve an approved selective DCA delta from the versioned queue."
    )
    parser.add_argument("--year", type=int, required=True)
    parser.add_argument("--queue", type=Path, default=DEFAULT_QUEUE)
    parser.add_argument("--github-output", type=Path)
    parser.add_argument("--output-json", type=Path)
    args = parser.parse_args()

    result = resolve_year(args.queue, args.year)
    if args.output_json:
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        args.output_json.write_text(
            json.dumps(result["plan"], ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    if args.github_output:
        with args.github_output.open("a", encoding="utf-8") as handle:
            handle.write(f"codes={result['codes_arg']}\n")
            handle.write(f"count={len(result['codes'])}\n")
            handle.write(f"pair_count={result['pair_count']}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
