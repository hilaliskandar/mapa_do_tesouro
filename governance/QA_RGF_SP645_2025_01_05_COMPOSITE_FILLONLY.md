# QA — composto RGF 01/05 SP645 2025 com suplemento fill-only

## Fontes

Base observada:

- run RGF: `37732303043`;
- 645 linhas;
- SHA-256 `9f3ced721fa2c767d24cdec8e464215b30932e820e01601f24bac9b1e76486ba`.

Suplemento local:

- `RGF_CAPAG_SP645_2025_SUPLEMENTO_FILLONLY.csv`;
- Drive ID `1-4B84oosvrq6XTWxgJZfgz0fsEYAywBz`;
- SHA-256 `494924aea17e531bd56a2b68b773585f8b33df586df7ee11b425ccd1571c781d`.

## Merge

Regra estrita: preencher somente célula vazia da base quando o suplemento tiver valor semanticamente equivalente.

Resultado:

- linhas: 645;
- células preenchidas: 366;
- conflitos: 0;
- nenhuma célula observada da API foi sobrescrita.

Cobertura após composição:

| Variável | Antes | Depois |
|---|---:|---:|
| Caixa bruta não vinculada | 526 | 635 |
| Demais obrigações não vinculadas | 93 | 108 |
| RP não liquidados anteriores não vinculados | 411 | 490 |
| RP liquidados anteriores não vinculados | 404 | 478 |
| RP liquidados do exercício não vinculados | 412 | 501 |

## Artefato composto

- nome: `RGF_SP645_2025_01_05_COMPOSTO_FILLONLY.csv`;
- Drive ID: `1hSlw6mJYEkPyGXK-sgUWWDlFAQ2PczWy`;
- SHA-256: `48b50b2df44eaddc2fc1c4ed096c057c2bea5d61cb850b37dc23e6037962aa24`.

## Limite

O composto não preenche:

- DTP;
- RCL legal ajustada;
- percentual oficial DTP/RCL;
- caixa líquida antes/depois de RPNP;
- RP não liquidados do exercício.

Esses campos permanecem vinculados ao demonstrativo oficial correspondente.
