# Finanças Municipais SP v0.4.0

release_universe: SP_645

Release funcional da API editorial estática para geração de boletins fiscais.

## API editorial v1

Base:

`/data/api/v1`

Contratos:

- `/publication/universes.json`;
- `/publication/contract.json`;
- `/publication/universes/{publication_id}/context.json`;
- `/publication/universes/{publication_id}/municipalities.json`;
- `/publication/universes/{publication_id}/municipalities/{codigo_ibge}.json`.

## Escopo

Onze universos editoriais:

- 9 regiões metropolitanas;
- AU de Franca;
- Cidades Médias.

A RMSP editorial possui 38 municípios e exclui a cidade de São Paulo sem alterar o universo analítico do painel.

Cidades Médias mantém as 33 cidades, inclusive as 27 que também integram RM/AU. A sobreposição é deliberada.

## Contextos

A API materializa:

- 11 contextos transversais;
- 287 contextos município × universo;
- cobertura e estados de disponibilidade;
- soma dos valores observados;
- média, mediana, Q1 e Q3;
- extremos municipais;
- percentil, quartil e posição intragrupo;
- diferença para a mediana;
- séries históricas e metadados de fonte.

## QA

Preview estadual aprovado:

- run: `37916874141`;
- artifact: `11609749928`;
- SHA-256: `2ff59a258578c84863c4cf9733224d816e006680d1acef582e0c18d20a587d3d`;
- QA local: aprovado;
- QA remoto: aprovado.

## Skills

A API foi desenhada para alimentar as Skills `boletim-fiscal-municipal` e `boletim-fiscal-universo`.

A geração editorial deve usar a API como camada de fatos e não recalcular indicadores oficiais dentro da Skill.
