# Universos territoriais paulistas — composição 2025

Data de referência: 2025.

## Objetivo

Registrar recortes metropolitanos paulistas como universos analíticos sobrepostos no modelo canônico, sem duplicar observações fiscais municipais.

A fonte primária desta versão é o arquivo `Composicao_RM_2025.xlsx`, fornecido pelo usuário, SHA-256 `8034d21968556bc2c8a0ae600ead000aad501bde3ae1eed4ef84b78e726e07d2`.

O `TIC_TIM_30` foi confrontado com o artefato canônico `FINBRA_TIC_TIM_30M_BASE_MULTIFONTES_2013_2025_v0_4.xlsx`, SHA-256 `f51d8615f3742b1d414f1edff67805cac1a10cbc18764b454aab518de9c9e3f1`.

## Universos

| ID | Recorte | Municípios |
|---|---|---:|
| RM_SAO_PAULO | Região Metropolitana de São Paulo | 39 |
| RM_BAIXADA_SANTISTA | Região Metropolitana da Baixada Santista | 9 |
| RM_CAMPINAS | Região Metropolitana de Campinas | 20 |
| RM_VALE_PARAIBA_LITORAL_NORTE | Região Metropolitana do Vale do Paraíba e Litoral Norte | 39 |
| RM_SOROCABA | Região Metropolitana de Sorocaba | 27 |
| RM_RIBEIRAO_PRETO | Região Metropolitana de Ribeirão Preto | 34 |
| RM_SAO_JOSE_RIO_PRETO | Região Metropolitana de São José do Rio Preto | 37 |
| RM_JUNDIAI | Região Metropolitana de Jundiaí | 7 |
| RM_PIRACICABA | Região Metropolitana de Piracicaba | 24 |
| AU_FRANCA | Aglomeração Urbana de Franca | 19 |

A união contém 255 municípios distintos. Não há sobreposição municipal entre esses dez recortes na composição fornecida.

## Relação com TIC-TIM 30

O cruzamento por código IBGE demonstra a identidade:

`TIC_TIM_30 = RM_CAMPINAS ∪ RM_JUNDIAI ∪ {Caieiras, Francisco Morato, Franco da Rocha}`.

Assim:

- RM_CAMPINAS: 20/20 municípios estão no TIC_TIM_30;
- RM_JUNDIAI: 7/7 municípios estão no TIC_TIM_30;
- RM_SAO_PAULO: 3/39 municípios estão no TIC_TIM_30;
- os três municípios da RMSP são Caieiras, Francisco Morato e Franco da Rocha;
- os três pertencem à Sub-região Norte da RMSP na planilha-fonte;
- os demais sete recortes não têm município no TIC_TIM_30;
- todos os 30 municípios do TIC_TIM_30 pertencem a exatamente um desses três recortes metropolitanos na composição de 2025.

A decomposição acima é descritiva. Ela não substitui `TIC_TIM_30` como universo de projeto.

## Regra de modelagem

O mesmo município pode pertencer simultaneamente a `SP_645`, `TIC_TIM_30` e a um universo metropolitano. Os valores fiscais permanecem armazenados uma única vez em `observacao`. O recorte analítico é definido por `universo_municipio`.

Percentis, estatísticas de janela, tipologias, marcadores e pares devem ser recalculados para o universo selecionado, porque a posição relativa depende do conjunto de comparação.

## Artefatos

- `data/catalogs/territorial_universes_sp_2025.yml`: definição canônica e códigos IBGE;
- `data/catalogs/territorial_overlap_tictim30_2025.csv`: síntese de sobreposição;
- `data/catalogs/tictim30_territorial_decomposition_2025.csv`: decomposição dos 30 municípios;
- `pipeline/ingest/import_territorial_universes.py`: importação idempotente para `universo` e `universo_municipio`.

A planilha derivada completa, com legislação, datas e sub-regiões por município, permanece como artefato de auditoria desta análise.
