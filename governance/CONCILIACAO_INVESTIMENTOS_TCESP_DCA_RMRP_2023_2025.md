# Conciliação de investimentos liquidados TCESP × DCA na RMRP, 2023–2025

Data de consolidação: 26/10/2026.

## Objeto e delimitação
Confronto de investimentos liquidados, grupo de natureza de despesa 44, apurados pelo TCESP, com a variável canônica `dca_investimentos_liquidada` da base DCA/FINBRA por município, código IBGE e exercício. Universo: **34 municípios da Região Metropolitana de Ribeirão Preto**, de 2023 a 2025; 102 pares município–ano. A fonte de evidências regional é `editorial/rmrp/QA_TCESP_102_EXTRATOS_DCA_20261019.md`, que documenta a execução 39203495737 e a conferência independente dos 102 JSONs.

## Resultado já comprovado na evidência regional
| Ano | Pares coincidentes | Pares confrontados | TCESP liquidado (R$) | DCA liquidado (R$) |
|---|---:|---:|---:|---:|
| 2023 | 33 | 34 | 484.958.575,24 | 484.948.399,24 |
| 2024 | 34 | 34 | 500.824.152,06 | 500.824.152,06 |
| 2025 | 34 | 34 | 302.301.895,18 | 302.301.895,18 |
| **Total** | **101** | **102** | **1.288.084.622,48** | **1.288.074.446,48** |

A divergência documentada é **Guatapará, código 3518859, exercício 2023**: TCESP **R$ 2.118.940,79**; DCA **R$ 2.108.764,79**; diferença TCESP menos DCA **R$ 10.176,00**. Não há evidência suficiente para atribuir causa ao desvio, substituir valores ou caracterizá-lo como erro de qualquer fonte.

## Regras para comparação e publicação
1. Comparar apenas mesmo município IBGE, exercício, estágio **liquidado** e grupo 44 de investimento. Empenhado e pago não são equivalentes a liquidado.
2. Valores monetários devem ser convertidos a centavos inteiros antes da comparação; ausência ou não aplicabilidade nunca equivale a zero.
3. Classificar pares como `concordante`, `divergente` ou `nao_confrontavel`, preservando procedência, data de obtenção, lote e origem.
4. A igualdade de totais não comprova equivalência metodológica integral da classificação de programa ou ação, atualização temporal ou abrangência institucional; manter camadas TCESP e DCA distintas, com indicação de origem.
5. Não comparar automaticamente códigos ou nomes de programas entre municípios; essas estruturas de classificação são municipais e exigem correspondência explícita.
6. Guatapará/2023 deve permanecer como ressalva auditável no relatório regional até exame dos documentos de origem, classificações e eventuais retificações.

## Alcance das conclusões e lacunas
Este resultado cobre a **RMRP**, não os 644 municípios da camada estadual TCESP. Os totais estaduais de 2023–2025 referem-se ao universo TCESP mais amplo e não devem ser confundidos com os totais regionais apresentados aqui. A conciliação SP645 integral exige acesso ao indicador DCA municipal anual em extração contemporânea da mesma versão canônica e às 1.932 observações municipais TCESP agregadas por estágio; a avaliação deve produzir matriz por código IBGE × exercício com distinção entre diferenças e casos sem confronto.

## Rastreabilidade
- `editorial/rmrp/QA_TCESP_102_EXTRATOS_DCA_20261019.md`, run `39203495737`.
- Camada TCESP estadual: `data/schema/006_tcesp_investimentos.sql`, `pipeline/build/export_tcesp_investimentos_api_v2.py`.
- Prévia integrada externa, sem promoção: `sp645-tcesp-qa-20261026.finbra-tic-tim-referencia.pages.dev`.

**Decisão de governança:** a comparação regional tem evidência suficiente para apresentar 101 concordâncias e a exceção isolada, com ressalvas; a camada estadual permanece sem homologação de paridade TCESP × DCA para todos os municípios.
