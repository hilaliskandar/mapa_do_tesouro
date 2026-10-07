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
    assert \'cache: "no-store"\' not in js
