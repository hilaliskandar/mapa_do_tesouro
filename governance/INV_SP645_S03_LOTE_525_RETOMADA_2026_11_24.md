# S03 — SIAFEM/SP 2025, lote 525, fora da RMRP

**Data:** 24/11/2026. **Escopo:** transferências voluntárias do Estado de São Paulo para prefeituras, natureza Investimento, exercício da liberação 2025, municípios fora da Região Metropolitana de Ribeirão Preto.

## Evidência da execução

- [GitHub Actions 45396257323](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/45396257323), workflow `sp645-siafem-annual-pilot-r2.yml`, branch `investimentos-territoriais-sp645-20261111`, `offset=525, limit=5, year=2025`: **success**.
- Cinco solicitações: **quatro com tabela verificada e conciliação do totalizador**, uma **inconclusiva** classificada `ValueError`.
- IBGE7 com dados reconciliados: `3549409`, `3549508`, `3549706`, `3549805`.
- IBGE7 inconclusivo: `3549607`. Ausência de linha financeira e totalizador **não demonstra zero** nem comprova inexistência de transferência.
- **Nove convênios-ano**, **11 pagamentos agregados**, **R$ 3.649.541,97** em liberações líquidas e estornos das respostas verificadas.
- `queries_with_footer_reconciliation=4`; `queries_with_no_reconciliation_footer=0`; `failed_reason_classes={"ValueError":1}`.
- `qa_status=pilot_regional_expansion_not_financial_homologation`; não homologar como execução financeira municipal.
- Arquivos privados: `r2://financas-municipais-sp-canonico/sp_645/estadual/siafem/batches/2025/piloto_extra_rmrp_offset_525_len5/4747226dafc60b121f780964f6eb1a5d3cdc59e1ae129d0734e40a985caa5647/raw.json` e `qa.json`. Snapshot de 5.212 bytes com SHA-256 `4747226dafc60b121f780964f6eb1a5d3cdc59e1ae129d0734e40a985caa5647`; foi registrado `SP645_SIAFEM_PILOT_READBACK_PASS` após download de conferência.
- Controles `governance/controls/investimentos_sp645/`: +1 execução, +1 snapshot, +5 registros de cobertura, +1 pendência (`S03-93`), preservadas as chaves preexistentes.

## Novo checkpoint agregado 2025, fora da RMRP

| Indicador | Valor acumulado |
|---|---:|
| Municípios consultados de 611 | **530** |
| Consultas reconciliadas | **449** |
| Consultas inconclusivas | **81** |
| Municípios ainda não consultados | **81** |
| Convênios-ano | **1.356** |
| Pagamentos agregados | **1.461** |
| Liberações líquidas e estornos nas respostas validadas | **R$ 964.394.325,57** |

Próxima consulta nova: `offset=530, limit=5, year=2025`, após conferir que não houve workflow sobreposto. A soma financeira é do conteúdo efetivamente validado da fonte, **não** é a totalidade de gastos municipais, nem autorização de publicação financeira. `public_release_authorized=false` permanece para essas medidas.

## Situação da plataforma pública

A release [v0.4.1](https://github.com/hilaliskandar/mapa_do_tesouro/releases/tag/v0.4.1) foi implantada em 24/11/2026 e o workflow de produção [45395727209](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/45395727209) terminou com **success**. Endereço: **https://finbra-tic-tim-referencia.pages.dev/**. O novo catálogo público da RMRP é **estritamente cadastral** e não utiliza os totais financeiros SIAFEM desse lote.
