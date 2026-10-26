# Reconciliação documental orientada dos dez maiores desvios TCESP–DCA

Data: 26/10/2026. Situação: **triagem dos critérios de classificação concluída; investigação dos documentos originais em aberto**.

## Base probatória já validada
A conciliação entre investimentos liquidados TCESP e DCA na matriz histórica de São Paulo apurou 55 diferenças entre 1.931 pares comparáveis em 2023–2025, com 1.876 concordâncias exatas. A reextração independente dos ZIPs TCESP, com hash SHA-256 da fonte preservado, reproduziu **10/10** valores dos casos de maior materialidade sem qualquer diferença em centavos. A base canônica DCA foi conferida contra o CSV original (Drive id `1BtXY_FxydMREEbMACJtaoW2n24ohVH33`, SHA-256 `67a94313e0f0557bc23f48c78a1396fd02ae10ad7923ea2ac2e5c9f2726f65d5`). A reprodução **não** equivale à validação documental cruzada das declarações.

## Critérios efetivamente implementados
- **DCA:** o mapeamento `data/mappings/dca_canonical_v1.yml` define `dca_investimentos_liquidada` como **DCA-Anexo I-D**, coluna **Despesas Liquidadas**, rótulo **Padrão**, conta **DO4.4.00.00.00.00**.
- **TCESP:** os extratores `governance/auditar_despesas_estaduais_historico_integral.py` e `governance/auditar_despesas_estaduais_2025_integral.py` selecionam linhas de `despesas-AAAA.csv` cujo prefixo de `ds_elemento` antes de ` - ` **começa com `44`**. A apuração considera somente `tp_despesa` normalizado como **valor liquidado** e soma `vl_despesa` em centavos.
- Essas regras foram verificadas **no código do repositório**, e não autorizam, por si, concluir equivalência completa de escopo contábil, ente, regime e eventuais deduções entre as bases.

## Matriz dos dez maiores casos

| Código IBGE | Ano | TCESP R$ | DCA R$ | TCESP − DCA R$ |
|---|---|---:|---:|---:|
| 3548807 | 2023 | 147.173.188,49 | 161.697.826,62 | −14.524.638,13 |
| 3554102 | 2024 | 45.431.933,66 | 40.273.274,12 | +5.158.659,54 |
| 3545209 | 2023 | 39.898.893,44 | 44.506.303,61 | −4.607.410,17 |
| 3522158 | 2024 | 3.903.919,12 | 7.786.197,26 | −3.882.278,14 |
| 3533254 | 2024 | 1.305.232,40 | 5.077.344,87 | −3.772.112,47 |
| 3548906 | 2024 | 138.740.832,67 | 135.579.005,97 | +3.161.826,70 |
| 3502804 | 2023 | 32.513.168,01 | 31.673.342,63 | +839.825,38 |
| 3534708 | 2024 | 90.267.507,66 | 89.545.844,38 | +721.663,28 |
| 3517901 | 2025 | 4.827.778,14 | 4.225.489,20 | +602.288,94 |
| 3520301 | 2024 | 15.548.454,11 | 15.053.443,43 | +495.010,68 |

Todos os valores desta matriz derivam das matrizes históricas auditadas TCESP–DCA; os valores TCESP foram posteriormente reproduzidos nos testes independentes. Não foram extraídos novamente os anexos DCA de origem neste dossiê.

## Hipóteses a testar, não conclusões
1. **Alcance da classificação:** confronto detalhado entre registros `ds_elemento` iniciados por `44` e a conta consolidada `DO4.4.00.00.00.00`, conferindo inclusão de subcontas, critérios e duplicidades possíveis.
2. **Versões/retificações:** data da remessa ou revisão do demonstrativo em cada sistema e se os arquivos comparados se referem à mesma versão.
3. **Abrangência do ente:** unidades gestoras e fundos integrados, operações intraorçamentárias, eventual eliminação de duplicidades, exclusões e ajustes.
4. **Estágio da execução:** identidade do conceito de liquidação e tratamento de estornos/cancelamentos, especialmente operações com valores negativos.
5. **Competência e consolidação anual:** apurar soma mensal TCESP versus saldo anual DCA e possíveis diferenças no período de referência.

Nenhuma hipótese é atribuída aos casos sem documento comprobatório.

## Próxima extração documental dirigida
Para cada par, capturar: endereço e identificador do demonstrativo original DCA no Siconfi, data/versão/retificação, linha exata DO4.4 Anexo I-D, memória da consulta; URL e versão do ZIP TCESP; decomposição mensal do estágio liquidado, códigos de `ds_elemento`, valores brutos e negativos, órgãos/unidades e critérios de inclusão. Armazenar evidências com hash e estabelecer a diferença explicada e o resíduo em centavos. Classificar cada caso como **explicado documentalmente**, **compatibilização metodológica testada** ou **pendente de comprovação**. Nunca corrigir uma fonte apenas para zerar uma diferença.

## Decisão de auditoria
A trilha principal passa de **suspeita de falha de extração TCESP** para **reconciliação de classificação, escopo e versões entre fontes**. Esse redirecionamento baseia-se na reprodutibilidade observada em 10/10, sem excluir problemas sistemáticos que seriam reproduzidos por implementações com a mesma regra de seleção `ds_elemento`. A independência da releitura foi de operação e agregação; a hipótese conceitual de seleção do grupo 44 precisa ser confrontada com o dicionário e os demonstrativos oficiais.

Documentos complementares: `governance/REEXTRACAO_TCESP_CASOS_PRIORITARIOS_20261026.md` e `governance/CONCILIACAO_INVESTIMENTOS_TCESP_DCA_SP645_2023_2025.md`. Produção e dados preservados.
