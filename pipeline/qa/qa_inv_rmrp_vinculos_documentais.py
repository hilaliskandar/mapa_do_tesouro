#!/usr/bin/env python3
"""QA de vínculos de investimentos RMRP, somente leitura, nunca cria pagamento.

Critério de vínculo: referência literal de identificador oficial no texto do
projeto. Mesmo uma correspondência futura será CANDIDATO, não comprovante de
execução. Localização e classificação de fonte não criam relação financeira.
"""
from __future__ import annotations
import csv
import json
from pathlib import Path
import re
import unicodedata

ROOT = Path(__file__).resolve().parents[2]
G = ROOT / "governance"
OBRAS = ROOT / "app/static/data/api/v3/investimentos/rmrp/obrasgov-triagem-espacial.json"
MAT = G / "INV_RMRP_SIAFEM_OBRASGOV_55_PROJETOS_ESTADUAIS_TRIAGEM_2026_11_12.csv"
QA = G / "INV_RMRP_VINCULOS_DOCUMENTAIS_TRIAGEM_QA_2026_11_12.json"
YEAR = G / "INV_RMRP_SIAFEM_889_CONVENIO_ANO_EXATO_2026_11_12.csv"
FED = G / "INV_RMRP_ESPECIAIS_284_CADEIAS_FINANCEIRAS_MATRIZ_2026_11_11.csv"


def read(path):
    with path.open(encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh, delimiter=";"))


def norm(s):
    return "".join(c for c in unicodedata.normalize("NFD", s.upper())
                   if unicodedata.category(c) != "Mn")


def main():
    projects = json.loads(OBRAS.read_text(encoding="utf-8"))["items"]
    annual = read(YEAR)
    federal = read(FED)
    triage = read(MAT)
    summary = json.loads(QA.read_text(encoding="utf-8"))
    unique = {(x["codigo_ibge"], x["numero_convenio_siafem"])
              for x in annual}
    localized = [x for x in projects if
                 x["estado_geo"] == "MUNICIPIO_CONFIRMADO_POR_POLIGONO"]
    state = [x for x in localized if
             any(f["fonte"] == "Estadual" for f in x["fontes_previstas"])]
    assert len(projects) == 224 and len(localized) == 130
    assert len(unique) == 752 and len(federal) == 284
    assert len(state) == 55 and len(triage) == 55
    by_project = {r["id_projeto_obrasgov"]: r for r in triage}
    assert len(by_project) == len(triage)
    direct_state = 0
    direct_federal = 0
    for p in projects:
        words = norm(p["nome"] + " " + p["descricao"])
        for ibge, number in unique:
            if norm(number) in words:
                direct_state += 1
        for x in federal:
            pattern = r"PLANO\s+DE\s+ACAO\s*#?\s*" + re.escape(x["id_plano_acao"]) + r"\b"
            if re.search(pattern, words):
                direct_federal += 1
        if p in state:
            row = by_project[p["id"]]
            assert row["codigo_ibge_geom"] == p["municipios_intersecao"][0]["code"]
            assert row["organizacao_responsavel_obrasgov"] == p["organizacao"]
            assert row["indicador_vinculo_siafem"] == "SEM_VINCULO_DOCUMENTAL"
            assert not re.search("PREFEITURA|MUNICIPIO", norm(p["organizacao"]))
    assert direct_state == 0, "Novo identificador SIAFEM em obra: exige auditoria, não cria vínculo"
    assert direct_federal == 0, "Novo identificador federal em obra: exige auditoria"
    expected = {
        "obras_total":224,"obras_localizadas_unico":130,
        "obras_estaduais_localizadas_unico":55,"obras_estaduais_outside":15,
        "convenios_siafem":752,"planos_federais":284,
        "correspondencias_documentais_siafem_obrasgov":0,
        "correspondencias_documentais_federal_obrasgov":0,
        "orgs_estado_unico":8,"obras_estaduais_responsavel_prefeitura":0,
        "municipios_estado_unico":22,"municipios_ambas":22
    }
    for key, value in expected.items():
        assert summary[key] == value, (key, summary.get(key), value)
    print(json.dumps({"status":"QA_PASS_SEM_VINCULOS_FINANCEIROS_INFERIDOS",
                      "projetos":224,"fontes_estaduais_em_malha":55,
                      "convenios_siafem":752,"planos_federais":284,
                      "chaves_documentais_literal_encontradas":0}, ensure_ascii=False))


if __name__ == "__main__":
    main()
