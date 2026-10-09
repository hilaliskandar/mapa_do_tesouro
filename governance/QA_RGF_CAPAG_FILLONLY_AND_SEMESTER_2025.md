# QA — suplemento fill-only CAPAG/RGF 2025 e teste semestral

Data: 2026-10-08.

## Suplemento local do Anexo 05

Fontes:

- RGF estadual 2025, run `37732303043`;
- CSV normalizado RGF SHA-256 `9f3ced721fa2c767d24cdec8e464215b30932e820e01601f24bac9b1e76486ba`;
- snapshot CAPAG `capag-municipios-posicao-2026-set.xlsx`;
- snapshot CAPAG SHA-256 `1b1379a5a531920223f1d448be155b70f51eb50180d8c819f1b7da3575a8eb11`.

O suplemento fill-only foi materializado com:

- 645 linhas;
- 366 células preenchíveis;
- zero conflitos;
- SHA-256 do suplemento `494924aea17e531bd56a2b68b773585f8b33df586df7ee11b425ccd1571c781d`.

Distribuição das células:

- caixa bruta não vinculada: 109;
- demais obrigações não vinculadas: 15;
- RP não liquidados anteriores não vinculados: 79;
- RP liquidados anteriores não vinculados: 74;
- RP liquidados do exercício não vinculados: 89.

Artefato no Google Drive:

- nome: `RGF_CAPAG_SP645_2025_SUPLEMENTO_FILLONLY.csv`;
- file ID: `1-4B84oosvrq6XTWxgJZfgz0fsEYAywBz`;
- pasta: acervo FINBRA do projeto.

Regra: o suplemento contém valor apenas quando a célula correspondente da API RGF está vazia. Valores observados da API nunca são substituídos.

## Teste de periodicidade semestral do Anexo 01

Workflow: `Gate C RGF Semester Smoke`.

Run: `37877212941`.

Sentinelas sem DTP no contrato Q/3:

- 3500105;
- 3500204;
- 3500600.

Teste:

- periodicidade `S`;
- período `2`;
- Anexo 01;
- exercício 2025.

Resultado:

- 3/3 requisições concluídas sem erro técnico;
- 3/3 payloads com `items=[]`;
- 0/3 recuperaram DTP, RCL legal ou percentual oficial.

## Padrão das lacunas legais

- municípios sem DTP no RGF Anexo 01: 115;
- municípios sem RCL no RREO Anexo 03: 114;
- interseção: 114;
- município adicional sem DTP no RGF: `3525003`.

A lista `RGF_Ultimo_Exercicio` do snapshot CAPAG contém 114 dos 115 municípios sem DTP; apenas `3525003` não aparece. Isso indica existência de algum dado RGF para esses 114 entes, mas não do contrato anual-final do Anexo 01 testado em Q/3 ou S/2.

## Decisão

1. rejeitar periodicidade semestral S/2 como solução geral para as 115 lacunas do Anexo 01;
2. preservar DTP, RCL legal e percentual como ausentes quando não observados no contrato anual-final;
3. aplicar suplemento local somente aos cinco campos do Anexo 05 com equivalência comprovada;
4. não usar RCL do RREO ou do CAPAG como substituto da RCL legal ajustada do Anexo 01.
