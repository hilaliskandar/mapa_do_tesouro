# INV-RMRP — Conciliação completa de 284 planos especiais e movimentação financeira por beneficiário

**Data:** 11/11/2026. **Escopo:** 34 municípios RMRP, Transferegov — Transferências Especiais. **Estado:** consulta documental e de movimentação financeira auditada; **crédito de cada plano e investimento executado ainda não homologados**.

## 1. Cadeia documental concluída para 284 planos

Foram confrontados `planos-acao-especiais` (id_plano_acao), `empenhos-especiais` (id_plano_acao/id_empenho), `documentos-habeis-especiais` (id_empenho/id_dh) e `ordens-pagamentos-ordens-bancarias-especiais` (id_dh/id_op_ob). Todas as relações foram feitas com identificadores oficiais. Os 284 planos são distintos, as consultas não apresentaram erro ou página de resultado pendente na cadeia; as respostas ficam em 11 lotes JSON e na matriz consolidada.

| Etapa mais avançada encontrada | Planos |
|---|---:|
| Com ordem bancária na consulta | **242** |
| Documento hábil sem ordem bancária retornada | **10** |
| Empenho sem documento hábil retornado | **32** |
| Sem empenho retornado | **0** |
| **Total** | **284** |

Documentos: **284 empenhos**, **257 documentos hábeis**, **246 ordens bancárias**. Os 242 planos com ao menos uma OB incluem alguns com mais de uma ordem. **Todos os estados de OB observados:** `OB Enviada à instituição bancária para pagamento`, sem verificação independente de crédito ao beneficiário.

**Conciliação monetária:** o conjunto tem **R$96.303.325,06 em registros de empenho**, **R$85.451.825,06 em documentos hábeis** e **R$10.851.500,00 de diferença**. Nos **252 planos com DH** a diferença entre total do empenho e soma dos DH por plano é **zero**; a diferença geral provém dos **32 planos sem DH retornado**, sem que isso autorize converter `DH ausente` em zero de receita ou empenho. Os R$96,3 milhões em empenhos abrangem todos os planos (investimento e custeio), e não correspondem somente aos R$93,0 milhões de investimento previsto. É necessário avaliar diferenças de situação, calendário e natureza entre empenhos e valores de planos.

**Fontes preservadas:**
- [matriz municipal e financeira dos 284 planos](INV_RMRP_ESPECIAIS_284_CADEIAS_FINANCEIRAS_MATRIZ_2026_11_11.csv);
- [resumo de QA e diferenças](INV_RMRP_ESPECIAIS_284_CADEIAS_FINANCEIRAS_QA_2026_11_11.json);
- lotes `governance/inv_rmrp_especiais_cadeias/parte_02...` até `parte_12...`, além dos oito casos originais em `INV_RMRP_ESPECIAIS_8_CADEIAS_EMPENHO_DH_OB_2026_11_11.csv`.

## 2. Gestão financeira das contas de transferências especiais

A API pública de **`gestao-financeira-lancamentos-especiais`** foi consultada por CNPJ do beneficiário jurídico dos 34 municípios da RMRP, com todas as páginas informadas (tamanho 200, até 12 páginas por consulta; nenhum município exigiu mais), cobrindo **2.385 lançamentos**; **34/34 consultas completas**, nenhum município sem registro.

A triagem de descrição e tipo de operação identificou **282 lançamentos candidatos a crédito/recebimento**, conforme palavras como `Ordem Bancária`, `CRED TED`, `CRED TEV` e `Transferência recebida`, que somam **R$68.327.205,37** no recorte de consulta. Esse montante **não deve ser reportado como repasse efetivamente creditado por plano**. Descrições são heterogêneas, o lançamento pode representar transferência interna ou outro crédito e não foi confrontado com o identificador SIAFI da OB específica. Além disso, os valores de créditos e débitos totais da conta podem conter aplicações financeiras, resgates, estornos, fornecedores, transferências internas e taxas, não constituindo fluxo orçamentário deduplicado. No teste foi verificada a descrição `CRED TED` para valor de R$0,11, seguida de aplicação automática correspondente, demonstrando que descrição genérica não identifica repasse de grande valor.

Para não expor informações financeiras excessivas e evitar confusões, o artefato guarda **apenas contadores, categorias normalizadas, intervalos de datas e somas agregadas por município**. Não foram publicados números de conta bancária, dados pessoais, CPF de favorecidos ou descrições individuais com identificadores de terceiros.

Arquivo: [auditoria de cobertura de 34 municípios e 2.385 lançamentos](INV_RMRP_ESPECIAIS_MOVIMENTACAO_FINANCEIRA_34_COBERTURA_2026_11_11.json).

## 3. Prévia consultável

Foram criados:
- [base JSON de 284 planos por município, ano e estágio](../app/static/data/api/v3/investimentos/rmrp/especiais-planos-etapas-preview.json);
- [consulta HTML de Transferências Especiais](../app/static/especiais-rmrp-preview.html), com filtros por município, ano, categoria e estágio documental.

A materialização de Cloudflare Pages foi ajustada para **incluir essa terceira consulta somente na PR nº 233**, com QA local e remoto para 284 IDs únicos, 34 municípios, 242 planos com OB e marcador de consulta não homologada. A disponibilidade no endereço de prévia será confirmada após aprovação do workflow. A base canônica produtiva não foi alterada.

## 4. Próximos passos técnicos

1. Conciliar a identidade de cada OB com lançamentos de gestão financeira **por referência exata e conta de destino devidamente registrada**, sem apresentar detalhes sigilosos na consulta pública. Distinguir OB enviada, crédito registrado, estorno e aplicação do recurso. Investigar 32 sem DH e 10 sem OB, separando impedimentos e atualizações posteriores.
2. Recuperar convênios e liberações **estaduais** Sefaz-SP/SIAFEM, com classificação de investimento/custeio e estornos. A integração do Estado é necessária para o balanço dos três níveis de governo.
3. Executar coletores íntegros de Obrasgov SP e Transferegov Parcerias/Discricionárias, verificando hashes e readback. Não substituir extração completa por contagem.
4. Carregar os planos e eventos em **cópia real do SQLite canônico**, mantendo `inv_plano_acao`, `inv_instrumento`, `inv_evento_financeiro`, `inv_projeto` e `inv_projeto_municipio` bem separados e respeitando relações comprovadas.
5. Homologar os filtros de RMRP, 50 consultas e indicadores sem dupla contagem entre repasse recebido e despesa executada.

**Estado:** nenhuma ordem bancária foi automaticamente promovida a crédito efetivo, nenhuma transferência foi somada à despesa final, nenhum merge/deploy produtivo nem alteração SQLite/R2/D1 canônicos. PR #233 draft, FED04/PR #232 preservados.
