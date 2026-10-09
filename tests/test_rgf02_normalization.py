from pipeline.normalize.rgf02 import normalize_long


def test_rgf02_normalization(tmp_path):
    source = tmp_path / "long.csv"
    source.write_text(
        "ano,cod_ibge,municipio,cod_conta,conta,coluna,valor,populacao,fonte_url,fonte\n"
        "2025,3501608,Americana,DividaConsolidada,DC,Até o 3º Quadrimestre,100,10,u,SICONFI_API\n"
        "2025,3501608,Americana,DividaConsolidadaLiquida,DCL,Até o 3º Quadrimestre,80,10,u,SICONFI_API\n"
        "2025,3501608,Americana,PercentualDaDCSobreARCL,DC pct,Até o 3º Quadrimestre,10,10,u,SICONFI_API\n"
        "2025,3501608,Americana,RGF2ReceitaCorrenteLiquida,RCL,Até o 3º Quadrimestre,1000,10,u,SICONFI_API\n",
        encoding="utf-8",
    )
    output = tmp_path / "out.csv"
    manifest = tmp_path / "manifest.json"
    result = normalize_long(source, output, manifest)
    assert result["rows"] == 1
    assert result["conflicts"] == []
    assert result["coverage"]["rgf02_divida_consolidada"] == 1
    assert result["coverage"]["rgf02_divida_consolidada_liquida"] == 1
    assert result["coverage"]["rgf02_dc_percentual_rcl"] == 1
    assert result["coverage"]["rgf02_rcl_bruta"] == 1



def test_rgf02_normalization_preserves_unobserved_universe_rows(tmp_path):
    source = tmp_path / "rgf02.csv"
    source.write_text(
        "ano,cod_ibge,municipio,cod_conta,conta,coluna,valor,populacao,fonte_url,fonte\n"
        "2025,3500105,A,DividaConsolidada,Dívida,Até o 3º Quadrimestre,30,100,url,SICONFI_API\n",
        encoding="utf-8",
    )
    geo = tmp_path / "sp.json"
    geo.write_text(
        '{"features":['
        '{"properties":{"id":"3500105","name":"A"}},'
        '{"properties":{"id":"3500204","name":"B"}}'
        ']}',
        encoding="utf-8",
    )
    output = tmp_path / "normalized.csv"
    manifest = tmp_path / "manifest.json"

    result = normalize_long(
        source,
        output,
        manifest,
        universe_geojson=geo,
        year=2025,
    )

    assert result["rows"] == 2
    rows = output.read_text(encoding="utf-8").splitlines()
    assert any(line.startswith("3500204,2025,") for line in rows)
