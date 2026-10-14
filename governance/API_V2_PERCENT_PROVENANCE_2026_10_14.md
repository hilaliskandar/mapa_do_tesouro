# Proveniência dos 17 percentuais da API v2 — execução de 14/10/2026

## Evidência canônica

- Construção privada [#38593209824](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/38593209824), aprovada.
- Commit `e358870d7d2d0b7c5bbbc942644268cccd013034` (PR #160).
- Artefato `sp645-private-site-38593209824`, ID `11908541959`, ZIP `sha256:9ca1688182eb90a02517c9664dabd4870d88a9abdaad28e6cafd82bd3be81b21`.
- Fonte de dados: `qa_percentage_provenance.json` recuperado do artefato, agrupando `observacao` por ano, variável, estado e `referencia_origem`.

## Tipos de proveniência

**Série importada de 2021 a 2024 e calculada em 2025 (3):**
- `receita_tributaria_pct_receita_corrente`: 645 observados por ano em 2021–2024; 644 em 2025, origem `pipeline:ratio`.
- `investimento_pct_receita_corrente`: 645 observados por ano em 2021–2024; 644 em 2025, origem `pipeline:ratio`.
- `despesa_territorial_pct_despesa`: 56, 66, 65, 72 observados em 2021–2024; 65 em 2025, origem `pipeline:ratio`.

**Série importada inclusive em 2025, com disponibilidade a partir de 2023 (3):**
- `dtp_pct_rcl`: 527 (2023), 530 (2024), 530 (2025).
- `dc_pct_rcl`: 471 (2023), 481 (2024), 476 (2025).
- `dcl_pct_rcl`: 527 (2023), 530 (2024), 530 (2025).
- Para os três indicadores, 2021 e 2022 constam como `nao_aplicavel` por regra de janela no mapeamento; isso não significa ausência do dado na origem oficial.

**Somente calculados em 2025 (11):**
- `caixa_pos_rpnp_pct_rcl`: 528 observados.
- `fpm_pct_receita_corrente`: 643.
- `icms_pct_receita_corrente`: 644.
- `ipva_pct_receita_corrente`: 643.
- `tributos_imobiliarios_pct_receita_tributaria`: 641.
- `transferencias_selecionadas_pct_receita_corrente`: 643.
- `urbanismo_pct_territorial`, `habitacao_pct_territorial`, `saneamento_pct_territorial`, `gestao_ambiental_pct_territorial`, `transporte_pct_territorial`: 65 observados cada.

## Decisões metodológicas

1. **Não publicar séries anuais homogêneas** dos três indicadores com troca de linhagem (2021–2024 importado, 2025 calculado) sem reconciliação independente de componentes, critérios de despesa/receita e janela de competência.
2. Para os três RGF importados, validar definição do período, base da RCL e escala original; a paridade da importação prova transformação, não homogeneidade entre 2023, 2024 e 2025.
3. Não inferir cobertura histórica dos onze indicadores atualmente calculados apenas em 2025.
4. A cobertura de despesa territorial (56–72 municípios por exercício) impede o uso de sua série como retrato representativo do conjunto estadual sem ressalvas e análise de seleção.
5. Não definir automaticamente `display_multiplier` nem alterar o estado `scale_verified=false` no catálogo até certificação substantiva.

## Auditorias anteriores

- [Conciliação de 11.374 valores percentuais importados](API_V2_PERCENT_SCALE_PARITY_2026_10_14.md), sem divergências de ingestão.
- [Conciliação de 5.420 razões calculadas em 2025](API_V2_DERIVED_RATIO_PARITY_2026_10_14.md), sem divergências aritméticas.
- Estas verificações são complementares e **não equivalem** à comprovação de comparabilidade temporal ou validação de valores declarados nas fontes oficiais.
