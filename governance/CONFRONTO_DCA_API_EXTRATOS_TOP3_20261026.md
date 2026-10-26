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
