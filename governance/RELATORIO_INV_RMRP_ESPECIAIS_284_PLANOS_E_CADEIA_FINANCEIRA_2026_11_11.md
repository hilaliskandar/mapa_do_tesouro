# INV-RMRP — Transferências Especiais: planos, custeio/investimento e cadeia financeira

**Data:** 11/11/2026. **PR:** #233 (draft). **Enquadramento:** auditoria documental estadual SP e piloto 34 municípios RMRP, sem homologar pagamentos efetivamente creditados nem execução final municipal.

## 1. Fonte e universo

Foi consultada a API oficial do módulo Transferências Especiais:

- `/especiais/beneficiarios-especiais?uf_beneficiario=SP&pagina={p}&tamanho_da_pagina=200`: quatro páginas completas, **628 beneficiários SP** retornados. Após normalização da denominação jurídica, correspondência **34/34** municípios RMRP, 34 beneficiários distintos, com `id_beneficiario`, `id_ente` e CNPJ de pessoa jurídica. Os identificadores IBGE7 foram preservados por *join* com a lista RMRP homologada no IBGE; o `id_ente` Transferegov não deve ser confundido com IBGE7.
- `/especiais/planos-acao-especiais?id_beneficiario={id}&pagina=1&tamanho_da_pagina=200`: 34 consultas, todas com apenas uma página e contagem recebida igual ao `total_items`, total **284 planos** com IDs únicos. Os registros foram minimizados para não armazenar campos de contas bancárias, endereços eletrônicos ou dados pessoais desnecessários.

Foram preservados os quatro lotes municipais `governance/inv_rmrp_especiais_planos/parte_01_2026_11_11.json` a `parte_04_2026_11_11.json`; o cadastro de beneficiários em `governance/INV_RMRP_TRANSFEREGOV_ESPECIAIS_BENEFICIARIOS_2026_11_11.json`; o [CSV dos 284 planos](INV_RMRP_ESPECIAIS_PLANOS_CONSOLIDADO_2026_11_11.csv) e [resumo QA](INV_RMRP_ESPECIAIS_RESUMO_2026_11_11.json).

## 2. Resultados declarados nos planos de ação, 2020–2026

| Informação | Total |
|---|---:|
| Municípios com beneficiário identificado | **34** |
| Planos com ID único | **284** |
| Planos categorizados `INVESTIMENTO` | **270** |
| Planos categorizados `CUSTEIO` | **14** |
| Soma dos campos `valor_investimento_plano_acao` | **R$ 93.046.325,06** |
| Soma dos campos `valor_custeio_plano_acao` | **R$ 3.257.000,00** |

**Situação administrativa:** 253 `CIENTE`; 25 `IMPEDIDO`; 4 `Plano de Trabalho em Elaboração/Aguardando Envio para Análise`; 2 `Impedido por Rejeição do Plano de Trabalho`. Não confundir situação `CIENTE` com pagamento. A soma é documental, inclui planos impedidos e **não deve ser publicada como investimento contratado, pago, creditado ou executado**.

O período de planos originais compreende 2020–2026; valores correntes nominais. Não foi aplicada deflação nem feita análise de estornos. O caráter especial da transferência não garante que a despesa final seja executada no território do município recebedor.

## 3. Primeira auditoria de cadeia financeira: oito planos de maior valor selecionados

A sequência oficial testada foi:

`id_plano_acao` → consulta `/empenhos-especiais?id_plano_acao={id}` → `id_empenho` → consulta `/documentos-habeis-especiais?id_empenho={id}` → `id_dh` → consulta `/ordens-pagamentos-ordens-bancarias-especiais?id_dh={id}`.

**Oito cadeias completas de IDs foram recuperadas**, referentes a planos selecionados de Barrinha, Ribeirão Preto (dois), Tambaú, Guariba, Cravinhos, Mococa e Sertãozinho. A soma dos valores presentes nos documentos hábeis é **R$ 12.020.000,00**. Cada cadeia tem documento de empenho, número de documento hábil, número de ordem de pagamento, número/data de ordem bancária e situação da ordem.

**Estado exato da OP/OB nas oito consultas:** `OB Enviada à instituição bancária para pagamento`. Isso é prova da emissão e do encaminhamento da ordem **de acordo com o cadastro da API**, mas **não é recibo de crédito em conta, transferência liquidada no banco, medição física ou despesa final da prefeitura**. A API consultada não apresentou, no mesmo registro, comprovação de efetivação bancária. Não classificar os R$12,02 milhões como efetivamente recebidos sem evidência complementar. Não somar essa quantia aos R$93 milhões: os planos testados são uma amostra contida no universo de planos.

Fonte auditável com cada elo e URLs específicas: [`INV_RMRP_ESPECIAIS_8_CADEIAS_EMPENHO_DH_OB_2026_11_11.csv`](INV_RMRP_ESPECIAIS_8_CADEIAS_EMPENHO_DH_OB_2026_11_11.csv).

## 4. Regras de integração

A nova dimensão Transferegov Especiais requer:

1. `inv_ator` para beneficiário, chave `id_beneficiario` e CNPJ com IBGE7 **somente quando município validado**;
2. `inv_instrumento` ou tabela própria `inv_plano_acao` para cada plano, com `id_plano_acao`, ano e categoria capital/custeio, situação e valores nominais planejados; **não** tratar planos como projetos de obras necessariamente;
3. `inv_evento_financeiro` (somente em cópia de desenvolvimento) para empenho e documentos comprovados por chave; a ordem bancária deve ser anotada em novo estágio ou campo próprio `ob_emitida_enviada`, **não como `pago`** sem confirmação bancária;
4. Fonte e número do documento em cada elo (`numero_empenho`, `id_dh`, `numero_ordem_bancaria`), data, valor, situação, timestamp de consulta e estado QA; garantir unicidade por ID/documento;
5. Classificar esfera repassadora União, município beneficiário e **local efetivo da execução** em relações distintas. Só vincular um plano a projeto Obrasgov mediante referência ou documento compartilhado; não vincular por valor, nome ou data aproximados;
6. Verificar pagamentos em outras bases oficiais CGU/STN e eventual extrato de conta/gestão financeira pública, preservando estornos e competências, antes de homologar crédito ou investimento executado.

## 5. Próximas prioridades

**P0:** ampliar a conciliação `plano→empenho→documento_habil→OB` para os 284 planos com paginação e checkpoints, respeitando HTTP 429, evitando salvar dados bancários e pessoais desnecessários. **P1:** revisar os 25 impedidos e os seis com pendência/rejeição sem presumir recebimento. **P2:** vincular atos comprovados às séries municipais TCESP e às intervenções Obrasgov e, em paralelo, obter transferências estaduais efetivamente liberadas pela Sefaz/SP. **P3:** materializar a primeira consulta por município e por ano no SQLite de desenvolvimento com estágio de ordem bancária distinto de pagamento.

**Status:** adquiridos 34 beneficiários municipais, 284 planos e oito cadeias documentais; **nenhuma transferência bancária efetivamente creditada ou despesa final homologada**. PR #233 draft; produção, R2/D1/SQLite canônicos e FED04/PR #232 preservados.
