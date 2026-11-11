# INV-RMRP — Movimentações financeiras em contas de Transferências Especiais: auditoria de cobertura e limites inferenciais

**Data da consulta:** 11/11/2026. **Universo:** 34 beneficiários municipais da Região Metropolitana de Ribeirão Preto. **PR:** #233 (rascunho). **Fonte:** API pública do Transferegov, módulo `especiais/gestao-financeira-lancamentos-especiais`, consultado com o CNPJ do ente solicitante identificado na lista de beneficiários do próprio Transferegov. O CNPJ utilizado na chamada não foi incorporado aos arquivos de divulgação das operações.

## Aquisição efetiva

Foram recuperadas todas as páginas informadas para cada um dos 34 beneficiários. Resultados: **2.385 lançamentos com IDs distintos, sem repetição, sem páginas ausentes e sem divergência em relação à contagem anteriormente auditada**. Distribuição: **924 créditos contábeis (tipo C)** e **1.461 débitos contábeis (tipo D)**, exercícios **2020–2026** (137, 142, 226, 700, 869, 202 e 109 lançamentos, respectivamente).

As respostas das consultas foram normalizadas em quatro lotes de registros, preservando somente `id_lancamento`, `origem`, `descricao`, `data`, `tipo`, `valor_centavos`, `categoria` e quantidade de subtransações. **Foram deliberadamente excluídos: banco, agência, número e DV de conta, identificadores de depositante e favorecido, documentos pessoais e informações bancárias de terceiros.** As operações individualizadas ficam documentadas em `governance/inv_rmrp_especiais_movimentacoes/lote_01_...json` a `lote_04_...json`. Verificação de consistência: [`INV_RMRP_ESPECIAIS_2385_LANCAMENTOS_QA_2026_11_11.json`](INV_RMRP_ESPECIAIS_2385_LANCAMENTOS_QA_2026_11_11.json).

Foi materializada consulta **somente agregada por município, ano, tipo de lançamento e descrição normalizada** em [`app/static/data/api/v3/investimentos/rmrp/especiais-movimentacoes-resumo-preview.json`](../app/static/data/api/v3/investimentos/rmrp/especiais-movimentacoes-resumo-preview.json): 778 linhas de agrupamento referentes aos 2.385 lançamentos. Interface [`app/static/movimentacoes-especiais-rmrp-preview.html`](../app/static/movimentacoes-especiais-rmrp-preview.html), exclusiva da PR nº 233, com filtros por município, exercício, operação de crédito/débito e descrição.

## Evidência financeira: interpretação precisa

A API não informa, nessa rota, um identificador determinístico compartilhado entre o lançamento da conta e o `id_plano_acao`, `id_dh` ou `id_op_ob`. Assim, o cadastro de contas por município **não autoriza vincular automaticamente um lançamento a um plano ou a uma ordem bancária**, nem afirmar o recebimento de um valor previsto específico apenas pela coincidência de data e montante.

A triagem descritiva localizou **282 créditos candidatos a ingresso** (alguns rotulados `CRED TED`, `CRED TEV`, `Ordem Bancária` ou `Transferência recebida`), equivalentes a **R$68.327.205,37 em movimentos**. **Esse valor é diagnóstico preliminar e não pode ser utilizado como total de transferências federais efetivamente recebidas ou como total de investimentos.** Mesmo os demais lançamentos de tipo C incluem movimentos contábeis internos. Exemplos de mistura de eventos:
- `C | RSG FUNDO`: resgate de aplicação — entrada na conta transitória, não novo repasse;
- `D | APL AUTOM` e `D | APL FUNDO`: aplicação financeira — não despesa de obra;
- `D | ENVIO TED`, `D | DÉB FORNEC`: saídas que requerem classificação, documento e distinção entre custeio e investimento;
- `C | CRED TED` e `C | Ordem Bancária`: possíveis ingressos a identificar na origem específica do crédito e em referência documental.

Há **284 planos de ação**, **284 empenhos**, **257 documentos hábeis** e **246 registros de OP/OB** na auditoria paralela, distribuídos por 242 planos com OB, dez com DH sem OB e 32 com empenho sem DH. O valor de empenhos totaliza **R$96.303.325,06** e o dos DH **R$85.451.825,06**. A diferença de **R$10.851.500,00** corresponde integralmente aos 32 planos sem DH retornado; entre os 252 com DH, a soma do DH coincide com o empenho. **Não somar valores de diferentes estágios ou adicionar o valor do lançamento bancário ao empenho como novo investimento.**

## Limites e próximos testes

1. Examinar na API a rota `gestao-financeira-subtransacoes-especiais` por `id_lancamento_gestao_financeira`: existe parâmetro de `situacao_pagamento_subtransacao_gestao_financeira`, mas duas consultas exploratórias a IDs conhecidos retornaram **zero subtransações**. Não inferir completude geral dessas subtransações.
2. Buscar uma **chave oficial de conciliação** entre extratos da gestão financeira e OP/OB: número de ordem bancária, referência única ou documentação de origem; não aceitar vínculos por mera proximidade temporal/monetária. Conferir estado de compensação/cancelamentos, estornos e retificações.
3. Separar transferências para caixa municipal, rendimentos de aplicação, devoluções, movimentações internas e despesas com fornecedores por classificação documentada. Não atribuir a uma obra sem instrumento/nota/contrato.
4. Verificar fontes estaduais e despesas diretas federais/estaduais; cruzar transferências de capital e investimentos liquidados TCESP **como métricas distintas**, não aditivas.
5. Manter fontes granulares na trilha interna de QA e disponibilizar na PR somente **agregados cautelares**, sem dados bancários/pessoais.
6. Executar QA local e remota do `deployment/materialize_investimentos_preview.py` e `deployment/qa_investimentos_preview.py` para habilitar a quarta página experimental. **Não afirmar implantação concluída antes da execução do workflow.**

**Condição de homologação:** os lançamentos financeiros são prova de operações registradas na plataforma e permitem estudar a trajetória financeira do ente. Sem reconciliação documental, não constituem prova de investimento realizado por projeto. A PR permanece draft; produção, SQLite/R2/D1 canônicos e FED04/PR #232 não foram modificados.
