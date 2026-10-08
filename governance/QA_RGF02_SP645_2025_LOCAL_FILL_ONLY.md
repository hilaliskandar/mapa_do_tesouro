# QA — RGF Anexo 02 SP645 2025 e composto fill-only

## Aquisição estadual

Run: `37739794707`.

- municípios solicitados: 645;
- municípios observados: 530;
- linhas longas: 43.920;
- códigos de conta distintos: 40;
- falhas: 0;
- linhas canônicas: 530;
- conflitos canônicos: 0;
- SHA-256 longo: `37c6ee8e9440f2e5cb4f4a8e1b035020f36c5d0b9631fde1463acdc3fbfc628f`;
- SHA-256 canônico: `8e4709727aa8fbf0023056982fe7927f5bd8e323354807604dbdc2a91cf8d75a`;
- artifact GitHub: `sha256:5c283c51965274fd745c464c0148c5b11d6376b800318db27a8213bb4961fb41`.

Cobertura canônica da base Siconfi:

| Variável | Observados |
|---|---:|
| Dívida Consolidada | 477/645 |
| Dívida Consolidada Líquida | 530/645 |
| DC/RCL | 476/645 |
| DCL/RCL | 530/645 |
| Dívida contratual | 454/645 |
| Parcelamento de dívidas | 373/645 |
| Precatórios vencidos não pagos | 265/645 |
| Outras dívidas | 52/645 |
| Deduções da dívida consolidada | 530/645 |
| Disponibilidade de caixa | 530/645 |
| Demais haveres financeiros | 300/645 |
| Restos a pagar processados | 510/645 |
| RCL bruta | 530/645 |
| RCL ajustada para endividamento | 530/645 |

## Suplemento CAPAG fill-only

O snapshot CAPAG Ano Base 2025 contém dois campos com equivalência direta ao contrato canônico do Anexo 02:

- Dívida Consolidada;
- Receita Corrente Líquida bruta.

Todos os 477 overlaps de Dívida Consolidada e 530 overlaps de RCL são idênticos, sem conflito.

Os valores zero do XLSX CAPAG não foram tratados como observação válida para preenchimento, porque aparecem em casos `n.d.` e funcionam como marcador operacional.

Preenchimentos:

- Dívida Consolidada: +100;
- RCL bruta: +114;
- conflitos: 0.

Cobertura após fill-only:

- Dívida Consolidada: 577/645 — 89,46%;
- RCL bruta: 644/645 — 99,84%.

Os demais campos permanecem exclusivamente sob o contrato RGF e não recebem proxy.

SHA-256 do composto de 645 linhas:

`0b31196dd1a692632b7c2b48a044ed64f5f56493eb8d50f818810cdd583fc139`.

## Decisão

O RGF Anexo 02 2025 está aprovado como fonte estadual privada. O composto CAPAG é uma camada derivada separada e não substitui os brutos Siconfi.
