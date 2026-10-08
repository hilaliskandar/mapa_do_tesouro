# QA — Gate C-R1 RREO RCL smoke 2025

Data: 2026-10-08.

## Resultado

Smoke aprovado com paridade integral contra a referência local validada no Google Drive.

Run: `37728544028`.

Sentinelas:

- Americana — 3501608;
- Araçatuba — 3502804;
- Araraquara — 3503208;
- Barueri — 3505708;
- Bauru — 3506003.

## Contrato validado

- endpoint: RREO;
- anexo: RREO-Anexo 03;
- período: 6;
- conta: `RREO3ReceitaCorrenteLiquida`;
- linha: `RECEITA CORRENTE LÍQUIDA (III) = (I - II)`;
- coluna: `TOTAL (ÚLTIMOS 12 MESES)`.

## QA

- municípios solicitados: 5;
- requisições concluídas: 5;
- RCL observadas: 5/5;
- issues de normalização: 0;
- paridade RCL com Drive: 5/5;
- paridade população com Drive: 5/5;
- SHA-256 normalizado: `c2e069aa5cf6fecdb4365caccebc372e0639b2c086e7918786c8fe1f96910c3e`;
- SHA-256 árvore bruta: `af5d46be8012ef65a63eaaef1f7d1de6f2227d42b033cc813aca6ae1dd554e84`.

## Decisão

Gate C-R1 aprovado em escala mínima.

Está autorizada a primeira carga estadual SP645 para 2025, sem alteração do painel público. A promoção da fonte somente ocorrerá após QA de cobertura e paridade estadual.
