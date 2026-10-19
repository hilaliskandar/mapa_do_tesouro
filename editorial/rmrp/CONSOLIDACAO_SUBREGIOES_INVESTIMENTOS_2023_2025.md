# RMRP — consolidação dos investimentos liquidados por sub-regiões (2023–2025)

Data: 19/10/2026. **Status: consolidação nominal TCESP auditada quanto à integridade interna; análise editorial candidata.**

## Base e universo

Fonte: quatro artefatos do GitHub Actions run `39203495737`: sub-região 1 `12164512559`; 2 `12164945873`; 3 `12164992449`; 4 `12164872696`. Composição territorial canônica: `editorial/rmrp/municipios_subregioes_tcesp.csv`; 34 municípios, distribuídos em 15, 6, 6 e 7 nas sub-regiões 1 a 4. Referência de delimitação no projeto: PDUI RMRP (ver `COLETA_TCESP_LOTES_SUBREGIOES.md`).

Foram conferidos 102 pares município–ano (34 × 2023, 2024 e 2025), todos com `bad_values=0`, unicidade da chave e igualdade em centavos entre total do grupo 44 liquidado e somas de programas/ações. A soma sub-regional reproduziu exatamente os totais TCESP regionais da auditoria `QA_TCESP_102_EXTRATOS_DCA_20261019.md`.

## Série nominal de investimentos liquidados — grupo 44

Valores em reais, sem atualização monetária.

| Recorte | Municípios | 2023 | 2024 | 2025 | Variação nominal 2024–2025 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Sub-região 1 | 15 | 310.532.839,23 | 327.997.332,21 | 208.212.555,64 | -36,52% |
| Sub-região 2 | 6 | 59.821.843,31 | 58.507.463,35 | 29.313.238,96 | -49,90% |
| Sub-região 3 | 6 | 28.733.930,90 | 29.897.759,53 | 23.837.004,17 | -20,27% |
| Sub-região 4 | 7 | 85.869.961,80 | 84.421.596,97 | 40.939.096,41 | -51,51% |
| **RMRP** | **34** | **484.958.575,24** | **500.824.152,06** | **302.301.895,18** | **-39,64%** |

Participações sub-regionais no total de 2025: SR1 68,88%; SR2 9,70%; SR3 7,89%; SR4 13,54%. Em 2023: SR1 64,03%; SR2 12,34%; SR3 5,93%; SR4 17,71%.

## Leitura fiscal e territorial

A trajetória regional esconde assimetrias importantes. Em 2025, a redução nominal dos investimentos foi observada nas quatro sub-regiões, com menor intensidade na SR3 e quedas próximas à metade dos montantes de 2024 nas SR2 e SR4. A SR1 elevou sua participação regional mesmo durante o recuo de seus investimentos; não confundir esse efeito composicional com crescimento absoluto.

Os totais são **nominais**, não constituem taxas reais de crescimento. Não permitem interpretar diretamente investimentos por habitante, esforço relativo a receitas, execução física ou qualidade do investimento sem denominadores e detalhamento próprios. A análise futura do caderno deverá apresentar, de forma sistemática, a região e as quatro sub-regiões, além de perfis municipais e da participação do município-polo.

## Tratamento de precatórios e limites

Nos detalhamentos disponíveis, destacar precatórios identificados na descrição da ação e/ou natureza, conforme deliberação registrada em `governance/RMRP_TCESP_NATUREZA_SUBSTANTIVA_2026_10_19.md`. Não aprofundar obrigação judicial originária. Não subtrair de toda a série de 102 extratos um valor de precatórios obtido apenas de quatro recortes investigados; a comparação de investimento excluídos os precatórios dependerá de cobertura identificada para todas as unidades do agregado.

Diferença externa TCESP × FINBRA/DCA: Guatapará 2023, SR1, TCESP excede DCA em R$ 10.176,00. Os totais apresentados aqui são TCESP; manter o confronto DCA explicitamente separado. Em 2023, os demais 33 casos coincidem; em 2024 e 2025 a paridade é integral (34/34).

## Critérios obrigatórios para os demais indicadores do caderno

- Publicar total da RMRP **e** resultados das quatro sub-regiões em receitas, despesas, investimentos, funções, dívida e CAPAG, conforme cobertura e pertinência de cada fonte.
- Agregados monetários: somar municípios observados, expondo cobertura e diferenças de fonte; não preencher ausentes como zero.
- Razões per capita: dividir a soma dos valores pela soma dos habitantes com mesmo recorte, ano e universo válido.
- Indicadores percentuais agregáveis: usar razão entre somas de numeradores e denominadores comparáveis, não médias simples de percentuais municipais.
- Indicadores legais/CAPAG: não produzir uma classificação oficial sub-regional fictícia; apresentar distribuição de municípios por classe, medianas ou outros resumos descritivos, com cobertura.
- Comparações monetárias interanuais: distinguir valores nominais e reais, IPCA e data-base.
- Impedir dupla contagem: cada município aparece uma vez na RMRP e exatamente em uma sub-região.

**Não publicar nova versão do caderno sem QA de cobertura, conciliação e leitura substantiva.**
