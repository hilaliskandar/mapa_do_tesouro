# Revisão de integração do PR #143 — 2026-10-15

Estado: **RETER EM RASCUNHO**. Não executar merge ou publicação de produção.

## Evidências verificadas
- PR #143 contém 15 arquivos alterados, incluindo boletim HTML, rotinas TCESP, testes de navegador, workflow de preview e protocolo dos 12 universos.
- Core CI e Pages Preview no commit `4530e9741bc390ad3c2293e3282a130c88202a2c`: concluídos com sucesso (runs 38083298053 e 38083298057). Isto não prova aprovação do workflow independente de extração `rmj-editorial-preview.yml`.
- `editorial/rmj/conciliacao_tcesp_dca_2023_2024.csv` declara 14 resultados `CONCILIADO`, mas `editorial/rmj/RETOMADA_2026-10-10.md` afirma que a execução anteriormente consultada foi cancelada antes de comprovar as 14 consultas. Há inconsistência de rastreabilidade, ainda que não se conclua erro dos valores.
- `editorial/rmj/qa_tcesp_2023_2024.py` verifica somente integridade de extração e escreve `PENDENTE_DCA`: não confere a DCA canônica.
- A extração TCESP no workflow é `continue-on-error`, e os testes e deploy prosseguem mesmo com ausência de evidência TCESP; isto é aceitável para complemento opcional, desde que nenhum conteúdo dependente dessa evidência seja anunciado como certificado.
- O protocolo editorial prioriza FINBRA/DCA e limita TCESP detalhado a estudos específicos. Não há justificativa para transformar a coleta dos 23 municípios externos à RMJ em requisito de merge.
- Protocolo propõe 12 universos, enquanto API editorial v0.4.0 tem 11; TIC_TIM_30 exige contrato editorial próprio se publicado como 12º.

## Gates antes do merge
1. **G0:** identificar o artifact, job, arquivo, SHA-256 e fonte oficial para cada uma das 14 conciliações TCESP × DCA 2023/24; não confiar apenas na tabela de resultados.
2. **G1:** rodar verificação em centavos, por município/ano e estágio, dos totais de investimento; erros e divergências impedem promoção desses dados. Uma execução sem erros de download não equivale à conciliação.
3. **G2:** manter o resumo FINBRA como independente da extração TCESP; marcar conteúdo complementar como `pendente` quando G0/G1 falharem.
4. **G3:** conferir dados, links, gráfico/tabela, acessibilidade e status HTML com prévia remota e evidência de navegador dos dois tamanhos de tela.
5. **G4:** resolver diferença 11 vs 12 universos, sem alterar cadastro fiscal de produção por conveniência editorial.
6. **G5:** confirmar deflator e ano-base antes de exibir valores reais; na falta, identificar a série como nominal.
7. **G6:** reexecutar CI e preview após integração dos PRs #166 e #167 em `main`. Não publicar automaticamente.
8. **G7:** obter aprovação editorial expressa para versão final.

## Extração adicional
Não realizar coleta maciça ou inferência de dados sem necessidade documentada. Prioridade: recuperar artifacts existentes do GitHub Actions, que preservam as fontes usadas, e confrontar os extratos com a DCA já homologada. Nova consulta à fonte TCESP somente para pares com artifact ausente, corrompido ou divergente; guardar SHA, URL, ano, município, estágio e momento da coleta.

## Situação em 2026-10-15
PR mantido em rascunho, pendências acima abertas. A incorporação dos PRs #166 e #167 não altera por si a prova de conciliação editorial.

## Evidência adicional recuperada e examinada

O artifact GitHub Actions `11680818755`, gerado no run `38083298057`, foi recuperado e auditado. O ZIP tem SHA-256 `3c7d59fdc6fe570d93af0f26ae4bbf0176dc24858f13fd8da5305f8bc0fd48c7`. Contém 14 JSONs municipais de 2023–2024, logs, manifesto e `qa_summary.json` com 14 extrações bem-sucedidas e zero erros. O controle original declara `pendentes_conciliacao_dca=14`.

A auditoria independente dos JSONs confirmou 14/14 equivalências exatas, em centavos, com **a coluna TCESP** de `editorial/rmj/conciliacao_tcesp_dca_2023_2024.csv`, além do fechamento dos totais de programa e ação do grupo 44 liquidado e presença de hashes ZIP nos 14 extratos. **Não foi feita leitura independente do arquivo canônico DCA para validar a coluna DCA da tabela.** Logo, a expressão `CONCILIADO` da tabela ainda requer comprovação dessa segunda fonte. Este achado substitui a suspeita inicial de ausência dos extratos, mas não aprova a conciliação interfontes.

Não é necessária nova extração TCESP para esses 14 casos: os dados primários da extração já estão preservados no artifact. Nova coleta só se justifica após demonstrar lacuna/retificação ou discrepância em fonte primária.
