# Regionalização estadual — candidata v0.5.0

Confronto integral em 24/11/2026 dos catálogos administrative_universes_sp_2026.yml e regional_universes_sp_seade_2026.yml: 59/59 nomes e conjuntos de membros iguais, zero divergências. Manter o primeiro como único catálogo operacional, IDs RA_SEADE e RG_SEADE; segundo somente evidência de conferência e hierarquia. Não importar ambos. Workflow inv-sp645-ra-rg-private-preview.yml contempla build real, 72 universos, mapas, API e paridade Gate D. Próximo gate: executar e verificar QA, conservação de valores por partição, teste de navegador e prévia isolada. Não promover dados financeiros novos nem alterar produção v0.4.1.

## Build real aprovado

Build real run 45526052647: success, 72 universos, 16 RA e 43 RG, 645 membros em cada partição, 645 geometrias estaduais, 11.501 células Gate D comparadas, QA estático aprovado; artifact 14982431513. Implementado gate adicional de conservação monetária e correspondência exata das listas municipais (f99721fc e 63952291); execução ainda a confirmar. Produção v0.4.1 preservada. Próximos gates: QA de conservação, hierarquia navegável, teste Chromium e prévia isolada.

## Publicação definitiva

Produção v0.5.1 confirmada em 25/11/2026 UTC: run 45537933507 success, 194 testes aprovados e 3 skipped, QA local e remoto aprovados, cadastro RMRP preservado, artifact 14987901682. Release v0.5.0 não implantado por teste legado de VERSION; correção 93b0437 e release v0.5.1 no commit 158fb5de. Homologação hierárquica run 45534881706 com 10 cenários aprovados. URL https://finbra-tic-tim-referencia.pages.dev/. Escopo fiscal permanece 2021–2025; sem promoção de novos dados financeiros. Rollback v0.4.1.
