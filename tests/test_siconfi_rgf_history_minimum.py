import csv
import json

import pipeline.acquire.siconfi_rgf_history_minimum as module
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
                    "cod_conta": "DividaConsolidada",
                    "coluna": "Até o 3º Quadrimestre",
                    "valor": 5,
                },
                {
                    "cod_conta": "DividaConsolidadaLiquida",
                    "coluna": "Até o 3º Quadrimestre",
                    "valor": 4,
                },
                {
                    "cod_conta": "PercentualDaDCSobreARCL",
                    "coluna": "Até o 3º Quadrimestre",
                    "valor": 25,
                },
                {
                    "cod_conta": "PercentualDaDCLSobreARCL",
                    "coluna": "Até o 3º Quadrimestre",
                    "valor": 20,
                },
            ]
        return FetchResult(items=items, pages=1, request_count=1)


def test_history_shard(tmp_path, monkeypatch):
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

    output = tmp_path / "history.csv"
    result = module.acquire_history_shard(
        geo,
        2024,
        tmp_path / "raw",
        output,
        start_index=1,
        limit_codes=1,
        min_interval=0,
        expected_municipalities=2,
    )

    rows = list(csv.DictReader(output.open(encoding="utf-8")))
    assert result["municipalities_requested"] == 1
    assert result["expected_raw_files"] == 2
    assert result["failed"] == []
    assert rows[0]["cod_ibge"] == "3500204"
    assert rows[0]["rgf_dtp_percentual_rcl"] == "50.0"
    assert rows[0]["rgf02_dc_percentual_rcl"] == "25.0"
