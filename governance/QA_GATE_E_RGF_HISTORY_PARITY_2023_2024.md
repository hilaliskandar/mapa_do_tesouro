# QA — Gate E — paridade histórica RGF 2023–2024

Data da validação: 2026-10-08.

## Candidato estadual

Histórico RGF corrigido 2023–2024:

- 1.290 linhas;
- 645 municípios × 2 exercícios;
- SHA-256 do CSV corrigido: `7faef8188fd56bff6bb8031dfe3a8eeec11fe56e67f986bdc0007a4ee7646eeb`;
- artifact: `gate-e-rgf-history-2023-2024-corrected`;
- artifact ID: `11548799933`;
- artifact digest: `sha256:68ebd055625a5960f5450d54a45840057caef487dd2f6986607a54e488d2a054`;
- run do pós-processamento corrigido: `37776058337`.

## Referências TIC-TIM 30

### RGF Anexo 01

- arquivo: `FINBRA_TIC_TIM_30M_RGF_2015_2025_ANEXOS_01_05_v1`;
- Drive file ID: `1U3l1dUEryYOWInFcN4GO5kKBWD0s5SSLDMhOXqRENfs`;
- abas usadas: `RGF_2023` e `RGF_2024`.

Campos comparados:

- DTP legal;
- RCL legal ajustada;
- percentual oficial DTP/RCL.

### RGF Anexo 02

- arquivo: `FINBRA_TIC_TIM_30M_RGF_ANEXO02_2015_2025_v1`;
- Drive file ID: `1t0HYxI9J4zvpKURDZJebkXNagdrf1f3PaZIMFzGcrDM`;
- aba: `RGF02_LONGA`;
- coluna: `Até o 3º Quadrimestre`.

Campos comparados:

- dívida consolidada;
- dívida consolidada líquida;
- percentual DC/RCL;
- percentual DCL/RCL.

## Resultado

Validador: `pipeline/qa/rgf_history_parity.py`.

Regras:

- tolerância monetária: R$ 0,01;
- tolerância percentual: 0,01 ponto percentual;
- ausência comparada como ausência;
- nenhuma imputação;
- nenhuma aproximação por DCA ou CAPAG.

Resultado:

- municípios de referência: 30;
- exercícios: 2023 e 2024;
- chaves município-ano de referência: 60;
- campos comparados por chave: 7;
- comparações: 420;
- valores dentro da tolerância: 420;
- ambos ausentes: 0;
- divergências: **0**;
- `strict_pass: true`.

SHA-256 do JSON de paridade: `c2503a004d7ebb215f2ecdb3465e3828a2443de8f94a2c0b62c4c42b5496b5f7`.

## Decisão

A série RGF estadual corrigida de 2023–2024 está aprovada para compor a entrada histórica do Gate E.

A condição de paridade histórica contra TIC-TIM 30 foi satisfeita. O próximo passo autorizado é construir a entrada canônica SP645 2021–2025 para tipologias e pares, preservando as regras de mínimo de três anos e ausência como ausência.
