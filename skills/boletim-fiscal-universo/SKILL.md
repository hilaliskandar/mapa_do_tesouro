---
name: boletim-fiscal-universo
description: "Gera análises transversais e cadernos fiscais para os 11 universos editoriais do projeto Finanças Municipais SP: 9 regiões metropolitanas, AU de Franca e Cidades Médias. Use quando o usuário pedir panorama do grupo, comparação intragrupo, composição fiscal, distribuição, extremos, cobertura ou texto-base de publicação do universo, usando a API editorial estática e sem tratar ausência como zero."
---

# Boletim fiscal do universo

Produzir a análise transversal de um universo editorial usando estatísticas já consolidadas pela API estática do projeto.

## Fluxo

1. Identificar o `publication_id`.
2. Consultar o índice em `.../data/api/v1/publication/universes.json`.
3. Obter `.../publication/universes/{publication_id}/context.json`.
4. Validar o payload. Se houver arquivo local, executar `scripts/validate_context.py universe <arquivo>`.
5. Ler `references/api.md` e `references/editorial.md`.
6. Redigir a análise transversal e, se solicitado, organizar a sequência das fichas municipais do mesmo caderno.
7. Explicitar cobertura e excluir qualquer interpretação fundada em valores ausentes.

## Estrutura padrão

# Indicador fiscal de [Universo]

## Panorama
Sintetizar os principais movimentos e a heterogeneidade interna.

## Receitas
Usar agregados apenas com a cobertura indicada. Para proporções e indicadores, priorizar mediana, quartis e dispersão.

## Despesas e investimento
Apresentar estrutura, dispersão e municípios nos extremos, sem transformar posição em avaliação normativa.

## Território
Analisar as funções territoriais e o agregado territorial estrito.

## Dívida, liquidez e CAPAG
Apresentar distribuição dos indicadores oficiais e cobertura.

## Diferenças internas
Identificar municípios nos extremos e padrões de concentração ou dispersão. Não atribuir causalidade sem fonte adicional.

## Municípios do caderno
Listar os integrantes e indicar que cada ficha municipal deve usar este mesmo universo como referência comparativa.

## Fontes, cobertura e cautelas
Registrar build, anos, cobertura e exclusões editoriais.

## Regras obrigatórias

- Para RMSP, trabalhar com 38 municípios: São Paulo está excluída do universo editorial.
- Cidades Médias contém as 33 cidades, inclusive as 27 que também pertencem a RM/AU.
- Não somar valores ausentes como zero.
- Somente chamar de total do universo uma soma cujo nível de cobertura esteja explicitado.
- Para comparação entre municípios, preferir mediana, quartis, percentis e extremos a médias simples quando houver forte assimetria.
- Não usar rankings como nota de desempenho.
- Não produzir inferência causal a partir de correlação ou posição relativa.
