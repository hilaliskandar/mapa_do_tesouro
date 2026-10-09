# API editorial estática v1

## Objetivo

Expor contextos de publicação auditáveis a partir da base canônica, sem introduzir servidor de API em runtime. Os arquivos JSON são gerados no mesmo build estadual e publicados no Cloudflare Pages.

A API editorial é a interface entre a base analítica e as Skills de geração de boletins. As Skills não recalculam indicadores oficiais nem harmonizações.

## Escopo inicial

Onze universos editoriais:

1. RM de São Paulo — 38 municípios, com exclusão editorial da capital;
2. RM da Baixada Santista;
3. RM de Campinas;
4. RM do Vale do Paraíba e Litoral Norte;
5. RM de Sorocaba;
6. RM de Ribeirão Preto;
7. RM de São José do Rio Preto;
8. RM de Jundiaí;
9. RM de Piracicaba;
10. AU de Franca;
11. Cidades Médias — 33 municípios.

As cidades médias que pertencem a uma RM/AU permanecem nos dois contextos editoriais. A sobreposição é intencional.

## Contratos

Base:

`/data/api/v1`

Índice:

`/publication/universes.json`

Contrato:

`/publication/contract.json`

Contexto transversal:

`/publication/universes/{publication_id}/context.json`

Lista municipal:

`/publication/universes/{publication_id}/municipalities.json`

Contexto municipal intragrupo:

`/publication/universes/{publication_id}/municipalities/{codigo_ibge}.json`

## Conteúdo do contexto transversal

Para cada variável editorial e ano:

- esperado;
- observado;
- percentual de cobertura;
- estados de disponibilidade;
- soma dos valores observados;
- média;
- mediana;
- Q1 e Q3;
- mínimo e máximo com identificação do município;
- distribuição de categorias quando a variável for textual.

Somas sempre devem ser lidas em conjunto com a cobertura. Ausência não é zero.

## Conteúdo do contexto municipal

Para cada variável:

- metadados metodológicos;
- série histórica;
- observação mais recente;
- fonte e referência;
- estatísticas do grupo;
- percentil intragrupo;
- quartil;
- posição decrescente;
- diferença absoluta e percentual em relação à mediana.

A posição é contextual ao universo editorial e não constitui avaliação normativa.

## Periodicidade editorial

Fase inicial:

- uma Edição de Referência produzida com a base canônica vigente;
- uma nova edição quando a próxima base anual relevante do FINBRA estiver publicada e validada;
- posteriormente, a periodicidade poderá ser ampliada com dados de transparência municipal, sem alterar estes contratos.

## Skills

A API v1 sustenta inicialmente duas Skills:

- `boletim-fiscal-universo`: análise transversal e caderno do grupo;
- `boletim-fiscal-municipal`: ficha do município dentro de um universo editorial.

A mesma cidade pode gerar mais de uma ficha quando integra mais de um universo editorial.
