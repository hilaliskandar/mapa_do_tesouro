# Auditoria das razões derivadas — resultado canônico de 14/10/2026

## Evidência e execução

- GitHub Actions: [SP645 Private Site Artifact #38589671843](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/38589671843), resultado `success`.
- Commit: `3c29e396b355fffd354166db05e25c4abb82430c` (após PR #158).
- Artefato: `sp645-private-site-38589671843`, ID GitHub `11907036274`.
- Fonte quantitativa: `qa_derived_ratio_parity.json`, extraído desse artefato; verificação independente da tabela `observacao`, para observações marcadas `referencia_origem=pipeline:ratio`.
- A auditoria de importação `qa_percentage_scale_parity.json` também foi aprovada na mesma construção, com zero divergências.

## Resultado

- 14 indicadores do mapa `RATIOS`.
- 3.225 pares município-ano inspecionados (645 municípios, 2021–2025).
- 5.420 valores observados conciliados numericamente, todos do exercício 2025.
- 3.610 combinações cujo estado armazenado era `ausente` e correspondia à regra do cálculo.
- 36.120 combinações excluídas da prova numérica pela proveniência distinta de `pipeline:ratio` ou falta do registro.
- **Zero divergências** entre resultados registrados como cálculo interno e a razão recalculada independentemente.

| Indicador | Observados conciliados em 2025 | Ausentes | Excluídos por proveniência ou falta de registro |
|---|---:|---:|---:|
| receita_tributaria_pct_receita_corrente | 644 | 1 | 2580 |
| fpm_pct_receita_corrente | 643 | 2 | 2580 |
| icms_pct_receita_corrente | 644 | 1 | 2580 |
| ipva_pct_receita_corrente | 643 | 2 | 2580 |
| tributos_imobiliarios_pct_receita_tributaria | 641 | 4 | 2580 |
| transferencias_selecionadas_pct_receita_corrente | 643 | 2 | 2580 |
| urbanismo_pct_territorial | 65 | 580 | 2580 |
| habitacao_pct_territorial | 65 | 580 | 2580 |
| saneamento_pct_territorial | 65 | 580 | 2580 |
| gestao_ambiental_pct_territorial | 65 | 580 | 2580 |
| transporte_pct_territorial | 65 | 580 | 2580 |
| investimento_pct_receita_corrente | 644 | 1 | 2580 |
| despesa_territorial_pct_despesa | 65 | 580 | 2580 |
| caixa_pos_rpnp_pct_rcl | 528 | 117 | 2580 |
| **Total** | **5420** | **3610** | **36120** |

## Limites e decisão

**Aprovado:** consistência da regra aritmética de razão interna e dos status para as observações produzidas pelo pipeline em 2025; não houve desacordo nos valores submetidos a comparação.

**Não aprovado automaticamente:** exatidão das fontes DCA e RGF; comparabilidade entre exercícios; razões históricas importadas; conversão final da escala interna 0–1 para percentuais exibidos; preenchimento das 48 cautelas editoriais. Os 17 indicadores percentuais continuam sem certificado final de apresentação, e `publication_qa` não deve ser promovido automaticamente.

**Alerta de interpretação:** 36.120 é uma contagem de combinações indicador × município × ano excluídas do recálculo, não um número de erros ou necessariamente de valores ausentes. As 3.610 ausências representam resultados legitimamente não observados dentro do escopo de 2025.

## Próximas verificações

1. Reconciliar os valores percentuais derivados com as contas de origem e o tratamento de escala também em fontes externas ao SQLite.
2. Realizar verificação comparativa da série histórica importada por exercício e variável; não presumir que a paridade de 2025 abranja 2021–2024.
3. Produzir matriz de apresentação `storage_scale`, `display_multiplier` e evidência para cada um dos 17 percentuais, sem preenchimento heurístico.
4. Concluir cautelas específicas, começando pelos indicadores que alimentam comparações regionais e narrativas editoriais.
