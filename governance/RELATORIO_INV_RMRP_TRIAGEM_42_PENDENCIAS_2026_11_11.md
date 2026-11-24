# INV-RMRP — Fila priorizada de reconciliação documental dos 42 planos sem OB retornada

**Data da triagem:** 11/11/2026. **Fonte exclusiva desta classificação:** matriz versionada `governance/INV_RMRP_ESPECIAIS_284_CADEIAS_FINANCEIRAS_MATRIZ_2026_11_11.csv`, oriunda da API oficial Transferegov. **PR:** #233. Esta rodada organiza dados existentes: não representa reconsulta aos endpoints federais nem confirmação de crédito.

## Resultado da triagem

- Universo: 284 planos em 34 municípios, dos quais 242 possuem ao menos uma ordem bancária retornada.
- **10 planos com documento hábil, mas sem ordem bancária retornada**, somando **R$ 3.383.000,00 em empenhos**. Priorizar reconsulta de OP/OB pelo identificador do documento hábil; conferir cancelamentos e estados, sem converter retorno vazio em pagamento zero.
- **32 planos com empenho, mas sem documento hábil retornado**, somando **R$ 10.851.500,00 em empenhos**. Reconsultar documentos hábeis por identificador oficial de empenho, conferir a situação administrativa e eventual impedimento.
- Os 42 planos sem OB retornada totalizam **R$ 14.234.500,00 em empenhos**; esse valor NÃO mede recursos perdidos ou investimentos efetivamente realizados.
- Situações administrativas entre os 42: **11 CIENTE**, **25 IMPEDIDO**, **2 Impedido por Rejeição do Plano de Trabalho** e **4 Plano de Trabalho em Elaboração/Aguardando Envio para Análise**. Logo, 27 casos com impedimento/rejeição e quatro em elaboração/análise exigem tratamento distinto dos 11 CIENTE.

## Contrato da fila

Arquivo: `governance/INV_RMRP_ESPECIAIS_42_PENDENCIAS_DOCUMENTAIS_FILA_2026_11_11.csv`. Uma linha por `id_plano_acao`; classificação e valores preservados da matriz original; ordenação: primeiro DH sem OB, depois empenho sem DH, e dentro de cada grupo, maior empenho. `PENDENTE_RECONSULTA_DOCUMENTAL` é status de investigação, não status bancário. Os valores não são acumuláveis com investimentos planejados, documentos hábeis ou lançamentos bancários.

## Próximo procedimento reproduzível

1. Para os 10 casos DH sem OB, recuperar os documentos hábeis pela cadeia `id_plano_acao → id_empenho → id_dh`, depois consultar `ordens-pagamentos-ordens-bancarias-especiais` pelo `id_dh`, com paginação, data da consulta, estado e identificador original preservados.
2. Para os 32 casos sem DH, consultar `documentos-habeis-especiais` a partir do empenho; registrar explicitamente `SEM_RETORNO_NA_CONSULTA`, `IMPEDIMENTO`, `DOCUMENTO_IDENTIFICADO` ou `ERRO_DE_COLETA`. Não interpretar ausência como zero.
3. Verificar os 11 `CIENTE` e os 27 impedidos/rejeitados com critérios administrativos diferentes; os quatro em elaboração/análise demandam atualização da situação antes de inferência financeira.
4. **Não associar** os 2.385 lançamentos de gestão financeira aos 284 planos por nome, valor ou data. Manter `SEM_CHAVE_DOCUMENTAL` até prova de identificador oficial ou documento vinculante. Não publicar créditos contábeis como repasses homologados.
5. Após nova aquisição, comparar versões, registrar mudanças e atualizar somente a branch isolada. Não alterar SQLite/R2/D1 produtivos nem integrar a PR #233 sem QA independente.

**Controle de implantação:** a quarta prévia e seus workflows não foram homologados nesta triagem; os IDs de runs anteriores não retornaram detalhes verificáveis de jobs pela consulta disponível. Verificação remota continua pendente.
