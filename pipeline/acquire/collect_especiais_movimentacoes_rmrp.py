#!/usr/bin/env python3
"""Aquisição read-only, minimizada, de lançamentos bancários Transferegov Especiais RMRP.

Não persiste CNPJ, CPF, banco, agência, conta nem favorecidos. Mantém IDs públicos
de lançamento, data, operação, descrição, categoria, centavos e origem. Nunca
transforma créditos contábeis em repasses comprovados ou débitos em investimento.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import gzip
import hashlib
import json
import os
from pathlib import Path
import random
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

BASE = "https://api-publica.transferegov.gestao.gov.br/especiais/gestao-financeira-lancamentos-especiais"
UA = "MapaDoTesouro-INV-RMRP/0.2 (public-api-audit-readonly)"
PAGE_SIZE = 200


def cents(value):
    try:
        n = Decimal(str(value))
        return int((n * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP)) if n.is_finite() else None
    except (ValueError, InvalidOperation):
        return None


def read_beneficiaries(path):
    data = json.loads(path.read_text(encoding="utf-8"))
    out = []
    for row in data["items"]:
        b = row["beneficiarios"]
        if len(b) != 1:
            raise ValueError("Beneficiário municipal ambíguo: " + row["municipio"])
        cnpj = "".join(x for x in str(b[0]["cnpj"]) if x.isdigit())
        ibge = str(row["codigo_ibge"])
        if len(cnpj) != 14 or len(ibge) != 7:
            raise ValueError("CNPJ/IBGE municipal inválido")
        out.append((ibge, row["municipio"], cnpj))
    if len(out) != 34 or len({x[0] for x in out}) != 34:
        raise ValueError("Esperados 34 municípios com beneficiário único")
    return out


def get_page(cnpj, page, max_tries=5):
    url = BASE + "?" + urlencode({
        "cnpj_ente_solicitante_gestao_financeira": cnpj,
        "pagina": page, "tamanho_da_pagina": PAGE_SIZE,
    })
    for attempt in range(max_tries):
        try:
            req = Request(url, headers={"Accept": "application/json", "User-Agent": UA})
            with urlopen(req, timeout=60) as response:
                raw = response.read()
            result = json.loads(raw)
            if not isinstance(result.get("data"), list):
                raise ValueError("Resposta sem array data")
            if result.get("page_number") != page:
                raise ValueError("Número de página não corresponde à requisição")
            return raw, result
        except (HTTPError, URLError, TimeoutError, OSError) as error:
            status = getattr(error, "code", None)
            if status is not None and status not in (408, 429, 500, 502, 503, 504):
                raise
            if attempt == max_tries - 1:
                raise
            time.sleep(min(35, 2 ** attempt + random.random()))
    raise RuntimeError("Falha ao obter página")


def sanitize(record):
    value = cents(record.get("valor_gestao_financeira"))
    if value is None:
        raise ValueError("Valor financeiro ausente ou inválido")
    obj = {
        "id_lancamento": str(record.get("id_lancamento_gestao_financeira") or ""),
        "origem": record.get("origem_solicitacao_gestao_financeira"),
        "descricao": record.get("descricao_gestao_financeira"),
        "data": record.get("data_lancamento_gestao_financeira"),
        "tipo": record.get("tipo_operacao_gestao_financeira"),
        "valor_centavos": value,
        "categoria": record.get("codigo_categoria_despesa_lancamento_gestao_financeira"),
        "numero_subtransacoes": record.get("quantidade_subtransacoes_lancamento_gestao_financeira"),
    }
    if not obj["id_lancamento"] or obj["tipo"] not in ("C", "D"):
        raise ValueError("ID ou tipo de lançamento inválido")
    return obj


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".partial")
    raw = (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    with tmp.open("wb") as f:
        f.write(raw)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)
    return hashlib.sha256(raw).hexdigest()


def run(beneficiaries, out, limit=0, pause=0.25):
    # Se houve interrupção antes do manifesto, refazer a captura em nova execução.
    # Nenhuma execução incompleta é considerada snapshot homologado.
    result = []
    errors = []
    seen_ids = set()
    selected = read_beneficiaries(beneficiaries)
    for code, municipality, cnpj in selected:
        sanitized = []
        total = pages = None
        fetched = 0
        error = None
        for page in range(1, 51):
            try:
                raw, data = get_page(cnpj, page)
                if total is None:
                    total, pages = data["total_items"], data["total_pages"]
                if total != data["total_items"] or pages != data["total_pages"]:
                    raise ValueError("Fonte alterou total_items/total_pages durante captura")
                fetched += 1
                for record in data["data"]:
                    item = sanitize(record)
                    if item["id_lancamento"] in seen_ids:
                        raise ValueError("ID de lançamento duplicado em municípios distintos")
                    seen_ids.add(item["id_lancamento"])
                    sanitized.append(item)
                if page >= pages or (limit and page >= limit):
                    break
                if pause:
                    time.sleep(pause)
            except Exception as exc:
                error = f"{type(exc).__name__}: {exc}".replace(cnpj, "[CNPJ_SUPRIMIDO]")
                errors.append({"codigo_ibge": code, "pagina": page, "erro": error})
                break
        all_pages = bool(total is not None and fetched == pages and len(sanitized) == total and error is None)
        path = out / "municipios" / f"{code}.json"
        sha = save(path, {
            "codigo_ibge": code,
            "municipio": municipality,
            "total_items": total, "total_pages": pages,
            "pages_fetched": fetched,
            "complete": all_pages,
            "records": sanitized,
        })
        result.append({"codigo_ibge": code, "total": total, "recuperados": len(sanitized),
                       "paginas": fetched, "completo": all_pages, "sha256": sha,
                       "path": str(path.relative_to(out))})
        print(f"{code} {municipality}: {len(sanitized)}/{total} lançamentos; {fetched}/{pages} páginas", flush=True)
    complete = not errors and len(result) == 34 and all(x["completo"] for x in result) and not limit
    manifest = {
        "schema": "inv_rmrp_especiais_ledger_minimized_v1",
        "source": BASE,
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "qa_status": "pass" if complete else "incomplete",
        "snapshot_complete": complete,
        "municipios": len(result),
        "lancamentos": sum(x["recuperados"] for x in result),
        "pages": sum(x["paginas"] for x in result),
        "privacy": "Banco, agência, conta, documentos pessoais e dados de favorecidos descartados em memória",
        "financial_policy": "crédito/débito bancário não comprova investimento nem vínculo ao plano sem ID documental",
        "coverage": result,
        "errors": errors,
    }
    save(out / "manifest.json", manifest)
    return 0 if (complete or limit and not errors) else 2


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--beneficiaries", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--limit-pages", type=int, default=0)
    p.add_argument("--pause", type=float, default=0.25)
    a = p.parse_args()
    if a.limit_pages < 0 or a.pause < 0:
        p.error("limit-pages e pause devem ser positivos")
    sys.exit(run(a.beneficiaries, a.out, a.limit_pages, a.pause))


if __name__ == "__main__":
    main()
