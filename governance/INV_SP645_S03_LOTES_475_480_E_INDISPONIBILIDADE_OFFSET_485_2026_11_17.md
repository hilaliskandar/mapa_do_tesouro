# S03 — aquisição SIAFEM/SP 2025: offsets 475 e 480, pausa técnica no 485

**Data:** 17/11/2026. **Fila:** 611 municípios fora da RMRP; exercício 2025, filtro Prefeitura/Investimento. **Objetivo:** coleta privada incremental, não homologação.

## Execuções e prova material

| Offset | GitHub Actions | Resultado | Convênios-ano | Pagamentos | Liberado/estornado líquido |
|---:|---|---|---:|---:|---:|
| 475 (5) | [44185244074](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/44185244074) | **4 válidos; 1 ConnectionError (Roseira, IBGE7 3544301)**, R2 readback PASS | 11 | 12 | R$ 5.475.959,94 |
| 480 (5) | [44185529892](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/44185529892) | **5 válidos; 0 erros**, R2 readback PASS | 10 | 10 | R$ 4.094.827,02 |
| 485 (5) | [44185809047](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/44185809047) | **0/5; falha de execução**, 5 `ConnectionError` no acesso à Sefaz; **sem gravação em R2** | — | — | **indeterminado**, não zero |

O workflow manteve o bloqueio preventivo quando nenhuma consulta foi validada. A repetição de `ConnectionError` em todos os cinco casos do offset 485 é indício de instabilidade da conectividade com `www.fazenda.sp.gov.br`, não comprova ausência de repasses municipais. O script `pipeline/coleta/collect_sp_siafem_annual_batch.py` registra `failed_reason_classes` e `SIAFEM_FAILURE_DIAGNOSTIC` nos logs; não foi feito novo disparo após a falha total.

**Staging imutável R2:**
- Offset 475: `r2://financas-municipais-sp-canonico/sp_645/estadual/siafem/batches/2025/piloto_extra_rmrp_offset_475_len5/b51c42b2d4cbb94efea490b897bd26c5e70c6ce65c3a9ffad9a9c8be12209a/raw.json`, SHA-256 `b51c42b2d4cbb94efea490b897bd26c5e70c6ce65c3a9ffad9a9c8be12209a`, 5.656 bytes.
- Offset 480: `r2://financas-municipais-sp-canonico/sp_645/estadual/siafem/batches/2025/piloto_extra_rmrp_offset_480_len5/c5521ed03c7f86e8ae34d44fa0ed135a496376de1f5e7a5b22faca622716d157/raw.json`, SHA-256 `c5521ed03c7f86e8ae34d44fa0ed135a496376de1f5e7a5b22faca622716d157`, 5.673 bytes.

## Cobertura acumulada após os dois lotes válidos

Checkpoint inicial desta rodada: **475/611**, 404 consultas reconciliadas, 71 inconclusivas, 136 não consultadas; R$ 787.776.649,99, 1.220 convênios-ano e 1.306 pagamentos.

**Checkpoint final: 485/611 municípios consultados, 413 reconciliados, 72 inconclusivos, 126 não consultados, 1.241 convênios-ano, 1.328 pagamentos, R$ 797.347.436,95**. Incremento válido: 10 municípios, nove reconciliados, um inconclusivo, R$ 9.570.786,96. Os cinco municípios do lote 485 malsucedido **não** foram marcados como consultados.

Os quatro CSVs de governança foram tratados de modo idempotente: `execucoes.csv` e `snapshots.csv` (+2), `cobertura.csv` (+10), `pendencias.csv` (+1 para Roseira). Falhas técnicas de lote não geram valores monetários presumidos.

**Próxima tentativa: `offset=485, limit=5, year=2025`**, condicionada a verificar acesso ao portal Sefaz-SP e runs recentes. Não avançar ao offset 490 enquanto a página inicial estiver indisponível. Com acesso validado, seguir lotes graduais. Não reconsultar séries RMRP já completas.

`public_release_authorized=false`; sem merge, deploy, D1 de produção ou alteração de dashboard público.
