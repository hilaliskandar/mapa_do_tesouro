# Conciliação numérica dos seis percentuais — 14/10/2026

## Origem e reprodução

- Execução GitHub Actions: [SP645 Private Site Artifact #38562576850](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/38562576850).
- Commit utilizado: `69039e9209e4f29ad790b20d07d1172b3d3a18f1`.
- Artefato: `sp645-private-site-38562576850`, ID GitHub 11893531740.
- Digest do artefato ZIP: `sha256:c292dacd65222cdcfa00ff4f78ea6c329c850b0ca08d3fcd141605569f3458d2`.
- Arquivo examinado: `qa_percentage_scale_parity.json`, armazenado no ZIP.
- Programa: `python -m pipeline.qa.audit_percentage_import_scale --database build/sp645_private.sqlite --workbook build/SP645_PRIVATE_SITE_INPUT_2021_2025.xlsx --mapping build/SP645_PRIVATE_SITE_MAPPING.yml --output build/qa_percentage_scale_parity.json`.

## Resultado

Amostra total de origem: 3.225 linhas município-ano (645 municípios, 2021 a 2025). A auditoria confrontou cada valor de entrada disponível com seu equivalente numérico na tabela `observacao`, após aplicar a transformação `scale=0.01`.

| Indicador | Valores conferidos | Fonte ausente dentro do período de disponibilidade | DB ausente para fonte observada | Divergências |
|---|---:|---:|---:|---:|
| receita_tributaria_pct_receita_corrente | 3.224 | 1 | 0 | 0 |
| investimento_pct_receita_corrente | 3.224 | 1 | 0 | 0 |
| despesa_territorial_pct_despesa | 324 | 2.901 | 0 | 0 |
| dtp_pct_rcl | 1.587 | 348 | 0 | 0 |
| dc_pct_rcl | 1.428 | 507 | 0 | 0 |
| dcl_pct_rcl | 1.587 | 348 | 0 | 0 |
| **Total** | **11.374** | **4.100** | **0** | **0** |

Nota: os três indicadores RGF só foram auditados para 2023–2025, conforme a janela de disponibilidade definida no mapeamento. Ausências de 2021–2022 não integram esses totais.

### Valores conferidos por exercício

| Indicador | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---:|---:|---:|---:|---:|
| receita_tributaria_pct_receita_corrente | 645 | 645 | 645 | 645 | 644 |
| investimento_pct_receita_corrente | 645 | 645 | 645 | 645 | 644 |
| despesa_territorial_pct_despesa | 56 | 66 | 65 | 72 | 65 |
| dtp_pct_rcl | — | — | 527 | 530 | 530 |
| dc_pct_rcl | — | — | 471 | 481 | 476 |
| dcl_pct_rcl | — | — | 527 | 530 | 530 |

## Delimitação da prova

**Aprovado:** paridade entre valor numérico presente na planilha canônica combinada e valor armazenado no SQLite após aplicar a escala declarada; zero divergências e zero registros ausentes na base quando a fonte apresentava valor.

**Não demonstrado por este teste:** se a fonte original fornecia efetivamente percentuais em 0–100, se os numeradores e denominadores estão conceitualmente corretos, se cada exercício mantém idêntico critério contábil, ou se `display_multiplier=100` é apropriado em todos os usos. Não altera o estado `scale_verified=false` da API v2.

**Lacunas de cobertura:** o indicador de despesa territorial apresenta somente 324 observações em 3.225 chaves possíveis. Sua cobertura limitada é um achado de disponibilidade, não uma divergência de conversão. Os percentuais RGF têm entre 1.428 e 1.587 observações para 1.935 chaves nos anos elegíveis.

## Próximo controle

1. Reconciliar, por município e ano, razões derivadas com seus numeradores e denominadores oficiais observados, diferenciando denominador nulo, zero e não comparável.
2. Comparar percentuais RGF com demonstrativos oficiais ou fonte canônica anterior à transformação, preservando evidência de origem.
3. Certificar escala interna e regra de exibição por indicador e janela temporal, com documentação verificável.
4. Tratar separadamente os onze indicadores percentuais não abrangidos por esta prova.
