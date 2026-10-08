# Fonte suplementar local RGF/CAPAG 2025

O snapshot oficial CAPAG de setembro de 2026 contém uma aba `Datalake` com componentes RGF úteis para São Paulo.

A cobertura foi medida diretamente nos 645 códigos paulistas.

| Campo | Observados | Ausentes | Cobertura |
|---|---:|---:|---:|
| RCL — RGF Anexo 02 | 644 | 1 | 99,84% |
| Dívida Consolidada | 577 | 68 | 89,46% |
| Caixa bruta não vinculada | 635 | 10 | 98,45% |
| Demais obrigações não vinculadas | 108 | 537 | 16,74% |
| RP não liquidados anteriores não vinculados | 490 | 155 | 75,97% |
| RP liquidados anteriores não vinculados | 478 | 167 | 74,11% |
| RP liquidados do exercício não vinculados | 501 | 144 | 77,67% |

## Uso

Essa camada será usada como:

- validação cruzada;
- suplemento local;
- fonte para redução de deltas externos, quando o conceito for semanticamente idêntico.

Não será usada para substituir:

- DTP legal do RGF Anexo 01;
- RCL ajustada para limite de pessoal;
- percentual oficial DTP/RCL;
- campos do Anexo 05 que não estejam presentes com o mesmo recorte.

A regra continua sendo cobertura variável a variável e ausência diferente de zero.
