from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml

from pipeline.acquire.dca_delta_orchestrator import (
    classify_manifest,
    load_queue,
    next_pending_year,
    update_queue_for_manifest,
    write_qa_markdown,
)
from pipeline.acquire.siconfi_dca_delta import acquire_delta_plan


def run_batch(
    queue_path: Path,
    geojson: Path,
    output_root: Path,
    normalized_root: Path,
    qa_root: Path,
    *,
    run_id: str | None = None,
    min_interval: float = 1.05,
    max_cycles: int = 10,
) -> dict:
    queue = load_queue(queue_path)
    results = []

    for _ in range(max_cycles):
        item = next_pending_year(queue)
        if item is None:
            break

        year = item["year"]
        manifest = acquire_delta_plan(
            geojson,
            year,
            item["plan"],
            output_root / str(year),
            normalized_root / f"dca_delta_{year}.csv",
            min_interval=min_interval,
            max_codes=int((queue.get("policy") or {}).get("max_codes_per_run", 100)),
        )

        if manifest.get("failed"):
            raise RuntimeError(
                f"Unresolved acquisition failures for {year}: "
                f"{manifest['failed'][:20]}"
            )

        queue, classification = update_queue_for_manifest(
            queue,
            manifest,
            run_id=run_id,
        )
        qa_path = qa_root / f"QA_DCA_DELTA_{year}_RUN_{run_id or 'manual'}.md"
        write_qa_markdown(manifest, classification, qa_path)

        results.append(
            {
                "year": year,
                "classification": classification,
                "pair_count": manifest["municipality_annex_pairs_requested"],
                "empty_source_pairs": manifest["empty_source_pair_count"],
                "normalized_sha256": manifest["normalized_sha256"],
                "qa_path": str(qa_path),
            }
        )

        if classification == "delta_recovered_pending_merge":
            break

    queue_path.write_text(
        yaml.safe_dump(queue, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )

    return {
        "cycles": len(results),
        "results": results,
        "stopped_for_review": bool(
            results and results[-1]["classification"] == "delta_recovered_pending_merge"
        ),
        "queue_empty": next_pending_year(queue) is None,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Process Gate B DCA delta queue in batches.")
    parser.add_argument("--queue", type=Path, required=True)
    parser.add_argument("--geojson", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--normalized-root", type=Path, required=True)
    parser.add_argument("--qa-root", type=Path, required=True)
    parser.add_argument("--run-id")
    parser.add_argument("--min-interval", type=float, default=1.05)
    parser.add_argument("--max-cycles", type=int, default=10)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()

    result = run_batch(
        args.queue,
        args.geojson,
        args.output_root,
        args.normalized_root,
        args.qa_root,
        run_id=args.run_id,
        min_interval=args.min_interval,
        max_cycles=args.max_cycles,
    )
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
