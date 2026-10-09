from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATIC = ROOT / "app" / "static"


def test_frontend_has_required_views_and_no_remote_runtime_dependency():
    html = (STATIC / "index.html").read_text(encoding="utf-8")
    js = (STATIC / "app.js").read_text(encoding="utf-8")

    for view in (
        'id="overview"',
        'id="series"',
        'id="compare"',
        'id="map"',
        'id="themes"',
        'id="sources"',
        'id="crosswalk"',
        'id="dictionary"',
        'id="methodology"',
    ):
        assert view in html

    for resource in (
        "./data/metadata.json",
        "./data/municipalities.json",
        "./data/catalog/variables.json",
        "./data/methodology/index.json",
        "./data/maps/municipalities.geojson",
        "./data/references.json",
        "./data/coverage.json",
        "./data/crosswalk.json",
    ):
        assert resource in js

    assert "https://raw.githubusercontent.com" not in js
    assert "api.github.com" not in js
    assert "workers.dev" not in js
    assert "cloudflare" not in js.lower()


def test_frontend_uses_documentation_catalog_for_help():
    js = (STATIC / "app.js").read_text(encoding="utf-8")
    assert "formula_publica" in js
    assert "componentes_publicos" in js
    assert "fonte_publica" in js
    assert "como_ler" in js
    assert "limitacoes" in js
    assert "regra_ausencia" in js
    assert 'data-help="' in js


def test_frontend_does_not_force_no_store_cache():
    js = (STATIC / "app.js").read_text(encoding="utf-8")
    assert 'cache: "no-store"' not in js


def test_tabs_remain_single_row_with_horizontal_overflow():
    css = (STATIC / "styles.css").read_text(encoding="utf-8")
    assert "flex-wrap: nowrap" in css
    assert "overflow-x: auto" in css
    assert "white-space: nowrap" in css



def test_frontend_treats_unclassified_markers_as_missing_coverage():
    js = (STATIC / "app.js").read_text(encoding="utf-8")
    assert 'item.status === "observado"' in js
    assert "marcadores classificáveis por cobertura suficiente" in js
    assert "são necessários pelo menos 4" in js
    assert "observedMarkerCount < 4" in js



def test_frontend_exports_current_annual_slice_as_csv():
    html = (STATIC / "index.html").read_text(encoding="utf-8")
    js = (STATIC / "app.js").read_text(encoding="utf-8")

    assert 'id="export-csv"' in html
    assert "function exportCurrentSliceCsv()" in js
    assert '["codigo_ibge", "municipio", "ano", "variavel_id", "valor", "status"]' in js
    assert 'entry.status || "ausente"' in js
    assert "new Blob" in js
    assert "URL.createObjectURL" in js



def test_frontend_exposes_review_status_in_coverage():
    js = (STATIC / "app.js").read_text(encoding="utf-8")
    assert "<th>Em revisão</th>" in js
    assert "item.em_revisao || 0" in js
