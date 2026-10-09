from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_frontend_exposes_universe_selector():
    html = (ROOT / "app" / "static" / "index.html").read_text(encoding="utf-8")
    js = (ROOT / "app" / "static" / "app.js").read_text(encoding="utf-8")

    assert 'id="universe-select"' in html
    assert "Recorte de análise" in html
    assert './data/universes.json' in js
    assert "async function loadUniverse" in js
    assert "state.currentUniverse" in js
    assert "state.dataBase" in js


def test_csv_export_records_selected_universe_in_filename():
    js = (ROOT / "app" / "static" / "app.js").read_text(encoding="utf-8")
    assert "financas_municipais_sp_${state.currentUniverse}_${state.currentYear}_${variable}.csv" in js
