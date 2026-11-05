# Fechamento G1-3 — Auditoria das despesas correntes e investimentos liquidados de 2025 na RMRP

**Data:** 05/11/2026. **Estado:** frente **G1-3/2025 validada**, demais anos (2023–2024), séries per capita e avaliação cartográfica **ainda pendentes**. **Volume II Lote 98 (66 páginas) preservado sem edição**.

## 1. Método e fonte primária

Consulta direta à API pública STN/Siconfi, endpoint `tt/dca`, filtro `an_exercicio=2025&id_ente={codigo_IBGE}&no_anexo=DCA-Anexo%20I-D`, em **34 municípios da RMRP**. Cada resposta retornou demonstração própria, selecionando exclusivamente a coluna **`Despesas Liquidadas`**. As contas observadas foram `DO3.0.00.00.00.00` (**Despesas Correntes**) e `DO4.4.00.00.00.00` (**Investimentos**). Despesas empenhadas, pagas e restos a pagar **não** foram utilizadas para o mesmo indicador. A consulta de Ribeirão Preto confirmou a existência de todas essas colunas como estágios distintos. Fonte geral: https://apidatalake.tesouro.gov.br/ords/cdwhprd/siconfi/tt/dca .

Foram preservados o código IBGE, população informada na própria DCA (para futuras conferências), município/sub-região e URL parametrizada da API no CSV detalhado por município. Denominador de cada participação: **Receitas Correntes Brutas Realizadas** da DCA Anexo I-C de 2025, extraídas de `receitas orçamentárias (anexo I-C) - municípios de sp 2025.csv` pela conta `siconfi-cor_RO1.0.0.0.00.0.0`, mesma fonte utilizada no G1-2. Isso assegura correspondência entre município, ano e conceito.

**Cobertura:** 34/34 municípios com ambas as rubricas de despesas liquidadas e o denominador de receita corrente; nenhuma imputação de zero ou substituição por empenho/pagamento. Rubricas de investimento e de despesas correntes foram coletadas do Anexo I-D, **não inferidas da receita de capital**.

## 2. Conferência do quadro metropolitano e sub-regional do Volume II

A Tabela 2 do Volume II apresenta dois indicadores de despesa — despesa corrente liquidada/receita corrente e investimento liquidado/receita corrente — em cinco recortes (RMRP, Ribeirão Preto, Jaboticabal, Mococa e Batatais). Cada indicador foi recalculado pelo quociente da **soma de valores** para o recorte pela soma da receita corrente, e não pela média simples de razões municipais.

| Recorte | Municípios | Despesa corrente liquidada, R$ | Investimento liquidado, R$ | Despesa corrente/receita, % | Investimento/receita, % |
|---|---:|---:|---:|---:|---:|
| RMRP | 34 | 10.526.057.811,59 | 302.301.895,18 | **88,93** | **2,55** |
| Ribeirão Preto | 15 | 7.280.800.218,42 | 208.212.555,64 | **88,87** | **2,54** |
| Jaboticabal | 6 | 1.283.116.564,77 | 29.313.238,96 | **91,21** | **2,08** |
| Mococa | 6 | 775.338.565,69 | 23.837.004,17 | **85,48** | **2,63** |
| Batatais | 7 | 1.186.802.462,71 | 40.939.096,41 | **89,27** | **3,08** |

**Resultado: 10/10 percentuais conforme, diferença máxima inferior a 0,0051 ponto percentual após arredondamento a duas casas.** Total metropolitano do denominador: receita corrente R$ 11.836.161.388,56 (conferida no G1-2).

O índice metropolitano representa participação de investimento **liquidado**, não prova de execução física de obra, efetiva transferência de capital ou pagamento financeiro.

## 3. Cinco verificações de percentuais em SWOT municipais

Foram localizadas e validadas cinco afirmações explícitas de **investimento liquidado/receita corrente em 2025** nas SWOT:

| Município | Percentual publicado | Percentual recalculado |
|---|---:|---:|
| Dumont | 6,74% | 6,7363% |
| Pradópolis | 4,26% | 4,2621% |
| Guariba | 3,76% | 3,7596% |
| Pitangueiras | 3,21% | 3,2060% |
| Nuporanga | 6,56% | 6,5596% |

**Resultado: 5/5 conforme.** Não confundir esses cinco achados com a auditoria integral das 34 matrizes, que apresentam outras afirmações sobre investimento real por habitante e variação entre 2023 e 2025.

A **mediana municipal** calculada sobre as 34 proporções `investimento liquidado / receita corrente` foi **2,3318097060%**, confirmando o arredondamento **2,33%** usado como referencial nas SWOT.

## 4. Limitações e próximos passos do G1

**Ainda não homologados nesta rodada:**
1. **2023 e 2024** para despesa corrente e investimento liquidado; a reconstrução deve recuperar a mesma conta `DO4.4` e estágio `Despesas Liquidadas` em cada um dos 34 municípios, com controle de cobertura.
2. **Variações reais do investimento per capita 2023–2025**: exige método de deflação compatível com as séries gerais do Volume II (preços de setembro de 2026) e critérios populacionais documentados; não transferir automaticamente o deflator de receita de capital que usa preços médios de 2025.
3. Verificação do conjunto das **34 SWOT municipais**, além das cinco afirmações de participação liquidação/receita reproduzidas.
4. Conferência das correspondências numéricas nos **mapas e gráficos** da série de investimentos; a prova por tabela não substitui QA da representação visual.

**Nota documental:** busca no Google Drive revelou planilhas financeiras gerais e capítulos históricos, mas não justificou usar números dessas fontes sem revalidar o estágio da despesa, período e município. A evidência substantiva desta rodada é extração oficial DCA I-D de 2025 para 34 municípios, com os resultados registrados no controle local.

## 5. Arquivos técnicos criados

- `/mnt/data/RMRP_FECHAMENTO_G1/auditar_g13_despesas.py`: script de reprodução da matriz e testes; possui os valores oficiais 2025 recuperados em 34 consultas, cada qual com URL de fonte parametrizada no resultado.
- `/mnt/data/RMRP_FECHAMENTO_G1/G13_DESPESAS_2025_34_MUNICIPIOS.csv`: 34 registros, códigos IBGE como texto, receitas e despesas, valores e participações, população e links oficiais.
- `/mnt/data/RMRP_FECHAMENTO_G1/G13_CONFERENCIA_TABELA2_DESPESAS.csv`: 10 comparações de percentuais por recorte e indicador.
- `/mnt/data/RMRP_FECHAMENTO_G1/G13_CONFERENCIA_SWOT_INVESTIMENTO.csv`: cinco verificações nominativas nas matrizes.
- `/mnt/data/RMRP_FECHAMENTO_G1/QA_G13_DESPESAS_2025.json`: somas, percentuais, cobertura, divergências e limites.

**Decisão:** a frente **G1-3 para as despesas de 2025 está aprovada**; não declarar concluída a auditoria trienal 2023–2025 nem G1 integral. O Volume II Lote 98 permanece sem modificação e em pré-homologação.
