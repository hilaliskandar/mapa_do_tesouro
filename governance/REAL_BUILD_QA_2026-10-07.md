# QA da primeira build real — 2026-10-07

## Escopo

Primeira reconstrução real do novo núcleo usando:

- `FINBRA_TIC_TIM_30M_BASE_MULTIFONTES_2013_2025_v0_4.xlsx`;
- branch `bootstrap-financas-municipais-sp`;
- cartografia municipal pinada em `tbrugz/geodata-br@c39dfb040bfd466fe2a476bafed00749c5c42f16`.

## Resultado do pipeline

- municípios: **30**;
- exercícios: **13** — 2013 a 2025;
- pares município-ano: **390**;
- variáveis diretamente importadas: **46**;
- observações diretamente importadas: **17.940**;
- observações totais após derivados: **29.250**;
- objetos no catálogo técnico/documental: **75**;
- estatísticas de janela calculadas: **1.890**;
- classificações de tipologia: **210**;
- marcadores comparáveis: **180**;
- pares dirigidos: **870**;
- pares principais recíprocos: **6**.

## Correções reveladas pela build real

### 1. Aplicação incompleta das migrations

A ingestão inicializava apenas `001_initial.sql`, embora o carregamento documental dependesse também de `002_analytical_layers.sql` e `003_documentation.sql`.

Correção: `import_multifuentes` passou a chamar `initialize_database` sem restringir a migration quando nenhum schema explícito é informado.

### 2. Sobrescrita indevida dos indicadores legais

O mapping já importava diretamente:

- `dtp_pct_rcl`;
- `dc_pct_rcl`;
- `dcl_pct_rcl`;

a partir dos percentuais oficiais dos demonstrativos RGF.

`calculate_annual` tentava posteriormente sobrescrever esses valores copiando IDs intermediários inexistentes, convertendo toda a série legal em ausência.

Correção: removida a sobrescrita. Os três indicadores legais permanecem valores oficiais importados.

Teste de regressão acrescentado para impedir recorrência.

## Validação pontual

Americana — 2025:

- DTP/RCL: **0,3669 = 36,69%**;
- DC/RCL: **0,9322 = 93,22%**;
- DCL/RCL: **0,8368 = 83,68%**.

Os valores coincidem com a base multifuentes.

## Regra territorial

Após aplicação de `strict_complete`:

- `despesa_territorial` observada: **85** município-ano;
- ausente: **305** município-ano;
- municípios com marcador territorial classificável na janela 2021–2025: **7**;
- municípios sem classificação territorial suficiente: **23**.

Os seis marcadores restantes preservam cobertura integral nas dimensões não territoriais:

- base tributária: 30 classificados;
- investimento: 30;
- pessoal: 30;
- dívida: 30;
- liquidez: 30.

## Pares

Com os seis marcadores aprovados e a regra territorial canônica:

- 870 pares dirigidos calculados;
- 6 pares principais recíprocos.

Esse resultado coincide com o cenário `strict_complete` já registrado na regressão metodológica.

## Artefatos static-first

Gerados e validados:

- 13 snapshots anuais;
- 30 arquivos municipais;
- 75 arquivos individuais do catálogo;
- índice metodológico + 9 seções metodológicas;
- 10 referências documentais;
- GeoJSON reduzido a **30 geometrias**;
- `manifest.json` com **zero divergências de SHA-256**.

O frontend não contém referências em runtime a:

- `workers.dev`;
- `api.github.com`;
- `raw.githubusercontent.com`;
- Cloudflare.

## Cartografia

O GeoJSON-fonte possui 22.549.321 bytes. O build filtrou corretamente 30 geometrias, uma para cada código IBGE do universo.

## QA visual

A tentativa de inspeção por Chromium headless no ambiente atual ficou bloqueada por limitação do processo do navegador/DBus. O servidor HTTP local respondeu corretamente e todos os contratos estáticos foram verificados, mas a aprovação visual final deve ser feita em navegador normal antes de promoção de `candidate` para `approved`.

## Status

**candidate — build real concluída com QA estrutural aprovado e QA visual pendente.**
