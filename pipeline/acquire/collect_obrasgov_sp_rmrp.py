#!/usr/bin/env python3
"""Obrasgov SP: aquisição paginada íntegra e verificável, para triagem posterior RMRP.

Read-only: não altera SQLite, R2, D1 ou arquivos de publicação.
Usar --max-pages 1 para testar sem afirmar completude.
"""
import argparse
import gzip
import hashlib
import json
import os
from pathlib import Path
import random
import sys
import time
from datetime import datetime, timezone
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

BASE = "https://api-publica.obrasgov.gestao.gov.br/obras/projeto-investimento"
UA = "MapaDoTesouro-INV-RMRP/0.2 (audit-read-only)"
SIZE = 200


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def put_atomic(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".partial")
    with tmp.open("wb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(tmp, path)


def request_page(page, max_attempts=6, sleep=time.sleep):
    url = BASE + "?" + urlencode({"uf_principal": "SP", "pagina": page, "tamanho_da_pagina": SIZE})
    for retry in range(max_attempts):
        try:
            with urlopen(Request(url, headers={"Accept": "application/json", "User-Agent": UA}), timeout=90) as r:
                payload = r.read()
            result = json.loads(payload)
            if not isinstance(result.get("data"), list):
                raise ValueError("Ausência de lista 'data'")
            if result.get("page_number") != page or result.get("page_size") != SIZE:
                raise ValueError("Incompatibilidade de parâmetros na resposta")
            if not isinstance(result.get("total_items"), int) or not isinstance(result.get("total_pages"), int):
                raise ValueError("Contadores de paginação ausentes")
            return url, payload, result
        except (HTTPError, URLError, TimeoutError, OSError) as e:
            status = getattr(e, "code", None)
            if status is not None and status not in (408, 425, 429, 500, 502, 503, 504):
                raise
            if retry >= max_attempts - 1:
                raise
            retry_after = None
            if isinstance(e, HTTPError):
                header = e.headers.get("Retry-After")
                if header and header.isdigit():
                    retry_after = int(header)
            sleep(min(90, retry_after if retry_after is not None else 2 ** retry + random.random()))
    raise RuntimeError("Tentativas esgotadas")


def inspect(output):
    pages = output / "pages"
    files = sorted(pages.glob("page-*.json.gz")) if pages.exists() else []
    found = {}
    for path in files:
        number = int(path.stem.split("-")[1].split(".")[0])
        payload = gzip.decompress(path.read_bytes())
        row = json.loads(payload)
        if row.get("page_number") != number or row.get("page_size") != SIZE:
            raise ValueError(f"Arquivo incompatível: {path}")
        found[number] = {"page": number, "raw_sha256": digest(payload), "gz_sha256": digest(path.read_bytes()),
                         "rows": len(row["data"]), "total_items": row["total_items"],
                         "total_pages": row["total_pages"], "file": str(path.relative_to(output))}
    return found


def check(pages):
    if not pages:
        return {"complete": False, "reason": "sem páginas"}
    total = {p["total_items"] for p in pages.values()}
    count = {p["total_pages"] for p in pages.values()}
    if len(total) != 1 or len(count) != 1:
        return {"complete": False, "reason": "total_items/total_pages alterado entre páginas"}
    count = count.pop()
    total = total.pop()
    expected = set(range(1, count + 1))
    missing = sorted(expected - set(pages))
    rows = sum(p["rows"] for p in pages.values())
    return {"complete": not missing and rows == total, "expected_pages": count,
            "retrieved_pages": len(pages), "missing_pages": missing, "source_total_items": total,
            "retrieved_rows": rows, "reason": None if not missing and rows == total else "cobertura incompleta"}


def extract_index(output, pages):
    """Gerar índice sem imputar municipalidade pelo nome do projeto."""
    index = []
    ids = set()
    duplicates = []
    for page in sorted(pages):
        blob = gzip.decompress((output / pages[page]["file"]).read_bytes())
        for row in json.loads(blob)["data"]:
            ident = str(row.get("id_projeto_investimento") or "")
            if not ident:
                raise ValueError("ID de projeto ausente")
            if ident in ids:
                duplicates.append(ident)
            ids.add(ident)
            pins = [
                {"lat": item.get("latitude"), "lon": item.get("longitude")}
                for item in (row.get("pins") or [])
            ]
            index.append({
                "id_projeto_investimento": ident,
                "desc_nome": row.get("desc_nome"),
                "situacao": row.get("situacao"),
                "uf_principal": row.get("uf_principal"),
                "pins": pins,
                "fontes_previstas": row.get("investimentos_previstos"),
                "raw_page": page,
                "qa_localizacao": "sem_confronto_com_poligono_municipal",
                "qa_financeiro": "valor_previsto_nao_equivale_a_pagamento",
            })
    return index, sorted(set(duplicates))


def run(output, max_pages, pause):
    output.mkdir(parents=True, exist_ok=True)
    seen = inspect(output)
    failures = []
    target_pages = max_pages if max_pages else (next(iter(seen.values()))["total_pages"] if seen else None)
    if target_pages is None:
        try:
            url, payload, response = request_page(1)
            put_atomic(output / "pages" / "page-00001.json.gz",
                       gzip.compress(payload, compresslevel=6, mtime=0))
            seen = inspect(output)
            target_pages = response["total_pages"] if not max_pages else max_pages
        except Exception as error:
            failures.append({"page": 1, "error": str(error)})
            target_pages = 0

    for page in range(1, target_pages + 1):
        if page in seen:
            continue
        try:
            url, payload, row = request_page(page)
            if seen:
                exemplar = next(iter(seen.values()))
                if exemplar["total_items"] != row["total_items"] or exemplar["total_pages"] != row["total_pages"]:
                    raise ValueError("A contagem da origem mudou; usar novo diretório de snapshot")
            put_atomic(output / "pages" / f"page-{page:05d}.json.gz",
                       gzip.compress(payload, compresslevel=6, mtime=0))
            new_path = output / "pages" / f"page-{page:05d}.json.gz"
            compressed = new_path.read_bytes()
            seen[page] = {
                "page": page,
                "raw_sha256": digest(payload),
                "gz_sha256": digest(compressed),
                "rows": len(row["data"]),
                "total_items": row["total_items"],
                "total_pages": row["total_pages"],
                "file": str(new_path.relative_to(output)),
            }
        except Exception as exc:
            failures.append({"page": page, "error": str(exc)})
            break
        if pause:
            time.sleep(pause)

    state = check(seen)
    state["requested_max_pages"] = max_pages
    state["run_started"] = utc_now()
    state["errors"] = failures
    state["manifest_sha256"] = None
    index = []
    duplicate_ids = []
    if seen:
        index, duplicate_ids = extract_index(output, seen)
    state["duplicate_project_ids"] = duplicate_ids
    state["unique_project_ids"] = len({r["id_projeto_investimento"] for r in index})
    # Não considerar aquisição truncada completa nem amostra temporalmente estável.
    state["complete"] = state["complete"] and not max_pages and not failures and not duplicate_ids
    state["status"] = "snapshot_capturado_sem_homologacao_territorial" if state["complete"] else "incompleto"
    manifest = {"source": BASE, "uf": "SP", "retrieved_at": utc_now(),
                "page_size": SIZE, "pages": [seen[i] for i in sorted(seen)],
                "qa": state, "limits": [
                    "API não garante snapshot transacional entre páginas",
                    "Arquivo completo não significa município de execução homologado",
                    "Investimentos previstos não são transferências realizadas nem despesas pagas"
                ]}
    put_atomic(output / "index.json.gz",
               gzip.compress(json.dumps(index, ensure_ascii=False).encode(), compresslevel=6, mtime=0))
    put_atomic(output / "manifest.json", (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode())
    print(json.dumps({"status": state["status"], "pages": len(seen),
                      "records": len(index), "failures": failures, "duplicates": len(duplicate_ids)},
                     ensure_ascii=False))
    return 0 if state["complete"] or max_pages and not failures else 2


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--max-pages", type=int, default=0, help="0 = todas as páginas; limite para teste")
    parser.add_argument("--pause", type=float, default=0.4)
    a = parser.parse_args()
    if a.max_pages < 0 or a.pause < 0:
        parser.error("max-pages e pause devem ser não-negativos")
    return run(a.output, a.max_pages, a.pause)


if __name__ == "__main__":
    sys.exit(main())
