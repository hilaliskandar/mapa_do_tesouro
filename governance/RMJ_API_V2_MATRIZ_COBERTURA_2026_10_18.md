# Matriz de cobertura da RMJ — API v2, exercício 2025

Conferência executada em 18/10/2026 a partir de `sp645-private-site-38593209824.zip`, SHA-256 `9ca1688182eb90a02517c9664dabd4870d88a9abdaad28e6cafd82bd3be81b21`. Foram lidos `manifest.json`, `catalog/variables.json`, `qa/readiness.json`, `universes/RM_JUNDIAI/context.json` e `universes/RM_JUNDIAI/coverage.json`.

## Resultado

- 75 variáveis distribuídas segundo regra de classificação **mutuamente exclusiva**: 17 percentuais sem certificação de escala; 44 não percentuais com `observed=7`; 13 não percentuais com `observed` entre 1 e 6; uma sem observação em 2025.
- As 48 cautelas ausentes são uma dimensão **transversal**, não um quinto grupo. `descritivo_candidato` não equivale a aprovação editorial.
- 7 membros esperados; exercícios disponíveis 2021–2025.
- `publication_qa=not_evaluated`; publicação não autorizada.
- Matriz integral e resumo JSON foram criados no ambiente da análise, sem alterar dados ou publicação.

## Metodologia

A classificação consulta o identificador `variavel_id` do catálogo e cruza por `variable_id` da cobertura e prontidão. Em 2025, variáveis de unidade `percentual` com `scale_verified=false` ou multiplicador ausente são bloqueadas antes da classificação de cobertura. Demais variáveis: `observed==7` classificada como cobertura integral candidata; `1<=observed<=6` como parcial; `observed==0` como sem observações. A ausência de cautelas é registrada em coluna independente.

## Limites e próximo gate

Não executar interpretação com LiteLLM como resultado publicável antes de confirmar proveniência, escala, cautelas e conjunto de evidências por indicador. A análise de cobertura de 2025 não comprova série histórica homogênea. Consolidar a correspondência destas 75 variáveis com as perguntas gerenciais e quadros reais do caderno RMJ após recuperar seu catálogo editorial canônico. O módulo `editorial/audit_v2_editorial_ready.py` integrado pelo PR #200 ainda não foi executado literalmente neste lote; a matriz foi calculada por rotina independente sobre os arquivos reais.
