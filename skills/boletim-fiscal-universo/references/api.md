# API editorial do universo

Base de produção esperada:
`https://finbra-tic-tim-referencia.pages.dev/data/api/v1`

Índice:
`/publication/universes.json`

Contexto:
`/publication/universes/{publication_id}/context.json`

Municípios do grupo:
`/publication/universes/{publication_id}/municipalities.json`

Campos do contexto:
- `publication_id`, `name`, `type`, `source_universe_id`.
- `excluded_members`.
- `member_count`, `members`.
- `years`, `latest_year`.
- `build` e `rules`.
- `variable_groups`.
- `variables`.

Cada variável contém `metadata`, `editorial_group`, `yearly` e `latest`.
Cada entrada anual informa cobertura e, quando numérica, soma, média, mediana, Q1, Q3, mínimo e máximo com o município associado. Variáveis categóricas informam contagens por categoria.

A soma é descritiva dos valores observados; conferir `observed`, `expected` e `coverage_pct` antes de apresentá-la como representativa do conjunto.
