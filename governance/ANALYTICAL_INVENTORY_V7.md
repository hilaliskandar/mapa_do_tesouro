# Inventário analítico recuperado do painel v7 e do Bloco 3

## Fontes verificadas

Foram inspecionados os seguintes artefatos:

- `FINBRA_TIC_TIM_30M_PAINEL_FISCAL_INTERATIVO_v7.xlsx`;
- `FINBRA_TIC_TIM_30M_BLOCO3_INDICADORES_TRAJETORIAS_v0_7.xlsx`;
- `FINBRA_TIC_TIM_30M_CONSOLIDADO_CANONICO_v1_0.xlsx`;
- `FINBRA_TIC_TIM_30M_BLOCO4_CONSOLIDADO_v0_2.xlsx`.

## Catálogo anual

O workbook v7 contém **50 contas/agregações**, sendo:

- 40 contas ou agregados diretamente provenientes das fontes integradas;
- 10 agregações analíticas produzidas pelo projeto.

Também contém **25 indicadores anuais documentados**, com fórmula, unidade, fonte, período, leitura, limitações, inputs e regra de ausência.

### Agregações analíticas recuperadas

1. `tributos_imobiliarios` = IPTU + ITBI;
2. `tributos_selecionados` = IPTU + ITBI + ISS;
3. `transferencias_selecionadas` = FPM + ICMS + IPVA;
4. `despesa_territorial` = Urbanismo + Habitação + Saneamento + Gestão Ambiental + Transporte;
5. `servico_divida_liquidado` = Juros e encargos + Amortização da dívida;
6. `receitas_capital_selecionadas` = Operações de crédito + Alienação de bens + Transferências de capital;
7. `despesas_capital_selecionadas` = Investimentos + Inversões financeiras + Amortização;
8. `gasto_social_selecionado` = Saúde + Educação;
9. `saldo_corrente_simplificado` = Receita corrente bruta - Despesa corrente liquidada;
10. `diferenca_capital_selecionada` = Receitas de capital selecionadas - Despesas de capital selecionadas.

## Indicadores anuais recuperados

Além dos indicadores já presentes no catálogo inicial, o v7 registra:

- IPTU, ITBI e ISS per capita;
- FPM, ICMS e IPVA / receita corrente;
- tributos imobiliários / receita tributária;
- transferências selecionadas / receita corrente;
- composição do agregado territorial por Urbanismo, Habitação, Saneamento, Gestão Ambiental e Transporte;
- investimento / receita corrente;
- investimento per capita;
- despesa territorial / despesa total;
- despesa territorial per capita;
- DTP/RCL, DC/RCL, DCL/RCL;
- caixa pós-RPNP/RCL;
- os três componentes oficiais da CAPAG.

## Estatísticas por janela 2021–2025

O Bloco 3 calculou, para diversos indicadores:

- média;
- desvio-padrão;
- coeficiente de variação;
- mudança ponta a ponta;
- amplitude;
- número de anos em valor igual ou superior à mediana do grupo;
- posição relativa pela média.

Essas métricas não devem ser gravadas como se fossem observações anuais. A migration `002_analytical_layers.sql` cria `estatistica_janela` para esse propósito.

## Tipologias transparentes

Foram recuperadas tipologias relativas nas dimensões:

- base tributária;
- investimento;
- gasto territorial;
- DTP;
- DC;
- DCL;
- caixa.

A classificação usa:

- mediana do grupo para nível;
- mediana do coeficiente de variação para estabilidade;
- mínimo de 3 anos observados em 2021–2025;
- ausência preservada;
- nenhum índice sintético.

Essas classificações entram em `classificacao_relativa`, não na tabela de observações anuais.

## Pares comparáveis

O Bloco 3 contém:

- matriz dirigida de pares comparáveis;
- número de dimensões comparáveis;
- número de dimensões coincidentes;
- proporção de coincidência;
- pares prioritários;
- pares recíprocos.

CAPAG é exibida, mas não entra na regra de similaridade. A proporção de coincidência é descritiva e não representa distância econômica ou nota.

Esses resultados entram em `par_municipal`.

## Elementos que não devem ser tratados como dado primário

- `leitura_interpretativa`;
- `sintese_interpretativa`;
- textos narrativos de fichas municipais;
- textos executivos do painel.

Esses elementos devem ser regenerados a partir dos dados e regras vigentes. Podem ser cacheados como artefatos de apresentação, mas não devem se tornar fonte canônica.

## Decisão de migração

**Incluir no núcleo canônico:**

1. as 50 contas/agregações no catálogo de variáveis;
2. os 25 indicadores anuais no catálogo de variáveis;
3. as 10 regras de agregação no pipeline;
4. estatísticas de janela em estrutura própria;
5. tipologias transparentes em estrutura própria;
6. pares comparáveis e prioritários em estrutura própria;
7. regras metodológicas e thresholds no catálogo de governança.

**Não importar como verdade primária:**

1. rankings como avaliação normativa;
2. textos interpretativos;
3. dashboards e tabelas redundantes;
4. cópias dos mesmos indicadores em várias abas.
