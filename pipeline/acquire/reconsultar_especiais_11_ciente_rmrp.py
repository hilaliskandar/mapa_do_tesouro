#!/usr/bin/env python3
"""Reconsulta documental, somente leitura, dos planos TE pendentes da RMRP.

Nunca equipara ausência de resultado a ausência de pagamento; nunca publica
conta, CNPJ, CPF, banco, agência ou favorecido. Gera somente metadados de
plano/documentos e links para a API, com estado de erro distinto.
"""
import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

BASE = "https://api-publica.transferegov.gestao.gov.br/especiais"
ROUTES = {
    "empenhos": ("empenhos-especiais", "id_plano_acao", "id_empenho"),
    "documentos": ("documentos-habeis-especiais", "id_empenho", "id_dh"),
    "ordens": ("ordens-pagamentos-ordens-bancarias-especiais", "id_dh", "id_op_ob"),
}
ALLOWED_STATES = {"CIENTE", "IMPEDIDO", "EM_ELABORACAO_OU_ANALISE"}
MAX_PAGES = 50


def fetch(route, key, value, retries=4):
    endpoint, _, _ = ROUTES[route]
    records = []
    pages = None
    for page in range(1, MAX_PAGES + 1):
        params = {key: value, "pagina": page, "tamanho_da_pagina": 100}
        url = BASE + "/" + endpoint + "?" + urlencode(params)
        for attempt in range(retries):
            try:
                with urlopen(Request(url, headers={
                    "Accept": "application/json",
                    "User-Agent": "MapaDoTesouro-RMRP-Auditoria/1",
                }), timeout=45) as response:
                    payload = json.load(response)
                break
            except (HTTPError, URLError, TimeoutError, OSError):
                if attempt == retries - 1:
                    raise
                time.sleep(2 ** attempt)
        if not isinstance(payload, dict) or not isinstance(payload.get("data"), list):
            raise ValueError("Resposta não contém lista data")
        if payload.get("page_number") not in (None, page):
            raise ValueError("Número de página inconsistente")
        page_total = payload.get("total_pages")
        if not isinstance(page_total, int) or page_total < 0 or page_total > MAX_PAGES:
            raise ValueError("total_pages inválido ou acima do limite")
        if pages is None:
            pages = page_total
        if page_total != pages:
            raise ValueError("Paginação alterada durante a consulta")
        records.extend(payload["data"])
        if page >= pages:
            break
    else:
        raise ValueError("Limite de páginas atingido sem conclusão")
    if isinstance(payload.get("total_items"), int) and page_total == 1 and len(records) != payload["total_items"]:
        raise ValueError("Contagem divergente na página única")
    return records


def ids(records, field):
    values = set()
    for item in records:
        identifier = item.get(field)
        if identifier is None or str(identifier).strip() == "":
            raise ValueError("Identificador documental ausente: " + field)
        values.add(str(identifier))
    return sorted(values)


def unique_records(route, identifiers, output):
    collected = set()
    for identifier in identifiers:
        data = fetch(route, ROUTES[route][1], identifier)
        for key in ids(data, ROUTES[route][2]):
            collected.add(key)
    return sorted(collected)


def inspect(row):
    plan = row["id_plano_acao"]
    result = {
        "id_plano_acao": plan,
        "codigo_ibge": row["codigo_ibge"],
        "municipio": row["municipio"],
        "estado_plano_na_matriz": row["estado_plano"],
        "classe_original": row["classe_pendencia"],
        "consulta_em": datetime.now(timezone.utc).isoformat(),
        "estado_consulta": "ERRO_COLETA",
        "empenhos_identificados": None,
        "documentos_identificados": None,
        "ordens_identificadas": None,
        "credito_bancario_confirmado": False,
        "erro": None,
    }
    try:
        empenhos = ids(fetch("empenhos", "id_plano_acao", plan), "id_empenho")
        result["empenhos_identificados"] = len(empenhos)
        dhs = unique_records("documentos", empenhos, result)
        result["documentos_identificados"] = len(dhs)
        obs = unique_records("ordens", dhs, result)
        result["ordens_identificadas"] = len(obs)
        result["estado_consulta"] = (
            "OB_DOCUMENTAL_RETORNADA_SEM_CREDITO_CONFIRMADO" if obs else
            "DH_SEM_OB_RETORNADA" if dhs else
            "EMPENHO_SEM_DH_RETORNADO" if empenhos else
            "SEM_EMPENHO_RETORNADO"
        )
    except Exception as exc:
        result["erro"] = type(exc).__name__ + ": " + str(exc)[:180]
    return result


def run(args):
    with args.queue.open(encoding="utf-8", newline="") as handle:
        pending = list(csv.DictReader(handle, delimiter=";"))
    if len(pending) != 42 or len({x["id_plano_acao"] for x in pending}) != 42:
        raise ValueError("Fila de 42 planos duplicada ou incompleta")
    selected = [x for x in pending if x["grupo_administrativo"] == "CIENTE"]
    if len(selected) != 11:
        raise ValueError("Esperados 11 planos CIENTE")
    results = [inspect(x) for x in selected]
    manifest = {
        "dataset": "inv_rmrp_especiais_11_ciente_reconsulta_v1",
        "run_at_utc": datetime.now(timezone.utc).isoformat(),
        "plans_expected": 11, "plans_examined": len(results),
        "errors": sum(x["estado_consulta"] == "ERRO_COLETA" for x in results),
        "disclaimer": "OB retornada não comprova crédito; retorno vazio não comprova inexistência de pagamento.",
        "results": results,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    raw = (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode()
    args.out.write_bytes(raw)
    print(json.dumps({"planos": len(results), "erros": manifest["errors"],
                      "sha256": hashlib.sha256(raw).hexdigest()}, ensure_ascii=False))
    return 2 if manifest["errors"] else 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--queue", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    raise SystemExit(run(parser.parse_args()))
