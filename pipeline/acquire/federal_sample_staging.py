"""Amostragem controlada em APIs federais publicas com persistencia local experimental.

Execucao voluntaria: python -m pipeline.acquire.federal_sample_staging
    --output /caminho/privado/absoluto
Nenhuma alteracao de banco, deploy, R2 ou cron.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from pipeline.acquire.federal_public_api import PublicFederalClient
from pipeline.acquire.federal_staging import persist_staging, verify_manifest


SAMPLES = (
    ("obrasgov", "projeto-investimento", {"uf_principal": "SP"}),
    ("parcerias", "proposta", {"sg_uf_recebedor": "SP"}),
    ("especiais", "programas-especiais", {}),
)


def run_sample(*, output: Path, client: PublicFederalClient | None = None) -> dict:
    """Executa tres GETs e persiste somente uma pagina de cada, fail closed."""
    if not output.is_absolute():
        raise ValueError("Output deve ser um diretorio absoluto privado")
    client = client or PublicFederalClient(timeout=25, retries=2)
    pages = [
        client.fetch_page(source, endpoint, filters=filters, page=1, page_size=2)
        for source, endpoint, filters in SAMPLES
    ]
    if len(pages) != 3 or any(not page.data for page in pages):
        raise RuntimeError("Amostra inesperadamente incompleta; nao persistir lote")
    manifest = persist_staging(pages, output_dir=output)
    checked = verify_manifest(output_dir=output, manifest_id=manifest["manifest_id"])
    if checked["artifact_count"] != 3:
        raise RuntimeError("Quantidade de artefatos inconsistente")
    return {
        "status": "staging_verified_local_only",
        "manifest_id": checked["manifest_id"],
        "artifact_count": checked["artifact_count"],
        "row_count": checked["row_count"],
        "source_counts": {
            item["source"]: {
                "sample_rows": item["row_count"],
                "total_items_reported": item["total_items_reported"],
            }
            for item in checked["artifacts"]
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Amostra limitada de APIs federais em diretorio privado local."
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    # Retorna somente contagens e hashes; nunca imprime nomes/valores/documentos.
    print(json.dumps(run_sample(output=args.output), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
