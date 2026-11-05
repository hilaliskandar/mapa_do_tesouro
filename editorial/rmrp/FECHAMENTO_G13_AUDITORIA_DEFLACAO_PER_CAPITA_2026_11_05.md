# RMRP — G1-3: auditoria da deflação dos investimentos e indicadores per capita, 2023–2025
**Data:** 05/11/2026. **Objeto:** continuação do fechamento G1, sem editar o Volume II (Lote 98, 66 páginas).

## Base e cobertura
A [extração DCA I-D de 2023 e 2024](G13_DESPESAS_INVESTIMENTOS_2023_2024_34_MUNICIPIOS_COMPLETO.csv) abrange 68 de 68 pares município-ano (34 municípios × 2 exercícios). A base de 2025, já aceita no G1-3, foi recuperada do Drive, ID `1RL02DEObzOQaehQeQzffdjjc1vswWpQm`. A [série real municipal](G13_SERIE_REAL_INVESTIMENTOS_DESPESAS_2023_2025_34_MUNICIPIOS.csv) tem 102 de 102 registros e nenhuma rubrica ausente; a [agregação por sub-região](G13_AGREGADOS_REAIS_TRIENAIS_SET2026.csv) contém 15 linhas (5 recortes × 3 exercícios).

## Método e fontes
- Siconfi, DCA Anexo I-D, conta `DO3.0.00.00.00.00` para despesa corrente e `DO4.4.00.00.00.00` para investimentos; coluna **Despesas Liquidadas** (nem empenhadas nem pagas). Fontes individuais no CSV.
- IPCA: Lote 17 `editorial/rmrp/IPCA_MEDIA_ANUAL_SET2026_LOTE17.md`, SIDRA 1737, média aritmética dos 12 números-índice mensais: **2023 6661,1500; 2024 6952,0733; 2025 7300,8417**. Referência documental setembro/2026: **7695,82**. Fator = 7695,82 / média anual. Média anual calculada com precisão de trabalho, arredondamento somente na apresentação.
- População: campo `populacao` dos próprios demonstrativos DCA. Valores por habitante calculados sobre soma de população municipal no respectivo ano; não implicam validação autônoma da série demográfica do IBGE.

## Conciliação metropolitana (preços de setembro/2026)

| Ano | Investimento liquidado nominal R$ | Investimento liquidado real R$ | Investimento real per capita, R$ |
|---|---:|---:|---:|
| 2023 | 484.948.399,24 | 560.274.966,01 | 319,24 |
| 2024 | 500.824.152,06 | 554.403.318,42 | 335,91 |
| 2025 | 302.301.895,18 | 318.656.543,61 | 193,07 |

**Variação real 2023–2025 pelo IPCA médio anual: -43,1250%.** Série baseada em IPCA dezembro, anteriormente apresentada no Volume I, resulta em **-42,9680%**. Não misturar métodos nem substituir automaticamente o valor publicado. Para fluxos anuais, o método da média anual é a convenção analítica preferencial do projeto, sujeita a decisão editorial final.

| Recorte | Variação real investimento 2023–2025 |
|---|---:|
| RMRP | -43,12% |
| Sub-região de Ribeirão Preto | -38,82% |
| Sub-região de Jaboticabal | -55,29% |
| Sub-região de Mococa | -24,31% |
| Sub-região de Batatais | -56,50% |

Todos os cinco agregados de investimento para 2023, 2024 e 2025 (15 comparações) reproduzem o Lote 19 até arredondamento de centavos. Valores reais per capita dos cinco recortes em 2023–2025 também coincidem ao centavo com o Lote 19.

## Divergência nova localizada
No exercício de **2024**, a despesa corrente **real** da sub-região de Batatais calculada a partir da extração direta atual totaliza **R$ 1.209.882.136,00**, enquanto o Lote 19 registra **R$ 1.213.203.081,98**: diferença de **R$ 3.320.945,98** (equivalente aproximadamente a R$ 3,0 milhões nominais). O total real metropolitano de despesa corrente calculado nesta coleta é **R$ 10.818.038.160,32**, enquanto o Lote 19 informa **R$ 10.821.359.106,30**. **Origem municipal identificada após nova conciliação:** Batatais, código IBGE 3505906, exercício 2024. A base canônica histórica DCA SP645 (Drive ID `1BtXY_FxydMREEbMACJtaoW2n24ohVH33`) contém despesa corrente liquidada nominal de **R$ 298.950.495,51**, enquanto a extração atual da API Siconfi DCA Anexo I-D apresenta **R$ 295.950.495,51**. Diferença exata de **R$ 3.000.000,00 nominais**; atualizada pelo fator médio de 2024 equivale a **R$ 3.320.945,98**, explicando integralmente a diferença sub-regional/metropolitana. O confronto de **204 valores** (102 município-ano × 2 rubricas, despesa corrente e investimento) entre a base canônica histórica e a extração atualmente recuperada encontrou **203 coincidências e apenas essa divergência**. A mudança do valor está demonstrada entre bases, mas sua causa e o status de eventual retificação **ainda não foram comprovados**. Não substituir o número antigo silenciosamente nem afirmar homologação definitiva da despesa corrente de 2024.

## QA populacional
- Os 34 municípios têm a **mesma população registrada na DCA de 2024 e 2025**, ao passo que todos diferem entre 2023 e 2024. Isso explica a mudança de denominadores na série, mas não demonstra que a convenção DCA seja uma série demográfica anual independente.
- O arquivo FINBRA_PARTE5 (aba METODOLOGIA) registra uma convenção IBGE distinta: estimativas e Censo 2022, conforme o ano. Seus denominadores não foram incorporados silenciosamente aos cálculos desta rodada.
- Valores reais por habitante **reproduzidos** com população DCA permanecem candidatos à comparação histórica, mas o aceite de sua interpretação populacional depende de cotejo com série IBGE canônica.

## Decisão de gate
- **Aprovado:** completude 102/102; despesa/investimento nominal extraído; investimento real e índices de investimento per capita recalculados; conciliação dos 15 agregados reais de investimento com o Lote 19.
- **Pendente:** resolução da divergência de despesa corrente de Batatais/2024, auditoria da série populacional IBGE, conferência das afirmações nas SWOT e de todos os mapas, confirmação final da convenção editorial do deflator.
- **Volume II:** preservar o Lote 98 e os documentos do G0; não declarar homologação final de G1 nem circulação externa.

## Fontes
1. https://apidatalake.tesouro.gov.br/ords/cdwhprd/siconfi/tt/dca
2. https://sidra.ibge.gov.br/tabela/1737
3. https://docs.google.com/spreadsheets/d/1ZiX9B2qgkUFcqibztgvGgvMdScqJGOvKLgL5nZfq6_I/edit
4. https://github.com/hilaliskandar/mapa_do_tesouro/blob/main/editorial/rmrp/IPCA_MEDIA_ANUAL_SET2026_LOTE17.md
5. https://github.com/hilaliskandar/mapa_do_tesouro/blob/main/editorial/rmrp/SERIES_REAIS_SUBREGIOES_NOMEADAS_2013_2025_LOTE19.md

## Registro adicional de conciliação canônica
Teste direto de chaves `(cod_ibge, ano, rubrica)` entre os arquivos oficiais atuais 2023–2025 e `DCA_SP_645_2013_2025_CANONICO.csv` (Drive ID `1BtXY_FxydMREEbMACJtaoW2n24ohVH33`): **204 comparações**, das quais **203 idênticas ao centavo** e **uma com diferença**, referente à despesa corrente de Batatais em 2024. Não há diferenças nos investimentos liquidados examinados. Esse achado delimita a investigação residual à genealogia e eventual retificação da rubrica municipal, em vez de revisar toda a série.
