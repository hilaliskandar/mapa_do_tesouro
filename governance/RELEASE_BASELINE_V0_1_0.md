# Release baseline v0.1.0 — 30 municípios TIC-TIM

## Estado congelado

Esta versão congela o primeiro baseline auditável e reproduzível do novo núcleo **Finanças Municipais SP**, ainda restrito ao universo inicial de 30 municípios TIC-TIM.

Commit de referência da `main` no início do freeze:

`f22152304871df3bd85caebe8dd81a133e79a39d`

## Universo

- 30 municípios;
- 13 exercícios;
- período 2013–2025;
- 390 pares município-ano.

## Catálogo

- 75 objetos técnicos/documentais;
- 25 indicadores públicos do painel v7;
- 50 contas/agregações documentadas;
- metodologia versionada;
- fontes, cobertura e crosswalk publicados como artefatos estáticos.

## Regras canônicas

- ausência não equivale a zero;
- agregado territorial em `strict_complete`;
- DTP/RCL, DC/RCL e DCL/RCL preservados como valores oficiais importados do RGF;
- CAPAG preservada como classificação oficial;
- tipologias relativas calculadas por universo e janela;
- pares calculados a partir de seis marcadores comparáveis;
- CAPAG e DCL não entram na assinatura de pares.

## Resultados da build real

- 17.940 observações diretamente importadas;
- 29.250 observações após derivados;
- 1.890 estatísticas de janela;
- 210 classificações de tipologia;
- 180 marcadores comparáveis;
- 870 pares dirigidos;
- 6 pares principais recíprocos no cenário `strict_complete`;
- 30 geometrias municipais.

## Hashes dos artefatos de referência

### Base multifuentes

Arquivo:

`FINBRA_TIC_TIM_30M_BASE_MULTIFONTES_2013_2025_v0_4.xlsx`

SHA-256:

`f51d8615f3742b1d414f1edff67805cac1a10cbc18764b454aab518de9c9e3f1`

### Painel v7 XLSX

`FINBRA_TIC_TIM_30M_PAINEL_FISCAL_INTERATIVO_v7.xlsx`

SHA-256:

`3db0d6782e1c31d0f0dd0292aca4542f9faac2d2b23c4ce2dd0f34905c5f298f`

### Bloco 3 v0.7

`FINBRA_TIC_TIM_30M_BLOCO3_INDICADORES_TRAJETORIAS_v0_7.xlsx`

SHA-256:

`2099d6c6c7af28f92701b8c1b9d3d880c3e2325b824ddf984a8e309cd193f101`

### Candidate estático de preview

`financas-municipais-sp-preview-ready.zip`

SHA-256:

`3ca3ceb8aebd8df1b37db4edfd91c6b9792e3aa4bdeda1509428348eb0014a90`

## Paridade

- 59 campos compartilhados entre base multifuentes e painel v7;
- 23.010 células comparadas;
- 0 divergências;
- seis agregações materializadas do v7 reproduzidas integralmente;
- pares legados reproduzidos 90/90 quando usada a regra `legacy_partial`;
- divergências do cenário canônico decorrem da decisão metodológica `strict_complete`, documentada e aprovada.

## Frontend

Inclui:

- panorama;
- perfil municipal;
- séries históricas;
- comparação anual;
- mapa temático;
- análises temáticas;
- fontes e cobertura;
- crosswalk;
- dicionário;
- metodologia;
- ajuda contextual “Como ler”.

## Deployment

O pacote estático foi preparado para Cloudflare Pages Direct Upload.

A publicação de preview permanece uma operação separada do freeze do baseline. A release v0.1.0 não depende de um domínio público para ser válida.

## Documentos de QA e governança

- `governance/REAL_BUILD_QA_2026-10-07.md`
- `governance/DECISION_TERRITORIAL_STRICT_COMPLETE.md`
- `governance/REGRESSION_TYPOLOGIES_PAIRS.md`
- `governance/FRONTEND_CANDIDATE_0_1.md`
- `governance/PARITY_REPORT_V7_BLOCK3.md`
- `deployment/PREVIEW_CANDIDATE_2026-10-07.md`
