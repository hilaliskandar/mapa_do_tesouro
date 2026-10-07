import json
from pathlib import Path

from pipeline.build.export_documentation import export_documentation
from pipeline.build.init_db import initialize_database
from pipeline.build.load_catalog import load_catalog
from pipeline.build.load_documentation import load_documentation


def test_documentation_exports_static_contract(tmp_path):
    db = tmp_path / "x.sqlite"
    out = tmp_path / "public" / "data"
    initialize_database(db)
    load_catalog(db)
    load_documentation(db, strict=True)

    result = export_documentation(db, out)
    assert result["variables"] == 75
    assert result["methodology_sections"] == 9

    item = json.loads(
        (out / "catalog" / "variables" / "investimento_pct_receita_corrente.json")
        .read_text(encoding="utf-8")
    )
    assert item["formula_publica"] == "Investimentos liquidados ÷ Receita Corrente bruta"
    assert item["como_ler"]
    assert item["limitacoes"]
    assert item["regra_ausencia"]
    assert item["url_fonte"]

    method = json.loads(
        (out / "methodology" / "indicadores_legais.json")
        .read_text(encoding="utf-8")
    )
    assert "RGF" in method["corpo_markdown"]
