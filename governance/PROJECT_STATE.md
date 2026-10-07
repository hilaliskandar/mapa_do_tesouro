# Estado do projeto

Data de referência: 2026-10-07.

## Estado operacional

A `main` é a fonte de verdade.

O baseline público TIC-TIM 30 permanece publicado e protegido por CI, QA de paridade e contratos metodológicos.

A expansão estadual está no estado `gate_b_active`.

## Hierarquia de fontes operacionais

Para reconstrução histórica e processamento em lote, o acervo local do Google Drive é a fonte operacional preferencial.

Pasta FINBRA/SP:

`https://drive.google.com/drive/folders/1K_Raj0pKEyktVY5BVa_raOZ4cQdJ8HQ4`

Regra:

1. Drive local para reconstrução histórica, cargas em lote e reprocessamento;
2. Siconfi externo para validação por amostra, atualização incremental, confirmação de versão e investigação de lacunas/divergências;
3. aquisição externa integral somente quando necessária para auditoria independente ou ausência de snapshot local adequado.

## Baseline público

- universo: `TIC_TIM_30`;
- período: 2013–2025;
- release funcional: v0.1.1;
- produção: `https://finbra-tic-tim-referencia.pages.dev`;
- preview: `https://preview.finbra-tic-tim-referencia.pages.dev`;
- metodologia territorial: `strict_complete`.

## SP_645

### Gate A — aprovado

A aquisição direta estadual de 2025 foi concluída com sucesso:

- 645 municípios;
- I-C, I-D e I-E;
- 1.935 respostas brutas;
- zero falhas;
- 645 linhas normalizadas;
- 26 variáveis;
- zero issues;
- SHA-256 normalizado `619367dd8b2c5b3db6f7a6c902b41e2f2685616cf8560e2e852e7583f386eec7`.

A execução independente anterior produziu o mesmo hash normalizado.

### Gate B — ativo

A reconstrução local já foi testada para 2020–2025.

Situação:

- 2020: 645 municípios nos três anexos;
- 2021: 645 municípios nos três anexos;
- 2022: 644 em I-C; 645 em I-D/I-E;
- 2023: 645 municípios nos três anexos;
- 2024: 630 municípios nos três anexos;
- 2025 local: 632 municípios; aquisição direta atual: 645.

O normalizador já aceita CSV e XLSX locais e produz cobertura/ausência frente ao universo estadual.

### Crosswalk temporal

Foi incorporada variante explícita para 2018–2021 nas contas de IPTU, ITBI, ISS, FPM mensal, ICMS e IPVA. Os códigos foram verificados diretamente nos anexos locais de 2018–2021.

## Próximo gate operacional

1. processar integralmente 2018 e 2019 com o mapping temporal já corrigido;
2. identificar o regime contábil anterior a 2018;
3. expandir progressivamente para 2013–2017;
4. produzir delta incremental apenas para exercícios/snapshots incompletos;
5. promover snapshots anuais aprovados para armazenamento privado versionado;
6. somente depois integrar RREO, RGF, CAPAG e demais fontes estaduais.

## Regras para retomada

1. ler este arquivo;
2. verificar `main`, PRs e CI;
3. consultar primeiro o acervo local do Drive;
4. não repetir coleta externa integral se houver snapshot local adequado;
5. preservar ausência como ausência;
6. registrar toda variante temporal explicitamente;
7. manter TIC-TIM 30 como baseline de regressão até a promoção formal do baseline estadual.
