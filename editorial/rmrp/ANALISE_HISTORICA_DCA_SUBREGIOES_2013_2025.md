# RMRP — base fiscal histórica nas quatro sub-regiões, 2013–2025

Data: 19/10/2026. **Estado: consolidação computacional concluída; edição analítica candidata, não homologada.**

Foi recuperada do Google Drive a base canônica `DCA_SP_645_2013_2025_CANONICO.csv` (file ID `1BtXY_FxydMREEbMACJtaoW2n24ohVH33`; SHA-256 `67a94313e0f0557bc23f48c78a1396fd02ae10ad7923ea2ac2e5c9f2726f65d5`). A base registra 8.385 observações (645 municípios × 13 exercícios). A seleção fechada é a composição RMRP já versionada em `editorial/rmrp/municipios_subregioes_tcesp.csv`: 34 municípios, 15/6/6/7 por sub-região.

Foram produzidas 11.050 células (34 × 13 × 25 contas DCA) e 1.625 agregados (13 × 25 × cinco escalas: SR1, SR2, SR3, SR4 e RMRP). Os totais foram reconciliados por somatório sub-regional em cada conta/ano; ausências preservadas em branco, sem imputação de zero. A promoção de um total como integral exige 100% de observações municipais no recorte.

## Variações nominais de 2023 a 2025

| Recorte | Receita corrente | Receita tributária | Despesa corrente liquidada | Investimento liquidado |
| --- | ---: | ---: | ---: | ---: |
| SR1 | +20,83% | +23,48% | +17,10% | -32,95% |
| SR2 | +18,28% | +17,76% | +15,63% | -51,00% |
| SR3 | +24,04% | +29,99% | +14,18% | -17,04% |
| SR4 | +18,57% | +24,35% | +20,32% | -52,32% |
| **RMRP** | **+20,51%** | **+23,32%** | **+17,05%** | **-37,66%** |

Receitas e despesa corrente cresceram nominalmente em todas as sub-regiões, enquanto o investimento liquidado caiu, sobretudo nas SR2 e SR4. Essas são diferenças descritivas e não demonstram causalidade. Comparações **reais** dependem de aplicação posterior do IPCA canônico com data-base set./2026.

## Observações relevantes para QA

Em 2013, receita corrente tem 33/34 observações e despesa total liquidada 32/34: nenhum dos dois agregados pode ser apresentado como total integral do universo. Em 2023, 2024 e 2025 as cinco grandes contas do quadro têm 34/34 observações.

O TCESP apresentou em Guatapará 2023 R$ 2.118.940,79 de investimento liquidado, ante R$ 2.108.764,79 na DCA. A diferença de R$ 10.176,00 afeta SR1 e RMRP em 2023. As séries aqui são **DCA**, não TCESP. A classificação simples de precatórios e o limite de escopo permanecem nos registros anteriores, sem diligências judiciais individualizadas.

Dados resultantes desta execução: `dca_historico_municipal_2013_2025.csv`, `dca_historico_subregional_2013_2025.csv`, `QA_DCA_HISTORICO.json`, reunidos em `RMRP_DCA_HISTORICO_2013_2025.zip` (arquivo anexo à conversa). Não criar nova base fiscal concorrente nem alterar publicação.

**Próximas etapas:** aplicar fatores IPCA já calculados e versionados, revisar comparabilidade dos denominadores, compor as séries e análises no caderno, testar cobertura e paridade e só então submeter à homologação editorial.