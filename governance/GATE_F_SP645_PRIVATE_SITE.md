# Gate F — build privado do site SP645

## Objetivo

Produzir um artefato navegável estadual para QA sem promover dados SP645 ao site público.

## Entradas canônicas

- histórico de tipologias 2021–2025: `SP645_TYPOLOGY_INPUT_2021_2025.xlsx`;
- base multifuentes 2025: `FINBRA_SP645_BASE_MULTIFONTES_2025_GATE_C.xlsx`;
- indicadores Gate D 2025: usados como referência independente de paridade;
- cartografia web: `geojs-35-mun.json` pinada no commit canônico.

## Estratégia

O workbook do build contém:

- seis indicadores históricos necessários às tipologias em 2021–2024;
- a base multifuentes completa em 2025;
- os indicadores anuais derivados são recalculados apenas para 2025.

Assim, o cálculo anual de 2025 não sobrescreve as séries históricas já aprovadas.

## Critérios obrigatórios

O artifact só é aceito se:

- município_count = 645;
- anos = 2021–2025;
- geometria = 645 feições;
- tipologias observadas = 645 / 645 / 56 / 505 / 439 / 505 / 0;
- marcadores observados = 645 / 645 / 56 / 505 / 439 / 0;
- 440 municípios elegíveis a pares;
- 1.320 posições prioritárias;
- CAPAG observada em 645/645;
- todos os valores disponíveis dos 25 indicadores 2025 forem iguais ao Gate D, respeitando escala percentual;
- `n.d.` em indicador numérico CAPAG for tratado como ausência esperada, sem conversão para zero; `capag=n.d.` permanece categoria textual oficial.

## Publicação

Este workflow gera apenas artifact privado no GitHub Actions.

Não faz deploy em Cloudflare Pages e não altera produção nem o alias `preview`.

Um preview navegável separado somente poderá ser criado após a aprovação deste build e da regressão contra TIC-TIM 30.
