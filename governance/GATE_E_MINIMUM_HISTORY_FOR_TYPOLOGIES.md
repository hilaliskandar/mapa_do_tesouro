# Gate E — mínimo histórico para tipologias e pares SP645

## Problema

As tipologias vigentes exigem pelo menos três anos observados por dimensão. Os seis marcadores dos pares são base tributária, investimento, gasto territorial, pessoal, dívida e liquidez. Os pares exigem pelo menos quatro dimensões comparáveis.

## Escopo mínimo

A série DCA estadual 2013–2025 já fornece base tributária e investimento. Para alcançar quatro marcadores comparáveis com uma janela trienal, basta acrescentar pessoal e dívida em 2023 e 2024, usando 2025 como terceiro ano.

Serão coletados somente:

- RGF Anexo 01 — DTP, RCL legal e percentual oficial;
- RGF Anexo 02 — dívida consolidada, DCL e percentuais oficiais.

Não serão coletados neste gate RREO histórico nem RGF Anexo 05 histórico.

## Validação local-first

O Datalake CAPAG local foi examinado antes da coleta. Ele contém Dívida Consolidada e RCL bruta em 2023–2025, mas não contém o denominador ou percentual oficial usado pelo RGF02. A fórmula simplificada 100 × DC / RCL bruta não reproduz o percentual oficial 2025; por isso não será usada.

## Execução

A coleta 2023–2024 é shardada em cinco lotes por ano, com paralelismo máximo de dois jobs. Cada shard consulta apenas A01 e A02, preserva payload vazio e gera CSV normalizado.

Após os dez shards, uma etapa final consolida exatamente 1.290 chaves município-ano, calcula cobertura por variável e produz hash.

## Regra de saída

Tipologias e pares SP645 só poderão usar essa série depois de:

1. cobertura por ano auditada;
2. paridade histórica dos municípios TIC-TIM 30 aprovada;
3. pelo menos três anos válidos por dimensão;
4. manutenção explícita de ausência como ausência.
