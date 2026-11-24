# S03 — SIAFEM/SP 2025, lote offset 535 fora da RMRP

**Data:** 24/11/2026. Fonte: Sefaz-SP/SIAFEM, transferências voluntárias a prefeituras, natureza Investimento, exercício de liberação 2025.

## Execução e QA

- [GitHub Actions 45401228164](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/45401228164): `offset=535`, `limit=5`, `year=2025`, **success**.
- Cinco solicitações e **cinco municípios com resposta reconciliada**; sem inconclusivos: IBGE7 `3550308`, `3550407`, `3550506`, `3550605`, `3550704`.
- **19 convênios-ano**, **23 pagamentos agregados**, **R$ 24.029.182,46** em liberações líquidas e estornos das respostas validadas.
- `queries_with_footer_reconciliation=5`, `queries_with_no_reconciliation_footer=0`, `failed_ibge7=[]`.
- Snapshot privado com **8.269 bytes**, SHA-256 `80f8bc9babbcca04604bcc787b7de5369af2f00471605a119f36e3421b1d1478`, caminho `r2://financas-municipais-sp-canonico/sp_645/estadual/siafem/batches/2025/piloto_extra_rmrp_offset_535_len5/80f8bc9babbcca04604bcc787b7de5369af2f00471605a119f36e3421b1d1478/raw.json`; `qa.json` no mesmo prefixo. Hash confrontado com retorno do R2; log confirma `SP645_SIAFEM_PILOT_READBACK_PASS`.
- `qa_status=pilot_regional_expansion_not_financial_homologation` — conciliação dos totalizadores de resposta **não** homologa execução financeira municipal.
- Controles da branch operacional: `execucoes.csv` +1, `snapshots.csv` +1, `cobertura.csv` +5; `pendencias.csv` sem alteração porque nenhum município resultou inconclusivo.

## Checkpoint agregado externo à RMRP, exercício 2025

| Indicador | Checkpoint anterior (535) | Incremento | Novo checkpoint (540) |
|---|---:|---:|---:|
| Consultados de 611 | 535 | 5 | **540** |
| Reconciliados | 454 | 5 | **459** |
| Inconclusivos | 81 | 0 | **81** |
| Não consultados | 76 | -5 | **71** |
| Convênios-ano | 1.371 | 19 | **1.390** |
| Pagamentos agregados | 1.479 | 23 | **1.502** |
| Liberações líquidas e estornos | R$ 974.301.499,13 | R$ 24.029.182,46 | **R$ 998.330.681,59** |

**Próximo lote:** `offset=540, limit=5, year=2025`, após conferir inexistência de execução sobreposta. Não imputar zero aos 81 inconclusivos nem publicar os montantes como investimentos municipais executados. A produção pública do Mapa do Tesouro permanece na release **v0.4.1**, com catálogo territorial RMRP validado e sem promoção da camada monetária SIAFEM.
