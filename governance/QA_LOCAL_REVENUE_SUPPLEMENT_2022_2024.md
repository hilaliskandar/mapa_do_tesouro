# QA — suplemento local de receitas 2022 e 2024

Data: 2026-10-07.

## Objetivo

Validar empiricamente o uso da planilha local `Receitas 2022-2025.xlsx` como complemento fill-only dos snapshots anuais FINBRA/DCA, sem consulta externa.

## 2022 — Guaraçaí

Código IBGE: `3517802`.

O snapshot anual de 2022 não contém Guaraçaí no Anexo I-C, embora I-D e I-E estejam presentes.

A aba `2022-finbra` da planilha consolidada local foi usada somente para esse município e somente para receitas/população.

Resultado da composição fill-only:

- linhas da base anual: 645;
- municípios suplementados: 1;
- células preenchidas: 9;
- conflitos: 0;
- SHA-256 do CSV composto: `387b61416817db342f94c86759811000ef40a627320308651ccd6e34cec7d9d0`.

Células preenchidas:

- receita corrente bruta;
- receita tributária bruta;
- IPTU;
- ITBI;
- ISS;
- FPM mensal;
- ICMS;
- IPVA;
- transferências de capital.

Operações de crédito e alienação de bens não aparecem no suplemento e permanecem ausentes.

## 2024 — 15 municípios

Os 15 códigos ausentes do snapshot anual de 2024 foram extraídos da aba `2024-finbra` da planilha consolidada local.

Todos os 15 códigos foram encontrados.

Cobertura do suplemento:

- receita corrente bruta: 15/15;
- receita tributária bruta: 15/15;
- IPTU: 15/15;
- ITBI: 15/15;
- ISS: 15/15;
- FPM mensal: 15/15;
- ICMS: 15/15;
- IPVA: 15/15;
- população DCA: 15/15;
- operações de crédito: 4/15;
- alienação de bens: 9/15;
- transferências de capital: 13/15.

SHA-256 do suplemento normalizado de 15 linhas:

`6638fece3b2849c5c24295787f32f68ea499df2eee3e418386cdf3638f6391b2`.

As rubricas de capital não observadas permanecem ausentes; não são convertidas em zero.

## Decisão

A fonte consolidada local está aprovada como suplemento fill-only de I-C para:

- Guaraçaí/2022;
- os 15 municípios ausentes do snapshot anual de 2024.

Consequências:

1. 2022 não requer delta externo;
2. 2024 requer eventual complemento externo somente para I-D e I-E dos 15 municípios;
3. valores existentes nos snapshots anuais continuam sendo preservados;
4. a planilha consolidada não substitui o snapshot anual em observações já existentes.
