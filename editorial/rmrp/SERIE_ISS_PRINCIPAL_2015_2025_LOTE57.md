# Lote 57 — Série municipal 2015–2025 do ISS principal na RMRP

**Data:** 02/11/2026. **Status:** reconciliação longitudinal concluída da variável ISS principal, com lacunas preservadas; ISS total ainda não recuperado, e impacto líquido IBS não estimado.

## Fonte e método

Base canônica preexistente: `DCA_SP_645_2013_2025_CANONICO.csv` (Google Drive ID `1BtXY_FxydMREEbMACJtaoW2n24ohVH33`, 2.096.525 bytes, 645 municípios por exercício no acervo). Municípios da RMRP e códigos IBGE conforme `MATRIZ_EXPOSICAO_FISCAL_RMRP_2025_LOTE12.md`. Os dados foram lidos da base já arquivada, **sem repetir extração FINBRA/DCA**, e identificados pelas chaves `(cod_ibge, ano)`. Foram selecionados 2015–2025 e os campos `dca_iss_principal`, `dca_receita_corrente_bruta`, `dca_receita_tributaria_bruta`, `dca_iptu_principal` e `dca_itbi_principal`.
A razão ISS principal/receita corrente bruta é obtida em cada município e exercício do mesmo registro. É uma **participação nominal**, comparável como proporção; não é série monetária deflacionada. Variações em pontos percentuais não representam crescimento real da arrecadação. A série não permite estimar distribuição municipal do IBS ou impacto de transição, pois falta a modelagem legal/distributiva e de destino.

## Auditoria de cobertura e integridade

- Universo esperado: 34 municípios × 11 exercícios = **374 registros**.
- Chaves distintas encontradas: **374/374**. Cobertura de chaves não deve ser confundida com cobertura dos valores.
- Linhas sem ISS principal preenchido ou sem denominador válido: **5**; nenhuma linha com ISS negativo e nenhuma em que ISS principal ultrapasse receita tributária bruta.
- Observações sem indicador válido: Brodowski (2016); Pradópolis (2016); Sales Oliveira (2016); Serra Azul (2016); Santa Rita do Passa Quatro (2021).
- Indicador 2025: 34/34 municípios com ISS principal e receita corrente positiva; informação de ISS **principal** não equivale a ISS total (principal, multas, juros e dívida ativa). A base canônica examinada não contém campos segregados de ISS acessórios, de modo que **não foi possível conciliar ISS total** nesta etapa.

## Série sintética municipal

| Município | SR | Anos válidos | ISS principal/RC 2015 (%) | ISS principal/RC 2025 (%) | Δ 2015–2025 (p.p.) | Amplitude observada (%) |
|---|---:|---:|---:|---:|---:|---:|
| Barrinha | 1 | 11/11 | 2,27 | 4,80 | 2,53 | 2,27–4,80 |
| Brodowski | 1 | 10/11 | 3,57 | 4,28 | 0,70 | 3,43–4,52 |
| Cravinhos | 1 | 11/11 | 6,02 | 7,97 | 1,95 | 5,21–7,97 |
| Dumont | 1 | 11/11 | 3,64 | 5,08 | 1,44 | 3,37–5,78 |
| Guatapará | 1 | 11/11 | 5,47 | 5,44 | -0,03 | 3,92–6,50 |
| Jardinópolis | 1 | 11/11 | 4,56 | 5,58 | 1,02 | 3,84–5,67 |
| Luís Antônio | 1 | 11/11 | 4,50 | 6,46 | 1,96 | 3,03–7,07 |
| Pontal | 1 | 11/11 | 3,18 | 3,63 | 0,45 | 3,18–4,39 |
| Pradópolis | 1 | 10/11 | 4,52 | 4,95 | 0,44 | 3,50–5,42 |
| Ribeirão Preto | 1 | 11/11 | 10,55 | 13,14 | 2,59 | 10,21–13,14 |
| Santa Rita do Passa Quatro | 1 | 10/11 | 7,88 | 8,20 | 0,32 | 6,84–9,15 |
| São Simão | 1 | 11/11 | 9,70 | 11,44 | 1,74 | 7,75–11,83 |
| Serra Azul | 1 | 10/11 | 1,47 | 1,53 | 0,06 | 0,83–1,64 |
| Serrana | 1 | 11/11 | 3,70 | 4,45 | 0,75 | 3,30–5,69 |
| Sertãozinho | 1 | 11/11 | 7,23 | 9,99 | 2,76 | 6,82–9,99 |
| Guariba | 2 | 11/11 | 4,00 | 4,46 | 0,45 | 3,29–4,71 |
| Jaboticabal | 2 | 11/11 | 5,75 | 6,91 | 1,16 | 5,75–7,22 |
| Monte Alto | 2 | 11/11 | 4,33 | 5,85 | 1,52 | 4,13–7,34 |
| Pitangueiras | 2 | 11/11 | 3,81 | 4,96 | 1,15 | 3,62–5,30 |
| Taiúva | 2 | 11/11 | 3,25 | 3,84 | 0,59 | 2,91–3,84 |
| Taquaral | 2 | 11/11 | 3,47 | 2,66 | -0,80 | 2,57–3,47 |
| Cajuru | 3 | 11/11 | 2,31 | 2,96 | 0,66 | 2,02–3,63 |
| Cássia dos Coqueiros | 3 | 11/11 | 0,42 | 1,06 | 0,64 | 0,42–1,32 |
| Mococa | 3 | 11/11 | 5,21 | 7,82 | 2,60 | 4,43–7,82 |
| Santa Cruz da Esperança | 3 | 11/11 | 1,04 | 0,44 | -0,60 | 0,22–1,04 |
| Santa Rosa de Viterbo | 3 | 11/11 | 3,31 | 4,32 | 1,00 | 2,74–4,89 |
| Tambaú | 3 | 11/11 | 2,26 | 3,24 | 0,98 | 2,00–3,30 |
| Altinópolis | 4 | 11/11 | 2,29 | 3,05 | 0,76 | 2,06–3,76 |
| Batatais | 4 | 11/11 | 4,18 | 4,53 | 0,35 | 3,79–4,87 |
| Morro Agudo | 4 | 11/11 | 2,67 | 5,16 | 2,49 | 2,65–5,16 |
| Nuporanga | 4 | 11/11 | 1,39 | 3,11 | 1,72 | 1,35–4,16 |
| Orlândia | 4 | 11/11 | 4,41 | 5,65 | 1,24 | 3,88–5,76 |
| Sales Oliveira | 4 | 10/11 | 6,28 | 6,60 | 0,32 | 5,09–6,60 |
| Santo Antônio da Alegria | 4 | 11/11 | 0,72 | 3,73 | 3,02 | 0,64–4,73 |

## Como utilizar a série para aperfeiçoar a SWOT

1. O peso do ISS principal em 2025 e sua trajetória de participação em 2015–2025 são **indicadores de estrutura arrecadatória observada**, com maior poder explicativo do que receita tributária total como proxy de ISS.
2. Uma participação do ISS principal elevada ou crescente indica a relevância fiscal corrente do tributo principal; não demonstra necessariamente perda futura com IBS, porque a arrecadação e a repartição mudam por regras próprias, transição e critério de destino.
3. Para oportunidades e ameaças, diferenciar exposição inicial ao ISS da **exposição líquida ao IBS ainda indeterminada**; a frase 'risco de perda' depende de simulação que incorpore distribuição e transição.
4. Para respostas administrativas, propor acompanhamento anual das rubricas ISS e de outros componentes tributários, no horizonte das mudanças institucionais, considerando capacidade de cada prefeitura.
5. Identificar, como pendência própria, ISS total e receitas acessórias ainda não discriminados nesta fonte; nunca preencher ISS total com ISS principal nem extrapolar com fatores inventados.

## Próximo gate

As 34 fichas municipais do Lote 55 devem receber **histórico individualizado do ISS principal** e uma indicação de estabilidade/volatilidade relativa, com anotação de lacunas. As regras transitórias e distributivas do IBS deverão ser examinadas separadamente no Lote 58. O texto não afirma que os cenários fiscais foram recalculados ou que impactos municipais tenham sido medidos.
