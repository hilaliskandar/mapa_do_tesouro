"""Persistencia experimental, local e content-addressed de paginas publicas federais.

Sem conexao com o SQLite canonico, R2, Cloudflare, Github Actions ou automacoes.
O chamador precisa fornecer explicitamente a pasta de destino.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlsplit

from pipeline.acquire.federal_public_api import BASE_URLS, ENDPOINTS, PublicPage


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _write_immutable(target: Path, content: bytes) -> bool:
    """False se objeto ja persistido com o mesmo conteudo; nunca sobrescrever."""
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        with target.open("xb") as handle:
            handle.write(content)
        return True
    except FileExistsError:
        if target.read_bytes() != content:
            raise RuntimeError(f"Conflito em snapshot imutavel: {target}")
        return False


def _validate_page(page: PublicPage) -> None:
    if page.source not in ENDPOINTS or page.endpoint not in ENDPOINTS[page.source]:
        raise ValueError("Fonte ou rota nao autorizada")
    request = urlsplit(page.request_url)
    expected = urlsplit(BASE_URLS[page.source])
    if (
        request.scheme != "https"
        or request.netloc != expected.netloc
        or request.path != expected.path.rstrip("/") + "/" + page.endpoint
        or request.username is not None
        or request.password is not None
    ):
        raise ValueError("URL fora do dominio oficial")
    if (
        not 1 <= page.page_size <= 100
        or not 1 <= page.page_number <= 10000
        or page.total_items < 0
        or page.total_pages < 0
        or len(page.data) > page.page_size
    ):
        raise ValueError("Paginacao invalida")
    if not all(isinstance(row, dict) for row in page.data):
        raise ValueError("Dados malformados")


def persist_staging(pages: Iterable[PublicPage], *, output_dir: Path) -> dict[str, Any]:
    """Grava JSON de dados por hash e manifesto reutilizavel para um lote pequeno.

    Os dados e URLs podem conter identificadores de pessoas juridicas e destinatarios:
    gravar apenas em diretorio local privado, sob data/snapshots (ignorado pelo Git).
    """
    output = Path(output_dir)
    if not output.is_absolute():
        raise ValueError("Destinatario deve ser caminho absoluto explicito")
    records: list[dict[str, Any]] = []
    staged: list[tuple[Path, bytes]] = []
    seen: set[tuple[str, str, str, int]] = set()
    for page in pages:
        _validate_page(page)
        key = (page.source, page.endpoint, page.request_url, page.page_number)
        if key in seen:
            raise ValueError("Pagina repetida no lote")
        seen.add(key)
        value = {
            "schema_version": 1, "source": page.source, "endpoint": page.endpoint,
            "request_url": page.request_url, "page_number": page.page_number,
            "page_size": page.page_size, "total_items": page.total_items,
            "total_pages": page.total_pages, "data": page.data,
        }
        content = canonical_bytes(value)
        digest = sha256(content)
        relpath = Path(page.source) / page.endpoint / f"{digest}.json"
        staged.append((output / relpath, content))
        records.append({
            "source": page.source, "endpoint": page.endpoint,
            "request_url": page.request_url, "page_number": page.page_number,
            "row_count": len(page.data), "total_items_reported": page.total_items,
            "sha256": digest, "relative_path": relpath.as_posix(),
        })
        if len(records) > 20:
            raise ValueError("Limite de 20 paginas por lote experimental")
    if not records:
        raise ValueError("Lote vazio")
    # Manifesto deterministico por conjunto de paginas; nova consulta so produz
    # nova versao se um byte do conteudo ou metadado relevante mudou.
    manifest_key = sha256(canonical_bytes(records))
    manifest_path = output / "manifests" / f"{manifest_key}.json"
    for target, content in staged:
        _write_immutable(target, content)
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("manifest_id") != manifest_key or manifest.get("artifacts") != records:
            raise RuntimeError("Manifesto existente com conteudo divergente")
        return manifest
    manifest = {
        "schema_version": 1, "status": "experimental_unvalidated",
        "manifest_id": manifest_key,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "artifact_count": len(records), "row_count": sum(r["row_count"] for r in records),
        "artifacts": records,
        "warning": "Staging apenas: sem conciliacao financeira ou classificacao Novo PAC.",
    }
    _write_immutable(manifest_path, canonical_bytes(manifest))
    return manifest


def verify_manifest(*, output_dir: Path, manifest_id: str) -> dict[str, Any]:
    """Verifica integridade em leitura, sem modificar os arquivos."""
    if len(manifest_id) != 64 or any(c not in "0123456789abcdef" for c in manifest_id):
        raise ValueError("Identificador invalido")
    output = Path(output_dir)
    manifest = json.loads((output / "manifests" / f"{manifest_id}.json").read_text(encoding="utf-8"))
    if manifest["manifest_id"] != manifest_id:
        raise ValueError("Manifesto adulterado")
    if sha256(canonical_bytes(manifest["artifacts"])) != manifest_id:
        raise ValueError("Lista do manifesto adulterada")
    for artifact in manifest["artifacts"]:
        rel = Path(artifact["relative_path"])
        if rel.is_absolute() or ".." in rel.parts:
            raise ValueError("Caminho inseguro")
        if sha256((output / rel).read_bytes()) != artifact["sha256"]:
            raise ValueError(f"Hash divergente: {rel}")
    return manifest
