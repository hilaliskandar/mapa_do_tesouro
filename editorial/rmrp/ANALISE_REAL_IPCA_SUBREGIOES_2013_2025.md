# RMRP — evolução fiscal real 2013–2025, IPCA setembro de 2026

Data: 19/10/2026. Situação: cálculos derivados verificados; texto editorial candidato.

**Origem fiscal:** DCA 645 municípios 2013–2025, CSV canônico no Google Drive `1BtXY_FxydMREEbMACJtaoW2n24ohVH33`, SHA-256 `67a94313e0f0557bc23f48c78a1396fd02ae10ad7923ea2ac2e5c9f2726f65d5`. **Parâmetros de IPCA:** planilha `FINBRA_PARTE5_parametros_temporais_IPCA_populacao_2013_2025.xlsx`, aba `IPCA_FATORES`, SIDRA IBGE tabela 1737 (https://sidra.ibge.gov.br/tabela/1737). Número-índice setembro de 2026: 7.695,82; índice de dezembro de cada exercício obtido da aba IPCA_FATORES. Fator: `7695.82 / índice_dez_ano`. Conservar precisão completa antes do arredondamento editorial.

34 municípios distribuídos entre quatro sub-regiões (15, 6, 6 e 7). Agregados: 13 anos × 25 variáveis × 5 recortes = 1.625 linhas. Destas, 995 possuem cobertura integral e 630, cobertura parcial. Para as parciais, o total integral permanece vazio; só há soma dos observados, explicitamente parcial. Nunca interpretar vazio como zero.

## Variação real acumulada 2023–2025 (%)

| Região | Receita corrente | Receita tributária | Despesa corrente liquidada | Investimento liquidado |
|---|---:|---:|---:|---:|
| Sub-região 1 | +10,55 | +12,97 | +7,13 | −38,65 |
| Sub-região 2 | +8,22 | +7,74 | +5,79 | −55,17 |
| Sub-região 3 | +13,49 | +18,93 | +4,46 | −24,10 |
| Sub-região 4 | +8,48 | +13,77 | +10,08 | −56,38 |
| **RMRP** | **+10,25** | **+12,83** | **+7,09** | **−42,97** |

A expansão real das receitas coexistiu com diminuição acentuada dos investimentos nos quatro recortes, em intensidades distintas. A SR3 teve crescimento tributário mais intenso e retração menos profunda dos investimentos. A SR4 combinou crescimento das despesas correntes superior ao das receitas correntes e retração de 56,38% no investimento. Esses padrões são descrições, não demonstrações de causalidade ou eficiência.

## Produtos reproduzíveis

A execução local produziu `dca_subregional_real_set2026_2013_2025.csv`, `variacoes_reais_2023_2025.csv`, `RM_RIBEIRAO_PRETO_IPCA_SET2026.xlsx`, `QA_IPCA_SET2026.json` e `atualizar_ipca.py` no diretório `rmrp_consolidacao` da conversa. A planilha inclui fórmulas visíveis; o CSV contém resultados calculados independentemente. Ainda se deve conferir recálculo e visualização finais em software de planilha antes de considerá-la homologada.

A fonte TCESP difere da DCA em Guatapará 2023 por R$ 10.176,00: as cifras aqui são DCA e nenhuma substituição foi realizada. O destaque simplificado dos precatórios permanece conforme deliberação anterior; não pesquisar processos judiciais individualmente.

**Próxima etapa:** redação cumulativa do caderno RMRP usando as três escalas; análise da trajetória completa quando a cobertura for suficiente; validação de população para per capita; QA editorial, tabelas e gráficos. Não criar uma nova versão do motor fiscal nem alterar a publicação sem gate.
