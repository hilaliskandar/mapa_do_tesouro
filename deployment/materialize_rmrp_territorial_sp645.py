"""Incorpora exclusivamente o cadastro territorial RMRP no build estadual SP645.

Com `--site`, valida o CSV IBGE original, o JSON e o HTML e materializa os
dois recursos no diretório da candidata. Com `--url`, valida os recursos
publicados na prévia sem alterar o site. Não toca em dinheiro ou dados fiscais.
"""
from __future__ import annotations

import argparse
import csv
import json
import shutil
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
CATALOG = "data/api/v3/investimentos/rmrp/territorio-validado.json"
HTML = "territorio-rmrp-validado.html"
SCRIPT = "territorio-rmrp-validado.js"
CROSSWALK = ROOT / "governance/controls/rmrp_cadastro_ibge34_2026_11_23.csv"
EXPECTED = {
    "Sub-região de Ribeirão Preto": 15,
    "Sub-região de Jaboticabal": 6,
    "Sub-região de Mococa": 6,
    "Sub-região de Batatais": 7,
}
FIELDS = {"codigo_ibge", "municipio", "sub_regiao"}
QA_STATUS = "validado_dimensao_territorial_sem_homologacao_financeira"


def check(read, *, require_nav=False):
    catalog = json.loads(read(CATALOG))
    if catalog.get("total_municipios") != 34:
        raise ValueError("Catálogo exige exatamente 34 municípios")
    if catalog.get("metadata", {}).get("qa_status") != QA_STATUS:
        raise ValueError("Marcador de homologação cadastral inválido")
    if set(catalog) != {"metadata", "total_municipios", "sub_regioes", "municipios"}:
        raise ValueError("Objeto de catálogo contém seções imprevistas")
    items = catalog["municipios"]
    if len(items) != 34 or any(set(x) != FIELDS for x in items):
        raise ValueError("Fichas precisam conter apenas os três campos cadastrais")
    codes = [x["codigo_ibge"] for x in items]
    if len(set(codes)) != 34 or any(not (x.isdigit() and len(x) == 7) for x in codes):
        raise ValueError("Códigos IBGE duplicados ou inválidos")
    counts = {name: sum(x["sub_regiao"] == name for x in items) for name in EXPECTED}
    if counts != EXPECTED:
        raise ValueError(f"Cardinalidade regional divergente: {counts}")
    regions = {x["nome"]: x["municipios"] for x in catalog["sub_regioes"]}
    if regions != EXPECTED or len(catalog["sub_regioes"]) != 4:
        raise ValueError("Resumo regional divergente")
    with CROSSWALK.open(encoding="utf-8-sig", newline="") as f:
        roster = list(csv.DictReader(f, delimiter=";"))
    expected_rows = {
        (x["codigo_ibge"], x["municipio"], x["sub_regiao"])
        for x in roster
    }
    actual_rows = {
        (x["codigo_ibge"], x["municipio"], x["sub_regiao"])
        for x in items
    }
    if len(roster) != 34 or actual_rows != expected_rows:
        raise ValueError("Catálogo diverge do crosswalk IBGE oficial do projeto")
    if require_nav:
        home = read("index.html").decode("utf-8")
        if '<a href="./territorio-rmrp-validado.html"' not in home:
            raise ValueError("Catálogo territorial não aparece na navegação do portal estadual")
    html = read(HTML).decode("utf-8")
    if "Cadastro territorial validado" not in html or CATALOG not in html:
        raise ValueError("HTML sem aviso cadastral ou vínculo com o JSON")
    if '<script src="./territorio-rmrp-validado.js" defer></script>' not in html or "<script>" in html:
        raise ValueError("Script territorial deve ser externo para respeitar CSP")
    script = read(SCRIPT).decode("utf-8")
    if CATALOG not in script or "textContent" not in script:
        raise ValueError("Script territorial ausente ou incompatível")
    if "obra executada" in html.lower() and "não" not in html.lower():
        raise ValueError("HTML ambíguo sobre execução")
    return {"status": "pass", "municipios": 34, "sub_regioes": counts,
            "somente_cadastro": True}


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--site", type=Path)
    group.add_argument("--url", type=str)
    args = parser.parse_args()
    if args.site:
        root = args.site.resolve()
        if not (root / "index.html").is_file() or not (root / "data/metadata.json").is_file():
            raise SystemExit("Build SP645 preexistente não identificado")
        source = ROOT / "app/static"
        check(lambda rel: (source / rel).read_bytes())
        for relative in (CATALOG, HTML, SCRIPT):
            dst = root / relative
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source / relative, dst)
        home = root / "index.html"
        home_html = home.read_text(encoding="utf-8")
        needle = "</header>"
        if home_html.count(needle) != 1:
            raise ValueError("Cabeçalho estadual inesperado; recusa injeção de navegação")
        link = '<p class="muted"><a href="./territorio-rmrp-validado.html">Municípios e sub-regiões da RMRP — cadastro territorial</a></p>'
        if link not in home_html:
            home.write_text(home_html.replace(needle, link + "\\n" + needle, 1), encoding="utf-8")
        result = check(lambda rel: (root / rel).read_bytes(), require_nav=True)
    else:
        base = args.url.rstrip("/")
        def get(rel):
            req = Request(base + "/" + rel, headers={"User-Agent": "sp645-cadastro-rmrp-qa/1"})
            with urlopen(req, timeout=45) as response:
                if response.status != 200:
                    raise ValueError(f"HTTP {response.status}: {rel}")
                if rel.endswith(".json") and "json" not in response.headers.get("Content-Type", ""):
                    raise ValueError("MIME JSON inválido")
                return response.read()
        result = check(get, require_nav=True)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
