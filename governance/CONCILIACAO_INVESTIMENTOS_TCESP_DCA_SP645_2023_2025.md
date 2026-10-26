# Matriz estadual TCESP × DCA — investimentos liquidados, primeira execução

Data: 26/10/2026. Execução auditável: [40333583682](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40333583682), `success`.

## Método e fontes
Confronto por código IBGE e exercício, em centavos inteiros, entre TCESP investimentos liquidados do grupo 44 e observação `dca_investimentos_liquidada` da API fiscal v2 estadual. Scripts `pipeline/qa/conciliar_tcesp_dca_sp645.py` e `.github/workflows/tcesp-dca-sp645-parity.yml`. Fonte TCESP: artefatos auditados 2023/24 run `40263996213`, 2025 run `40262193781`; fonte DCA: artefato SP645 `40317752109`. Nenhuma alteração às bases originais ou publicação.

## Resultado global da execução
- Universo: 645 códigos municipais × 3 exercícios = **1.935** linhas, incluindo São Paulo capital como não confrontável no TCESP.
- **Concordantes:** 633.
- **Divergentes:** 10.
- **Não confrontáveis:** 1.292, incluídos casos sem cobertura TCESP, observação ausente, status distinto de `observado` e valores não utilizáveis.
- Os 10 registros divergentes disponíveis na saída da execução pertencem a **2025**. O conjunto de 2023 e 2024 deve ser examinado quanto à disponibilidade de registros DCA na versão do artefato; esta matriz **não substitui** a auditoria externa regional RMRP de 102 pares realizada com outro arquivo canônico DCA.

## Divergências encontradas em 2025
| Código IBGE | TCESP R$ | DCA R$ | TCESP − DCA R$ |
|---|---:|---:|---:|
| 3517901 | 4.827.778,14 | 4.225.489,20 | 602.288,94 |
| 3514908 | 6.794.049,04 | 6.429.659,00 | 364.390,04 |
| 3519501 | 4.299.056,58 | 4.149.056,58 | 150.000,00 |
| 3554300 | 8.613.031,78 | 8.522.462,78 | 90.569,00 |
| 3544004 | 1.662.746,75 | 1.582.029,19 | 80.717,56 |
| 3535309 | 6.068.206,43 | 6.012.578,59 | 55.627,84 |
| 3541208 | 5.299.667,85 | 5.309.417,85 | −9.750,00 |
| 3525805 | 1.272.941,01 | 1.263.356,09 | 9.584,92 |
| 3549904 | 211.165.220,29 | 211.167.807,29 | −2.587,00 |
| 3552304 | 1.864.029,11 | 1.865.779,11 | −1.750,00 |

Os valores da tabela refletem o resultado computacional e não implicam erro em nenhuma fonte. Os códigos devem ser associados ao cadastro municipal aprovado antes da divulgação editorial.

## Interpretação e lacunas
A proporção de concordâncias só é informativa **entre as linhas efetivamente confrontáveis**. Não se deve usar como taxa de cobertura da totalidade estadual. O total de 1.292 não confrontáveis exige distribuição por exercício e motivo, com prioridade para recuperar a série DCA dos exercícios 2023–2024 na mesma base canônica que embasou o confronto RMRP. Preservar a distinção entre fonte, exercício, estágio liquidado e disponibilidade. A exceção regional **Guatapará/2023 (R$ 10.176,00)** continua documentada em `governance/CONCILIACAO_INVESTIMENTOS_TCESP_DCA_RMRP_2023_2025.md`, independentemente da ausência de paridade estadual nessa versão de dados.

## Artefatos
O run 40333583682 produz `conciliacao_tcesp_dca_sp645.csv` e `conciliacao_tcesp_dca_sp645.summary.json` como artefato de workflow; não são a base oficial canônica nem substituem os dados de origem.

## Próximas verificações
1. Resumir cobertura DCA por ano/status e confrontabilidade dos 1.935 pares, com contagens exatas.
2. Conferir a escala e versão da variável DCA e os dez casos divergentes 2025 diretamente nos documentos de origem.
3. Reexecutar contra extrato DCA completo 2023–2025, verificar a conhecida exceção de Guatapará e documentar divergências remanescentes.
4. Manter bloqueada a promoção à produção até completar QA metodológico e editorial.
