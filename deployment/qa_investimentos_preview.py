"""QA isolado de prévia RMRP: HTML/JSON acessíveis, estados candidatos preservados."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.request import Request, urlopen


def fetch(remote: str, path: str) -> bytes:
    req = Request(remote.rstrip("/") + "/" + path,
                  headers={"User-Agent": "MapaDoTesouro-PreviewQA/1"})
    with urlopen(req, timeout=40) as res:
        content_type = res.headers.get("Content-Type", "")
        if res.status != 200:
            raise RuntimeError(f"HTTP {res.status} em {path}")
        if path.endswith(".json") and "json" not in content_type:
            raise RuntimeError(f"JSON não servido como JSON em {path}: {content_type}")
        return res.read()


def validate(read):
    html = read("obrasgov-rmrp-preview.html").decode("utf-8")
    html2 = read("investimentos-rmrp-preview.html").decode("utf-8")
    if "não homologada" not in html.lower() or "não homologada" not in html2.lower():
        raise RuntimeError("Aviso de não homologação ausente")
    if "obrasgov-triagem-espacial.json" not in html:
        raise RuntimeError("HTML não aponta para conjunto espacial")
    proposals = json.loads(read("data/api/v3/investimentos/rmrp/preview-amostras.json"))
    obras = json.loads(read("data/api/v3/investimentos/rmrp/obrasgov-triagem-espacial.json"))
    if proposals["meta"]["status"] != "preview_qa_nao_publicavel":
        raise RuntimeError("Propostas incorretamente promovidas")
    if obras["meta"]["qa_status"] != "triagem_espacial_nao_validacao_financeira":
        raise RuntimeError("Obras incorretamente promovidas")
    if len(proposals["municipios"]) != 34 or len(proposals["propostas_amostrais"]) != 200:
        raise RuntimeError("Contagens da amostra Transferegov inesperadas")
    if len(obras["items"]) != 224:
        raise RuntimeError("Contagem de projetos Obrasgov inesperada")
    if len({i["id"] for i in obras["items"]}) != 224:
        raise RuntimeError("ID Obrasgov repetido")
    if len({m["codigo_ibge"] for m in obras["municipios"]}) != 34:
        raise RuntimeError("Municípios do Obrasgov não são 34 códigos únicos")
    counts = {}
    for x in obras["items"]:
        counts[x["estado_geo"]] = counts.get(x["estado_geo"], 0) + 1
    if counts != {
        "SEM_PONTO": 32, "FORA_DAS_MALHAS_RMRP": 61,
        "MUNICIPIO_CONFIRMADO_POR_POLIGONO": 130,
        "MULTIPLOS_MUNICIPIOS_POR_PONTOS": 1
    }:
        raise RuntimeError("Divergência na QA espacial do JSON")
    return {"qa": "pass", "municipios": 34, "propostas_amostrais": 200,
            "projetos_obrasgov": 224, "contagens": counts}


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--site", type=Path)
    group.add_argument("--url")
    a = parser.parse_args()
    if a.site:
        def reader(p):
            return (a.site / p).read_bytes()
    else:
        def reader(p):
            return fetch(a.url, p)
    print(json.dumps(validate(reader), ensure_ascii=False))


if __name__ == "__main__":
    main()
