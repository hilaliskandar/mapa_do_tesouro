import json

import pipeline.acquire.siconfi_rgf_state as module
from pipeline.sources.siconfi import FetchResult


class FakeClient:
    def __init__(self, min_interval):
        self.min_interval = min_interval

    def fetch_rgf(self, **kwargs):
        annex = kwargs["annex"]
        if annex == "RGF-Anexo 01":
            items = [
                {
                    "cod_conta": "DespesaComPessoalTotal",
                    "conta": "DESPESA TOTAL COM PESSOAL - DTP (VI) = (IIIa + IIIb)",
                    "coluna": "Valor",
                    "valor": 10,
                },
                {
                    "cod_conta": "ReceitaCorrenteLiquidaAjustada",
                    "conta": "= RECEITA CORRENTE LÍQUIDA AJUSTADA PARA CÁLCULO DOS LIMITES DA DESPESA COM PESSOAL (V)",
                    "coluna": "Valor",
                    "valor": 20,
                },
                {
                    "cod_conta": "DespesaComPessoalTotal",
                    "conta": "DESPESA TOTAL COM PESSOAL - DTP (VI) = (IIIa + IIIb)",
                    "coluna": "% sobre a RCL Ajustada",
                    "valor": 50,
                },
            ]
        else:
            items = [
                {
                    "cod_conta": "DisponibilidadeDeCaixaBruta",
                    "conta": "TOTAL DOS RECURSOS NÃO VINCULADOS (I)",
                    "coluna": "DISPONIBILIDADE DE CAIXA BRUTA (a)",
                    "valor": 30,
                }
            ]
        return FetchResult(items=items, pages=1, request_count=1)


def test_rgf_state_acquisition(tmp_path, monkeypatch):
    geo = tmp_path / "sp.json"
    geo.write_text(
        json.dumps(
            {
                "features": [
                    {"properties": {"id": "3500105", "name": "A"}},
                    {"properties": {"id": "3500204", "name": "B"}},
                ]
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(module, "SiconfiClient", FakeClient)

    result = module.acquire_state_year(
        geo,
        2025,
        tmp_path / "raw",
        tmp_path / "normalized.csv",
        min_interval=0,
        expected_municipalities=2,
    )

    assert result["municipalities_requested"] == 2
    assert result["expected_raw_files"] == 4
    assert result["completed_now"] == 4
    assert result["failed"] == []
    assert result["normalization"]["rows"] == 2
    assert result["normalization"]["issues"] == 0
    assert result["normalization"]["coverage"]["rgf_despesa_total_pessoal"] == 2



def test_rgf_state_supports_indexed_shard(tmp_path, monkeypatch):
    geo = tmp_path / "sp.json"
    geo.write_text(
        json.dumps(
            {
                "features": [
                    {"properties": {"id": "3500105", "name": "A"}},
                    {"properties": {"id": "3500204", "name": "B"}},
                    {"properties": {"id": "3500303", "name": "C"}},
                ]
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(module, "SiconfiClient", FakeClient)

    result = module.acquire_state_year(
        geo,
        2025,
        tmp_path / "raw",
        tmp_path / "normalized.csv",
        min_interval=0,
        start_index=1,
        limit_codes=1,
        expected_municipalities=3,
    )

    assert result["start_index"] == 1
    assert result["municipalities_requested"] == 1
    assert result["expected_raw_files"] == 2
