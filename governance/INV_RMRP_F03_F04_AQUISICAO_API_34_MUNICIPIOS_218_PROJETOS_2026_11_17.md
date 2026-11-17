# F03/F04 — aquisição direta da API: Transferências Especiais, Gestão de Parcerias e Obrasgov

**Data:** 17/11/2026. **Escopo:** valores e metadados financeiros por beneficiário, proposta e projeto, **sem reconciliação aprofundada**, sem localização física, sem dossiês de obra e sem deploy público. **Fontes:** APIs oficiais `api-publica.transferegov.gestao.gov.br` e `api-publica.obrasgov.gestao.gov.br`; consultas reais via Crawl2AI, não inferências a partir do README. `public_release_authorized=false`.

## 1. Transferências Especiais — planos de ação

A API `/especiais/beneficiarios-especiais?uf_beneficiario=SP` retornou **628 beneficiários** paulistas em quatro páginas de 200/200/200/28. A identificação nominal com os 34 municípios IBGE7 da RMRP resultou em **34 correspondências**, com ID oficial `id_beneficiario`. Para cada uma das 34, foi consultado:
`/especiais/planos-acao-especiais?id_beneficiario={id}&pagina=1&tamanho_da_pagina=200`.

**Resultado:** 34/34 consultas, todas com `total_pages=1` e `len(data)=total_items`: **284 planos de ação, 284 IDs únicos, exercícios 2020–2026**. Valor de `valor_investimento_plano_acao` = **9.304.632.506 centavos (R$ 93.046.325,06)**; valor de `valor_custeio_plano_acao` = **325.700.000 centavos (R$ 3.257.000,00)**. São **valores de planos** e não pagamentos realizados ou investimentos liquidados.

| Exercício do plano | Planos | Investimento previsto (R$) | Custeio previsto (R$) |
|---:|---:|---:|---:|
| 2020 | 18 | 3.620.000,00 | 180.000,00 |
| 2021 | 23 | 6.059.993,00 | 0,00 |
| 2022 | 49 | 13.748.047,00 | 0,00 |
| 2023 | 60 | 17.230.022,00 | 300.000,00 |
| 2024 | 45 | 19.361.585,00 | 790.000,00 |
| 2025 | 56 | 19.494.678,06 | 594.000,00 |
| 2026 | 33 | 13.532.000,00 | 1.393.000,00 |

**Arquivos:** `governance/controls/investimentos_sp645/RMRP_ESPECIAIS_PLANOS_2026_11_17_B01.csv` a `B06.csv`. Cada linha contém IBGE7, ID oficial do plano, ID beneficiário, exercício, situação e valores separadamente, em centavos, mais URL exata da consulta. Nenhum campo de conta bancária nem informação pessoal foi copiado dos JSON originais.

## 2. Gestão de Parcerias — propostas

A API `/parcerias/proposta?cd_ibge_recebedor={ibge7}&pagina=1&tamanho_da_pagina=200` foi consultada para **34/34 municípios**. Todas as respostas declararam **uma página e contagem retornada igual à contagem total**. Foram recuperadas **743 propostas com 743 IDs distintos** — cobertura de propostas, não de instrumentos e pagamentos.

**Campo `nr_vlr_total`:** `null` em **743/743** registros; **não há valor total de proposta disponível neste campo** na fotografia.

**Campo `vl_total_planejamento_gastos`:** preenchido em **672/743** propostas, soma aritmética dos valores **25.647.378.783 centavos = R$ 256.473.787,83**. Os **71 registros sem valor** permanecem nulos (não zeros), e a soma disponível é **parcial, planejada, sem exclusão por situação ou categoria**. Não representa transferência federal desembolsada nem somente investimento de capital. A fonte registra situações: **663 Aprovada, 29 Em Análise, 31 Em Elaboração, 18 Rejeitada, 2 Inativada**.

| Ano da proposta | Propostas | Com valor de planejamento | Soma disponível (R$) |
|---:|---:|---:|---:|
| 2024 | 14 | 10 | 34.014.051,07 |
| 2025 | 335 | 299 | 131.413.436,49 |
| 2026 | 394 | 363 | 91.046.300,27 |

A identificação dos recebedores compreende entidades diversas, não necessariamente prefeituras; a localização `cd_ibge_recebedor` **não prova transferência municipal contabilizada**. A categorização prévia das propostas (94 investimento, 588 custeio, 59 misto e duas indefinidas) deve permanecer separada até conferência com o contrato de classificação.

**Arquivos:** `governance/controls/investimentos_sp645/RMRP_PARCERIAS_PROPOSTAS_VALORES_2026_11_17_B01.csv` a `B06.csv`, preservando município, ID da proposta, ano, situação, campos `nr_vlr_total` e `vl_total_planejamento_gastos` em centavos quando presentes, categoria da fonte e URL.

## 3. Obrasgov — valor previsto por projeto

A partir dos **218 IDs únicos de projetos** do staging RMRP FED08B, registrados em `governance/controls/investimentos_sp645/RMRP_OBRASGOV_218_IDS_2026_11_17.csv`, foram recuperadas individualmente 218 fichas via:
`/obras/projeto-investimento?id_projeto_investimento={id}&pagina=1&tamanho_da_pagina=5`.

**Resultado:** **218/218 fichas únicas**, sem falhas e sem campos monetários vazios na lista `investimentos_previstos`. Cada ficha retornou **uma linha de financiamento classificada como `Federal`**, valor `vl_investimento_previsto`. **Soma aritmética dos valores previstos dos 218 candidatos: 41.653.125.299 centavos = R$ 416.531.252,99**.

| Ano de cadastro do projeto | Projetos | Soma de valores previstos (R$) |
|---:|---:|---:|
| 2022 | 33 | 19.093.605,30 |
| 2023 | 53 | 105.684.583,60 |
| 2024 | 51 | 163.307.195,95 |
| 2025 | 31 | 83.409.159,00 |
| 2026 | 50 | 45.036.709,14 |

**Não confundir ano de cadastro com exercício do gasto.** São projetos ligados a proponentes dos municípios da RMRP, não o universo comprovado de obras localizadas dentro da RMRP. A fonte de financiamento `Federal` é rótulo cadastral e os valores **podem estar duplicados** nos instrumentos Transferegov; **não somar** a outros montantes até etapa de deduplicação posterior.

**Arquivos:** `governance/controls/investimentos_sp645/RMRP_OBRASGOV_VALORES_PREVISTOS_2026_11_17_B01.csv` a `B11.csv`, cada registro com ID, ano de cadastro, situação, sistema, fonte e valor em centavos, estado de aquisição, URL oficial.

## 4. Interpretação, rastreabilidade e próximos dados

**Três medidas distintas sem totalização entre fontes:**
- Especial: valor de plano de ação de investimento (R$ 93.046.325,06).
- Gestão de Parcerias: valor disponível de planejamento de gastos, misturando categorias e status (R$ 256.473.787,83 para 672 propostas).
- Obrasgov: valor de investimento *previsto* em 218 projetos (R$ 416.531.252,99).

**Não somar os três valores**, nem com os desembolsos/convênios D/L do FED08B, contratos CIPI, SIAFEM estadual ou despesas municipais FINBRA/TCESP. Nenhuma dessas três somas é pagamento federal líquido ou investimento executado.

**Aquisição ainda não compilada neste ciclo:** eventos efetivos de **empenho/OB/DH das Especiais** vinculados aos 284 planos; pares `id_proposta -> id_parceria -> id_documento_habil -> id_op` e valores da Gestão de Parcerias; demais modalidades Fundo a Fundo/TED pertinentes; atualização incremental e módulos de execução financeira Obrasgov (a última consulta global em 16/11 retornara zero para contrato/empenho/execução, não inexistência de obras).

**Infraestrutura:** o acesso oficial por Crawl2AI permitiu aquisição real das fichas; o workflow novo `.github/workflows/rmrp-obrasgov-planned-values-r2.yml` e coletor Python foram preparados para preservação futura em R2, porém **o dispatch do workflow novo retornou 404 porque não está registrado como executável no catálogo de workflows da branch padrão**. Não houve execução desse workflow nem upload dos novos JSON brutos no R2. As séries filtradas e URLs oficiais foram efetivamente preservadas em CSVs na branch de desenvolvimento, sem publicação no site.

## 5. Próximo passo recomendado

Agora que **planos Especiais e projetos Obrasgov estão todos presentes com valores previstos**, priorizar consulta de valores de **empenhos e ordens bancárias** dessas modalidades, e eventos financeiros efetivos de Parcerias. Manter a ordem documental dos IDs, sem imputar valor zero a registros sem campo, sem reabrir reconciliação e sem alterar banco fiscal ou plataforma pública.

