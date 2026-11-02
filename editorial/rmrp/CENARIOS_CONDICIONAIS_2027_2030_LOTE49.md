# Lote 49 — Cenários fiscais condicionais 2027–2030 para a RMRP

**Data:** 02/11/2026. **Estado:** capítulo prospectivo qualitativo e matriz de critérios de quantificação; projeções monetárias não homologadas. **Fontes existentes:** Lotes 33, 35, 46 e 48. Nenhuma extração de dados fiscais nesta etapa.

## 1. Escopo, unidade de análise e base temporal

O exercício prospectivo cobre 34 municípios, quatro exercícios (2027, 2028, 2029 e 2030) e três cenários condicionais (adverso, continuidade e favorável). São 408 chaves município-ano-cenário e 60 chaves ano-cenário-território para quatro sub-regiões e RMRP, conforme estrutura validada no Lote 35.

O ano de 2025 constitui a base DCA observada; fluxos reais estão expressos a preços de setembro de 2026, com fator documentado de 1,0541003834032834 para 2025. Dados parciais de 2026 não são anualizados. Séries de 2015–2025 e 2023–2025 sustentam identificação de amplitudes e perfis, não taxas futuras automaticamente replicáveis.

O Lote 35 atesta QA local de cardinalidade e reconciliação, mas alerta que os cinco arquivos gerados naquele ambiente não tiveram persistência externa comprovada. **Nesta etapa não se declara que os CSVs, XLSX ou script de geração estejam depositados no GitHub, Drive ou R2.** O documento é uma especificação editorial e metodológica, não substitui os arquivos da grade.

## 2. Separação de fatos observados, mecanismos e hipóteses

| Dimensão | Evidência-base disponível | Mecanismo condicionado | Limite de inferência |
|---|---|---|---|
| Receita corrente e tributária | DCA municipal 2025 e trajetória histórica | Variação real por componente de arrecadação | Não extrapolar crescimento de 2015–2025 como previsão |
| FPM | Proporção no total das receitas correntes por município | Mudança de base arrecadatória e critérios aplicáveis | LC 200/2023 não implica corte automático de FPM |
| Transferências voluntárias e capital | Fluxos contábeis 2025, sem vínculos projeto a projeto | Seleção, desembolso e contrapartida por instrumento | Não atribuir investimentos a programa sem prova |
| Despesa corrente e pessoal | DCA 2025; RGF/RREO com cobertura parcial | Rigidez de custeio, compromissos e pessoal | Razões DCA não são DTP/RCL legal |
| Investimento | Investimento liquidado 34/34 em 2025 | Carteira verificável, execução física e financeira | Não supor continuidade de obras episódicas |
| Reforma tributária | Corpus normativo do Lote 48 | Regras de transição e repartição do IBS | Sem ganho/perda municipal quantificado |
| Dívida e disponibilidade | Snapshots legais heterogêneos | Restrições de financiamento e caixa | Pontal e casos sem cobertura permanecem segregados |

## 3. Definição operacional dos cenários

**Adverso.** Hipóteses testáveis de menor dinamismo de receitas específicas, crescimento de despesas correntes em ritmo relativamente superior ao das receitas e pior desempenho na execução de projetos cuja carteira e fontes sejam comprovadas. Não pressupõe interrupção geral do FPM, corte obrigatório de investimento ou efeito uniformemente negativo da reforma tributária.

**Continuidade.** Preserva mecanismos efetivamente documentados e condiciona novos dispêndios de capital à existência de projeto, fonte e estágio de execução verificáveis. Não constitui extrapolação mecânica das taxas históricas, nem projeção automática do investimento executado em 2025.

**Favorável.** Considera melhoria documentável de arrecadação em rubricas específicas, melhor execução de projetos com fontes identificadas e condições de custeio compatíveis com obrigações existentes. Não admite ganho uniforme ou imediato de IBS por município sem regra e modelo validado.

Os cenários expressam **condições**, não probabilidades de ocorrência, metas oficiais ou previsão de equilíbrio fiscal.

## 4. Heterogeneidade territorial e eixos de sensibilidade

| Sub-região | Exposição observada | Sensibilidade que deverá ser examinada |
|---|---|---|
| Ribeirão Preto | Receita tributária/receita corrente de 28,89% em 2025 | ISS, IPTU, estrutura econômica e concentração entre polo e municípios menores |
| Jaboticabal | Despesa corrente/receita de 91,21%, investimento/receita de 2,08% | Evolução do custeio, carteira de capital e heterogeneidade entre municípios |
| Mococa | FPM/receita de 24,06%, receita real per capita de R$ 6.854,98 em 2025 | Composição das transferências, demais receitas e variabilidade dos investimentos |
| Batatais | Investimento/receita de 3,08% em 2025, queda real per capita de 51,77% de 2023 a 2025 | Concentração temporal de obras e continuidade de financiamento |

Os indicadores agregados são razões entre somas, não a exposição do município mediano. Cada choque deverá ser especificado no município e agregado posteriormente, mantendo a identidade contábil e a cobertura registrada.

## 5. Regras explícitas de parametrização

Cada variável futura deve registrar: município IBGE, ano, cenário, rubrica, valor observado de 2025, unidade, natureza nominal ou real, fonte, data de referência, hipótese de taxa ou montante, mecanismo de incidência, status de QA, responsável pela revisão e estado de cobertura.

**Estados de informação:** observado, hipótese explicitamente calibrada, não disponível, não aplicável e em revisão. Uma célula sem parâmetro validado permanece vazia; jamais recebe zero técnico. O cenário qualitativo pode ser descrito sem imputação numérica.

**Regras de cálculo quando os dados forem homologados:** (1) calcular componentes da receita e despesa sem dupla contagem; (2) registrar operações anuais e valores de estoque separadamente; (3) manter transferências vinculadas e contrapartidas identificadas; (4) estimar valores per capita apenas com denominador demográfico pertinente; (5) reconciliar município → sub-região → RMRP com tolerância contábil documentada; (6) executar teste de sensibilidade isolando um mecanismo por vez; (7) não converter despesas correntes/receita em saldo financeiro ou índice legal.

## 6. Condicionantes normativas

O âmbito direto da LC 200/2023 é federal, conforme analisado no Lote 48; efeitos municipais requerem programa, dotação, repasse e execução concretos. EC 132/2023, LC 214/2025 e LC 227/2026 compõem o corpus de análise da reforma tributária, mas cronograma e regras aplicáveis ao IBS em 2027–2030 exigem verificação artigo a artigo antes de qualquer percentual municipal. IPTU e ITBI não são assimilados ficticiamente ao IBS.

## 7. Evidências necessárias para avanço numérico

1. Disponibilizar ou recuperar no acervo permanente as bases operacionais efetivamente homologadas de 408 e 60 registros do Lote 35; não reconstruir se já disponíveis.
2. Validar as premissas de receita por componente, regras de repartição e parâmetros econômicos usados nos cenários.
3. Identificar carteira de obras, projetos e convênios por instrumento quando a estimativa envolver investimento vinculado.
4. Revisar RGF/RREO e disponibilidade de caixa por ente, sem extrapolar índices parciais; manter observações anômalas de Pontal em revisão.
5. Testar sensibilidade e reconciliar territorialmente os resultados, documentando cobertura e eventual impossibilidade de quantificação.

## 8. Uso editorial e relação com a etapa E8

O Volume II pode apresentar desde já os três cenários como **narrativas condicionais comparadas**, articuladas às desigualdades fiscais do Lote 46 e às SWOT do Lote 47. Não deve apresentar tabelas com quantias previstas, intervalos monetários ou taxas futuras sem parâmetros verificáveis.

**Situação final do Lote 49:** integração qualitativa e método de parametrização concluídos; quantificação futura e persistência externa do pacote operacional do Lote 35 continuam pendentes de auditoria específica. Próxima entrega: Lote 50, montagem da versão integral do Volume II com integração de capítulos, referências, tabelas e plano de figuras, seguida de revisão metodológica e editorial.
