#!/usr/bin/env python3
"""QA conservador de metadados oficiais e candidatos SIAFEM/Obrasgov.

Nunca atribuir desembolso, obra ou executor a um instrumento por título,
semelhança temática, município ou fontes orçamentárias genéricas.
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
G = ROOT / "governance"
META = G / "INV_RMRP_SIAFEM_752_CONVENIOS_METADADOS_OBJETOS_ORGAOS_2026_11_12.csv"
CAND = G / "INV_RMRP_SIAFEM_OBRASGOV_17_PARES_CANDIDATOS_NAO_HOMOLOGADOS_2026_11_12.csv"
OBRAS = ROOT / "app/static/data/api/v3/investimentos/rmrp/obrasgov-triagem-espacial.json"
ANUAL = G / "INV_RMRP_SIAFEM_889_CONVENIO_ANO_EXATO_2026_11_12.csv"
DETALHES = G / "INV_RMRP_OBRASGOV_4_PROJETOS_CANDIDATOS_DETALHE_API_2026_11_12.json"
MUNICIPAIS = G / "INV_RMRP_OBRASGOV_4_PROJETOS_DOCUMENTOS_MUNICIPAIS_FEDERAIS_2026_11_12.csv"
SERRANA_CONFLITO = G / "INV_RMRP_SERRANA_117_2024_CONFLITO_REPASSES_952819_952816_2026_11_12.json"
PB_STZ = G / "INV_RMRP_SERTAOZINHO_004_2025_953043_PROJETO_BASICO_EVIDENCIA_2026_11_12.json"
ESTADOS = {
    "CANDIDATO_SEM_CHAVE_DOCUMENTAL": 10,
    "LOCALIZACOES_DISTINTAS": 1,
    "OBJETOS_DISTINTOS": 4,
    "DIVERGENCIA_TERRITORIAL": 2,
}


def read(path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter=";"))


def main():
    meta, cand, ano = read(META), read(CAND), read(ANUAL)
    obra = {x["id"]: x for x in json.loads(OBRAS.read_text(encoding="utf-8"))["items"]}
    ids = {(x["codigo_ibge"], x["numero_convenio_siafem"]) for x in ano}
    assert len(ids) == 752 and len(ano) == 889
    assert len(meta) == 752 and len(cand) == 17 and len(obra) == 224
    index = {(x["codigo_ibge"], x["numero_convenio_siafem"]): x for x in meta}
    assert len(index) == 752 and set(index) == ids
    ok = [x for x in meta if x["estado_extracao"] == "OK"]
    errors = [x for x in meta if x["estado_extracao"] != "OK"]
    assert len(ok) == 747 and len(errors) == 5
    assert all(x["objeto_oficial"] and x["orgao_concedente"] for x in ok)
    assert all(not x["objeto_oficial"] and not x["orgao_concedente"] for x in errors)
    assert all(x["url_oficial"].startswith(
        "https://www.fazenda.sp.gov.br/TransferenciaVoluntaria/Sistema/Novo/Convenio.aspx")
        for x in meta)

    details = {x["id"]: x for x in json.loads(DETALHES.read_text(encoding="utf-8"))}
    assert len(details) == 4
    municipal = read(MUNICIPAIS)
    assert len(municipal) == 4
    assert {r["id_projeto_obrasgov"] for r in municipal} == set(details)
    expected_federal = {
        "30964.35-52": "953042/2023",
        "30461.35-22": "952816/2023",
        "31536.35-60": "953043/2023",
        "30692.35-17": "",
    }
    for m in municipal:
        oid = m["id_projeto_obrasgov"]
        assert m["instrumento_federal"] == expected_federal[oid]
        assert m["status_vinculo_siafem"] == "NAO_HOMOLOGADO"
        assert m["fonte_1"].startswith("https://") and m["fonte_2"].startswith("https://")
        assert "NAO" in m["status_vinculo_siafem"]
    assert all(m["executor"].startswith("Município de ") for m in municipal)
    pb = json.loads(PB_STZ.read_text(encoding="utf-8"))
    stz = next(x for x in municipal if x["municipio"] == "Sertãozinho")
    assert pb["obrasgov_project_id"] == stz["id_projeto_obrasgov"]
    assert pb["project_basic"]["federal_transfer_agreement"].split("/MCidades")[0] == stz["instrumento_federal"]
    assert stz["status_vinculo_federal"] == "CONFIRMADO_PROJETO_BASICO_MUNICIPAL_953043_2023"
    assert pb["project_basic"]["sha256"] == stz["projeto_basico_sha256"]
    assert pb["archive"]["size_bytes"] == 2888706
    assert len(pb["project_basic"]["streets"]) == 6
    assert pb["project_basic"]["budget_cents"] == (
        pb["project_basic"]["federal_cents"] +
        pb["project_basic"]["municipal_contribution_cents"]
    )
    assert stz["orcamento_projeto_centavos"] == "64204659"
    assert stz["recurso_federal_centavos"] == "57800300"
    assert stz["contrapartida_municipal_centavos"] == "6404359"
    assert pb["qa"]["state_siafem_link"] == "nao_comprovado"
    serrana = next(x for x in municipal if x["municipio"] == "Serrana")
    assert "952819" in serrana["nota"] and "952816" in serrana["nota"]
    assert serrana["revisao_documental"] == "CONTRADICAO_NUMEROS_952819_952816_NO_MESMO_CONTRATO_117_2024"
    assert serrana["status_vinculo_federal"] == "DIVERGENCIA_INSTRUMENTO_ORIGINAL_952819_ADITIVO_952816_NAO_HOMOLOGADO"
    record = json.loads(SERRANA_CONFLITO.read_text(encoding="utf-8"))
    evidence = {e["document"]: e["agreement"] for e in record["chronology"]}
    assert evidence["Contrato 117/2024, Concorrência 014/2024, Processo 135/2024"] == "952819/2023"
    assert evidence["Primeiro aditamento Contrato 117/2024"] == "952816/2023"
    assert record["status"] == "CONTRADICAO_DOCUMENTAL_REQUER_RETIFICACAO_OU_CONTRATO_ASSINADO"
    assert record["siafem_relation"] == "NAO_COMPROVADA"
    assert all(m["status_vinculo_siafem"] == "NAO_HOMOLOGADO" for m in municipal)
    n_details = 0
    seen, states = set(), {x: 0 for x in ESTADOS}
    for r in cand:
        key = (r["codigo_ibge"], r["convenio_siafem"], r["id_projeto_obrasgov"])
        assert key not in seen
        seen.add(key)
        source = index[(r["codigo_ibge"], r["convenio_siafem"])]
        project = obra[r["id_projeto_obrasgov"]]
        assert source["estado_extracao"] == "OK"
        assert source["objeto_oficial"] == r["objeto_siafem"]
        assert source["orgao_concedente"] == r["orgao_concedente_siafem"]
        assert source["url_oficial"] == r["url_siafem"]
        assert project["nome"] == r["projeto_obrasgov"]
        assert project["organizacao"] == r["orgao_responsavel_obrasgov"]
        assert project["estado_geo"] == "MUNICIPIO_CONFIRMADO_POR_POLIGONO"
        assert len(project["municipios_intersecao"]) == 1
        assert project["municipios_intersecao"][0]["code"] == r["codigo_ibge"]
        assert r["chave_documental_comum"] == "NAO_ENCONTRADA"
        assert r["vinculo_financeiro_confirmado"] == "NAO"
        if r["id_projeto_obrasgov"] in details:
            item = details[r["id_projeto_obrasgov"]]
            assert item["project"]["http"] == 200
            assert item["project"]["total_items"] == 1
            assert item["contracts"]["total_items"] == 0
            info = item["project"]["data"][0]
            executors = "|".join(x["organizacao_executor"] for x in info.get("executores", []))
            repassadores = "|".join(x["organizacao_repassador"] for x in info.get("repassadores", []))
            commitments = "|".join(x["nr_empenho"] for x in item["commitments"]["data"]
                                   if x.get("nr_empenho"))
            assert r["executor_obrasgov_api"] == executors
            assert r["repassador_obrasgov_api"] == repassadores
            assert r["empenho_federal_obrasgov"] == commitments
            assert r["contratos_retornados_api"] == "0"
            assert r["status_confirmacao"] == (
                "EXECUTOR_MUNICIPAL_FONTE_FEDERAL_SEM_VINCULO_ESTADUAL"
            )
            assert "MUNICIPIO DE" in executors
            assert "MINISTÉRIO DAS CIDADES" in repassadores
            n_details += 1
        else:
            assert r["status_confirmacao"] == "NAO_CONSULTADO_API_AMPLIADA"
            assert not r["executor_obrasgov_api"]
        assert r["estado_triagem"] in states
        states[r["estado_triagem"]] += 1

    assert states == ESTADOS, (states, ESTADOS)
    assert n_details == 10
    print(json.dumps({
        "status": "QA_PASS_VINCULOS_NAO_CONFIRMADOS",
        "convenios": 752, "metadados": 747, "falhas_detalhamento": 5,
        "pares": 17, "classes": states, "vinculos_financeiros_homologados": 0,
        "unidade_analitica": "instrumento e projeto separados",
        "projetos_api_ampliada": 4, "pares_api_ampliada": 10
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
