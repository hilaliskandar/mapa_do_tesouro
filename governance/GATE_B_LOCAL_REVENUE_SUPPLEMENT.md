# Gate B — suplemento local de receitas 2022–2025

## Fonte

Arquivo no Google Drive: `Receitas 2022-2025.xlsx`

- file ID: `1FX1QFhv3_lUhfqxEW0z5KJ0EWGPoMZGQ`;
- tamanho: 30.466.010 bytes;
- SHA-256: `60c8f9cd356a4294b694263654f385b1b6e6aed20581ce8b5ddb1cd01a36105c`.

Abas FINBRA:

- 2022-finbra: 645 municípios;
- 2023-finbra: 645 municípios;
- 2024-finbra: 645 municípios;
- 2025-finbra: 642 municípios.

## Política de uso

Essa fonte é **suplementar e fill-only**.

Ela não substitui o snapshot anual quando existe valor observado. Em observações comuns, foram detectadas pequenas diferenças de arredondamento e algumas revisões posteriores. Por isso:

1. o snapshot anual continua sendo a base histórica;
2. a planilha consolidada preenche somente município/conta ausente no snapshot;
3. valores já existentes no snapshot não são substituídos;
4. divergências são tratadas como QA, nunca como atualização silenciosa.

## 2022

O snapshot anual do Anexo I-C contém 644 municípios e não contém Guaraçaí, código `3517802`.

A aba `2022-finbra` contém Guaraçaí com 126 linhas de receita. Todas as receitas estruturais do mapping estão presentes. Operações de crédito e alienação de bens não aparecem e permanecem como ausência declaratória.

Decisão: 2022 não requer consulta externa para I-C.

## 2024

O snapshot anual contém 630 municípios nos três anexos.

A aba `2024-finbra` contém os 15 municípios ausentes do snapshot anual de receitas. Para todos eles, as receitas estruturais do mapping estão presentes. Em alguns municípios, rubricas de capital esparsas não aparecem e permanecem ausentes.

Decisão:

- I-C: recuperar localmente os 15 municípios;
- I-D: delta ainda necessário para 15 municípios;
- I-E: delta ainda necessário para 15 municípios.

## Implementação

O módulo `pipeline.normalize.dca_revenue_supplement` lê a aba anual, filtra códigos explícitos e produz CSV normalizado no mesmo esquema de 26 variáveis.

Somente variáveis de receita e população são preenchidas. Variáveis de despesa permanecem vazias, permitindo composição segura pelo merge fill-only já existente.
