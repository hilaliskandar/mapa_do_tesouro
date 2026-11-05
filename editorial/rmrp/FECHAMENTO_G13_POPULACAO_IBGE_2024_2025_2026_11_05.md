# RMRP — G1-3: cotejo demográfico oficial DCA × IBGE 2024–2025

Data: 05/11/2026. Fonte oficial: IBGE, SIDRA Tabela 6579, variável 9324 (População residente estimada), 34 municípios, exercícios 2024 e 2025. Consulta reproduzível: https://servicodados.ibge.gov.br/api/v3/agregados/6579/periodos/2024,2025/variaveis/9324?localidades=N6[3501004,3505609,3505906,3507803,3509403,3510906,3513108,3514601,3518602,3518859,3524303,3525102,3527603,3530508,3531308,3531902,3533601,3534302,3539509,3540200,3540903,3543402,3544905,3546256,3547502,3547601,3547908,3550902,3551405,3551504,3551702,3553203,3553302,3553658]&view=flat

**Cobertura:** 68/68 populações municipais obtidas diretamente do IBGE (34 × 2 exercícios). Na DCA, a população de 2024 é idêntica à de 2025 para todos os 34 municípios. A tabela IBGE fornece estimativas específicas para cada ano. Isso impede interpretar os denominadores DCA como uma série anual IBGE 2024–2025 sem ressalva.

| Indicador | DCA | IBGE 6579 |
|---|---:|---:|
| População agregada 2024 | 1650449 | 1702452 |
| População agregada 2025 | 1650449 | 1707166 |

Em 34 municípios há pelo menos uma diferença em 2024 ou 2025 entre DCA e a estimativa oficial consultada. Em 2025, 34/34 diferem; em 2024, 34/34 diferem. São diferenças de fonte/ano de referência, não evidência automática de erro do órgão declarante.

**Impacto para as séries per capita:** os investimentos nominais e reais extraídos da DCA não mudam; o quociente por habitante muda. A retração dos investimentos reais totais da RMRP em 2023–2025 é -43,12497%. Pela população **declarada na DCA**, a retração real per capita é -39,52111%; a queda menor em per capita é efeito aritmético de redução do denominador agregado DCA entre 2023 e 2025. Nenhuma inferência de êxodo ou encolhimento populacional deve ser feita.

**Limite essencial:** o SIDRA 6579 consultado não contém 2023, pois os períodos disponíveis saltam de 2021 para 2024. Sem uma série oficial específica de 2023, **não** se deve apresentar uma nova variação IBGE 2023–2025 como recalculada/homologada. A matriz anexa apenas substitui **2025** pelo denominador IBGE para teste transversal e registra os indicadores históricos com DCA para referência, jamais mesclando esses denominadores numa variação temporal.

**Próximo gate:** recuperar a publicação oficial IBGE/TCU de 2023 compatível com a referência do relatório; comparar os 34 códigos e documentar o ponto de corte. Corrigir após decisão o glossário e notas da versão de trabalho (Lote 98 congelado), inclusive a expressão 'população IBGE' quando o denominador for na realidade DCA. A norma é não alterar o valor fiscal por causa do ajuste populacional.

[Dados nominais e por habitante do teste](G13_AUDITORIA_POPULACAO_DCA_VS_IBGE_2024_2025.csv)

## Retificação de encaminhamento — 05/11/2026
Em continuidade, foi novamente verificado o arquivo-base FINBRA/DCA já arquivado, `DCA_SP_645_2013_2025_CANONICO.csv` (Google Drive ID `1BtXY_FxydMREEbMACJtaoW2n24ohVH33`): cabeçalho contém `cod_ibge`, `ano` e `populacao_dca`; são 8.385 registros, correspondentes a 645 municípios × 13 exercícios. Exemplo Ribeirão Preto: 2023 = 720.116, 2024 = 702.739, 2025 = 702.739. **A série populacional por exercício já está preservada na base FINBRA e não necessita ser novamente coletada para reprocessar os indicadores do relatório.** A comparação feita anteriormente com o SIDRA 6579 usou outra série estatística e não constitui prova de erro no denominador FINBRA nem razão para substituição automática. O rótulo `populacao_dca` por si só não comprova a portaria/critério TCU de cada exercício: essa referência deve ser verificada no dicionário/metadados preexistentes, caso seja necessário descrevê-la nominalmente. **Cancelar a diligência de nova coleta IBGE 2023 como pré-requisito do G1-3.** Preservar valores, metodologias e versão-base Lote 98; concentrar o QA na coerência dos denominadores do próprio corpus canônico e da redação editorial.
