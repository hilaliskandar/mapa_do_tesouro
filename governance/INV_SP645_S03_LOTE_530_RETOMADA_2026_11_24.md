# S03 — SIAFEM/SP 2025, lote offset 530 fora da RMRP

**Data:** 24/11/2026. **Fonte:** Sefaz-SP/SIAFEM, transferências voluntárias a prefeituras, natureza Investimento, exercício de liberação 2025.

## Execução e QA

- Workflow [GitHub Actions 45399204887](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/45399204887): `offset=530`, `limit=5`, `year=2025`, `conclusion=success`.
- Todos os **cinco municípios reconciliados**, sem inconclusivos, com totalizadores completos: IBGE7 `3549904`, `3549953`, `3550001`, `3550100`, `3550209`.
- **15 convênios-ano**, **18 pagamentos agregados** e **R$ 9.907.173,56** em liberações líquidas/estornos registrados nas consultas validadas.
- `queries_with_footer_reconciliation=5`, `queries_with_no_reconciliation_footer=0`, `failed_ibge7=[]`.
- `qa_status=pilot_regional_expansion_not_financial_homologation`: respostas reconciliadas não equivalem à homologação de execução financeira municipal.
- Snapshot bruto de **7.235 bytes**, SHA-256 `bd139fc410993c0ca3a781d37f013a5c1c1509dc1b848b003c530ae9ae7728e7`. Acervo R2 privado: `r2://financas-municipais-sp-canonico/sp_645/estadual/siafem/batches/2025/piloto_extra_rmrp_offset_530_len5/bd139fc410993c0ca3a781d37f013a5c1c1509dc1b848b003c530ae9ae7728e7/raw.json` e `qa.json`. Confirmado `SP645_SIAFEM_PILOT_READBACK_PASS` e hash de retorno.
- Governança sincronizada em `governance/controls/investimentos_sp645/`: `execucoes.csv` +1, `snapshots.csv` +1, `cobertura.csv` +5. `pendencias.csv` não recebeu nova ocorrência, pois não houve erro.

## Checkpoint consolidado fora da RMRP

| Indicador | Antes (525) | Incremento | Depois (535) |
|---|---:|---:|---:|
| Municípios consultados /611 | 530 | 5 | **535** |
| Consultas reconciliadas | 449 | 5 | **454** |
| Consultas inconclusivas | 81 | 0 | **81** |
| Municípios ainda não consultados | 81 | -5 | **76** |
| Convênios-ano | 1.356 | 15 | **1.371** |
| Pagamentos agregados | 1.461 | 18 | **1.479** |
| Liberações líquidas e estornos | R$ 964.394.325,57 | R$ 9.907.173,56 | **R$ 974.301.499,13** |

O checkpoint 525 consta do relatório [lote 525](INV_SP645_S03_LOTE_525_RETOMADA_2026_11_24.md). Valores somam somente as respostas validadas; **não** significam totalidade dos investimentos públicos, gasto municipal efetivo ou aprovação de publicação da camada financeira.

**Próxima consulta nova:** `offset=535, limit=5, year=2025`, somente após conferência de execuções sobrepostas. Não alterar o banco produtivo nem incorporar os montantes na versão pública v0.4.1. A release pública contém apenas o catálogo territorial dos 34 municípios da RMRP.
