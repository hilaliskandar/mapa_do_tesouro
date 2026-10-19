# Matriz de aderência — Nota Técnica fiscal TIC–TIM v1.3 × RMRP × acervo FINBRA/SCN

Data da revisão: 19/10/2026. **Estado: diagnóstico documental inicial, não execução integral dos indicadores.** Objetivo: utilizar a nota técnica como contrato analítico sem ignorar os procedimentos canônicos já consolidados. Distinção obrigatória: a nota trata do corredor TIC–TIM e de cerca de 72 conceitos, enquanto o estudo atual cobre 34 municípios da RMRP em quatro sub-regiões. Não confundir os universos ou transportar resultados sem recalcular.

## Fontes examinadas

- [Nota Técnica v1.3](https://docs.google.com/document/d/1SvarT65MQMU-qmpjqFzxLjf0d4uKkXpkegmjVCIJZ14/edit), roteiro conceitual dos blocos 3–11, ITBI, cobertura, matriz de 72 variáveis e indicadores.
- [Caderno metodológico consolidado FINBRA TIC–TIM](https://docs.google.com/document/d/1ak4JsDeXaAG2eIsqiJJS-y4T25wBa14YrBQ7yA73PUA/edit), incluindo gates A1–A11 e frente B; regras de qualidade, cruzamento contábil, indicadores calculáveis e produtos não defensáveis.
- [README operacional](https://docs.google.com/document/d/1RQM0fxV2DK__nxfpfBHeWdO0SgySG5Q6-FugZWjQ8U0/edit), preservar proveniência e evitar regressões.
- [IBGE SCN, Nota Metodológica nº 02 — estrutura](https://drive.google.com/file/d/1TgAEWJuNB1ZRdjNJURynD7a3NQTliuXs/view), referências da estrutura integrada e consistência entre contas econômicas.
- [IBGE, Sistema de Contas Nacionais, 2004](https://drive.google.com/file/d/1IfsVzeps-xeFCr2qptYTv-w0E7tLVcem/view): referência conceitual histórica, não base para transposição automática de classificações orçamentárias municipais.
- [DCA SP645 canônica 2013–2025](https://drive.google.com/file/d/1BtXY_FxydMREEbMACJtaoW2n24ohVH33/view): amostra RMRP 34 municípios, com 25 contas originais sintéticas na exportação usada.
- [Documentação já consolidada para RMRP](https://github.com/hilaliskandar/mapa_do_tesouro/tree/main/editorial/rmrp): séries nominais e reais, decomposição municipal de investimento, RGF/RREO/CAPAG parcial e quatro sub-regiões.

**Sobre SCN:** O Sistema de Contas Nacionais é arcabouço de contas integradas sobre produção, renda, acumulação, patrimônio e setores institucionais. Sua estrutura ajuda a distinguir fluxos e estoques e a manter categorias coerentes. **Não autoriza equiparar** automaticamente investimento liquidado do grupo de natureza 4.4 da DCA à formação bruta de capital fixo do SCN; tampouco autoriza tratar saldo orçamentário de receitas e despesas correntes como capacidade de financiamento SCN. Essas aproximações precisam ser explicitamente qualificadas.

## Aderência por bloco analítico

| Bloco da nota | Produtos e indicadores | Situação na RMRP | Complemento necessário | Restrição e fonte |
|---|---|---|---|---|
| 1. Cobertura/qualidade | Município-ano, população, QA, revisão e transição 2018–19 | Parcial: 34 × 13 DCA, cobertura registrada | Incorporar qualidade Siconfi, revisão e flags temporais ano a ano; certificar população por município | Não converter ausente em zero; não explicar rupturas automaticamente pelo ementário |
| 2. Autonomia e receitas próprias (17 conceitos) | IPTU, ISS, ITBI, taxas, melhoria, IRRF, contribuições, receita própria, autonomia estrita/ampliada/econômica | Parcial: IPTU, ISS, ITBI principais e tributária DCA, participação observada | Reutilizar crosswalk FINBRA para taxas, melhoria, IRRF, contribuições, patrimônio, serviços, custo administrativo; RCL oficial onde existir | Denominador RCL não é automaticamente receita corrente DCA; caixas ampliados IPTU/ITBI não implementáveis defensavelmente para série 2013–25 |
| 3. Transferências (10) | FPM, ICMS, IPVA, ITR, FUNDEB, SUS, assistência, transferências de capital, dependência, HHI | Parcial: FPM, ICMS, IPVA e transferências de capital na base DCA | Reaproveitar componentes FUNDEB desagregados, subcomponentes SUS/assistência com hierarquia validada, dependência e HHI apenas sobre fontes mutuamente exclusivas | Não reconstruir FUNDEB agregado ou somar SUS/assistência sem exclusividade comprovada |
| 4. Equilíbrio e rigidez (10) | Poupança corrente, pressão, pessoal, custeio, previdência, custo administrativo | Parcial: receita corrente, despesa corrente, pessoal 3.1 e razões agregadas | Ajustes intraorçamentários e deduções, custeio, previdência, função Administração; RGF Anexo 01 para DTP/RCL | DCA 3.1 liquidado é proxy, não indicador legal de pessoal |
| 5. Investimento/execução (14) | 4.4, 4.5, investimento amplo, per capita, liquidação, pagamento, fontes extraordinárias, médias, persistência/volatilidade | Parcial: 4.4 liquidado 2013–25, renda relativa e variações reais; ações TCESP 2023–25 | Recuperar estágios empenhado e pago e 4.5 da base granular validada; calcular médias móveis 3 anos, dispersão de 5 anos e persistência com coverage flags | 4.5 tem cobertura baixa no acervo TIC–TIM; operações de crédito + alienações + transf. capital são exposição potencial, não financiamento demonstrado |
| 6. Dívida, restos e liquidez (6) | Juros + amortização/RCL; caixa líquido, obrigações, restos a pagar | Parcial: juros e amortização DCA quando informados; RGF 2025 incompleto | Usar RGF Anexos 02, 05 e RREO 03 segundo vigência, com estágio/documento apropriados | Diferença entre empenhado e pago não é estoque oficial de restos a pagar |
| 7. Funções territoriais (7) | Urbanismo, habitação, saneamento, ambiente, transporte; esforço e diversidade | Parcial: funções DCA, cobertura variável | Fazer painel de cobertura e calcular agregado apenas quando todas cinco funções observadas ou hierarquia reconciliada | Função não determina se despesa é investimento; SCN não permite ligação função × elemento inexistente na fonte |
| 8. ITBI / mercado | ITBI real/per capita, % RCL/tributária, média móvel 3a, volatilidade 5a e referências complementares | ITBI principal DCA presente; não há módulo derivado completo RMRP | Computar com datas/coverage, RCL oficial e série IBGE de população | ITBI não é número de transações ou valorização imobiliária |
| 9. Série temporal 2013–25 | Crescimento real, mediana 3a, volatilidade 5a, quebras 2018–19, mandatos completos | Real nominais atualizados e 2023–25 comparados | Reaproveitar critérios A7/A9 de janelas consecutivas e mínimo de observações; diferenças por porte, sub-região | 2025 não integra mandato completo 2021–24; não inferir efeitos eleitorais |
| 10. Diagnóstico municipal e regional | Perfis, medianas, quartis, tipologias, sub-regiões, diferenciais | 34 fichas e 4 sub-regiões disponíveis em edição candidata | Substituir texto repetitivo por perfis fundamentados nos indicadores adicionais e status de cobertura; validar páginas e remissões | Somar contas com cobertura parcial não fornece total da região |
| 11. Referenciais | IFGF, CAPAG, solvência caixa/orçamentária/serviços/LP | Distribuição CAPAG snapshot 2025 e proxies DCA | Nota CAPAG oficial, DTP legal, liquidez e dívida por demonstrativos completos | Não produzir escore único nem reproduzir IFGF/CAPAG com denominadores não equivalentes |

## Gates de fonte e comparabilidade

1. **SCN ↔ contabilidade pública:** publicar conceitos lado a lado e ponte interpretativa, sem equivalência automática entre grupo 4.4 e formação bruta de capital fixo, e entre liquidação e produção/entrega física.
2. **Finbra semântico:** preservar pai/filhas, conta terminal, estágio, dedução, intraorçamentárias e ementário por vigência. O histórico TIC–TIM A8 concluiu que o caixa ampliado de IPTU e ITBI não pode ser reconstruído defensavelmente nos treze anos com a DCA disponível.
3. **RCL e pessoal:** utilizar RREO Anexo 03 (RCL oficial) e RGF Anexo 01 (DTP legal), sem substituir por receita corrente bruta ou grupo 3.1 da DCA.
4. **CAPAG:** valor oficial canônico do Tesouro; simulações locais como QA apenas. Cobertura parcial da RMRP deve ser comunicada.
5. **Geografia:** manter 34 municípios e suas quatro sub-regiões, inclusive nas médias/medianas, gráficos e regras de avaliação de completude.
6. **Preços:** a nota técnica usou junho/2026 como data-base em sua origem; o caderno RMRP já adotou setembro/2026. Conservar a regra matemática, identificar alteração de data-base na edição e jamais comparar magnitudes monetárias deflacionadas por bases distintas.
7. **Ordem de trabalho:** reutilizar produtos prontos, mapear cada conceito à coluna/crosswalk e estágio, calcular módulos viáveis, registrar lacunas formais, submeter QA e integrar ao caderno sem refazer o motor fiscal.

## Prioridade de execução

- **Imediata — inteiramente DCA/IBGE, após verificar dados completos:** módulo ITBI (principal) em 2013–25, médias móveis e volatilidade; desagregar autonomia por IPTU/ISS/ITBI e transferência FPM/ICMS/IPVA; decomposição de pressão e poupança correntes; séries de concentração e dispersão municipal por sub-região.
- **Seguinte — dados granulares já mapeados, exige junção auditada:** fontes da receita próprias completas; transferências especiais e finalísticas; empenhado/liquidado/pago de investimentos; custo administrativo e funções.
- **Dependente de demonstrativos adicionais:** RCL e DTP legal, caixa, restos a pagar, dívida, CAPAG e IFGF rigorosos.
- **Documentação regional:** perfis municipais e análise regional, tabelas de conceitos/fontes/cobertura, diagrama de contas e 50 perguntas com referências a páginas verificadas apenas depois de fechar a paginação.

Este arquivo registra o inventário metodológico. **Não afirma que os cerca de 72 indicadores já foram calculados para os 34 municípios**.
