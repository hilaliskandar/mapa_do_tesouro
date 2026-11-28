# Release candidate v0.7.0 — Finanças Municipais SP

**Status:** candidata em branch de integração; ainda sem publicação.  
**Base funcional:** produção documentada `v0.6.0`.  
**Quadro de integração:** [`WORKSTREAMS_AND_INTEGRATION_2026_11_27.md`](WORKSTREAMS_AND_INTEGRATION_2026_11_27.md).

## Escopo desta candidata

- Atualização incremental estadual e seus controles de calendário, ledger, proveniência e recuperação missing-only.
- Publicação de agregado do Transferegov por município proponente, ano e etapa, a partir do snapshot fixado por SHA-256.
- Consulta visual correspondente, sem exportar registros individuais, identificadores de convênio ou dados de favorecidos.
- Conectores federais GET limitados, staging imutável e normalização territorial por código IBGE, com modos de leitura e amostragem opt-in.
- Preservação dos gates de conservação territorial e de bloqueio de variáveis não publicáveis.
- Catálogo cadastral RMRP com JavaScript externo compatível com a CSP.

## Fora do escopo de publicação

- Valores SIAFEM ainda inconclusivos ou não homologados como execução municipal.
- Pré-visualizações de planos, empenhos, lançamentos, pagamentos ou candidatos de obras que não tenham passado por homologação própria.
- Agendamentos recorrentes de coleta: o calendário e o ledger não habilitam disparos de produção automaticamente.

## Condições para a release formal

1. CI completo da branch e gates de segurança/integração aprovados.
2. Prévia isolada com QA local e remoto da página Transferegov, da API JSON e da navegação.
3. Conferência de cobertura e dos totais contra o relatório da auditoria agregada.
4. Conferência de que o artefato de Pages contém somente os agregados autorizados para a nova consulta.
5. Merge revisado, release GitHub `v0.7.0` com `release_universe: SP_645` e execução bem-sucedida de `pages-sp645-production`.

O texto registra uma candidata de release e seus gates; não afirma que esses gates ou o deploy já foram concluídos.
