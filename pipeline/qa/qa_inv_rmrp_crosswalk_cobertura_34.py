#!/usr/bin/env python3
"""Audita cobertura RMRP e cria fila de crosswalk sem promover coincidencias a fatos.

Fonte de contratos municipais: dossie com referencias documentais para dois
contratos de Serrana; NAO representa universo de contratos dos 34 municipios.
O verificador NAO estabelece vinculo por igualdade de valor ou municipio.
"""
from __future__ import annotations
from collections import Counter
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GOV = ROOT / "governance"
META = GOV / "INV_RMRP_SIAFEM_752_CONVENIOS_METADADOS_OBJETOS_ORGAOS_2026_11_12.csv"
ANNUAL = GOV / "INV_RMRP_SIAFEM_889_CONVENIO_ANO_EXATO_2026_11_12.csv"
COVERAGE = GOV / "INV_RMRP_SIAFEM_CROSSWALK_COBERTURA_34_MUNICIPIOS_2026_11_12.json"
EVIDENCE = GOV / "INV_RMRP_SERRANA_CROSSWALK_100540_101375_SIAFEM_510101_2026_11_12.json"


def read(path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter=";"))


def main():
    metadata, annual = read(META), read(ANNUAL)
    coverage = json.loads(COVERAGE.read_text(encoding="utf-8"))
    evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    assert len(metadata) == 752 and len(annual) == 889
    keys = {(r["codigo_ibge"], r["numero_convenio_siafem"]) for r in metadata}
    assert len(keys) == 752
    assert len({(r["codigo_ibge"], r["numero_convenio_siafem"], r["ano"]) for r in annual}) == 889
    assert {(r["codigo_ibge"], r["numero_convenio_siafem"]) for r in annual} == keys
    assert len({r["codigo_ibge"] for r in metadata}) == 34

    by_mun = Counter(r["codigo_ibge"] for r in metadata)
    with_obj = Counter(r["codigo_ibge"] for r in metadata if r["estado_extracao"] == "OK")
    assert sum(with_obj.values()) == 747
    assert len(coverage["municipalities"]) == 34
    assert coverage["totals"]["convenios"] == 752
    assert coverage["totals"]["details"] == 747
    assert coverage["totals"]["errors"] == 5
    for row in coverage["municipalities"]:
        code = row["ibge7"]
        assert row["total"] == by_mun[code]
        assert row["detalhes_recuperados"] == with_obj[code]
        assert row["excecoes"] == by_mun[code] - with_obj[code]

    checked = evidence["entries"]
    assert len(checked) == 2
    status = {r["public_instrument"]: r for r in checked}
    assert set(status) == {"100540/2024", "101375/2024"}
    allowed = {
        "100540/2024": ("51010120240419991", "CANDIDATO_FORTE_AINDA_SEM_TERMO_ESTADUAL_COM_CHAVE_CRUZADA"),
        "101375/2024": ("51010120240581081", "CORRESPONDENCIA_DOCUMENTAL_COMPOSTA_ALTA_CONFIANCA_SEM_CHAVE_LITERAL")
    }
    candidate_keys = set()
    for label, (internal, state) in allowed.items():
        item = status[label]
        assert (evidence["geo"]["ibge7"], internal) in keys
        assert item["siafem_number"] == internal
        assert item["status"] == state
        assert item["municipal_contract_url"].startswith("https://")
        assert item["siafem_url"].startswith("https://")
        candidate_keys.add((evidence["geo"]["ibge7"], internal))

    overall = 0
    by_key = Counter()
    for item in annual:
        cents = int(item["valor_liberado_estornado_ano_centavos"])
        overall += cents
        by_key[(item["codigo_ibge"], item["numero_convenio_siafem"])] += cents
    assert overall == 30552102920
    assert sum(by_key[key] for key in candidate_keys) == 93758062
    assert evidence["summary"]["confirmed_exact_number_crosswalks"] == 0
    assert evidence["summary"]["not_additive_to_existing_siafem_30552102920"] is True

    queue = []
    for m in sorted(coverage["municipalities"], key=lambda r: (-r["total"], r["ibge7"])):
        queue.append({
            "codigo_ibge":m["ibge7"], "municipio":m["municipio"],
            "instrumentos_siafem":m["total"],
            "metadados_com_objeto":m["detalhes_recuperados"],
            "detalhes_indisponiveis":m["excecoes"],
            "contratos_estado_examinados_neste_crosswalk":2 if m["ibge7"] == "3551504" else 0,
            "proximo_passo":"Localizar termos e contratos municipais com numero publico, demanda e referencia financeira",
            "nota":"Ausencia de dossie NAO significa ausencia de contrato ou obra"
        })
    result = {
        "status":"QA_PASS_COBERTURA_34_RMRP_SEM_PROMOCAO_AUTOMATICA",
        "fonte_siafem":{"municipios":34,"instrumentos":752,
                         "metadados_com_objeto":747,"falhas_detalhamento":5,
                         "linhas_convenio_ano":889,
                         "total_liberado_centavos":overall},
        "crosswalk_publico_interno":{"chaves_literais_comprovadas":0,
                                   "correspondencias_compostas_alta_confianca":1,
                                   "candidatos_fortes":1,
                                   "instrumentos_sem_dossie_individual_homologado":750,
                                   "valor_dos_2_ja_incluido_no_total_centavos":93758062},
        "fila_municipal":queue,
        "regras":[
            "Somente coincidencia de municipio, objeto, valor ou ano nao homologa vinculo",
            "Correspondencia por evidencias compostas requer fontes independentes identificadas",
            "O codigo unico de processo SIAFEM nao equivale necessariamente ao numero publico do convenio",
            "Nenhum pagamento a contratada nem obra executada e inferido das liberacoes ao municipio",
            "Nao somar subtotal de candidatos ao total ja registrado no SIAFEM",
            "Status da fila nao representa levantamento completo de contratos municipais"
        ]
    }
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("--output", type=Path, required=True)
    args=p.parse_args()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({"status":result["status"],"municipios":34,
                      "instrumentos":752,"alta_confianca":1,"candidato":1,
                      "chaves_literais":0},ensure_ascii=False))


if __name__=="__main__":
    main()
