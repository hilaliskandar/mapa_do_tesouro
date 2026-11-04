# Lote 94 — Deflação da receita de capital da RMRP (2015–2025) e QA de demonstrativos

**Data:** 04/11/2026. **Estado:** componente de deflação e QA de fórmula **executado e validado**; **não** implica homologação fiscal ou editorial do Volume II.

## 1. Objeto e fontes

Continuidade dos Lotes 92 e 93. Foram mantidos 34 municípios, onze anos e 374 chaves município–ano na série sintética **receitas de capital brutas realizadas** da DCA Anexo I-C do Siconfi, mantendo 369 observações (98,66%) e 5 lacunas documentadas. Origem: planilha auditada Lote 93 (Drive ID `1OUjD12f46k7EZQ44FCyNLb-GhesCbUk7`) e registros do Lote 38 para 2015–19. O valor de 2024 foi corrigido no Lote 93 com Cajuru e Morro Agudo, total R$363.799.964,55.

**Fonte do deflator:** IBGE/SIDRA, **tabela 1737, variável 2266**, IPCA Brasil, *número-índice mensal, base dezembro de 1993 = 100*. Foram consultados diretamente via Crawl2AI os três intervalos oficiais:
- https://apisidra.ibge.gov.br/values/t/1737/n1/all/v/2266/p/201501-201912?formato=json
- https://apisidra.ibge.gov.br/values/t/1737/n1/all/v/2266/p/202001-202312?formato=json
- https://apisidra.ibge.gov.br/values/t/1737/n1/all/v/2266/p/202401-202512?formato=json

**Cobertura do deflator: 132 índices mensais de jan./2015 a dez./2025, 12 por ano**, sem imputação. Índice médio anual de 2025 = **7.300,84166667**. Para cada exercício `t`, adotou-se: `IPCA_medio_t = MEDIA(IPCA_jan_t ... IPCA_dez_t)`; `fator_t = IPCA_medio_2025 / IPCA_medio_t`; `receita_capital_real_t = receita_capital_bruta_nominal_t * fator_t`. Unidade: **R$ a preços médios de 2025**. Não confundir com deflação a **dezembro de 2025**, que utiliza índice de fim de período e pode servir a estoques ou a cartografia específica.

O procedimento usa o mesmo deflator para todos os municípios em um dado ano. **Não se imputou valor à conta ausente.** Valores anuais não constituem estimativas dos períodos sem cobertura integral.

## 2. Série agregada resultante

| Ano | Observações | Receita nominal observada (R$) | Receita real observada (R$ médios 2025) | Fator 2025/ano |
|---|---:|---:|---:|---:|
| 2015 | 33/34 | 145.496.484,69 | 246.454.159,78 | 1,693884 |
| 2016 | 34/34 | 159.118.107,21 | 247.866.222,57 | 1,557750 |
| 2017 | 32/34 | 121.487.429,28 | 182.942.166,08 | 1,505853 |
| 2018 | 34/34 | 140.360.152,20 | 203.889.462,17 | 1,452616 |
| 2019 | 34/34 | 185.061.364,14 | 259.149.198,80 | 1,400342 |
| 2020 | 34/34 | 311.469.228,18 | 422.590.802,28 | 1,356766 |
| 2021 | 33/34 | 212.418.462,03 | 266.110.518,65 | 1,252765 |
| 2022 | 33/34 | 295.518.170,79 | 338.776.177,34 | 1,146380 |
| 2023 | 34/34 | 291.477.896,93 | 319.469.457,20 | 1,096033 |
| 2024 | 34/34 | 363.799.964,55 | 382.050.909,44 | 1,050168 |
| 2025 | 34/34 | 327.942.785,14 | 327.942.785,14 | 1,000000 |

**Comparação válida de cobertura:** 2024→2025 (34/34 em ambos): de **R$382.050.909,44** a **R$327.942.785,14** em preços médios de 2025, redução real de aproximadamente **14,16%**. Comparações com anos de cobertura parcial carecem de delimitação a um painel equilibrado de municípios observados, ou de resolução documental das lacunas; **não** transformar soma parcial em valor regional integral.

**Conceito:** receita de capital bruta realizada, diferente de transferência de capital, investimento liquidado, disponibilidade em caixa e gastos com obras. A deflação não resolve diferenças de ementário/classificação em 2015–2025.

## 3. Lacunas ainda presentes — sem atribuição de zero

Cássia dos Coqueiros (2015); Cajuru (2017); Santa Cruz da Esperança (2017); Santa Rita do Passa Quatro (2021); Santa Cruz da Esperança (2022). Todos têm registros de DCA Anexo I-C na API STN, **mas não apresentaram a conta sintética de capital selecionada no retorno recuperado**. O RREO de Cássia dos Coqueiros do 6º bimestre de 2015 indica R$257.239,70 de receita de capital até o bimestre, mas é um **demonstrativo distinto da DCA**; o valor não foi transportado para a série principal. Antes de preencher qualquer lacuna, exigir confirmação da correspondência contábil, versão e retificação.

## 4. QA dos RGF e exceções

A consulta dos RGF simplificados semestrais do Executivo de oito municípios foi consolidada no Lote 93 (fonte STN) e preservada na planilha. O Lote 94 calculou automaticamente a relação DCL/RCL ajustada a partir dos numeradores e denominadores declarados nos Anexos 02, comparando-a ao percentual do Anexo 06:

- **Barrinha:** DCL/RCL no Anexo 06 **31,40%**, no Anexo 02 **26,62%**; numerador R$42.986.801,45 e denominador R$161.507.819,10 confirmam **26,62%**. Divergência de **4,78 pontos percentuais**. Sem substituição silenciosa.
- **Orlândia:** Anexo 06 **-6,59%**, Anexo 02 **-6,55%**; numerador R$-17.264.485,35 e denominador R$263.501.501,04 são compatíveis com o segundo. Divergência de **-0,04 ponto percentual**, ainda a conferir.
- **Pontal:** permanece em quarentena: RGF Q3 2025 RCL R$13.494.039,69 versus RREO B6 2025 RCL R$209.571.785,24, além das relações declaradas muito elevadas. O Lote 94 não encontrou retificação nem manifestação oficial resolutiva. Sem inferência de descumprimento da LRF.

**Não se estendeu no Lote 94 o cotejo dos Anexos 01 e 06 aos outros 26 municípios**; o conjunto de 34 registros de RGF continua em consolidação e QA legal.

## 5. Artefatos e validação técnica

Foram gerados localmente:
- `/mnt/data/RMRP_LOTE94_DEFLATOR_QA/RMRP_RECEITAS_CAPITAL_REAL_IPCA_LOTE94.xlsx` (original Lote93 preservado; acrescentadas abas IPCA_2015_2025, RECEITA_REAL_2025, RESUMO_REAL, QA_LACUNAS_94, QA_RGF_DIVERGENCIAS_94);
- `/mnt/data/RMRP_LOTE94_DEFLATOR_QA/RMRP_RECEITAS_CAPITAL_REAL_IPCA_LOTE94.csv` (CSV BR, separador ponto-e-vírgula, decimal vírgula, identificador IBGE como texto);
- `/mnt/data/RMRP_LOTE94_DEFLATOR_QA/QA_IPCA_LOTE94.json`;
- `/mnt/data/RMRP_LOTE94_DEFLATOR_QA/gerar_lote94.py` (script gerador).

**QA efetivamente realizado:** arquivo XLSX ZIP íntegro (`testzip` sem erro), 12 abas legíveis no `openpyxl`, 374 registros no painel real, 369 com valor observado, média anual IPCA 2025 e fator unitário, total 2024 R$363.799.964,55, cache numérico de fórmulas conferido, nenhum erro de fórmula identificado. Fórmulas e valores numéricos em cache foram gravados no XLSX. **A biblioteca de renderização `artifact_tool` não foi usada**, tampouco foi realizada inspeção visual pixel a pixel da planilha. A tentativa de salvar o XLSX na Library falhou por limite de armazenamento; **não foi validado upload dos arquivos do Lote94 ao Google Drive**. A documentação deste dossiê foi persistida no GitHub; arquivos da execução estão disponíveis como anexos locais da conversa.

## 6. Pendências e encaminhamentos

1. Inspecionar declarações DCA originais/retificadas dos cinco casos, e RREO correspondente, sem alterar a rubrica por inferência.
2. Completar cruzamento RGF/RREO e eventuais retificações dos 34 municípios, sobretudo Pontal, Barrinha e Orlândia.
3. Examinar se as comparações históricas do Volume II necessitam painel equilibrado ou painel incompleto com legenda explícita, e avaliar mudança de ementário por exercício.
4. Conciliar FNDE 959097/2024 de Guariba com desembolsos e pagamentos, ainda sem ZIP oficial disponível no ambiente anterior.
5. Concluir QA gráfico integral do Volume II e análise jurídica; **não homologar nem alterar DOCX/PDF** nesta rodada.

**Resultado auditável:** deflação anual por médias IPCA com cobertura documentada, e localização de divergências oficiais, sem extrapolação de valores ausentes.
