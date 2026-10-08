# QA — RGF SP645 — 2025

Run fonte: `37732303043`.

## Resultado

- municípios solicitados: 645;
- linhas normalizadas: 645;
- falhas de aquisição: 0;
- issues de normalização: 0;
- SHA-256 normalizado: `9f3ced721fa2c767d24cdec8e464215b30932e820e01601f24bac9b1e76486ba`;
- SHA-256 árvore bruta: `1f1bc9a06fdd64e8e5c36912273f8ef955fa76db486e76d50f2a4c54b31ebb23`;
- artifact GitHub: `sha256:cfa7cb450c34a44abf2a26c184a44ad2361157abc45249e4ccf617e68d9a1a8e`.

## Cobertura por variável

| Variável | Observados | Ausentes | Cobertura |
|---|---:|---:|---:|
| DTP legal | 530 | 115 | 82,17% |
| RCL denominador legal | 530 | 115 | 82,17% |
| Percentual oficial DTP/RCL | 530 | 115 | 82,17% |
| Caixa bruta não vinculada | 526 | 119 | 81,55% |
| RP liquidados anteriores não vinculados | 404 | 241 | 62,64% |
| RP liquidados do exercício não vinculados | 412 | 233 | 63,88% |
| RP não liquidados anteriores não vinculados | 411 | 234 | 63,72% |
| Demais obrigações não vinculadas | 93 | 552 | 14,42% |
| Caixa líquida antes RPNP | 528 | 117 | 81,86% |
| RP não liquidados do exercício não vinculados | 410 | 235 | 63,57% |
| Caixa líquida após RPNP | 528 | 117 | 81,86% |

## Interpretação

A execução estadual foi tecnicamente íntegra: a API respondeu sem falhas de aquisição e o normalizador não encontrou ambiguidade.

A cobertura varia por variável porque os demonstrativos não apresentam todas as linhas canônicas para todos os municípios. Ausência permanece ausência.

Não foram usadas:

- soma de sublinhas;
- imputação por zero;
- substituição por DCA;
- substituição por RREO;
- preenchimento automático a partir do snapshot CAPAG.

O suplemento CAPAG/RGF local deve ser usado apenas em etapa posterior, variável a variável e somente quando o conceito for semanticamente idêntico.

## Decisão

A carga RGF Anexos 01/05 2025 está aprovada como snapshot estadual privado de referência para o Gate C.

O próximo passo é qualificar as lacunas contra o suplemento local CAPAG/RGF antes de qualquer delta externo e decidir a necessidade efetiva de executar o RGF Anexo 02 estadual.
