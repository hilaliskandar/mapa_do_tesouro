#!/usr/bin/env python3
"""Aquisição read-only Transferegov RMRP: todos os registros paginados, em staging.
Não altera o SQLite, R2, D1 ou o site. Sem merge de módulos ou classificação por heurística.
Uso: python pipeline/acquire/collect_investimentos_rmrp.py --roster governance/INV_RMRP_34_MUNICIPIOS_PILOTO_IBGE_VERIFICADO_2026_11_11.csv --output /tmp/inv-rmrp
"""
import argparse
import csv
import gzip
import hashlib
import json
import os
import pathlib
import random
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from datetime import datetime, timezone

BASE = "https://api-publica.transferegov.gestao.gov.br"
MODULES = {
    "parcerias": ("proposta", "cd_ibge_recebedor", "id_proposta"),
    "discricionarias": ("propostas", "cod_munic_ibge", "id_proposta"),
}
USER_AGENT = "MapaDoTesouro-RMRP-Acquisition/1.0 (open public API; QA only)"


def fetch_json(url, attempts=5):
    for i in range(attempts):
        try:
            req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=50) as response:
                raw = response.read()
            obj = json.loads(raw)
            if not isinstance(obj, dict) or not isinstance(obj.get("data"), list):
                raise ValueError("Resposta sem lista 'data'")
            return obj, raw
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, OSError) as exc:
            code = getattr(exc, "code", None)
            if code is not None and code not in (408, 425, 429, 500, 502, 503, 504):
                raise
            if i == attempts - 1:
                raise
            time.sleep(min(30, 2 ** i + random.random()))
    raise RuntimeError("Falha de leitura")


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def atomic_write(path, body):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    with tmp.open("wb") as f:
        f.write(body)
    os.replace(tmp, path)


def roster_read(path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        records = list(csv.DictReader(f, delimiter=";"))
    ids = [x["codigo_ibge"] for x in records]
    if len(records) != 34 or len(set(ids)) != 34 or any(len(x) != 7 or not x.isdigit() for x in ids):
        raise ValueError("Roster RMRP deve conter 34 codigos IBGE7 unicos")
    return records


def classify(row, module):
    if module == "parcerias":
        return row.get("categoria_despesa_proposta_categoria_despesa")
    return row.get("categorias_proposta")


def run(roster, output, limit_pages=0, delay=0.1):
    cities = roster_read(roster)
    output.mkdir(parents=True, exist_ok=True)
    staging = output / "raw"
    run_date = datetime.now(timezone.utc).isoformat()
    manifest = {"schema": "inv_rmrp_transferegov_raw_v1", "retrieved_at": run_date,
                "universo": "RMRP_34", "municipalities": 34, "qa_status": "candidate",
                "snapshot_complete": False, "sources": [], "warnings": [],
                "financial_evidence": "proposals_not_payments"}
    errors = []
    for city in cities:
        code = city["codigo_ibge"]
        for module, (route, parameter, primary) in MODULES.items():
            folder = staging / module / code
            page = 1
            seen = set()
            count = 0
            declared = None
            pages = None
            duplicate_ids = []
            while True:
                query = urllib.parse.urlencode({parameter: code, "pagina": page, "tamanho_da_pagina": 200})
                url = f"{BASE}/{module}/{route}?{query}"
                path = folder / f"page-{page:05d}.json.gz"
                # A página é guardada inteira, permitindo uma futura normalização reprodutível.
                try:
                    obj, raw = fetch_json(url)
                    if obj.get("page_number") != page:
                        raise ValueError(f"Pagina retornada inconsistente: {obj.get('page_number')} != {page}")
                    if declared is None:
                        declared = int(obj["total_items"])
                        pages = int(obj["total_pages"])
                    elif int(obj["total_items"]) != declared or int(obj["total_pages"]) != pages:
                        raise ValueError("Contagem/paginacao alterada durante a captura")
                    data = obj["data"]
                    for item in data:
                        rid = item.get(primary)
                        if rid is None:
                            raise ValueError(f"ID primario ausente em {module} {code}")
                        key = str(rid)
                        if key in seen:
                            duplicate_ids.append(key)
                        seen.add(key)
                        municipal_code = item.get(parameter)
                        if str(municipal_code) != code:
                            raise ValueError(f"Municipio de retorno incorreto: {municipal_code} em {code}")
                    atomic_write(path, gzip.compress(raw, compresslevel=6, mtime=0))
                    count += len(data)
                    manifest["sources"].append({
                        "module": module, "codigo_ibge": code, "page": page, "url": url,
                        "count": len(data), "sha256": sha256(path), "bytes_gzip": path.stat().st_size,
                        "total_items_declared": declared, "total_pages_declared": pages,
                        "artifact": str(path.relative_to(output))
                    })
                    if page >= pages or not data or (limit_pages and page >= limit_pages):
                        break
                    page += 1
                    if delay > 0:
                        time.sleep(delay)
                except Exception as exc:
                    errors.append({"module": module, "codigo_ibge": code, "page": page,
                                   "url": url, "error": str(exc)})
                    break
            manifest.setdefault("coverage", []).append({
                "codigo_ibge": code, "municipio": city["municipio"], "module": module,
                "expected": declared, "retrieved": count, "duplicate_ids": duplicate_ids,
                "all_pages": bool(pages is not None and page >= pages and not errors
                                  or pages is not None and page >= pages and count == declared
                                  and not duplicate_ids),
                "page_count": pages
            })
            print(f"{module} {code}: {count}/{declared} itens, {page}/{pages} paginas", flush=True)

    # O QA opera sobre cada chave API e não deduplica indevidamente entre módulos.
    complete = not errors and not limit_pages and all(
        entry["expected"] == entry["retrieved"] and not entry["duplicate_ids"]
        for entry in manifest["coverage"]
    )
    manifest["errors"] = errors
    manifest["snapshot_complete"] = complete
    manifest["qa_status"] = "pass" if complete else "incomplete"
    path = output / "manifest.json"
    atomic_write(path, (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode())
    with (output / "coverage.csv").open("w", newline="", encoding="utf-8") as f:
        fields = ["codigo_ibge", "municipio", "module", "expected", "retrieved",
                  "page_count", "all_pages", "duplicate_ids"]
        writer = csv.DictWriter(f, fieldnames=fields, delimiter=";")
        writer.writeheader()
        for x in manifest["coverage"]:
            writer.writerow({**x, "duplicate_ids": "|".join(x["duplicate_ids"])})
    return 0 if complete or limit_pages else 2


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--roster", type=pathlib.Path, required=True)
    parser.add_argument("--output", type=pathlib.Path, required=True)
    parser.add_argument("--limit-pages", type=int, default=0, help="Somente smoke test; nao representa censo")
    parser.add_argument("--delay", type=float, default=0.1)
    args = parser.parse_args()
    return run(args.roster, args.output, args.limit_pages, args.delay)


if __name__ == "__main__":
    sys.exit(main())
