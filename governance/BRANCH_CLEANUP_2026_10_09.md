# Saneamento de branches

Data de referência: 2026-10-09.

## Decisão

`main` é a única branch operacional canônica. Nenhuma outra branch deve ser retomada como fonte de trabalho sem nova auditoria explícita.

Situação no momento desta auditoria:

- branches totais: 138;
- branch canônica preservada: `main`;
- branches de PR já merged ainda existentes: 118;
- branches integralmente atrás da main, sem commit exclusivo: 7;
- branches divergentes auditadas e consideradas superadas: 12;
- issues abertas: 0;
- pull requests abertos: 0;
- merges pendentes: 0.

## Elegíveis à exclusão imediata — PR já merged

- `bootstrap-financas-municipais-sp`
- `canonical-r2-rebuild-infra`
- `ci-pages-preview-production`
- `close-gate-b-dca-2013-2025`
- `dca-normalization-v1`
- `dca-temporal-variants-2013-2017`
- `dca-temporal-variants-2018-2021`
- `delta-from-versioned-queue`
- `fix-delta-code-parser`
- `fix-f116-export-csv`
- `fix-gate-e-corrected-history-paths`
- `fix-gate-e-corrected-history-source-run`
- `fix-import-missing-tokens`
- `fix-legal-reports-cli`
- `fix-marker-stability-accent`
- `fix-rgf-postprocess-and-record-qa`
- `fix-sp645-gated-parity-nd`
- `fix-sp645-multisource-source-catalog`
- `fix-sp645-private-site-r2-bucket`
- `fix-sp645-private-site-r2-inputs`
- `fix-sp645-private-site-triggers`
- `fix-tabs-responsive-v0.1.1`
- `fpm-definition-precision`
- `frontend-explicit-insufficient-coverage`
- `gate-b-auto-2016`
- `gate-b-batch-orchestrator`
- `gate-b-fill-only-delta-merge`
- `gate-b-finbra-tabular-local`
- `gate-b-full-history-2013-2025`
- `gate-b-local-revenue-supplement`
- `gate-b-local-supplement-validation`
- `gate-b-orchestrator`
- `gate-b-orchestrator-chain`
- `gate-b-selective-dca-delta`
- `gate-c-2025-core-complete`
- `gate-c-2025-state-finalize`
- `gate-c-capag-sp645-local`
- `gate-c-multisource-contracts`
- `gate-c-rgf-auto-fallback`
- `gate-c-rgf-capag-local-supplement`
- `gate-c-rgf-composite-finalize`
- `gate-c-rgf-fill-only-composite`
- `gate-c-rgf-fillonly-finalize`
- `gate-c-rgf-gap-classification`
- `gate-c-rgf-local-fillonly-qa`
- `gate-c-rgf-normalizer-smoke`
- `gate-c-rgf-qa-generator`
- `gate-c-rgf-shard-postprocess`
- `gate-c-rgf-sharded`
- `gate-c-rgf-sp645-2025`
- `gate-c-rgf-taxonomy-smoke`
- `gate-c-rgf02-auto-2025`
- `gate-c-rgf02-first-state-load`
- `gate-c-rgf02-live-smoke`
- `gate-c-rgf02-postprocess`
- `gate-c-rgf02-postprocess-v2`
- `gate-c-rgf02-sharded-fallback`
- `gate-c-rgf02-sp645-prepared`
- `gate-c-rreo-2025-rgf-taxonomy`
- `gate-c-rreo-rcl-auto-2025`
- `gate-c-rreo-rcl-parity-fix`
- `gate-c-rreo-rcl-state`
- `gate-c-sp645-2025-mapping`
- `gate-c-sp645-multifuentes-builder`
- `gate-d-parity-tictim30-2025`
- `gate-d-sp645-indicator-readiness`
- `gate-d-sp645-indicators-calculation`
- `gate-e-dca-window-catalog`
- `gate-e-history-parity-approved`
- `gate-e-history-postprocess`
- `gate-e-rgf-2023-a01-fix`
- `gate-e-rgf-2023-taxonomy-smoke`
- `gate-e-rgf-historical-minimum`
- `gate-e-rgf-history-parity`
- `gate-e-sp645-cartography-qa`
- `gate-e-sp645-typologies-pairs-private`
- `gate-e-sp645-typology-adapter`
- `generalize-universe-645`
- `governance-canonical-state-20261007`
- `governance-close-p0-gate-f`
- `governance-gate-c-sync`
- `governance-gatea-gateb-2020-2025`
- `governance-inventory-2026-10-09`
- `governance-sp645-production-live`
- `governance-sync-after-p2-3`
- `guard-sp645-release-preview`
- `maintenance-strict-sum-dca-qa`
- `p1-1-coverage-em-revisao`
- `p1-1-coverage-report`
- `p1-1-refresh-coverage-sources`
- `p2-1-candidate-manifest-retry`
- `p2-2-rollback-and-checklist`
- `p2-3-sp645-preview-route`
- `postmerge-ci-main`
- `postmerge-frontend-publish-prep`
- `prefer-drive-finbra-history`
- `provenance-schema-v004`
- `qa-dca-sp645-2025-pre-gatea`
- `r2-canonical-source-rebuild`
- `r2-sp645-pilot-scale`
- `record-2015-source-confirmed-absence`
- `record-2018-empty-source-and-annex-delta`
- `release-v0-2-0-sp645`
- `release-v0.1.0`
- `release-v0.1.1`
- `rreo-2025-crosssource-diagnostic`
- `siconfi-baseline-crosscheck`
- `siconfi-direct-acquisition`
- `siconfi-http-resilience`
- `siconfi-rreo-rgf-acquisition-v1`
- `siconfi-state-smoke`
- `siconfi-statewide-acquisition-v1`
- `sp645-full-dca-gate-a`
- `sp645-private-site-artifact`
- `sp645-production-workflow`
- `sp645-promote-approved-dca-r2`
- `sp645-scale-validation`
- `trigger-gate-f-sp645-post-rgf02`

## Elegíveis à exclusão imediata — totalmente absorvidas pela main

- `canonical-source-registry-r2-v2`
- `canonical-source-storage`
- `close-p1-2-p1-3`
- `gate-f-record-and-final-regression`
- `gate-f-tictim30-regression`
- `r2-sp645-pilot`
- `sp645-dca-load`

## Divergentes auditadas e classificadas como superadas

- `canonical-r2-csv-pilot` — protótipo antigo de ingestão CSV/piloto; PR #20 fechado sem merge; funcionalidades posteriores substituem o fluxo.
- `gate-b-direct-safe-commit` — experimento de automação/auto-merge do Gate B; fluxo atual usa orquestração posterior e governança consolidada.
- `gate-b-local-receipts-delta` — protótipo de delta por workbook; substituído por dca_revenue_supplement/delta e Gate B consolidado.
- `gate-c-rgf-capag-fillonly-tool` — conteúdo funcional idêntico aos arquivos já presentes na main.
- `gate-c-rgf-fillonly-merge` — conteúdo funcional idêntico aos arquivos já presentes na main.
- `legal-crosswalk-v1` — workflow exploratório de probe; crosswalk legal posterior foi incorporado por outras rotas e não depende desse workflow.
- `ops-siconfi-sp645-2025` — workflow operacional antigo; substituído por siconfi-sp645-full-dca.yml e siconfi-sp645-year.yml.
- `rreo-rgf-official` — implementação monolítica preliminar; substituída pela arquitetura atual de legal_reports, rgf/rreo state e normalizadores específicos.
- `sp645-dca-canonical-load` — preparador inicial substituído por sp645_private_input e builders estaduais atuais.
- `sp645-pilot-rebuild-v1` — piloto estadual antigo; PR #18 fechado sem merge e substituído pelo pipeline SP645 completo em produção.
- `sp645-pilot-source-r2` — piloto R2 antigo; substituído pelos inputs canônicos pinados e workflows atuais.
- `verify-cloudflare-ci-config` — workflow diagnóstico antigo; verificações de configuração estão incorporadas nos workflows Pages atuais.

## Regra operacional

1. preservar apenas `main` como linha de desenvolvimento vigente;
2. não criar PR a partir das branches listadas neste documento;
3. excluir fisicamente as branches listadas quando houver acesso a operação de remoção de refs;
4. manter tags e releases como trilha histórica, especialmente `v0.1.0`, `v0.1.1` e `v0.2.0`;
5. novas frentes devem nascer de `main` e ter issue/critério de aceite quando forem executáveis.

## Limitação da limpeza automática

O conector GitHub disponível nesta sessão não expõe operação de exclusão de branch/ref. Por isso, a classificação e o saneamento lógico foram concluídos, mas a remoção física das refs deve ser feita por uma interface com permissão de `DELETE /git/refs` ou pela interface do GitHub.
