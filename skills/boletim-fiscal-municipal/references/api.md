# API editorial municipal

Base de produção esperada:
`https://finbra-tic-tim-referencia.pages.dev/data/api/v1`

Endpoint:
`/publication/universes/{publication_id}/municipalities/{codigo_ibge}.json`

Campos centrais:
- `publication_universe`: id, nome, tipo e quantidade de membros.
- `municipality`: código IBGE, nome e UF.
- `years` e `latest_year`.
- `build`: versão e proveniência do build.
- `rules`: regras metodológicas, inclusive ausência diferente de zero.
- `variables`: objeto por `variavel_id`.

Para cada variável:
- `metadata`: nome, grupo, tipo, unidade, definição, fórmula, cautelas e fonte preferencial.
- `series`: observações anuais com status e fonte.
- `latest`: observação do último ano do contexto, se houver.
- `relative_latest`: percentil, quartil, posição decrescente e diferença para a mediana quando a observação for numérica.
- `group_latest`: cobertura e estatísticas do grupo no último ano.

Nunca inferir um dado ausente a partir de outra variável. Use `relative_latest` somente dentro do universo indicado no próprio payload.
