import json

import pipeline.acquire.siconfi_rgf_history_a01 as module
from pipeline.sources.siconfi import FetchResult


class FakeClient:
    def __init__(self, min_interval):
        self.min_interval = min_interval

    def fetch_rgf(self, **kwargs):
        return FetchResult(
            items=[
                {
                    "cod_conta": "ReceitaCorrenteLiquidaAjustada",
                    "conta": "= RECEITA CORRENTE LÍQUIDA AJUSTADA PARA CÁLCULO DOS LIMITES DA DESPESA COM PESSOAL (VII) = (IV - V - VI)",
                    "coluna": "Valor",
                    "valor": 20,
                },
                {
                    "cod_conta": "DespesaComPessoalTotal",
                    "conta": "DESPESA TOTAL COM PESSOAL - DTP (VIII) = (IIIa + IIIb)",
                    "coluna": "Valor",
                    "valor": 10,
                },
                {
                    "cod_conta": "DespesaComPessoalTotal",
                    "conta": "DESPESA TOTAL COM PESSOAL - DTP (VIII) = (IIIa + IIIb)",
                    "coluna": "% sobre a RCL Ajustada",
                    "valor": 50,
                },
            ],
            pages=1,
            request_count=1,
        )


def test_a01_history_shard(tmp_path, monkeypatch):
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

    result = module.acquire_a01_shard(
        geo,
        2023,
        tmp_path / "raw",
        tmp_path / "normalized.csv",
        min_interval=0,
        expected_municipalities=2,
    )
    assert result["municipalities_requested"] == 2
    assert result["completed_now"] == 2
    assert result["failed"] == []
    assert result["normalization"]["rows"] == 2
    assert result["normalization"]["coverage"]["rgf_despesa_total_pessoal"] == 2
    assert result["normalization"]["coverage"]["rgf_rcl_denominador_legal"] == 2
    assert result["normalization"]["coverage"]["rgf_dtp_percentual_rcl"] == 2
