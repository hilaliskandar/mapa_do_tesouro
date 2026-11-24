# S03 — SIAFEM/SP 2025, lote offset 545 fora da RMRP

**Data:** 24/11/2026. Fonte: Sefaz-SP/SIAFEM, transferências voluntárias para prefeituras, natureza Investimento, exercício de liberação 2025. Universo: 611 municípios externos à RMRP.

## Resultado, controle de integridade e rastreabilidade

- [GitHub Actions 45405898519](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/45405898519), `offset=545,limit=5,year=2025`: **success**.
- Municípios com tabela e totalizador reconciliados (IBGE7): `3551603`, `3551801`, `3551900`, `3552007`, `3552106`. **5/5 reconciliados, zero inconclusivos**.
- Total incremental: **18 convênios-ano**, **18 pagamentos agregados**, **R$ 14.446.321,31** em liberações líquidas/estornos das respostas verificadas.
- `queries_with_footer_reconciliation=5`, `queries_with_no_reconciliation_footer=0`, `failed_ibge7=[]`.
- Snapshot privado de 7.852 bytes, SHA-256 `8bca929affcca69734fb369079007bf2193f7429423d60d34401b02336a5f6dd` em `r2://financas-municipais-sp-canonico/sp_645/estadual/siafem/batches/2025/piloto_extra_rmrp_offset_545_len5/8bca929affcca69734fb369079007bf2193f7429423d60d34401b02336a5f6dd/raw.json`, com `qa.json` no mesmo prefixo. O log confirma `SP645_SIAFEM_PILOT_READBACK_PASS` depois de conferir o hash do arquivo lido do R2.
- `qa_status=pilot_regional_expansion_not_financial_homologation`: QA da resposta e armazenamento não configuram homologação da execução financeira municipal.
- Os arquivos `governance/controls/investimentos_sp645/execucoes.csv`, `snapshots.csv` e `cobertura.csv` receberam respectivamente +1, +1, +5 registros, com chaves verificadas. `pendencias.csv` permanece inalterado porque não houve consulta inconclusiva.

## Checkpoint acumulado, exercício 2025, fora da RMRP

| Indicador | Anterior (545) | Incremento | Novo (550) |
|---|---:|---:|---:|
| Municípios consultados de 611 | 545 | 5 | **550** |
| Municípios reconciliados | 463 | 5 | **468** |
| Consultas inconclusivas | 82 | 0 | **82** |
| Ainda não consultados | 66 | -5 | **61** |
| Convênios-ano | 1.413 | 18 | **1.431** |
| Pagamentos agregados | 1.526 | 18 | **1.544** |
| Liberações líquidas e estornos | R$ 1.017.934.039,76 | R$ 14.446.321,31 | **R$ 1.032.380.361,07** |

Próximo lote novo: `offset=550,limit=5,year=2025`, após verificação de execuções sobrepostas. A série financeira não foi promovida à [plataforma pública v0.4.1](https://finbra-tic-tim-referencia.pages.dev/), cuja incorporação de novos dados permanece limitada à dimensão cadastral RMRP devidamente homologada. Não imputar zero às 82 consultas inconclusivas.
