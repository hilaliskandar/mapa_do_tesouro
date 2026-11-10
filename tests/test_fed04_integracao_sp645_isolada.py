"""FED04: isolated 645-row end-to-end publication regression.

This uses synthetic municipal identifiers in a disposable SQLite database.
It does NOT read or modify the canonical SP645 database, R2 or Cloudflare.
"""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from pipeline.build.load_catalog import load_catalog
from pipeline.build.export_state_api_v2 import export_state_api
from pipeline.build.export_regional_api_v2 import export_regional_api

ROOT = Path(__file__).resolve().parents[1]
PROPOSAL = ROOT / "governance/proposals/FED04_VARIAVEIS_DCA_ITR_FUNDEB_CANDIDATAS.yml"
CANDIDATES = {
    "dca_itr_cota_parte_bruta",
    "dca_itr_deducao_fundeb",
    "dca_fundeb_recebido_bruto",
    "dca_fundeb_complementacao_uniao_bruta",
}


def test_fed04_candidates_not_exposed_in_sp645_synthetic_build(tmp_path):
    database = tmp_path / "disposable.sqlite"
    with sqlite3.connect(database) as con:
        for schema in sorted((ROOT / "data/schema").glob("[0-9][0-9][0-9]_*.sql")):
            con.executescript(schema.read_text(encoding="utf-8"))
        con.execute("INSERT INTO universo(universo_id,nome,tipo) "
                    "VALUES ('SP_645','SP synthetic QA','analitico')")
        con.execute("INSERT INTO variavel(variavel_id,nome,grupo,tipo,unidade,definicao) "
                    "VALUES('baseline','Baseline','receitas','conta_oficial','BRL','QA')")
        for i in range(1, 646):
            code = str(3500000 + i)
            con.execute("INSERT INTO municipio(codigo_ibge,nome,uf) VALUES (?,?,?)",
                        (code, f"Fixture {i}", "SP"))
            con.execute("INSERT INTO universo_municipio(universo_id,codigo_ibge) "
                        "VALUES ('SP_645',?)", (code,))
            con.execute("INSERT INTO observacao(codigo_ibge,ano,variavel_id,"
                        "valor_num,status) VALUES (?,2025,'baseline',?,'observado')",
                        (code, float(i)))
    load_catalog(database, [PROPOSAL])
    with sqlite3.connect(database) as con:
        flags = con.execute("SELECT variavel_id,publicavel,ativo FROM variavel "
                            "WHERE variavel_id!='baseline'").fetchall()
        assert {v[0] for v in flags} == CANDIDATES
        assert all(p == 0 and a == 0 for _, p, a in flags)
        for variable in CANDIDATES:
            con.execute("INSERT INTO observacao(codigo_ibge,ano,variavel_id,"
                        "fonte_id,valor_num,status) "
                        "VALUES ('3500001',2025,?,'SICONFI_DCA',100,'observado')",
                        (variable,))
        assert con.execute("SELECT count(*) FROM v_observacao_publicavel").fetchone()[0] == 645
        assert con.execute("SELECT count(*) FROM observacao").fetchone()[0] == 649

    v2 = tmp_path / "v2"
    summary = export_state_api(database, v2)
    assert summary == {"municipalities": 645, "variables": 5, "observations": 645}
    manifest = json.loads((v2 / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["exposed_variable_count"] == 1
    municipal = json.loads((v2 / "municipalities/3500001.json").read_text(encoding="utf-8"))
    assert set(municipal["variables"]) == {"baseline"}
    catalogue = json.loads((v2 / "catalog/variables.json").read_text(encoding="utf-8"))
    availability = {v["variavel_id"]: v["api_available"] for v in catalogue["variables"]}
    assert availability == {"baseline": True, **{k: False for k in CANDIDATES}}

    regional = tmp_path / "regional"
    regional_summary = export_regional_api(database, regional)
    assert regional_summary["universes"] == 1
    assert regional_summary["municipality_universe_contexts"] == 645
    assert regional_summary["variables"] == 1
    regional_context = json.loads(
        (regional / "universes/SP_645/context.json").read_text(encoding="utf-8"))
    assert regional_context["variable_ids"] == ["baseline"]
