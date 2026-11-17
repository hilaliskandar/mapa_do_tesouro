# S03 — retomada 2025 offset 470: sucesso parcial de lote de 5 e indisponibilidade de conexão

**Data:** 17/11/2026. **Fonte:** SIAFEM/SP `https://www.fazenda.sp.gov.br/TransferenciaVoluntaria/Sistema/Novo/PesquisaComposta.aspx`. **Escopo:** 611 municípios de São Paulo externos à RMRP, exercício 2025, filtros Prefeituras/Investimento. Sem dados de produção ou publicação.

## 1. Execuções reais

| GitHub Actions | Parâmetros | Resultado | Situação dos dados |
|---|---|---|---|
| [44183165048](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/44183165048) | `offset=470,limit=25,year=2025` | **failure**, 0/25 verificações, processo saiu com código 3 | **NÃO** gravado no R2 e **NÃO** registrado como cobertura/inconclusão municipal; diagnóstico de fonte requerido |
| [44183565735](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/44183565735) | `offset=470,limit=5,year=2025` | **success**, 5/5 com totalizadores reconciliados | **R2 readback PASS**, incorporado aos controles de execução/snapshot/cobertura |
| [44183709018](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/44183709018) | `offset=475,limit=10,year=2025` | **failure**, 0/10 verificações | O novo diagnóstico instrumentado confirmou **10 `ConnectionError` no host `www.fazenda.sp.gov.br`**, todos antes da recuperação da tabela. **Não** gravado no R2 nem marcado como zero/ausência de repasse |

Os logs da tentativa inicial de 25 consultas não disponibilizavam classes de erro, mas o ensaio subsequente de dez consultas produziu `failed_reason_classes: {"ConnectionError": 10}`. Isso **indica falha de conectividade da fonte**, sem comprovar que a primeira tentativa teve a mesma causa. O coletor foi atualizado nesta branch para imprimir `SIAFEM_FAILURE_DIAGNOSTIC` e contagem de classes de erro, preservando a regra de bloquear upload se nenhum município for validado.

## 2. Lote de cinco municípios válido

**IDs IBGE7:** `3543907` (Rio Claro), `3544004` (Rio das Pedras), `3544103` (Rio Grande da Serra), `3544202` (Riolândia), `3544251` (Rosana).

**QA:** cinco consultas, cinco reconciliadas, zero falhas, 18 convênios-ano, 18 pagamentos, **R$ 5.569.196,06** em liberações líquidas/estornos do exercício 2025.

**Artefato R2:** `r2://financas-municipais-sp-canonico/sp_645/estadual/siafem/batches/2025/piloto_extra_rmrp_offset_470_len5/a9655468a229c2f48c52ca276914f80355fc2f85a3b630aa3b8dc326404bba7d/raw.json`; **7.911 bytes**, SHA-256 `a9655468a229c2f48c52ca276914f80355fc2f85a3b630aa3b8dc326404bba7d`, `qa.json` no mesmo prefixo, `SP645_SIAFEM_PILOT_READBACK_PASS` no log.

Foram atualizados com idempotência `governance/controls/investimentos_sp645/execucoes.csv` (+1), `snapshots.csv` (+1), `cobertura.csv` (+5), sem registrar como pendência as 35 consultas globais malsucedidas por conexão. Elas pertencem ao diagnóstico de disponibilidade da fonte, não à fila de 71 resultados municipais inconclusivos já existentes.

## 3. Checkpoint correto e retomada

Cobertura anterior: **470/611**, 399 reconciliados, 71 inconclusivos, 141 não consultados, 1.202 convênios-ano, 1.288 pagamentos, R$ 782.207.453,93.

Cobertura após lote válido: **475/611 municípios consultados, 404 reconciliados, 71 inconclusivos, 136 não consultados, 1.220 convênios-ano, 1.306 pagamentos e R$ 787.776.649,99** em liberações líquidas/estornos do recorte estadual 2025. Esses montantes são preliminares no âmbito SP645; não são despesas próprias dos municípios.

**Próximo offset: `475`.** Recomenda-se retomar com **`limit=5`**, após prova de disponibilidade da consulta SIAFEM. **Não** avançar para offset 485/495 e **não** declarar os dez registros por falha de rede como consultados. Quando o acesso estiver restaurado, verificar runs recentes, retomar os IDs ainda sem cobertura, avançar em lotes graduais e manter QA, hash e readback R2 obrigatórios.

## 4. Governança

RMRP34 histórica permanece completa até corte 12/11/2026, com liberação exata 2020–2026. Parêntese de aquisição federal RMRP permanece encerrado como prioridade, com lacunas preservadas; [termo de encerramento](ENCERRAMENTO_PARENTESE_FEDERAL_RMRP_RETOMADA_SIAFEM_2026_11_17.md).

`public_release_authorized=false`. Não houve merge, deploy público, alteração em D1/SQLite fiscal produtivo nem homologação dos valores.
