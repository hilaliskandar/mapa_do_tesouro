# Diagnóstico da cobertura territorial — 14/10/2026

## Evidência
- Base privada canônica da execução [#38593209824](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/38593209824), artefato `11908541959`.
- Conferência diretamente no `sp645_private.sqlite` e no `SP645_PRIVATE_SITE_INPUT_2021_2025.xlsx` presentes no mesmo artefato.
- Universo: 645 municípios, exercício 2025.

## Cobertura das cinco contas da soma estrita

| Função | Observados | Ausentes | Cobertura |
|---|---:|---:|---:|
| Urbanismo | 639 | 6 | 99,1% |
| Habitação | 146 | 499 | 22,6% |
| Saneamento | 330 | 315 | 51,2% |
| Gestão Ambiental | 527 | 118 | 81,7% |
| Transporte | 458 | 187 | 71,0% |
| **Agregado territorial de cinco funções** | **65** | **580** | **10,1%** |

Em 2025, o arquivo de entrada contém células `None` (vazias de fato) para 499 municípios em Habitação, 315 em Saneamento e 6 em Urbanismo. Não há zeros numéricos nessas colunas nas linhas 2025 verificadas. A lacuna antecede o banco SQLite: **não decorre de perda de registro na importação**. Contudo, a classificação `None` não demonstra que o demonstrativo oficial tenha omitido o valor: a transformação anterior à planilha integrada pode ter suprimido os registros de valor zero ou falhado na extração.

## Efeito da regra `strict_sum`

A agregação `despesa_territorial` em `pipeline/transform/calculate_annual.py` exige observação de todas as cinco contas para publicar o total. Municípios distribuídos por número de funções sem observação:

| Funções ausentes | Municípios |
|---:|---:|
| 0 | 65 |
| 1 | 192 |
| 2 | 254 |
| 3 | 113 |
| 4 | 19 |
| 5 | 2 |

Padrões relevantes: 138 municípios têm apenas Habitação ausente; 136 têm apenas Habitação e Saneamento ausentes. Assim, a regra completa impede a apresentação de um agregado territorial para 580 municípios, mesmo quando existem valores de algumas funções.

## Separação das hipóteses

1. **Confirmado:** as células vazias de funções selecionadas já estão no arquivo combinado de entrada de 2025; não foram criadas pelo cálculo da razão.
2. **Confirmado:** a regra estrita explica por que somente 65 municípios recebem o agregado completo.
3. **Não verificado:** se as células vazias correspondem a zero efetivamente declarado, omissão da informação, falta de execução orçamentária na função, problema de classificação contábil ou falha na extração da DCA.
4. **Não permitido:** preencher ausentes com zero ou usar soma parcial como se fosse total territorial sem documentação específica.

## Próximas ações

- Confrontar amostra estratificada de municípios sem Habitação/Saneamento com os itens originais da DCA/SICONFI, incluindo casos com todas as cinco funções e casos com nenhuma.
- Inspecionar o transformador do Gate C/D que gerou o workbook `FINBRA_SP645_BASE_MULTIFONTES_2025_GATE_C.xlsx` e confirmar explicitamente o destino de itens de valor `0`.
- Caso a DCA confirme `0`, persistir valor observado zero com fonte, ano, conta e prova; recalcular agregados.
- Caso a DCA confirme ausência real, preservar `ausente`, mas publicar funções isoladas e eventual **soma parcial identificada como limite inferior**, sem tratá-la como total.
- Publicar metadados de cobertura por função e município e comunicar a ressalva em tabelas, mapas e boletins.

**Bloqueio:** não homologar a cobertura do agregado territorial como representativa dos 645 municípios antes de concluir a verificação da fonte.
