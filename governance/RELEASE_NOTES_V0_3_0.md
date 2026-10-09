# Finanças Municipais SP v0.3.0

release_universe: SP_645

Release funcional do painel estadual com seleção de universos analíticos sobrepostos.

## Novidade principal

O painel passa a operar com 13 universos, preservando `SP_645` como padrão:

- Estado de São Paulo — 645 municípios;
- TIC-TIM 30 — 30 municípios;
- Cidades Médias — 33 municípios;
- 9 regiões metropolitanas paulistas;
- Aglomeração Urbana de Franca.

## Regra analítica

A seleção de universo não é apenas um filtro visual. Para cada universo são recalculados:

- cobertura;
- estatísticas de janela;
- tipologias;
- marcadores comparáveis;
- pares prioritários.

Os valores fiscais municipais continuam armazenados uma única vez.

## Interface

Foi adicionado o seletor **Recorte de análise**. Município, comparação, mapa, cobertura, marcadores e pares acompanham o universo selecionado.

A exportação CSV inclui o universo no nome do arquivo.

## QA

Preview estadual multiuniverso aprovado:

- run: `37908586197`;
- artifact: `11605622431`;
- SHA-256: `395a733d332bb871b8ccdd8ce3e9e2f76fcaee0b1e5c53cfd965618742e194fb`;
- QA local: aprovado;
- QA remoto: aprovado;
- 13 universos validados com contagens e mapas específicos;
- SP645 permanece com 645 municípios;
- TIC-TIM 30 permanece com 30;
- Cidades Médias contém 33 municípios.

Preview:

`https://sp645-candidate.finbra-tic-tim-referencia.pages.dev`

## Compatibilidade

A raiz `/data/` continua representando `SP_645`. Os recortes adicionais são publicados em `/data/universes/<ID>/`, preservando os contratos estaduais existentes.

## Publicação

A release congela a candidata multiuniverso. A promoção à produção continua separada e manual por meio do workflow `SP645 Pages Production`.
