# S03 — lote 520 SIAFEM/SP, exercício 2025

**Data:** 23/11/2026. Fonte: Sefaz-SP/SIAFEM, transferências voluntárias para prefeituras, tipo Investimento, ano de liberação 2025, municípios fora da RMRP.

- [GitHub Actions run 45281338743](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/45281338743); workflow `sp645-siafem-annual-pilot-r2.yml`, branch `investimentos-territoriais-sp645-20261111`.
- Parâmetros: `offset=520, limit=5, year=2025`.
- **Cinco consultas**, **três reconciliadas**, **duas inconclusivas** (`ValueError`).
- **Seis convênios-ano, seis pagamentos agregados, R$ 1.641.299,88** de liberações líquidas e estornos.
- IDs IBGE7 validados: `3549102`, `3549201`, `3549300`.
- Pendências inconclusivas, **não imputar zero**: `3549003` e `3549250`.
- QA: `queries_with_no_reconciliation_footer=0`, `SP645_SIAFEM_PILOT_READBACK_PASS` nos logs; `qa_status=pilot_regional_expansion_not_financial_homologation`.
- Snapshot `raw.json`: 3.929 bytes, SHA-256 `1f2fe3888647d32636d73bb52bf5f36097ac31841f64f89966f02138b60ebf38`.
- Arquivos privados: `r2://financas-municipais-sp-canonico/sp_645/estadual/siafem/batches/2025/piloto_extra_rmrp_offset_520_len5/1f2fe3888647d32636d73bb52bf5f36097ac31841f64f89966f02138b60ebf38/raw.json` e `qa.json`.

## Novo checkpoint acumulado, fora da RMRP, SIAFEM 2025

| Indicador | Acumulado |
|---|---:|
| Consultados de 611 | **525** |
| Reconciliados | **445** |
| Inconclusivos | **80** |
| Ainda não consultados | **86** |
| Convênios-ano | **1.347** |
| Pagamentos agregados | **1.450** |
| Liberações líquidas e estornos nas respostas validadas | **R$ 960.744.783,60** |

Próximo lote novo `offset=525, limit=5, year=2025`, desde que não exista execução sobreposta. Atualizar os quatro CSVs de controle somente após conferir suas chaves e estados existentes; este relatório é a evidência do incremento, não uma afirmação de atualização dos CSVs.

Não houve homologação independente dos fluxos financeiros, merge, deploy nem alteração no banco produtivo. `public_release_authorized=false`.
