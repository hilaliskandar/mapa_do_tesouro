# FED04 — Verificação de Rio das Pedras e Sarutaiá, DCA 2025

**Data de verificação:** 10/11/2026 (continuidade da auditoria iniciada em 09/11/2026). **Escopo:** SICONFI, somente leitura; **sem imputação, migração ou alteração no painel**.

## Fontes oficiais consultadas

- Rio das Pedras (IBGE 3544004): [DCA Anexo I-C 2025](https://apidatalake.tesouro.gov.br/ords/siconfi/tt/dca?an_exercicio=2025&no_anexo=DCA-Anexo%20I-C&id_ente=3544004), [extrato de entregas 2025](https://apidatalake.tesouro.gov.br/ords/siconfi/tt/extrato_entregas?id_ente=3544004&an_referencia=2025).
- Sarutaiá (IBGE 3551207): [DCA Anexo I-C 2025](https://apidatalake.tesouro.gov.br/ords/siconfi/tt/dca?an_exercicio=2025&no_anexo=DCA-Anexo%20I-C&id_ente=3551207), [extrato de entregas 2025](https://apidatalake.tesouro.gov.br/ords/siconfi/tt/extrato_entregas?id_ente=3551207&an_referencia=2025).
- Controles pontuais: [Areias](https://apidatalake.tesouro.gov.br/ords/siconfi/tt/dca?an_exercicio=2025&no_anexo=DCA-Anexo%20I-C&id_ente=3503505) e [Ribeirão Preto](https://apidatalake.tesouro.gov.br/ords/siconfi/tt/dca?an_exercicio=2025&no_anexo=DCA-Anexo%20I-C&id_ente=3543402).

Todas as respostas de dados das diligências principais tiveram `hasMore=false`; os conceitos e números abaixo foram extraídos do JSON oficial. `status_relatorio=HO` reflete o código retornado pelo extrato, sem presumir revisão substantiva independente.

## Rio das Pedras — anomalia estrutural comprovada

O extrato registra **Balanço Anual (DCA), 2025, HO, 14/05/2026 17:01:17 UTC**. Seu Anexo I-C contém **206 registros**, correspondentes a **54 contas distintas**, distribuídos por colunas: 54 receitas brutas, 54 deduções de transferências constitucionais, 44 deduções Fundeb e 54 outras deduções.

As quatro contas específicas investigadas — FPM mensal `RO1.7.1.1.51.1.0`, ITR `RO1.7.1.1.52.0.0`, Fundeb recebido `RO1.7.5.1.00.0.0` e complementação da União `RO1.7.1.5.00.0.0` — **não aparecem no anexo**.

Na coluna `Receitas Brutas Realizadas`, constam receitas correntes de R$ 187.129.000; transferências correntes de R$ 136.437.000; transferências da União `RO1.7.1.0.00.0.0` de R$ 50.388.000, integralmente concentradas na conta genérica `RO1.7.1.9.99.0.0`; outras transferências correntes `RO1.7.9.9.00.0.0` de R$ 34.100.000; transferências de capital R$ 12.270.000. Esses níveis de hierarquia **não podem ser somados entre si como rubricas independentes**.

**Testes de consistência por chave `cod_conta`:**
1. Em **54/54 contas**, `Deduções - Transferências Constitucionais` tem **exatamente o mesmo valor** que `Receitas Brutas Realizadas`.
2. Nas **44/44 contas** com coluna `Deduções - FUNDEB`, tem-se, à precisão de centavo, `Outras Deduções da Receita = (Deduções - FUNDEB) - (Receitas Brutas Realizadas)`.
3. Os **54/54 valores de receitas brutas** são múltiplos inteiros de R$1.000.
4. A consulta de controle a Areias (94 registros) e Ribeirão Preto (185 registros) não apresentou contas com as mesmas quatro colunas comparáveis; a ausência de análogo não demonstra a causa da anomalia.

Essa regularidade matemática exige **ressalva de qualidade e investigação do mecanismo de preenchimento/classificação**, mas não comprova, isoladamente, se o problema foi introduzido na declaração municipal, em uma retificação, na serialização ou no processamento pelo serviço. **Não imputar valores FPM/ITR/Fundeb mediante operações sobre as contas-pai ou sobre a STN**. Próxima evidência recomendada: comparar as naturezas e os valores com o RREO (6º bimestre de 2025, homologado em 03/02/2026) e, conforme viabilidade documental, a MSC de encerramento.

## Sarutaiá — ausência de DCA delimitada, outras entregas comprovadas

O endpoint DCA Anexo I-C para 2025 retornou **zero registros**, `hasMore=false`. O extrato de entregas **não apresentou Balanço Anual (DCA) 2025**, mas comprovou:
- **12 períodos** de MSC Agregada (mensal);
- **MSC Encerramento**, referência 2025, registrada em **08/06/2026 15:23:26 UTC**;
- **seis bimestres do RREO**, identificados como `HO`, o sexto com data **18/02/2026 18:33:03 UTC**.

Logo o status adequado é `dca_2025_not_found_in_official_queries_msc_rreo_available`, e não `receita_zero`, `ausencia_de_toda_prestacao` ou `inadimplencia`. Recomendam-se consultas compatíveis ao RREO e à MSC para **checagem de contexto**, sem convertê-las automaticamente em DCA substituta.

## Conclusões operacionais e controles

- Preservar os 53 preenchimentos complementares já conciliados com a API, sem refazer a matriz estadual.
- Classificar Rio das Pedras como anomalia estrutural do Anexo I-C; não promover as quatro variáveis ausentes nem derivar valores de contas genéricas.
- Classificar Sarutaiá como DCA sem registro consultável no recorte, com MSC/RREO disponíveis, sem inferir receita zero.
- Prosseguir à comparação RREO/MSC e à harmonização histórica 2013–2024.
- **FED04 em andamento.** Nenhuma alteração no SQLite canônico, `observacao`, no R2 já homologado ou na publicação do painel.
