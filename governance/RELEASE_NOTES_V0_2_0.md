# Finanças Municipais SP v0.2.0

release_universe: SP_645

Primeira release estadual congelada do novo núcleo, ainda sem promoção automática para produção.

## Universo

- 645 municípios paulistas;
- janela operacional 2021–2025;
- 2021–2024 tratados como histórico mínimo para tipologias e comparação;
- 2025 como exercício multifuentes estadual completo no contrato atual.

## Conteúdo validado

- DCA estadual;
- RREO e RGF com cobertura explicitamente documentada;
- CAPAG 645/645;
- indicadores, tipologias e pares por universo;
- 645 geometrias municipais;
- cobertura final e contribuição por fonte;
- exportação CSV;
- mapa, séries, comparação, análises, fontes, crosswalk, dicionário e metodologia.

## QA

- preview estadual manual: aprovado;
- run: `37889265727`;
- artifact: `11598005846`;
- SHA-256: `45950e38e559a9d668d75725d9a7c8f30f1942b6d11f03c050f4790ebb521570`;
- QA local SP645: aprovado;
- QA remoto SP645: aprovado;
- 11.501 células confrontadas com Gate D;
- regressões não explicadas contra TIC-TIM 30: zero.

Preview aprovado:

`https://sp645-candidate.finbra-tic-tim-referencia.pages.dev`

## Política de ausência

Ausência não é zero. Contas esparsas permanecem ausentes quando a fonte não fornece observação canônica. O preenchimento fill-only do RGF02 permanece limitado a conceitos com equivalência semântica demonstrada e zero conflitos.

## Publicação

Esta release congela e identifica a candidata estadual. Ela não promove automaticamente SP645 à produção. O baseline TIC-TIM 30 permanece publicado até execução e aprovação de um fluxo estadual de produção explicitamente autorizado.
