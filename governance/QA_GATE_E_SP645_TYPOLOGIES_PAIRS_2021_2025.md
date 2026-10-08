# QA — Gate E — tipologias e pares SP645 2021–2025

Data: 2026-10-08.

## Entrada canônica

Arquivo:

- `SP645_TYPOLOGY_INPUT_2021_2025.xlsx`;
- Drive file ID: `1QPY6sMSqrl3SFnq7Z5qRYXoHiCVXhdAb`;
- 3.225 linhas;
- 645 municípios;
- janela 2021–2025;
- SHA-256: `72e6302e5331ba05f066eebe55df914a7fc2dd7b6d2114e6df374bfc606977ce`.

Hashes das três fontes:

- DCA 2021–2025: `bd1bfe175886fe84c969778bb9d545c5deb4836e16de4ddd6d7ddc9c4848f93d`;
- RGF histórico corrigido 2023–2024: `7faef8188fd56bff6bb8031dfe3a8eeec11fe56e67f986bdc0007a4ee7646eeb`;
- Gate D 2025: `adb9b5b6abbd3f439f3b39cc356522d21430de74117de4bf9ca1589c40e9c161`.

## Cobertura anual do input

| Variável | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---:|---:|---:|---:|---:|
| Receita tributária / receita corrente | 645 | 645 | 645 | 645 | 644 |
| Investimento / receita corrente | 645 | 645 | 645 | 645 | 644 |
| Despesa territorial / despesa | 56 | 66 | 65 | 72 | 65 |
| DTP / RCL | 0 | 0 | 527 | 530 | 530 |
| DC / RCL | 0 | 0 | 471 | 481 | 476 |
| DCL / RCL | 0 | 0 | 527 | 530 | 530 |
| Caixa após RPNP / RCL | 0 | 0 | 0 | 0 | 528 |

## Municípios com pelo menos três anos

- base tributária: 645;
- investimento: 645;
- territorial strict_complete: 56;
- DTP: 505;
- DC: 439;
- DCL: 505;
- liquidez: 0.

## Tipologias calculadas

Classificações observadas:

- base tributária: 645;
- investimento: 645;
- territorial: 56;
- DTP: 505;
- DC: 439;
- DCL: 505;
- liquidez: 0.

Medianas da média e do CV:

| Dimensão | Mediana da média | Mediana do CV |
|---|---:|---:|
| Base tributária | 11,98409678 | 0,08952154 |
| Investimento | 5,11169516 | 0,48342652 |
| Territorial | 16,42799908 | 0,09901760 |
| DTP | 44,03333333 | 0,05851842 |
| DC | 9,04 | 0,22110638 |
| DCL | -1,21 | -0,08092221 |
| Liquidez | 2,01783836 | não classificável |

### Cautela DCL

A regra histórica usa CV = desvio-padrão amostral / média. Médias negativas produzem CV negativo. Essa regra foi preservada para paridade metodológica e deve ser revista apenas em mudança metodológica versionada.

DCL não entra na assinatura de pares.

## Marcadores

Cobertura:

- base: 645;
- investimento: 645;
- territorial: 56;
- pessoal: 505;
- dívida: 439;
- liquidez: 0.

A integração entre tipologias e marcadores foi corrigida no PR #92 para aceitar a grafia canônica `mais estavel` produzida por `calculate_typologies`, mantendo o texto final dos marcadores com acento.

## Pares

Regra:

- seis marcadores possíveis;
- DCL e CAPAG não entram na assinatura;
- mínimo de quatro marcadores comparáveis;
- ordenação por proporção de coincidência, número de coincidências, cobertura, nome e código;
- três pares prioritários por município elegível.

Resultado:

- municípios com pelo menos quatro marcadores: 440;
- municípios sem par elegível: 205;
- distribuição de marcadores comparáveis:
  - 2 marcadores: 136 municípios;
  - 3 marcadores: 69;
  - 4 marcadores: 389;
  - 5 marcadores: 51;
  - 6 marcadores: 0;
- pares dirigidos auditados: 415.380;
- posições prioritárias materializadas: 1.320;
- pares principais recíprocos: 40.

## Artifact canônico privado

Workbook:

- `SP645_TIPOLOGIAS_PARES_2021_2025_CANONICO.xlsx`;
- Drive file ID: `1zA0zNM_pYzkMk88XttNi17on6w_l98__`;
- SHA-256: `ea2d31b53c2558cebfb02d4342c26561cbcf21497aab0b61af2b54a07ce6e46a`.

Hashes auxiliares:

- tipologias CSV: `6b2f9a22016df2dc70c6783b2b6a8a30a74d345171ea701be7628872fd7fdd34`;
- marcadores CSV: `7ea2d4fe71ccd68d7e7882cb6a8bd65e0d4e0b96b0aa35872d94854503c64c3a`;
- pares prioritários CSV: `21a36f0322d500eee8a3c7a7703e989231be0be8265356668dc69aca34a2502c`;
- todos os pares, CSV.gz: `e169ae0a2dddef7a99346a6f07ca36038795f67ba0bc0a07d53f7110b808378c`.

## Decisão

Tipologias e pares SP645 2021–2025 estão aprovados para camada privada de QA.

Não promover ao painel público antes de:

1. validar a camada cartográfica estadual;
2. definir como comunicar os 205 municípios sem pares elegíveis;
3. explicitar a ausência de tipologia de liquidez;
4. executar a regressão final do site estadual contra o baseline TIC-TIM 30.
