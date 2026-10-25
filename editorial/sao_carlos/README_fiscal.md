# Sao Carlos — inventario de fontes e extracoes fiscais

Atualizado em 2026-10-25. Municipio IBGE 3548906, TCESP `sao-carlos`.

## Fontes principais
- Despesas e investimentos: `https://transparencia.tce.sp.gov.br/sites/default/files/csv/despesas-sao-carlos-{ano}.zip`
- Receitas: `https://transparencia.tce.sp.gov.br/sites/default/files/csv/receitas-sao-carlos-{ano}.zip`
- Balancetes oficiais da Prefeitura: https://www.saocarlos.sp.gov.br/index.php/balancete-de-receita.html
- Referencia monetaria prevista: IPCA/IBGE, setembro de 2026, atualizacao mensal de fluxos.

## Extracoes concluidas
| Assunto | Execucao GitHub | Artefato | Vencimento |
|---|---|---|---|
| TCESP investimentos 2023–2026 | https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40213455640 | `sao-carlos-tcesp-2023-2026` | 2026-11-24 |
| TCESP despesas por mes, orgao, fonte e acao | https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40222584058 | `sao-carlos-tcesp-detalhe-2023-2026` | 2026-11-24 |
| Esquema dos CSVs de receita | https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40226770931 | `sao-carlos-receitas-tcesp-esquema-2023-2026` | 2026-11-24 |
| IPTU, ISS e ITBI por mes e rubrica | https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40226826428 | `sao-carlos-tributos-2023-2026` | 2026-11-24 |

ATENCAO: artefatos de Actions nao sao arquivos versionados no repositorio. Todos os artefatos acima possuem retencao de 30 dias. Nao ha comprovacao de copia automatica para Google Drive ou banco permanente. O codigo e os workflows estao versionados, permitindo repetir as consultas enquanto a fonte estiver disponivel.

## Numeros de controle
- Investimentos liquidados TCESP: 2023 R$ 76.808.334,24; 2024 R$ 138.740.832,67; 2025 R$ 43.514.422,78; janeiro–agosto de 2026 R$ 27.105.369,39.
- Comparacao de investimentos TCESP versus DCA 2024: diferenca aproximada R$ 3,16 milhoes, a conciliar.
- IPTU ISS ITBI 2026: comparar janeiro–agosto com mesmos meses 2023, 2024 e 2025; distinguir codigos de principal, divida ativa, multas e juros.
- IPCA de setembro de 2026 como data-base; nao misturar atualizacao anual por dezembro com atualizacao mensal.

## Pendencias prioritarias
1. Guardar versao permanente das tabelas processadas e hashes, de preferencia em Drive ou dados versionados no projeto, respeitando limites do repositorio.
2. Validar valores mensais de cada tributo com balancetes municipais e explicitar receita principal versus receitas acessorias.
3. Atualizar arrecadacao pelo IPCA mensal antes de interpretar variacoes reais de 2026.
4. Apurar empenhos, anulacoes, liquidacoes e pagamentos por acao e por contrato, inclusive restos a pagar.
5. Conciliar diferenca TCESP x DCA em 2024 e identificar a natureza institucional da acao 2074.
