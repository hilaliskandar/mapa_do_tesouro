# Lote 92 — consolidação da série de receitas de capital 2015–2025 e auditoria dos indicadores de Pontal

**Data:** 04/11/2026. **Volume II da RMRP — pré-homologação.** A presente rodada produziu base municipal consolidada e verificou diretamente em API oficial da STN os denominadores e percentuais de Pontal. Não foram alterados os DOCX/PDF do Volume II, as matrizes SWOT ou os cenários 2027–2030.

## 1. Consolidação efetivamente executada

- **2015–2019:** importada planilha histórica de 170 município–ano (Lote 38), Drive `1ZddPo59osLV8L7J1pXJsgnmw2GJP_G5x`. Não reextraída dos arquivos FINBRA originais nesta rodada.
- **2020–2025:** incorporados os 204 município–ano efetivamente extraídos dos seis arquivos anuais no Lote 91; referência Drive `1_pykfuwvsFF-2Cle4sHLrmqsxvU7JyUJ`.
- As chaves são `(ano, codigo_ibge)`, para 34 municípios e onze exercícios; selecionada somente conta sintética de **Receitas de Capital brutas realizadas**, sem soma de contas filhas e sem equiparar a transferências de capital.
- **374 chaves, 367 observações monetárias, sete ausências, zero duplicações.** Ausência não foi convertida em zero.

| Ano | Cobertura | Total observado, R$ correntes | Situação |
|---|---:|---:|---|
| 2015 | 33/34 | 145.496.484,69 | parcial |
| 2016 | 34/34 | 159.118.107,21 | integral |
| 2017 | 32/34 | 121.487.429,28 | parcial |
| 2018 | 34/34 | 140.360.152,20 | integral |
| 2019 | 34/34 | 185.061.364,14 | integral |
| 2020 | 34/34 | 311.469.228,18 | integral |
| 2021 | 33/34 | 212.418.462,03 | parcial |
| 2022 | 33/34 | 295.518.170,79 | parcial |
| 2023 | 34/34 | 291.477.896,93 | integral |
| 2024 | 32/34 | 356.106.269,27 | parcial |
| 2025 | 34/34 | 327.942.785,14 | integral |

Lacunas: Cássia dos Coqueiros 2015; Cajuru e Santa Cruz da Esperança 2017; Santa Rita do Passa Quatro 2021; Santa Cruz da Esperança 2022; Cajuru e Morro Agudo 2024.

**Artefato principal arquivado com upload confirmado no Drive:** `RMRP_SERIE_RECEITA_CAPITAL_BRUTA_2015_2025_LOTE92.xlsx` — https://docs.google.com/spreadsheets/d/1FZTTtIRLJkoY_iwKhjsWC6leI1icZCgu/edit (ID `1FZTTtIRLJkoY_iwKhjsWC6leI1icZCgu`). Possui abas `SERIE_374`, `COBERTURA_ANUAL`, `LACUNAS`, `LEIA_ME`, `PONTAL_QA_RGF_RREO` e `RGF_8_PENDENCIAS`. Nas abas de controle foram mantidas fórmulas com resultados em cache, conferidos programaticamente em modo `data_only`: C2 33, D2 1, E2 145.496.484,69; C13 367, D13 7. A biblioteca `artifact_tool` não disponibilizou a classe esperada neste ambiente; conferência foi realizada com `openpyxl` e inspeção estrutural do arquivo.

CSV local `RMRP_SERIE_RECEITA_CAPITAL_BRUTA_2015_2025_LOTE92.csv` (74 KB), script `gerar_consolidacao_lote92.py`, complemento `complementar_lote92_pontal.py` e `QA_LOTE92.json` foram gerados no ambiente da conversa. **O CSV não foi arquivado no Drive nesta rodada**: a tentativa de persisti-lo na Library ultrapassou o limite de armazenamento, embora o XLSX principal tenha upload Drive confirmado. QA e nota metodológica auxiliares tiveram depósito na Library, mas a tentativa de remessa ao Drive não foi confirmada; o relatório GitHub é a referência textual permanente.

## 2. Pontal: causa objetiva do outlier localizada em declarações oficiais

Foram efetivamente consultados os endpoints da API pública STN `https://apidatalake.tesouro.gov.br/ords/cdwhprd/siconfi/tt/` com filtros de **município 3540200**, **Poder Executivo (E)**, exercício e período exatos.

- RGF **Anexo 02**, **2025, 2º quadrimestre**: RCL **R$ 203.662.085,89**; DCL **R$ 63.005.269,88**; relação DCL/RCL informada **30,94%**.
- RGF **Anexo 02**, **2025, 3º quadrimestre**: RCL **R$ 13.494.039,69**; DC **R$ 173.246.915,32**; DCL **R$ 179.919.782,20**; relações DC/RCL **1.283,88%** e DCL/RCL **1.333,33%**. O denominador de 13,49 milhões é reproduzido pelo **RGF Anexo 06** da mesma declaração.
- RGF **Anexo 06**, **2025, 3º quadrimestre**: DTP **R$ 108.682.695,50**, percentual DTP/RCL ajustada **805,41%** e RCL ajustada para pessoal **R$ 13.494.039,69**.
- **RREO Anexo 03**, **2025, 6º bimestre**: RCL **R$ 209.571.785,24**; RCL ajustada para cálculo dos limites de pessoal **R$ 209.271.785,24**.
- RGF **Anexo 06**, **2024, 3º quadrimestre**: RCL **R$ 202.225.623,72**, DTP **R$ 98.231.768,49** e indicador DTP/RCL ajustada **49,46%**.

**Divergência objetiva 2025:** RREO RCL R$209.571.785,24 menos RGF RCL R$13.494.039,69 = **R$196.077.745,55**. O RREO registra RCL **15,53 vezes** a do RGF no mesmo encerramento. Não se trata de um mero ponto percentual isolado, mas de **incompatibilidade entre denominadores oficialmente informados**. Os percentuais 805,41%, 1.283,88% e 1.333,33% **são efetivamente dados da declaração de RGF**, não erro de transcrição da matriz do projeto; contudo, a divergência do denominador torna **inadequado** utilizá-los para caracterizar infração à LRF, ranking fiscal ou simulação. **Manter quarentena** e solicitar verificação/retificação oficial, sem substituir automaticamente pelos índices calculados a partir do RREO.

Consulta RGF Anexo 02 Q3: https://apidatalake.tesouro.gov.br/ords/cdwhprd/siconfi/tt/rgf?an_exercicio=2025&in_periodicidade=Q&nr_periodo=3&co_tipo_demonstrativo=RGF&no_anexo=RGF-Anexo%2002&id_ente=3540200&co_poder=E

Consulta RGF Anexo 06 Q3: https://apidatalake.tesouro.gov.br/ords/cdwhprd/siconfi/tt/rgf?an_exercicio=2025&in_periodicidade=Q&nr_periodo=3&co_tipo_demonstrativo=RGF&no_anexo=RGF-Anexo%2006&id_ente=3540200&co_poder=E

Consulta RREO Anexo 03 B6: https://apidatalake.tesouro.gov.br/ords/cdwhprd/siconfi/tt/rreo?an_exercicio=2025&nr_periodo=6&co_tipo_demonstrativo=RREO&no_anexo=RREO-Anexo%2003&id_ente=3540200

Consulta RGF Q2: https://apidatalake.tesouro.gov.br/ords/cdwhprd/siconfi/tt/rgf?an_exercicio=2025&in_periodicidade=Q&nr_periodo=2&co_tipo_demonstrativo=RGF&no_anexo=RGF-Anexo%2002&id_ente=3540200&co_poder=E

**Interpretação:** a apuração do RREO e do RGF pode envolver ajustes de RCL segundo a finalidade; a diferença observada é excessiva para ser esclarecida por simples troca de indicadores. **Hipótese de erro na declaração é plausível, não comprovada**; a manifestação oficial do ente, retificação e exame do demonstrativo publicado são necessários. Não imputar conduta nem usar percentuais em análise normativa.

## 3. Oito municípios antes ausentes — teste pontual não decisivo

Na API STN foram realizadas consultas RGF Anexo 06, Q3/2025, Executivo para **Barrinha, Guariba, Nuporanga, Orlândia, Pitangueiras, Sales Oliveira, Taiúva e Taquaral**. Para sete municípios, filtro retornou 0 registros; **Taiúva** não pode ser concluída, porque a ferramenta bloqueou a consulta. Testes adicionais (Guariba Q2 e S2, Barrinha Q2, Taquaral S2) também retornaram 0.

**Não interpretar** 0 registros no filtro como comprovação de não entrega: outro período, periodicidade, identificação da declaração, esfera/poder e situação de transmissão podem mudar a consulta. Ainda é necessário verificar o **extrato oficial de entregas**, modalidade de declaração, anexos específicos e eventual data de retificação. A cobertura interna histórica de 26/34 registros, documentada no Lote 36, permanece **não homologada** para comparações legais.

## 4. Próximas providências de QA

1. Revisar na fonte Siconfi eventual retificação do RGF 2025 de Pontal; conciliar RCL 209,57 milhões no RREO com 13,49 milhões no RGF e obter explicação formal do ente, sem estimativa corretiva automática.
2. Investigar as sete lacunas de receitas de capital por declarações substitutivas e verificar transição dos códigos contábeis DCA; só então completar a série em preços reais pelo IPCA médio anual.
3. Reabrir extratos de entregas e RGF/RREO de cada um dos oito municípios antes ausentes, separando verdadeira não entrega de lacuna de extração.
4. Recuperar e conciliar CSVs Transferegov FNDE 959097/2024 e instrumento 953042; não foi resolvido neste Lote 92.
5. Completar QA visual e revisão jurídica do Volume II; **pré-homologação permanece**.

**Conclusão:** a série municipal de onze anos está materialmente integrada, com observações e lacunas rastreáveis. No caso de Pontal, foi comprovada a inconsistência interdeclarações que explica a origem dos percentuais anômalos, sem autorização para afirmar irregularidade ou violação legal.
