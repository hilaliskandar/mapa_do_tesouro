#!/usr/bin/env python3
"""QA de colisoes potenciais de IDs do SIAFEM na amostra da RMRP.

Normalizacao para detectar anomalias NAO autoriza mesclar registros nem valores.
Conferencia sobre snapshots CSV versionados e dossie de auditoria documentado.
"""
import csv
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] / "governance"
META = ROOT / "INV_RMRP_SIAFEM_752_CONVENIOS_METADADOS_OBJETOS_ORGAOS_2026_11_12.csv"
ANUAL = ROOT / "INV_RMRP_SIAFEM_889_CONVENIO_ANO_EXATO_2026_11_12.csv"
EVID = ROOT / "INV_RMRP_BATATAIS_COLISAO_IDS_SIAFEM_5128032447861_2026_11_12.json"


def records(path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter=";"))


def normalized(value):
    # Mantem letras e digitos; NAO elimina zeros a esquerda ou a direita.
    return re.sub(r"[^A-Z0-9]", "", value.upper())


def main():
    m = records(META)
    a = records(ANUAL)
    d = json.loads(EVID.read_text(encoding="utf-8"))
    assert len(m) == 752 and len(a) == 889
    assert len({(x["codigo_ibge"], x["numero_convenio_siafem"]) for x in m}) == 752
    assert sum(int(x["valor_liberado_estornado_ano_centavos"]) for x in a) == 30552102920

    groups = defaultdict(list)
    for x in m:
        groups[(x["codigo_ibge"], normalized(x["numero_convenio_siafem"]))].append(x)
    collisions = {k: v for k, v in groups.items() if len(v) > 1}
    expected = ("3505906", "512803244786119")
    assert len(collisions) == 1, f"Novas colisoes exigem auditoria: {list(collisions)}"
    assert set(collisions) == {expected}
    ids = {x["numero_convenio_siafem"] for x in collisions[expected]}
    assert ids == {"5128032447861-19", "5128032447861\\19"}
    assert d["normalized_group"] == "|".join(expected)
    assert {x["id"] for x in d["members"]} == ids

    by_id = defaultdict(list)
    for x in a:
        if x["codigo_ibge"] == expected[0]:
            by_id[x["numero_convenio_siafem"]].append(x)
    amounts = {
        key: sum(int(x["valor_liberado_estornado_ano_centavos"]) for x in by_id[key])
        for key in ids
    }
    assert amounts == {"5128032447861-19": 27314707, "5128032447861\\19": 38500000}
    assert len(by_id["5128032447861-19"]) == 1
    assert len(by_id["5128032447861\\19"]) == 2
    assert d["amounts"]["group_aggregate_cents"] == sum(amounts.values()) == 65814707
    assert d["amounts"]["amount_under_review_cents"] == 38500000
    assert d["decision"]["no_merge"] and d["decision"]["no_deduction"]
    assert d["decision"]["financial_total_remains_source_gross"]
    assert d["members"][0]["http"] == 200 and d["members"][1]["http"] == 500
    assert d["amounts"]["source_rmrp_total_centavos"] == 30552102920
    public = d["public_instrument"]
    assert public["convenio_publico"] == "101/2019"
    assert public["administrative_process"] == "DETRAN 2447861/2019"
    assert public["state_total_foreseen_centavos"] == 68930177
    assert public["signed"] == "2019-12-18"
    assert d["amounts"]["difference_original_public_value_vs_sum_siafem_centavos"] == (
        public["state_total_foreseen_centavos"] - sum(amounts.values())
    ) == 3115470
    assert d["decision"]["possible_shared_legal_instrument"]
    assert d["decision"]["exact_crosswalk_documented"] is False
    assert d["decision"]["accounting_duplicate_proved"] is False
    assert d["decision"]["new_classification"] == (
        "PROVAVEL_MESMO_PROCESSO_DETRAN_2447861_MAS_LANCAMENTOS_DISTINTOS_NAO_CONCILIADOS"
    )

    print(json.dumps({
        "status": "QA_PASS_SIAFEM_ID_COLLISION_UNRESOLVED",
        "unique_raw_ids": 752,
        "punctuation_normalized_collisions": 1,
        "affected_raw_ids": sorted(ids),
        "amount_under_review_centavos": 38500000,
        "source_total_unchanged_centavos": 30552102920,
        "decision": "NEITHER_MERGE_NOR_DEDUCT_WITHOUT_DOCUMENTARY_PROOF"
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
