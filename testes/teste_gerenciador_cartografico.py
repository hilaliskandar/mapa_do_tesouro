"""Testes do gerenciador cartografico sem depender de acesso a internet."""

from __future__ import annotations

import json
from pathlib import Path

from nucleo.gerenciador_cartografico import (
    ConfiguracaoCartografica,
    GerenciadorCartografico,
)


def criar_geojson_teste(caminho: Path) -> None:
    conteudo = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"id": "3509502", "name": "Campinas"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [-47.2, -23.0],
                            [-46.8, -23.0],
                            [-46.8, -22.7],
                            [-47.2, -22.7],
                            [-47.2, -23.0],
                        ]
                    ],
                },
            }
        ],
    }
    caminho.write_text(json.dumps(conteudo), encoding="utf-8")


def teste_carrega_geojson_local_e_seleciona_municipio(tmp_path: Path) -> None:
    arquivo = tmp_path / "municipios.geojson"
    criar_geojson_teste(arquivo)
    configuracao = ConfiguracaoCartografica(
        provedor="geojson_local",
        arquivo=arquivo,
        campo_codigo="id",
        campo_nome="name",
    )
    gerenciador = GerenciadorCartografico(configuracao)

    recorte = gerenciador.selecionar_municipios(["3509502"])

    assert len(recorte) == 1
    assert recorte.iloc[0]["name"] == "Campinas"
    assert len(gerenciador.calcular_hash(arquivo)) == 64


def teste_rejeita_arquivo_que_nao_e_feature_collection(tmp_path: Path) -> None:
    arquivo = tmp_path / "invalido.geojson"
    arquivo.write_text(json.dumps({"type": "Feature"}), encoding="utf-8")
    configuracao = ConfiguracaoCartografica(
        provedor="geojson_local",
        arquivo=arquivo,
        campo_codigo="id",
        campo_nome="name",
    )
    gerenciador = GerenciadorCartografico(configuracao)

    try:
        gerenciador.carregar_malha()
    except ValueError as erro:
        assert "FeatureCollection" in str(erro)
    else:
        raise AssertionError("Era esperado erro de validacao do GeoJSON.")
