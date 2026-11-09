# RMSJRP — G06 | Incidência normativa e simulações condicionais 2027–2030
**Data:** 9 de novembro de 2026. **Estado:** primeiro lote quantitativo de cenários executado com QA e persistência R2; não equivale a previsão municipal, estimativa de impacto da LC 200/2023 ou homologação final das premissas. **G06 em andamento — lote numérico experimental aprovado quanto ao cálculo.**

## 1. Critério de interpretação e base normativa atualizada

A Lei Complementar nº 200, de 30 de agosto de 2023, em seu art. 1º, §1º, I, delimita a incidência às receitas e despesas primárias dos orçamentos fiscal e da seguridade social **da União**, não impondo teto municipal automático. No art. 3º, §2º, I, a própria lei exclui da base e dos limites de despesa federais determinadas transferências constitucionais, entre elas as referidas no art. 159 da Constituição; **não é juridicamente adequado simular corte uniforme do FPM por aplicação direta dos limites da LC 200**. A norma também foi alterada por leis complementares posteriores, razão pela qual o texto atualizado, e não apenas o publicado em agosto de 2023, deve orientar a discussão.

Fonte primária: Câmara dos Deputados, [texto atualizado da LC 200/2023](https://www2.camara.leg.br/legin/fed/leicom/2023/leicomplementar-200-30-agosto-2023-794631-normaatualizada-pl.html), arts. 1º, 3º, 4º e 5º, consulta em 09/11/2026. **As taxas de cenário abaixo NÃO são as taxas legais de correção das despesas federais.** O teto da União não foi aplicado às receitas ou aos investimentos municipais.

A repercussão sobre a RMSJRP só será demonstrável caso seja possível identificar **programa federal, orçamento, instrumento de transferência, calendário de desembolso e execução municipal correspondente**. O investimento liquidado TCESP/DCA é observação contábil local; o contrato ou aditivo isolado não estabelece nexo com a LC 200. O G05-D permanece documentalmente aberto.

O [PLOA 2027](https://www.congressonacional.leg.br/web/orcamento/acompanhe/orcamento-anual/-/loa/2027), **PLN 24/2026**, e o [PLDO 2027](https://www.congressonacional.leg.br/web/orcamento/acompanhe/diretrizes-orcamentarias/-/ldo/2027), **PLN 2/2026**, continuavam em tramitação em **09/11/2026**. Fontes: Congresso Nacional, tramitação e cronograma oficiais, consultados nesta data. O Ministério da Fazenda divulgou o limite de despesa primária de R$ 2,576 trilhões para o PLOA 2027, com crescimento nominal de 7,7%, parte real de 2,5%, mas **isso não é uma autorização de dispêndio municipal nem transferência garantida para a RMSJRP**: https://www.gov.br/fazenda/pt-br/assuntos/noticias/2026/setembro/governo-federal-apresenta-projeto-de-orcamento-de-2027-com-previsao-de-superavit-primario-de-r-18-6-bilhoes .

A transição do IBS em 2027–2030 é matéria distinta, a examinar com EC 132/2023, LC 214/2025 e LC 227/2026; **não há percentuais de ganho ou perda municipal de IBS homologados neste projeto**. IPTU, ITBI e FPM não foram substituídos ficticiamente pelo IBS.

## 2. Fontes observadas, parâmetros e horizonte

**Base efetivamente utilizada:** `rmsjrp/g04/2026_11_09/SERIES_MUNICIPAIS_2013_2025.csv` do R2 privado; 37 municípios com informações completas de 2025 para receita corrente, despesa corrente liquidada, investimentos liquidados e cota mensal FPM. SHA-256 do snapshot `1f0413304c54edbe57fe129a506d088da2cd296d767f901992c02f803fbd62e5`. A unidade de preços é **R$ de setembro/2026**, aplicando o fator de IPCA por média anual do G04.

O ano-base observado é **2025**. Os exercícios **2027, 2028, 2029 e 2030** são simulados. Como não existe série anual observada de 2026 homologada, **a passagem de 2025 para 2026 é uma ponte inteiramente hipotética**, usando as mesmas taxas anuais declaradas nos parâmetros. Não foi observado nem publicado qualquer valor anualizado de 2026. Não confundir a simulação com orçamento oficial, projeção populacional ou expectativa probabilística.

Configuração versionada: [`PARAMETROS_G06_2027_2030.json`](PARAMETROS_G06_2027_2030.json); código [`build_cenarios_g06.py`](build_cenarios_g06.py). São **37 municípios × quatro anos × três cenários = 444 linhas municipais** e **(quatro sub-regiões + RMSJRP) × quatro anos × três cenários = 60 linhas territoriais**. Os resultados municipais são calculados primeiro; somatórios sub-regionais e regionais só são apresentados com cobertura completa.

### Hipóteses deliberadamente contrafactuais

| Parâmetro | Adverso | Continuidade | Favorável |
|---|---:|---:|---:|
| Crescimento real anual da receita corrente, inclusive ponte 2026 | **−1,0%** | **+1,5%** | **+3,0%** |
| Crescimento real anual da despesa corrente liquidada | **+2,5%** | **+1,5%** | **+1,5%** |
| Proporção de investimentos na receita corrente em 2030 | **85% da proporção municipal observada em 2025** | **igual à de 2025** | **proporção de 2025 acrescida de 50% da diferença positiva até 2024, se existir** |

Os parâmetros são **hipóteses de tensão e recuperação, e não estimativas econométricas ou extrapolações estatisticamente calibradas**. O cenário favorável usa, para cada município, parte da distância entre a proporção de investimento em 2025 e em 2024; quando a proporção de 2024 é menor, preserva a de 2025, sem forçar reversão. Isso mantém heterogeneidade e evita projetar a mesma razão regional nos 37 municípios. A proporção adversa cai linearmente no horizonte 2025–2030. A continuidade conserva a proporção de 2025, mas permite variar o montante conforme a receita real condicional.

Uma quarta hipótese isolada é **sensibilidade de −10% sobre o FPM real observado em 2025**, por município. Ela **não** é incorporada automaticamente ao total projetado de receita e **não constitui previsão de corte constitucional**, apenas mede a magnitude aritmética de uma perturbação hipotética independente.

## 3. Fórmulas, coerência e limites
Para o município `i`, cenário `s` e ano `t`, com `n=t−2025`:
- `Receita_real(i,s,t) = Receita_real(i,2025) × (1+g_receita_s)^n`.
- `DespesaCorrente_real(i,s,t) = DespesaCorrente_real(i,2025) × (1+g_despesa_s)^n`.
- `RazãoInvestimento(i,s,t)` é determinada pela função linear ou constante de cada cenário e das razões observadas de 2024/2025.
- `Investimento_real(i,s,t) = Receita_real(i,s,t) × RazãoInvestimento(i,s,t)`.
- `Sensibilidade_FPM(i) = −10% × FPM_real_observado(i,2025)`; **não aplicada** como efeito da LC 200.
- `Receita−DespesaCorrente` é **diferença parcial de fluxos contábeis**. **Não é resultado primário, saldo orçamentário, disponibilidade de caixa, teto LRF nem capacidade líquida de investimento**: não abrange todos os ingressos, despesas e operações relevantes.

Os resultados futuros permanecem **sem denominador populacional projetado**, logo não foram calculados investimentos ou receitas futuras per capita. Não se utilizaram classificações CAPAG como multiplicadores, RGF/RREO incompletos como estimativas, nem preços correntes futuros sem caminho de inflação documentado. Programas, obras e transferências de capital são mantidos fora desta primeira modelagem agregada.

## 4. Resultado comparativo experimental em 2030

| Indicador 2030, R$ reais de set./2026 | Adverso | Continuidade | Favorável |
|---|---:|---:|---:|
| Receita corrente, R$ milhões | **7.270,57** | **8.236,12** | **8.862,95** |
| Despesa corrente liquidada, R$ milhões | **7.374,30** | **7.021,53** | **7.021,53** |
| Investimentos liquidados, R$ milhões | **177,28** | **236,26** | **453,27** |
| Investimentos / receita corrente | **2,44%** | **2,87%** | **5,11%** |

**Comparação observada:** em 2025 a receita corrente real regional era R$ **7.645,26 milhões** e os investimentos liquidados reais R$ **219,31 milhões**, com proporção investimento/receita de **2,87%**. Os valores de 2030 acima são **simulações condicionadas às hipóteses**, não receitas ou investimentos previstos em orçamento, não quantificação de perdas causadas pela LC 200, nem promessa de retomada de obras. A diferença parcial receita corrente − despesa corrente no cenário adverso é negativa em 2030; isso sinaliza **tensão interna dos parâmetros selecionados** e **não déficit fiscal oficial**.

As projeções são frágeis a mudanças de taxa, às escolhas da ponte hipotética de 2026 e à não repetibilidade de investimentos extraordinários de 2024/2025. A distância entre cenário adverso e favorável **não deve ser divulgada como montante de investimentos perdido pelo arcabouço**.

## 5. Cobertura, QA e persistência
O workflow [GitHub Actions **42569549086**](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42569549086) executou o processo e concluiu `success`; artifact `13652304360`. QA confirmou:
- 444 chaves município–ano–cenário **distintas**;
- 60 chaves território–ano–cenário, abrangendo quatro sub-regiões e total RMSJRP;
- **37/37** informações observadas de 2025 para receita corrente, despesa corrente, investimento e FPM;
- confrontos aritméticos de agregação das quatro sub-regiões contra a região para todas as rubricas completas, tolerância de até R$ 0,02;
- ausência deliberada de população futura, per capita futuro, efeito atribuído à LC 200 e ganho/perda com IBS;
- readback SHA-256 bem-sucedido de **três objetos** persistidos no R2 privado `rmsjrp/g06/2026_11_09/cenarios_v1/`:
  `G06_SIMULACOES_444_MUNICIPIOS.csv`, `G06_SIMULACOES_60_TERRITORIOS.csv`, `QA_G06.json`.

**Limitação do QA:** um algoritmo aprovado aritmeticamente não valida as hipóteses de crescimento, trajetória de investimentos ou causalidade. A política `strict_complete` mantém ausências como vazios; a comparação regional é soma de linhas completas e percentuais como razão entre somatórios, não média simples dos municípios. Sem reclassificação de FPM como transferências voluntárias.

## 6. Próximos controles antes da homologação substantiva
1. Validar os limites de variação por município, verificar extremos da proporção de investimento de 2024 e executar sensibilidades `±1 p.p.` de crescimento real de receita/despesa; preservar ramos alternativos sem substituir a versão v1.
2. Confirmar as premissas macro e os parâmetros específicos do PLOA/PLDO conforme a aprovação futura; distinguir projeto, autorização e execução. Não converter índices legais do governo central em taxas de crescimento municipais.
3. Identificar carteira de projetos vinculados a repasses federais ou estaduais, transferências voluntárias e contrapartidas para calibrar **apenas** mecanismos efetivamente documentados.
4. Prosseguir na auditoria documental G05-D de Olímpia, Monte Aprazível e São José do Rio Preto; ausência de medição não demonstra ausência de obra. Separar bloco de hipóteses do bloco de conclusões.
5. Acrescentar análise de reforma tributária por fase legal verificável, **sem estimativa monetária municipal por IBS** enquanto não houver dados homologados.
6. Produzir quadro narrativo e matriz de premissas para os 37 municípios após QA de sensibilidade; avançar a G07 com fichas de fatos e diferenciação territorial.
7. Manter os resultados e scripts em GitHub/R2; criar e conferir cópia documental no Drive antes de declarar o pacote editorial final persistido em todos os destinos do plano.

**Status final do lote:** `G06=in_progress`; especificação, simulação 444/60 e QA técnico aprovados; hipóteses ainda não homologadas como previsão. `G05-D=in_progress`; investigação contratual pode continuar em paralelo. Nenhum deploy ou divulgação.
