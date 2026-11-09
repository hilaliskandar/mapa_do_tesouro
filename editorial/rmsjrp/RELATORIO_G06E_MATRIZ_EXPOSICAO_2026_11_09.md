# RMSJRP — G06-E | Matriz de exposição às fontes fiscais e mecanismos federativos
**Data:** 09/11/2026. **Situação:** matriz inicial 37×12 auditada e persistida no R2; cinco modalidades requerem documentação complementar. **Não equivale a estimativa de efeito causal da LC 200/2023.**

## 1. Objetivo e origem dos dados
O estudo dá continuidade ao caderno de revisão jurídica G06-J, cujo texto consolidado da LC 200/2023 delimita a incidência direta da regra de despesa à União. Para construir as bases de uma avaliação empírica foram separadas receitas observadas dos 37 municípios e modalidades de transferências que precisarão ser identificadas por programa e instrumento.

A fonte quantitativa é a série canônica `rmsjrp/g04/2026_11_09/SERIES_MUNICIPAIS_2013_2025.csv`, no R2 privado, SHA-256 `1f0413304c54edbe57fe129a506d088da2cd296d767f901992c02f803fbd62e5`; a fonte deriva da DCA/FINBRA, com valores nominais e reais em setembro de 2026. Não foram efetuadas novas extrações estaduais nem correções silenciosas às bases.

A rotina [`build_exposicao_g06e.py`](build_exposicao_g06e.py) produz 37 municípios × 12 classes = **444 registros** e (quatro sub-regiões + RMSJRP) × 12 classes = **60 linhas territoriais**. Os valores de 2023, 2024 e 2025 por município servem à investigação da trajetória; participações usam o denominador de receitas correntes brutas de **2025**. A fonte é estritamente DCA municipal: **não contém ainda a execução federal da transferência ou a chave do convênio**.

## 2. Resultado metropolitano de 2025
| Rubrica ou indicador | Valor nominal (R$) | Receita corrente (%) | Cobertura |
|---|---:|---:|---:|
| FPM, cota mensal | 1.083.377.408,23 | 14,94 | 37/37 |
| Cota-parte ICMS | 1.228.910.270,08 | 16,94 | 37/37 |
| Cota-parte IPVA | 406.761.346,41 | 5,61 | 37/37 |
| ISS principal | 629.488.253,23 | 8,68 | 37/37 |
| IPTU principal | 543.536.096,02 | 7,49 | 37/37 |
| ITBI principal | 161.913.305,44 | 2,23 | 37/37 |
| Receita tributária bruta | 1.701.096.570,89 | 23,45 | 37/37 |
| Fundeb ou complementação | — | — | 0/37 na fonte |
| SUS fundo a fundo | — | — | 0/37 na fonte |
| Outras transferências legais federais | — | — | 0/37 na fonte |
| Convênios, PAC, contratos de repasse | — | — | 0/37 na fonte |
| Emendas e transferências especiais | — | — | 0/37 na fonte |

**Três ressalvas de leitura:** (i) valor ausente em fonte não significa repasse inexistente; (ii) receita tributária bruta agrega outras rubricas, inclusive os principais impostos, de modo que **não se podem somar as sete classes da tabela**; (iii) ICMS e IPVA são repartições estaduais, e o FPM é repartição constitucional federal — **não são transferências discricionárias afetadas automaticamente pelo limite da LC 200**.

A observação de um montante de FPM mede a **importância contábil dessa fonte na receita de 2025**, não mede quanto seria atingido por qualquer contingenciamento da União. Não há percentual causal identificado.

## 3. Estrutura jurídico-analítica
A matriz contém, por município e categoria: código IBGE, sub-região, natureza jurídica, base normativa classificatória, valores de 2023–2025 em reais nominais e constantes set./2026, participação em receita corrente, situação da prova e campos obrigatórios ainda em branco para órgão federal, ação orçamentária, instrumento, empenho federal, pagamento da União, recebimento municipal conciliado, empenho local, medição e liquidação local.

As cinco modalidades ainda não cobertas quantitativamente exigem bases específicas para **Fundeb e sua complementação federal**, **SUS fundo a fundo**, **transferências legais diversas**, **convênios/PAC/contratos de repasse**, **emendas/transferências especiais**. Os documentos da LRF e da LC 200 demonstram que nenhuma delas deve ser tratada genericamente como FPM; algumas possuem regimes legais de execução e contabilização próprios, e eventuais exceções aos limites federais precisam ser verificadas por programa e exercício.

## 4. QA técnico e persistência
O [run 42571426458](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42571426458) terminou **success**, verificando a integridade SHA da fonte, 37 municípios, quatro sub-regiões com 14, 11, 6 e 6 municípios, 444 pares município–categoria, 60 pares território–categoria, distinção entre sete rubricas contábeis e cinco modalidades sem parâmetro extraído, e reconciliação dos totais regionais com as sub-regiões **por categoria, sem soma entre categorias sobrepostas**.

Artefatos verificados por leitura de retorno SHA no R2 privado `rmsjrp/g06/2026_11_09/exposicao_v1/`:
- `G06E_MATRIZ_EXPOSICAO_37x12.csv`;
- `G06E_RESUMO_TERRITORIAL_5x12.csv`;
- `QA_G06E.json`.

Este QA valida a correspondência com a base contábil de origem e a cardinalidade, mas **não substitui auditoria dos instrumentos e não aprova a hipótese causal da LC 200**.

## 5. Próxima diligência prioritária
1. **Identificar instrumentos concretos** nos registros do Transferegov, Portal da Transparência federal e Tesouro Transparente, especialmente programas de investimento do Ministério das Cidades, FNDE, saúde e Novo PAC com vínculo aos 37 municípios.
2. Separar **concedente, modalidade, valor pactuado, empenho, liquidação/pagamento federal, transferência creditada ao município e contrapartida**; identificar no sistema municipal o uso em investimento liquidado, distinguindo exercício orçamentário e financeiro.
3. Completar as cinco classes com dados observáveis, **sem alterar os sete indicadores da DCA** e sem substituir célula ausente por zero.
4. Produzir classificação de exposição municipal e sub-regional apenas depois de definir denominadores homogêneos. **A ocorrência de convênio não equivale a exposição líquida, e exposição não prova impacto causal.**
5. Manter G06-C de robustez dos cenários como análise genérica separada, sem alegar efeito jurídico da LC 200, e conservar G05-D documental em paralelo.

**Estado:** G06-E `qa_pass` para o inventário DCA e a matriz estruturada; **G06 `in_progress`** para identificação de instrumentos, fontes e demonstração causal. O relatório não deve ser publicado como resultado de impacto do novo arcabouço.
