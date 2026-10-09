# Diagnóstico — suplemento local CAPAG para lacunas RGF 2025

Data: 2026-10-08.

## Objetivo

Qualificar as lacunas da carga estadual RGF Anexos 01/05 sem imputação automática e antes de qualquer nova consulta externa.

Fonte estadual observada:

- run RGF SP645 2025: `37732303043`;
- CSV normalizado: SHA-256 `9f3ced721fa2c767d24cdec8e464215b30932e820e01601f24bac9b1e76486ba`.

Fonte local suplementar:

- `capag-municipios-posicao-2026-set.xlsx`;
- aba `Datalake`;
- SHA-256 `1b1379a5a531920223f1d448be155b70f51eb50180d8c819f1b7da3575a8eb11`.

## Paridade dos campos semanticamente idênticos

| Variável | API observada | API ausente | CAPAG observado | Lacunas API com valor local | Restam sem valor local | Sobreposição comparada | Divergências > R$ 0,01 | Cobertura potencial |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Caixa bruta não vinculada | 526 | 119 | 635 | 109 | 10 | 526 | 0 | 635/645 — 98,45% |
| Demais obrigações não vinculadas | 93 | 552 | 108 | 15 | 537 | 93 | 0 | 108/645 — 16,74% |
| RP não liquidados anteriores não vinculados | 411 | 234 | 490 | 79 | 155 | 411 | 0 | 490/645 — 75,97% |
| RP liquidados anteriores não vinculados | 404 | 241 | 478 | 74 | 167 | 404 | 0 | 478/645 — 74,11% |
| RP liquidados do exercício não vinculados | 412 | 233 | 501 | 89 | 144 | 412 | 0 | 501/645 — 77,67% |

Total de células ausentes da API com valor local semanticamente equivalente: **366**.

Total de valores sobrepostos usados na validação de equivalência: **1.846**.

Todos os valores sobrepostos coincidem centavo a centavo.

## Campos sem equivalente local seguro

O snapshot CAPAG não fornece equivalente canônico para:

- DTP legal do RGF Anexo 01;
- RCL ajustada para limite de pessoal;
- percentual oficial DTP/RCL;
- caixa líquida antes de RPNP no recorte não vinculado;
- RP não liquidados do exercício no recorte não vinculado;
- caixa líquida após RPNP no recorte não vinculado.

Esses campos não serão preenchidos por aproximação.

## Decisão metodológica

Os cinco campos equivalentes do Anexo 05 são elegíveis para uma camada suplementar **fill-only**, preservando:

- valor original da API quando observado;
- valor CAPAG apenas quando a API estiver vazia;
- fonte do valor por célula;
- posição do snapshot;
- nenhuma alteração do snapshot RGF bruto/canônico observado.

Antes de criar essa composição, as lacunas do Anexo 01 serão testadas quanto à periodicidade semestral.
