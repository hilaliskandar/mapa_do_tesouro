# RMRP — decomposição municipal da trajetória de investimentos (2023–2025)

Data: 19/10/2026. Fonte: DCA SP645 canônica 2013–2025, recorte de 34 municípios segundo `editorial/rmrp/municipios_subregioes_tcesp.csv`. Séries nominais de investimento liquidado e receita corrente, sem substituição por TCESP em Guatapará 2023.

## Distribuição e mudança de investimentos

| Sub-região | Municípios | Maior investimento em 2025 | Participação do maior | Participação dos três maiores | Municípios em queda | Variação nominal agregada 2023–2025 |
|---|---:|---|---:|---:|---:|---:|
| SR1 | 15 | Ribeirão Preto | 53,64% | 82,32% | 13/15 | −R$ 102.310.107,59 |
| SR2 | 6 | Guariba | 28,49% | 77,68% | 6/6 | −R$ 30.508.604,35 |
| SR3 | 6 | Mococa | 37,16% | 77,84% | 4/6 | −R$ 4.896.926,73 |
| SR4 | 7 | Batatais | 39,58% | 82,09% | 7/7 | −R$ 44.930.865,39 |

Na SR1, Ribeirão Preto respondeu por −R$ 81.066.853,46 da queda de −R$ 102.310.107,59; os outros 14 municípios registraram retração conjunta de 18,04% no período. Na SR2 todos os municípios registraram queda; as maiores reduções absolutas foram Pitangueiras (−R$ 12,15 milhões), Guariba (−R$ 9,59 milhões) e Jaboticabal (−R$ 4,63 milhões). Na SR3 dois municípios tiveram aumento e quatro queda; na SR4 todos apresentaram retração, destacando-se Batatais (−R$ 17,78 milhões), Morro Agudo (−R$ 7,42 milhões) e Orlândia (−R$ 7,28 milhões).

## Método e QA

Foram calculados para os 34 municípios os valores liquidados de investimento de 2023 e 2025, variação absoluta e percentual, participação no investimento total da sub-região, intensidade investimento/receita corrente de cada exercício e receita corrente nominal. Os valores de 2023 e 2025 são observados nos 34 municípios; por sub-região e por ano, o somatório dos registros municipais coincide exatamente, até centavos, com o agregado DCA histórico `dca_historico_subregional_2013_2025.csv`. Filtros de 2023 e 2025 foram usados na comparação; as séries reais do IPCA continuam registradas separadamente.

Arquivos derivados: `decomposicao_investimentos_municipal_2023_2025.csv`, `concentracao_investimentos_subregioes_2025.csv` e script `decomposicao_municipal.py` no diretório de execução do projeto. Não confundir concentração de investimento com população ou demanda territorial; não inferir causalidade a partir da decomposição. Classificação de precatórios permanece simplificada e não demanda exames de processos individuais.

## Integração ao caderno

Usar perfil metropolitano → comparação sub-regional → decomposição municipal. Nas fichas, destacar participação no total, trajetória e divergência de padrão sub-regional quando material. Não substituir as tabelas municipais por perfis somente de municípios-polo. Manter séries nominais e reais explicitamente distintas, bem como cobertura de contas e qualidade da conciliação TCESP/DCA.
