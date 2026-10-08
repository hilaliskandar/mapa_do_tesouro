# QA — Gate C RGF taxonomy smoke — Americana 2025

Run: `37729526198`.

## Aquisição

Sentinela: Americana — `3501608`.

- RGF Anexo 01: 173 itens;
- RGF Anexo 05: 140 itens;
- ambos os payloads observados e não vazios.

## Anexo 01 — conceitos legais observados

- DTP: `DespesaComPessoalTotal`, coluna `Valor` = R$ 533.730.391,12;
- RCL ajustada: `ReceitaCorrenteLiquidaAjustada`, coluna `Valor` = R$ 1.454.899.326,74;
- percentual DTP/RCL: `DespesaComPessoalTotal`, coluna `% sobre a RCL Ajustada` = 36,69%.

Os três valores reproduzem a base TIC-TIM 30 já validada.

## Anexo 05 — regra de seleção

A linha canônica é `TOTAL DOS RECURSOS NÃO VINCULADOS (I)`, não o total geral `TOTAL (IV)`.

Para Americana 2025, reproduzem exatamente a base TIC-TIM 30:

- caixa bruta não vinculada: R$ 129.054.745,41;
- RP liquidados anteriores: R$ 1.103.513,24;
- RP liquidados do exercício: R$ 52.469.314,19;
- RP não liquidados anteriores: R$ 53.094,36;
- caixa líquida antes RPNP: R$ 75.428.823,62;
- RP não liquidados do exercício: R$ 9.470.385,18;
- caixa líquida após RPNP: R$ 65.958.438,44.

Para `DemaisObrigacoesFinanceiras`, a API de Americana 2025 não apresenta linha `TOTAL DOS RECURSOS NÃO VINCULADOS (I)`; portanto o valor canônico permanece ausente, coerente com a base validada.

## Decisão

Taxonomia 2025 aprovada para construção do normalizador RGF. Nenhuma carga estadual deve usar soma de sublinhas ou total geral como substituto do recorte não vinculado.
