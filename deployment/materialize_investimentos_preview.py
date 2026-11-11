"""Materializa apenas a prévia INV-RMRP no build/site da PR #233.

Uso explícito no job de preview da PR 233. Não altera implantação principal,
SQLite, R2 ou fontes canônicas e não transforma candidatos em dados homologados.
"""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FRONTEND = ROOT / "app" / "static"

FILES = (
    "investimentos-rmrp-preview.html",
    "obrasgov-rmrp-preview.html",
    "data/api/v3/investimentos/rmrp/preview-amostras.json",
    "data/api/v3/investimentos/rmrp/obrasgov-triagem-espacial.json",
)


def overlay(site: Path, source: Path = FRONTEND) -> dict:
    if not (site / "index.html").is_file():
        raise RuntimeError("Candidato Pages não materializado")
    missing = [p for p in FILES if not (source / p).is_file()]
    if missing:
        raise RuntimeError(f"Arquivos INV-RMRP ausentes: {missing}")

    proposals = json.loads((source / FILES[2]).read_text(encoding="utf-8"))
    obras = json.loads((source / FILES[3]).read_text(encoding="utf-8"))
    if proposals["meta"]["status"] != "preview_qa_nao_publicavel":
        raise RuntimeError("Propostas sem marcador de prévia")
    if obras["meta"]["qa_status"] != "triagem_espacial_nao_validacao_financeira":
        raise RuntimeError("Obrasgov sem marcador de triagem")

    codes = {m["codigo_ibge"] for m in proposals["municipios"]}
    geocodes = {m["codigo_ibge"] for m in obras["municipios"]}
    if len(codes) != 34 or codes != geocodes:
        raise RuntimeError("Os 34 municípios da RMRP não coincidem entre as bases")
    if len(proposals["propostas_amostrais"]) != 200:
        raise RuntimeError("Amostra Transferegov alterada sem revisão")
    if len(obras["items"]) != 224:
        raise RuntimeError("Amostra Obrasgov alterada sem revisão")

    ids = [x["id"] for x in obras["items"]]
    if len(set(ids)) != len(ids):
        raise RuntimeError("IDs Obrasgov duplicados")

    counts = {}
    for x in obras["items"]:
        counts[x["estado_geo"]] = counts.get(x["estado_geo"], 0) + 1
    expected = {
        "SEM_PONTO": 32,
        "FORA_DAS_MALHAS_RMRP": 61,
        "MUNICIPIO_CONFIRMADO_POR_POLIGONO": 130,
        "MULTIPLOS_MUNICIPIOS_POR_PONTOS": 1,
    }
    if counts != expected:
        raise RuntimeError(f"Distribuição espacial diferente da auditada: {counts}")

    for name in FILES:
        destination = site / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source / name, destination)

    summary = {
        "preview_only": True,
        "site": str(site),
        "municipios": len(codes),
        "transferegov_amostra": len(proposals["propostas_amostrais"]),
        "obrasgov_triagem": len(obras["items"]),
        "estado_espacial": counts,
        "files_copied": list(FILES),
    }
    (site / "data" / "api" / "v3" / "investimentos" / "rmrp" / "qa_preview_overlay.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", type=Path, required=True)
    a = parser.parse_args()
    print(json.dumps(overlay(a.site), ensure_ascii=False))


if __name__ == "__main__":
    main()
