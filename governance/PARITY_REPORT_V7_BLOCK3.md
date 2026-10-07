# Paridade numérica — base multifuentes, painel v7 e Bloco 3

## Artefatos

- `FINBRA_TIC_TIM_30M_BASE_MULTIFONTES_2013_2025_v0_4.xlsx`
  - SHA-256: `f51d8615f3742b1d414f1edff67805cac1a10cbc18764b454aab518de9c9e3f1`
- `FINBRA_TIC_TIM_30M_PAINEL_FISCAL_INTERATIVO_v7.xlsx`
  - SHA-256: `3db0d6782e1c31d0f0dd0292aca4542f9faac2d2b23c4ce2dd0f34905c5f298f`
- `FINBRA_TIC_TIM_30M_BLOCO3_INDICADORES_TRAJETORIAS_v0_7.xlsx`
  - SHA-256: `2099d6c6c7af28f92701b8c1b9d3d880c3e2325b824ddf984a8e309cd193f101`

## Universo validado

- 30 municípios;
- 13 exercícios, 2013–2025;
- 390 pares município-ano.

## Paridade da camada de origem

A aba `Base multifuentes` e a aba `Dados anuais` do painel v7 possuem 59 campos de origem compartilhados, além do nome municipal.

Foram comparadas **23.010 células** (390 × 59).

Resultado:

- divergências: **0**;
- paridade: **100%**.

Isto confirma que o painel v7 preserva integralmente a camada integrada usada como sua origem.

## Paridade das agregações materializadas no v7

A regra estrita do núcleo canônico reproduz integralmente as agregações que já possuem valores materializados no XLSX v7:

| Agregação | Observações | Divergências |
|---|---:|---:|
| Serviço da dívida liquidado | 328 | 0 |
| Receitas de capital selecionadas | 140 | 0 |
| Despesas de capital selecionadas | 42 | 0 |
| Gasto social selecionado | 389 | 0 |
| Saldo corrente simplificado | 389 | 0 |
| Diferença de capital selecionada | 26 | 0 |

Para essas seis variáveis, a regra de propagação estrita de ausência é compatível com os valores materializados no v7.

## Divergência encontrada — agregado territorial

O Bloco 3 v0.7 utiliza para `despesa_territorial`:

```excel
=IF(COUNT(O2,P2,Q2,R2,S2)=0,"",SUM(O2,P2,Q2,R2,S2))
```

Essa fórmula soma os componentes disponíveis sempre que pelo menos um deles estiver presente.

A regra atual do núcleo canônico é mais restritiva:

> Urbanismo + Habitação + Saneamento + Gestão Ambiental + Transporte somente é calculado quando os cinco componentes estão observados; caso contrário, permanece NA.

Impacto observado:

| Situação | Pares município-ano |
|---|---:|
| 5 componentes observados | 85 |
| Pelo menos 1 componente observado | 389 |
| Afetados pela diferença entre as regras | **304** |
| Nenhum componente observado | 1 |

Distribuição:

| Componentes observados | Pares |
|---:|---:|
| 0 | 1 |
| 1 | 14 |
| 2 | 50 |
| 3 | 106 |
| 4 | 134 |
| 5 | 85 |

Principais padrões de ausência:

- apenas Habitação ausente: 51 pares;
- apenas Transporte ausente: 47;
- apenas Saneamento ausente: 36;
- Saneamento + Transporte: 33;
- Habitação + Transporte: 29;
- Habitação + Saneamento: 25;
- Habitação + Saneamento + Transporte: 25.

## Decisão provisória

A fórmula permissiva do Bloco 3 não será promovida automaticamente porque é incompatível com a regra de governança **ausência ≠ zero**.

A regra estrita permanece no núcleo até que a origem das ausências nas funções DCA seja examinada e seja demonstrado que uma ausência específica pode ser interpretada contabilmente como zero sem imputação indevida.

A questão está registrada na issue #3.

## Consequência para a regressão

Há dois tipos distintos de baseline:

1. **baseline numérico aprovado**, quando os valores legados são reproduzidos exatamente;
2. **baseline metodológico para revisão**, quando uma fórmula legada conflita com regra de governança mais forte.

A regressão não deve obrigar o novo núcleo a repetir uma inconsistência antiga. Nesses casos, a diferença deve ser documentada e explicitamente aprovada.
