#!/usr/bin/env python3
"""Testes sem rede do gate de extracao RMJ: cenarios positivo e negativo."""
import csv
import json
import pathlib
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import qa_tcesp_2023_2024 as qa


def read_rows(folder):
    with (folder / "controle_conciliacao.csv").open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter=";"))


def fixture(folder):
    for year in qa.YEARS:
        for city in qa.CITIES:
            (folder / f"{city}_{year}.json").write_text(json.dumps({
                "slug": city, "year": year, "bad_values": 0, "rows": 100,
                "totals_44_by_type": {"Valor Liquidado": 1234.56}
            }), encoding="utf-8")


def test_positive():
    with tempfile.TemporaryDirectory() as directory:
        folder = pathlib.Path(directory)
        fixture(folder)
        assert qa.main(folder) == 0
        rows = read_rows(folder)
        assert len(rows) == 14
        assert all(r["situacao_extracao"] == "OK" for r in rows)
        assert all(r["investimento_liquidado_tcesp_rs"] == "1234.56" for r in rows)
        assert all(r["investimento_liquidado_dca_rs"] == "" for r in rows)
        assert all(r["situacao_conciliacao"] == "PENDENTE_DCA" for r in rows)
        summary = json.loads((folder / "qa_summary.json").read_text())
        assert summary["extraidos_com_sucesso"] == 14


def test_negative():
    with tempfile.TemporaryDirectory() as directory:
        folder = pathlib.Path(directory)
        fixture(folder)
        (folder / "jundiai_2024.json").unlink()
        target = folder / "jarinu_2023.json"
        data = json.loads(target.read_text())
        data["bad_values"] = 1
        target.write_text(json.dumps(data))
        target = folder / "louveira_2024.json"
        data = json.loads(target.read_text())
        data["slug"] = "municipio-errado"
        target.write_text(json.dumps(data))
        (folder / "jundiai_2024.stderr").write_text("Erro de rede demonstrativo")
        assert qa.main(folder) == 1
        rows = read_rows(folder)
        failures = [r for r in rows if r["situacao_extracao"] == "ERRO"]
        assert len(failures) == 3
        assert any("Erro de rede demonstrativo" in r["diagnostico_extracao"] for r in failures)
        assert all(r["situacao_conciliacao"] == "PENDENTE_DCA" for r in rows)


if __name__ == "__main__":
    test_positive()
    test_negative()
    print("QA_RMJ_TESTS_OK")
