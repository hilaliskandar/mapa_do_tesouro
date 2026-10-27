# Confronto direto da API Siconfi — três maiores diferenças TCESP–DCA

Data: 26/10/2026. Situação: **consultas diretas concluídas para 3 pares; evidência de divergência entre snapshot DCA e API atual em 1 par; causa ainda não demonstrada**.

## Protocolo
Foram consultados `GET /dca` (por exercício, ente e anexo `DCA-Anexo I-D`) e `GET /extrato_entregas` (por exercício e ente). O filtro da linha de investimento é `rotulo=Padrão`, `coluna=Despesas Liquidadas` e `cod_conta=DO4.4.00.00.00.00`. Todas as três respostas DCA indicavam `hasMore=false`, com 132, 332 e 188 linhas, respectivamente; as respostas de extrato apresentavam 39 linhas por ente, `hasMore=false`. Consulta sem escrever em nenhum sistema e sem alterar dados anteriores.

## Resultados

| IBGE | Município | Ano | TCESP R$ | DCA canônica do snapshot R$ | DCA API atual R$ | Situação |
|---|---|---:|---:|---:|---:|---|
| 3548807 | São Caetano do Sul | 2023 | 147.173.188,49 | 161.697.826,62 | 161.697.826,62 | DCA antiga=atual; desvio TCESP persiste |
| 3554102 | Taubaté | 2024 | 45.431.933,66 | 40.273.274,12 | **45.431.933,66** | DCA atual=TCESP; snapshot DCA diferente |
| 3545209 | Salto | 2023 | 39.898.893,44 | 44.506.303,61 | 44.506.303,61 | DCA antiga=atual; desvio TCESP persiste |

**Atenção ao caso Taubaté:** a diferença de **R$ 5.158.659,54** da matriz histórica desaparece quando se compara o TCESP à consulta DCA atual. A alteração da resposta da API em relação ao snapshot canônico indica diferença de versão ou tratamento da fonte, mas **não demonstra ainda a causa**. Não substituir automaticamente o snapshot; criar uma camada versionada de observações.

## Extratos consultados no mesmo atendimento
- 3548807/2023: `entregavel=Balanço Anual (DCA)`, instituição Prefeitura Municipal de São Caetano do Sul, `status_relatorio=RE`, `data_status=2024-07-10T11:41:01Z`.
- 3554102/2024: `entregavel=Balanço Anual (DCA)`, instituição Prefeitura Municipal de Taubaté, `status_relatorio=RE`, `data_status=2025-08-14T09:07:00Z`.
- 3545209/2023: `entregavel=Balanço Anual (DCA)`, instituição Prefeitura Municipal de Salto, `status_relatorio=HO`, `data_status=2024-04-30T15:30:00Z`.

Os códigos `RE` e `HO` foram preservados literalmente; sua interpretação formal e eventual sequência de eventos devem ser confirmadas em documentação oficial. **Não atribuir ao valor divergente uma retificação específica sem comprovação do histórico das versões**.

## URLs reproduzíveis
- https://apidatalake.tesouro.gov.br/ords/siconfi/tt/dca?an_exercicio=2023&id_ente=3548807&no_anexo=DCA-Anexo%20I-D
- https://apidatalake.tesouro.gov.br/ords/siconfi/tt/dca?an_exercicio=2024&id_ente=3554102&no_anexo=DCA-Anexo%20I-D
- https://apidatalake.tesouro.gov.br/ords/siconfi/tt/dca?an_exercicio=2023&id_ente=3545209&no_anexo=DCA-Anexo%20I-D
- Para extratos: https://apidatalake.tesouro.gov.br/ords/siconfi/tt/extrato_entregas?id_ente=3554102&an_referencia=2024 e mesma estrutura para os outros dois entes/anos.

## Próxima auditoria
Consultar os outros sete casos prioritários, resguardando o limite de uma requisição por segundo. Registrar arquivo JSON completo ou hash, quantidade de itens, `hasMore`, valor da conta, data de consulta e extrato. Em seguida comparar a matriz original de 55 diferenças com o **snapshot atual Siconfi, versionado**, para identificar quais discrepâncias persistem e quais desapareceram sem reescrever a base original. Investigar o histórico de envio e retificação especialmente em Taubaté; conferir escopo, elementos e unidades gestoras nos pares ainda divergentes.

Integridade TCESP (10/10 reextraídos) permanece documentada em `governance/REEXTRACAO_TCESP_CASOS_PRIORITARIOS_20261026.md`. Produção inalterada.

## Ampliação: consulta direta de todos os dez casos prioritários
Após o primeiro lote de três, os **outros sete** pares foram consultados pelo mesmo endpoint e critério exato DCA (Anexo I-D, Padrão, Despesas Liquidadas, DO4.4.00.00.00.00). Cada uma das respostas apresentou `hasMore=false`, sem paginação adicional no atendimento. São **consultas do valor atual**, não testes de histórico de versões.

| Município | IBGE | Exercício | DCA histórica R$ | DCA API atual R$ | TCESP R$ | Efeito da atualização na divergência |
|---|---|---:|---:|---:|---:|---|
| Itaóca | 3522158 | 2024 | 7.786.197,26 | 7.786.197,26 | 3.903.919,12 | persiste |
| Novais | 3533254 | 2024 | 5.077.344,87 | 5.077.344,87 | 1.305.232,40 | persiste |
| São Carlos | 3548906 | 2024 | 135.579.005,97 | 135.579.005,97 | 138.740.832,67 | persiste |
| Araçatuba | 3502804 | 2023 | 31.673.342,63 | 31.673.342,63 | 32.513.168,01 | persiste |
| Ourinhos | 3534708 | 2024 | 89.545.844,38 | **90.267.507,66** | 90.267.507,66 | desaparece na API atual |
| Guaraci | 3517901 | 2025 | 4.225.489,20 | 4.225.489,20 | 4.827.778,14 | persiste |
| Iguape | 3520301 | 2024 | 15.053.443,43 | **15.548.454,11** | 15.548.454,11 | desaparece na API atual |

**Balanço dos dez casos:** Taubaté, Ourinhos e Iguape (todos em 2024) mostram na API atual valor DCA idêntico ao TCESP, ao contrário do snapshot DCA anteriormente preservado. Nos outros sete, o valor DCA atual coincide com o snapshot e mantém diferença TCESP. **São diferenças de versão ou conteúdo observado**, sem explicação causal ainda. Para os sete pares deste segundo lote, os extratos de entrega ainda não foram consultados nesta diligência.

URLs são geradas por `https://apidatalake.tesouro.gov.br/ords/siconfi/tt/dca?an_exercicio=AAAA&id_ente=CODIGO&no_anexo=DCA-Anexo%20I-D` para os códigos/anos acima. As consultas retornaram respectivamente 111, 163, 264, 216, 246, 144 e 120 itens, `hasMore=false`. Preservar o snapshot anterior como fonte histórica, sem sobrescrevê-lo.

## Conclusão da consulta de extratos de entrega — dez pares
Foram consultados também os extratos dos sete pares restantes na operação oficial `/extrato_entregas`, com filtros `id_ente` e `an_referencia`, conforme a matriz abaixo. Todos retornaram `hasMore=false`. O número de linhas total das respostas foi registrado, sem confundir as diversas entregas MSC/RREO/RGF com a DCA anual.

| IBGE | Município | Ano | Situação literal DCA | Data do status em UTC | Linhas extrato |
|---|---|---:|---|---|---:|
| 3522158 | Itaóca | 2024 | HO | 2025-06-16T09:34:40Z | 28 |
| 3533254 | Novais | 2024 | HO | 2025-04-03T09:04:17Z | 26 |
| 3548906 | São Carlos | 2024 | HO | 2025-04-30T16:48:54Z | 33 |
| 3502804 | Araçatuba | 2023 | HO | 2024-03-27T17:30:27Z | 36 |
| 3534708 | Ourinhos | 2024 | RE | 2025-10-20T09:24:23Z | 39 |
| 3517901 | Guaraci | 2025 | HO | 2026-03-30T16:52:35Z | 39 |
| 3520301 | Iguape | 2024 | RE | 2026-05-14T14:08:16Z | 38 |

Os três extratos já examinados eram: São Caetano do Sul/2023 `RE` (2024-07-10T11:41:01Z); Taubaté/2024 `RE` (2025-08-14T09:07:00Z); Salto/2023 `HO` (2024-04-30T15:30:00Z). Assim, **10/10 extratos DCA foram consultados**, com três casos de valor atualmente coincidente com TCESP (Taubaté, Ourinhos e Iguape), todos com código `RE`. São Caetano do Sul também apresenta `RE` mas a divergência permanece, o que demonstra que o código sozinho não implica convergência de valor.

Padrão de consulta: `https://apidatalake.tesouro.gov.br/ords/siconfi/tt/extrato_entregas?id_ente=CODIGO&an_referencia=AAAA`. As siglas `RE` e `HO` são transcritas literalmente sem inferir histórico de versões. **O endpoint de extrato não disponibilizou, nesta consulta, o valor anterior de cada retificação.** É necessário investigar a documentação de status e, quando possível, a sequência de arquivos/declarações antigas antes de atribuir causalidade. A base canônica histórica permanece preservada.

## Conclusão da consulta de extratos dos dez casos — 27/10/2026
Consulta independente ao endpoint oficial `/extrato_entregas?id_ente=CODIGO&an_referencia=ANO`. Todos os sete extratos adicionais vieram com `hasMore=false`. Para a Prefeitura Municipal, entregável `Balanço Anual (DCA)`:

| Município | Código IBGE | Exercício | status_relatorio | data_status (UTC) | forma_envio |
|---|---|---:|---|---|---|
| Itaóca | 3522158 | 2024 | HO | 2025-06-16T09:34:40Z | M |
| Novais | 3533254 | 2024 | HO | 2025-04-03T09:04:17Z | P |
| São Carlos | 3548906 | 2024 | HO | 2025-04-30T16:48:54Z | M |
| Araçatuba | 3502804 | 2023 | HO | 2024-03-27T17:30:27Z | P |
| Ourinhos | 3534708 | 2024 | RE | 2025-10-20T09:24:23Z | M |
| Guaraci | 3517901 | 2025 | HO | 2026-03-30T16:52:35Z | M |
| Iguape | 3520301 | 2024 | RE | 2026-05-14T14:08:16Z | M |

Juntamente com os três previamente examinados: São Caetano do Sul/2023 `RE` (2024-07-10), Taubaté/2024 `RE` (2025-08-14) e Salto/2023 `HO` (2024-04-30), temos **10/10 extratos DCA inspecionados**. Os três casos de concordância da DCA atual com o TCESP (Taubaté, Ourinhos, Iguape) têm `RE`; São Caetano do Sul também tem `RE` apesar da divergência persistente. A interpretação formal das siglas e a versão exata de cada declaração ainda dependem de verificação oficial adicional: a correlação não prova causa.

URLs reproduzíveis: `https://apidatalake.tesouro.gov.br/ords/siconfi/tt/extrato_entregas?id_ente=CODIGO&an_referencia=ANO`. Preservar em todas as análises o valor do snapshot DCA histórico e o valor atual como observações separadas.
