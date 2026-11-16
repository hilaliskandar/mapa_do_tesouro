#!/usr/bin/env python3
"""Fail-closed audit for the RMRP static API v3 package (FED07).
Run: python pipeline/qa/validate_rmrp_api_v3_fed07.py DIR/data/api/v3/investimentos/rmrp
This script tests technical consistency, NOT legal or financial homologation.
"""
import argparse
import json
from pathlib import Path

def read(p):
    if not p.is_file():
        raise AssertionError(f"Missing JSON: {p}")
    return json.loads(p.read_text(encoding="utf-8"))

def validate(root: Path):
    manifest = read(root / "manifest.json")
    idx = read(root / "municipios.json")
    pend = read(root / "pendencias.json")
    municipalities = idx["municipios"]
    assert len(municipalities) == 34
    codes = [m["ibge"] for m in municipalities]
    assert len(set(codes)) == 34
    assert all(isinstance(x, str) and len(x) == 7 and x.isdecimal() for x in codes)
    assert manifest["public_release_authorized"] is False
    assert manifest["coverage"]["localizacoes_fisicas_homologadas"] == 0
    assert manifest["coverage"]["projetos_com_ponte_documental_instrumento"] == 218
    assert manifest["coverage"]["pagamentos_favorecidos_movimentos"] == 28503
    assert "financeiro" in pend and "territorial" in pend
    checks = 0
    sums = {"pay": 0, "amount": 0, "coords": 0, "project_links": 0}
    for row in municipalities:
        code = row["ibge"]
        j = read(root / "municipios" / f"{code}.json")
        assert j["codigo_ibge"] == code
        assert j["subregiao_rmrp_codigo"] in {"01", "02", "03", "04"}
        assert j["totais_por_dimensao"]["federal_pagamentos_diretos_investimento_centavos"] is None
        assert j["totais_por_dimensao"]["transferencias_federais_creditadas_centavos"] is None
        ev = j["evidencias_auditadas"]
        payment = ev["pagamentos_a_favorecidos"]
        assert payment["qa_status"] == "em_revisao"
        assert payment["compoe_investimento_executado"] is False
        assert payment["natureza_despesa"] == "nao_classificado"
        assert ev["localizacao_fisica_homologada"] == 0
        sums["pay"] += payment["linhas"]
        sums["amount"] += payment["valor_bruto_nominal_centavos"]
        sums["coords"] += ev["coordenadas_cadastrais_propostas"]
        sums["project_links"] += ev["projetos_obrasgov_com_instrumento_documental"]
        checks += 8
    assert sums == {
        "pay": 28503, "amount": 62728767810,
        "coords": 441, "project_links": 218,
    }
    for sub in ["01", "02", "03", "04"]:
        j = read(root / "subregioes" / f"{sub}.json")
        assert j["subregiao_codigo"] == sub
        checks += 1
    assert len(read(root / "subregioes.json")["subregioes"]) == 4
    for year in range(2008, 2027):
        assert read(root / "anos" / f"{year}.json")["comprovacao_gnd4_pago"] is False
        checks += 1
    project_files = list((root / "projetos").glob("*.json"))
    assert len(project_files) == 218
    for file in project_files:
        p = read(file)
        assert len(p["instrumentos_vinculados"]) == 1
        assert p["instrumentos_vinculados"][0]["qa_vinculo"] == "verificado_chaves_oficiais"
        assert p["localizacao_fisica"]["qa_status"] == "nao_comprovada"
        assert not p["localizacao_fisica"]["pontos"]
        assert p["valores_investimento_pago_centavos"] is None
        assert p["public_release_authorized"] is False
        checks += 6
    return {"technical_checks_passed": checks, "municipios": 34,
            "projetos": 218, "status": "private_qa_only",
            "public_release_authorized": False}
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("root", type=Path)
    args = ap.parse_args()
    print(json.dumps(validate(args.root), ensure_ascii=False))
