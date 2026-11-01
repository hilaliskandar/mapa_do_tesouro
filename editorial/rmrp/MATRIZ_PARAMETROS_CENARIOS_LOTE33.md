# Lote 33 — matriz de parâmetros auditáveis para cenários fiscais 2027–2030

**Data:** 01/11/2026. **Estado:** matriz metodológica e critérios de entrada, sem quantificação de choques ainda não observados. **Fontes já arquivadas:** Lotes 12, 17, 19, 26–32; DCA canônica 2013–2025. Não houve pesquisa externa nesta etapa.

## Unidade de modelagem
34 municípios × 4 anos (2027–2030) × três cenários condicionais, com agregação posterior para a Sub-região de Ribeirão Preto, Sub-região de Jaboticabal, Sub-região de Mococa, Sub-região de Batatais e total RMRP. Não aplicar cenários apenas no agregado e distribuir proporcionalmente, pois isso apagaria diferenças territoriais.

**Base anual observada:** 2025 (DCA), em reais correntes e convertida ao nível de preços de setembro/2026 para a análise real. **Ano de 2026:** dados parciais separados, sem anualização automática. DCA de exercícios anteriores serve para amplitude, volatilidade, teste de sensibilidade e consistência, não como taxa futura garantida.

## Matriz de parâmetros, fonte e porta de validação

| Variável por município e ano | Observação-base já disponível | Parâmetro do cenário | Fonte complementar indispensável | Regra de QA |
|---|---|---|---|---|
| Receita tributária própria | DCA: receita tributária bruta, IPTU, ISS, ITBI | Crescimento real por tributo, explicitamente assumido | séries municipais tributárias e eventual legislação vigente | Conferir principal versus receita total e evitar dupla contagem |
| FPM | DCA: cota mensal FPM | Variação real de repasse, por município | STN/FPM e regras de distribuição | Não confundir FPM com transferências totais |
| ICMS/IPVA e outras transferências | DCA: campos individualizados quando disponíveis | Variação por origem | bases estaduais, DCA e regras atuais de repartição | Separar transferências ordinárias de vinculadas |
| Despesa corrente | DCA: despesa corrente liquidada | Elasticidade por classe ou crescimento real assumido | detalhamento de pessoal, manutenção, contratos, serviços | Não derivar DTP/RCL legal dessas razões |
| Pessoal e encargos | DCA: rubrica liquidada | Crescimento de folha por hipóteses explícitas | RGF/DTP/RCL e regras de carreira | Flag de cobertura: 26/34 para alguns indicadores legais em 2025 |
| Investimentos | DCA: investimentos liquidados | Carteira de execução por projeto e fontes | obras, PAC, convênios, orçamento e restos a pagar | Não projetar apenas média histórica; verificar execução |
| Receitas e transferências de capital | DCA e registros de capital quando completos | Ingressos vinculados e contrapartidas | RREO, Transferegov, contratos de repasse e convênios | Autorização, empenho, repasse e liquidação em estados distintos |
| Caixa e dívida | snapshots RGF/RREO com lacunas | Restrições observadas, sem preenchimento forçado | RGF, RREO, disponibilidade de caixa, CAPAG verificável | Nunca tratar n.d. como zero; Pontal fora de ranking legal sem saneamento |
| População | população DCA município-ano | trajetória demográfica documentada | projeções demográficas oficiais adequadas | Indicador pc usa população do mesmo ano projetado |
| Deflator | IPCA mensal arquivado, base setembro/2026 | inflação condicional explicitada | cenário macro de fonte identificada | Não misturar valores reais e nominais |
| Implementação da reforma tributária | sem estimativa municipal homologada | mecanismos de transição e reação institucional | EC 132/2023 e regulamentação vigente | Sem percentuais municipais de ganho/perda inventados |
| Arcabouço fiscal federal | sem incidência automática demonstrada | hipóteses sobre programas e repasses específicos | LC 200/2023, orçamento/transferências e execução | Não transpor teto federal para despesas municipais |

## Regras de cenarização

- **Adverso:** parâmetros condicionais desfavoráveis somente quando mecanismo e amplitude forem documentados; admite pior execução de carteira e maior pressão de despesa sem imputar corte legal automático.
- **Continuidade:** parâmetros derivados de base observada e projeto/carteira verificável; continuidade não é repetição mecânica da taxa 2015–2025.
- **Favorável:** melhorias comprováveis de arrecadação, repasses e execução de obras condicionadas a capacidades administrativas e fontes de financiamento explícitas.
- **Sensibilidade:** mostrar isoladamente efeito de choques em transferências, tributação, pessoal, custos e carteira de investimentos, sem confundir associação com causalidade.
- **Reconciliação:** soma das projeções municipais por sub-região e metrópole; checar a consistência de fontes vinculadas, componentes tributários, conceitos de despesa e saldo fiscal; nenhuma célula sem fonte deve receber zero arbitrário.
- **Proibição metodológica:** não emitir projeções monetárias quantitativas enquanto parâmetros não forem observados, justificados ou explicitamente definidos como hipóteses testáveis. Nunca chamar cenário de previsão probabilística.

## Pontos de exposição fiscal e investigação

1. **Sub-região de Ribeirão Preto:** maior participação tributária agregada em 2025 (28,89%); examinar exposição de ISS/IPTU/ITBI e concentração em municípios maiores.
2. **Sub-região de Jaboticabal:** maior razão despesas correntes/receita corrente (91,21%) e menor proporção de investimento/receita (2,08%) em 2025; investigar rigidez de gasto e carteira efetiva.
3. **Sub-região de Mococa:** maior participação do FPM entre as quatro (24,06%) e menor receita real por habitante em 2025 (R$ 6.854,98); explorar sensibilidade de transferências e heterogeneidade interna.
4. **Sub-região de Batatais:** maior receita real por habitante (R$ 8.418,05) e maior investimento/receita (3,08%) em 2025, mas redução expressiva de investimento real per capita frente a 2023; verificar volatilidade de obras.

## Gates de conclusão
**E4:** dados DCA e série real consolidados, mas a integração RGF/RREO e casos legais ausentes permanecem pendentes. **E5:** carteira de obras, PAC e repasses de capital carecem de inventário verificado. **E6:** matriz de variáveis e condições concluída neste lote; coeficientes numéricos, dados institucionais, 34 cenários municipais e quatro sub-regionais não homologados. **E8:** redação interpretativa preliminar, ainda sem revisão editorial e validação gráfica final.

**Próximo lote:** produzir dicionário de entradas e esquema tabular dos cenários, marcar campos observados e não disponíveis, testar agregação municipal→sub-região→RMRP, iniciar inventário da carteira de projetos somente a partir de fontes já arquivadas ou mediante autorização para novas consultas.
