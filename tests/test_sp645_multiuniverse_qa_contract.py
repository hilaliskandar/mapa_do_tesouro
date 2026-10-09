from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_sp645_pages_qa_requires_multiuniverse_contract():
    qa = (ROOT / "deployment" / "qa_sp645_pages.py").read_text(encoding="utf-8")
    for universe_id, count in (
        ("SP_645", 645),
        ("TIC_TIM_30", 30),
        ("CIDADES_MEDIAS", 33),
        ("RM_SAO_PAULO", 39),
        ("RM_CAMPINAS", 20),
        ("RM_JUNDIAI", 7),
        ("AU_FRANCA", 19),
    ):
        assert f'"{universe_id}": {count}' in qa
    assert "universes.json" in qa
    assert 'id="universe-select"' in qa
    assert "loadUniverse" in qa
