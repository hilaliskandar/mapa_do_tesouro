# RMRP — consolidação fiscal nas escalas municipal, sub-regional e metropolitana

Data: 19/10/2026. Estado: **candidata analítica, sem homologação editorial**.

Fonte: artifact privado `sp645-private-site-38593209824` (GitHub Actions run `38593209824`, artifact `11908541959`), cadastro `editorial/rmrp/municipios_subregioes_tcesp.csv` de 34 municípios, distribuídos em quatro sub-regiões. Recorte 2023–2025, 22 variáveis, 2.244 registros municipais e 330 agregados (quatro sub-regiões mais RMRP). Foram reconciliados os totais completos com as respectivas somas sub-regionais. Ausência não equivale a zero.

## Contas integrais em 2025

Valores nominais em R$ milhões, apresentados com arredondamento apenas editorial.

| Recorte | Receita corrente | Receita tributária | Despesa total liquidada | Investimento liquidado | Tributos / receita corrente | Investimentos / receita corrente |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| SR1 (15) | 8.192,90 | 2.366,55 | 7.683,13 | 208,21 | 28,89% | 2,54% |
| SR2 (6) | 1.406,75 | 270,63 | 1.334,98 | 29,31 | 19,24% | 2,08% |
| SR3 (6) | 907,05 | 156,65 | 827,10 | 23,84 | 17,27% | 2,63% |
| SR4 (7) | 1.329,46 | 217,12 | 1.242,25 | 40,94 | 16,33% | 3,08% |
| **RMRP (34)** | **11.836,16** | **3.010,95** | **11.087,46** | **302,30** | **25,44%** | **2,55%** |

Proporções calculadas pela razão entre somas (não média dos indicadores municipais). RMRP 2025 receita corrente exata R$ 11.836.161.388,56 e investimentos R$ 302.301.895,18. Consistência do investimento com a extração TCESP em 2025 já documentada em `QA_TCESP_102_EXTRATOS_DCA_20261019.md`.

## CAPAG — composição do snapshot 2025

| Recorte | A+/A/B+/B | C | D | n.d. |
| --- | ---: | ---: | ---: | ---: |
| SR1 | 3 | 9 | 1 | 2 |
| SR2 | 2 | 4 | 0 | 0 |
| SR3 | 2 | 3 | 0 | 1 |
| SR4 | 1 | 5 | 0 | 1 |
| **RMRP** | **8** | **21** | **1** | **4** |

Essas são contagens de classificações municipais extraídas do snapshot. Não há CAPAG oficial coletiva para cada sub-região.

## Cobertura e ressalvas

A DCA possui cobertura completa nas quatro contas do quadro. Já no conjunto metropolitano em 2025, Habitação apresenta 2/34 municípios, Saneamento 25/34, Transporte 20/34, Gestão Ambiental 27/34; RCL oficial 26/34, pessoal RGF 26/34, dívida consolidada 32/34, DCL 26/34 e caixa após RPNP 26/34. Não apresentar somas parciais como totais completos. A escala dos indicadores percentuais RGF/RREO ainda requer certificação; nenhuma escala foi inferida aqui.

A sub-região 1 reúne aproximadamente 69,2% das receitas correntes, mas o maior investimento relativo à receita corrente está na SR4 (3,08%). Nenhuma dessas proporções, isoladamente, certifica desempenho ou eficiência municipal. As séries são nominais, não deflacionadas, e a comparação 2023–2025 deverá tratar atualização monetária no produto editorial definitivo.

Pacote de dados gerado nesta revisão: `RMRP_CONSOLIDACAO_SUBREGIONAL_2023_2025.zip`, com CSV municipal, agregados sub-regionais, CAPAG e README. Não substituir nem republicar dados oficiais sem QA e homologação.

**Próxima atividade:** integrar as séries e interpretações ao caderno regional, calcular valores reais segundo o protocolo vigente e recuperar dados faltantes apenas quando suas ausências forem comprovadas nas fontes canônicas.