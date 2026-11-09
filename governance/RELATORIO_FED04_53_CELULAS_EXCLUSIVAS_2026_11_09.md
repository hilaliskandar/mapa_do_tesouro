# FED04 — Auditoria das 53 células exclusivas do suplemento DCA 2025

**Referência:** 09/11/2026. **Situação:** auditoria estrutural e de cobertura concluída; integração contábil ainda não homologada.

## Procedimento reprodutível

Confrontaram-se os dois arquivos já preservados no Drive, sem nova captura estadual: (1) CSV de receitas orçamentárias SICONFI DCA, Anexo I-C, SP 2025, 632 municípios e (2) XLSX `Receitas 2022-2025.xlsx`, aba `2025-finbra`, 642 municípios. Utilizou-se chave `codigo_ibge × conta × coluna`, para `RO1.7.1.1.51.1.0` FPM mensal; `RO1.7.1.1.52.0.0` ITR; `RO1.7.5.1.00.0.0` Fundeb recebido; `RO1.7.1.5.00.0.0` complementação federal ao Fundeb. Colunas admitidas: `Receitas Brutas Realizadas`, `Deduções - FUNDEB` e `Outras Deduções da Receita`.

O CSV é codificado em Windows-1252, separado por `;` e contém três linhas de metadados antes do cabeçalho. O XLSX foi inspecionado somente para leitura, com `openpyxl` e `reset_dimensions()` para evitar limites de dimensão declarados incorretamente. Os valores foram lidos com `Decimal`. O processamento não modificou os arquivos originais.

## Resultado das 53 células adicionais

**Todas as 53 células pertencem exclusivamente aos mesmos dez municípios ausentes no CSV anual e existentes no suplemento.** Não foi identificado registro monetário vazio nas 53 células. Assim, elas constituem *complementação candidata de cobertura*, e não retificação de valor de município já registrado no CSV anual.

| Código IBGE | Município | Células |
|---|---|---:|
| 3503505 | Areias | 3 |
| 3503604 | Areiópolis | 6 |
| 3506607 | Biritiba-Mirim | 5 |
| 3514007 | Dobrada | 6 |
| 3521705 | Itaberá | 6 |
| 3528106 | Macaubal | 5 |
| 3533700 | Ocauçu | 6 |
| 3537404 | Pereira Barreto | 6 |
| 3540408 | Populina | 5 |
| 3542701 | Restinga | 5 |
| **Total** | **10 municípios** | **53** |

**Por conceito:** 19 células FPM mensal, 19 ITR, 10 Fundeb recebido e cinco complementação federal do Fundeb. **Por coluna:** 35 receitas brutas e 18 deduções Fundeb. Os registros selecionados têm ausência de duplicação na chave examinada.

O CSV de auditoria foi produzido na sessão como `FED04_53_CELULAS_EXCLUSIVAS_SUPLEMENTO_2025.csv`; SHA-256 **`f68704015159f6e5b02d5132d799666fd139cc981795cd1d5f7c6f81b4efa56c`**. Sua persistência externa ainda não foi demonstrada; não atribuir ao GitHub/R2 armazenamento inexistente.

## Exceções documentais verificadas no CSV anual

- **Rio das Pedras, IBGE 3544004:** 206 linhas de Anexo I-C, sendo 54 de receitas brutas, 54 de deduções de transferências constitucionais, 54 de outras deduções e 44 de deduções Fundeb. Nenhuma das quatro contas analíticas selecionadas apareceu no CSV anual. Há contas agregadas, mas não há base para deduzir o desdobramento entre FPM, ITR e Fundeb; exige verificação da declaração, eventual retificação e granularidade.
- **Sarutaiá, IBGE 3551207:** zero linhas no CSV anual consultado. Registros anteriores do projeto indicam também ausência de retorno no teste da API DCA 2025; isso representa ausência de informação comprovada nesse anexo e não valor igual a zero, nem prova de infração de obrigação declaratória.

## Decisões e próximos passos

1. Manter **fonte anual prioritária para todas as chaves coincidentes** e suplemento `fill-only` para os dez municípios, sujeito a QA específico de origem, versões e contabilidade.
2. Não interpretar 53 células como 53 municípios ou 53 novas receitas; são 53 posições `município × conta × coluna` distribuídas entre dez municípios.
3. Conferir no extrato de entregas e, se necessário, na API SICONFI, a situação dos dez municípios em 2025, antes de homologar o preenchimento definitivo.
4. Investigar Rio das Pedras por rubricas-pai e eventuais alterações de classificação; não inferir a conta-filha da soma hierárquica.
5. Investigar Sarutaiá e registrar estado documental distinto de zero explícito.
6. Prosseguir à harmonização de códigos 2013–2024 usando os exercícios respectivos e o MCASP, sem usar a contagem de linha como medida de arrecadação.
7. Preservar o SQLite, `observacao`, série FINBRA e publicação; nenhuma migration ou deploy foi realizado.

**Relatório complementar:** [auditoria das 128 divergências e teste de precisão](RELATORIO_FED04_DIVERGENCIAS_PRECISAO_DCA_2025_2026_11_09.md). **Controle:** [FED00–FED08](STATUS_FED_SP645.csv).

## Conferência independente com a matriz estadual já preservada no Drive

Foi recuperada novamente a matriz final [`QA_FED04_DCA_ITR_FUNDEB_2025_SP645_COMPLETO.csv`](https://drive.google.com/file/d/1Tik1vEa5tSIIHp0GLPEjgJi_M6HUdP_d/view) e examinadas todas as linhas dos dez códigos IBGE. Foram identificadas **120 posições** (dez municípios × quatro conceitos × três colunas), das quais **53 classificadas `preenchimento_candidato_suplemento`**, com `fonte_prioritaria=suplemento_2022_2025` e valores não vazios; outras **67 classificadas `linha_ausente`**, com fonte `nenhuma`. Nenhum preenchimento foi incorretamente rotulado `anual_2025`. Assim, a matriz estadual anterior **já contém os 53 preenchimentos candidatos corretamente identificados e não precisa ser reconstruída**. Essa conferência valida o estado e a proveniência das posições, não a correção contábil independente dos valores.
