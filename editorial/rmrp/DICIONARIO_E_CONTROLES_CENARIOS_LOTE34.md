# Lote 34 — dicionário de entradas e controles de cenários 2027–2030

Data: 01/11/2026. Fonte metodológica: Lote 33; cadastro territorial municipal existente; DCA canônica 2013–2025. Estado: especificação operacional versionada, **sem projeções numéricas homologadas**.

## Chaves e cardinalidade

A chave única de cenário municipal é `codigo_ibge;ano_cenario;cenario`, com 34 municípios × 4 exercícios (2027, 2028, 2029, 2030) × 3 cenários (adverso, continuidade, favorável) = **408 linhas esperadas**. O cadastro dos 34 municípios determina quatro grupos: Sub-região de Ribeirão Preto (15), Sub-região de Jaboticabal (6), Sub-região de Mococa (6) e Sub-região de Batatais (7). Para cada ano e cenário, devem ser produzidos quatro agregados sub-regionais e um metropolitano, isto é, 5 × 4 × 3 = **60 linhas de agregados**. Agregados jamais são computados pela média simples de quocientes.

## Esquema tabular do painel

| Campo | Tipo | Unidade / domínio | Procedência | Controle |
|---|---|---|---|---|
| codigo_ibge | texto | 7 dígitos | cadastro municipal versionado | obrigatório e único na combinação |
| municipio | texto | nome oficial | cadastro | ligação 1:1 por código |
| subregiao_nome | texto | um dos quatro nomes completos | cadastro | somas em grupos de 15, 6, 6 e 7 |
| ano_cenario | inteiro | 2027 a 2030 | grade da simulação | obrigatório |
| cenario | categoria | adverso, continuidade, favorável | grade | obrigatório |
| preco_base | texto | setembro/2026 | protocolo Lote 17 | não misturar moeda real/nominal |
| receita_corrente_2025_real | número anulável | R$ set/2026 | DCA 2025 + IPCA | base observada, nunca projetada |
| receita_tributaria_2025_real | número anulável | R$ set/2026 | DCA 2025 + IPCA | distinguir total de principal |
| fpm_2025_real | número anulável | R$ set/2026 | cota mensal FPM da DCA | não equiparar a todas transferências |
| despesa_corrente_2025_real | número anulável | R$ set/2026 | DCA liquidada 2025 | conceito contábil específico |
| pessoal_2025_real | número anulável | R$ set/2026 | DCA pessoal e encargos liquidados | não confundir com DTP/RCL |
| investimento_2025_real | número anulável | R$ set/2026 | DCA investimento liquidado | não confundir com empenhado/pago |
| populacao_2025 | inteiro anulável | habitantes | DCA | denominador de referência |
| crescimento_real_tributos | decimal anulável | fator anual | parâmetro documentado | não imputar taxa sem fonte |
| crescimento_real_transferencias | decimal anulável | fator anual | parâmetro documentado | separar FPM e demais fontes |
| crescimento_real_despesa | decimal anulável | fator anual | parâmetro documentado | decompor pessoal e demais classes |
| aporte_capital_vinculado | decimal anulável | R$ set/2026 | convênio/carteira verificados | registrar objeto, fonte, fase e ano |
| investimento_execucao | decimal anulável | R$ set/2026 | projetos e cronogramas | condicionado a capacidade de execução |
| receita_corrente_projetada | decimal anulável | R$ set/2026 | fórmula | deixar nulo sem hipóteses |
| despesa_corrente_projetada | decimal anulável | R$ set/2026 | fórmula | deixar nulo sem hipóteses |
| investimento_projetado | decimal anulável | R$ set/2026 | fórmula condicionada | não usar receita menos despesa como investimento automático |
| populacao_projetada | inteiro anulável | habitantes | projeção fundamentada | não repetir 2025 inadvertidamente |
| receita_real_pc_projetada | decimal anulável | R$/hab | quociente, se ambos disponíveis | divisor >0 |
| investimento_real_pc_projetado | decimal anulável | R$/hab | quociente, se ambos disponíveis | divisor >0 |
| status_parametro | categoria | observado, hipótese documentada, pendente, inaplicável | QA | nulo permanece nulo |
| fonte_parametro | texto | URL/caminho + data | proveniência | obrigatório se valor futuro não nulo |
| ressalvas | texto | livre | auditoria | flag RGF/RREO, Pontal, capital |

## Operações e validação

1. Construir uma grade de 408 linhas a partir dos códigos IBGE; **não** preencher valores futuros por padrão.
2. Juntar apenas as variáveis-base observadas de 2025, com fonte e data. Ausente ≠ zero.
3. Juntar hipóteses de cenário apenas quando documentadas, diferenciando variável exógena, resposta municipal e execução de projetos.
4. Derivar valores monetários projetados por fórmulas reproduzíveis, distinguindo taxas de crescimento real de valores absolutos, e controlando os anos 2027–2030 sem anualizar 2026.
5. Agregar fluxos monetários por soma apenas se a cobertura esperada estiver completa; uma ausência em município bloqueia o total da variável e exige quadro de cobertura explícito.
6. Agregar população por soma e indicadores per capita por quociente de somas; **não** somar nem tirar médias simples de razões.
7. Reconciliar a soma das quatro sub-regiões com a RMRP para cada combinação de ano, cenário e variável monetária completa. Tolerância de arredondamento explicitada em centavos.
8. Manter indicadores legais RGF/RREO separados: cobertura incompleta em alguns campos (26/34); anomalia de Pontal fora de inferência legal até saneamento. Não há presunção de exposição ao arcabouço federal.

## Gate e continuidade

E6: **dicionário e esquema de controle definidos**. Cálculos de cenários, parâmetros quantificados e integração com carteira de investimentos **pendentes**. Próximo lote: construir grade física 408 linhas, catálogo de ausências e teste de agregação em uma base tabular; persistir resultado e atualizar README e plano.
