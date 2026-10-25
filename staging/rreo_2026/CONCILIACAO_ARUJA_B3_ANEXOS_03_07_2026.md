# Auditoria do RREO de Arujá — Anexos 03 e 07 — 3º bimestre de 2026

**Base:** registros JSON de consulta Siconfi recuperados por Crawl2AI e preservados em `staging/rreo_2026/3503901/`, na ramificação editorial E2. Valores nominais em reais; conciliação interna entre colunas e linhas da mesma fonte; não é auditoria externa independente.

## Anexo 03 — receita corrente líquida

Somadas as doze colunas `<MR-11>` a `<MR>` de cada rubrica, comparadas com `TOTAL (ÚLTIMOS 12 MESES)`:

| Código da rubrica | Meses | Soma mensal R$ | Total declarado R$ | Diferença R$ |
|---|---:|---:|---:|---:|
| `RREO3ReceitaCorrenteLiquida` | 12 | 690.264.222,57 | 690.264.222,57 | 0,00 |
| `RREO3ReceitaCorrenteLiquidaAjustadaParaCalculoDosLimitesDeEndividamento` | 12 | 670.622.728,57 | 670.622.728,57 | 0,00 |

A janela de RCL cobre doze meses móveis; **não** é receita acumulada no primeiro semestre. A RCL ajustada para despesa com pessoal consta em rubrica específica e não foi confundida com receita corrente bruta.

## Anexo 07 — restos a pagar

Selecionada exclusivamente a linha agregada `TOTAL (III) = (I + II)`, sem somar as linhas hierárquicas do Executivo, Legislativo e Câmara.

- Processados: inscritos em exercícios anteriores R$ 60,23 + inscritos em 31/12/2025 R$ 4.174.547,27 − pagos R$ 4.165.567,01 − cancelados R$ 9.040,49 = **R$ 0,00**.
- Não processados: inscritos anteriores R$ 2.073,00 + inscritos em 31/12/2025 R$ 2.424.739,42 − pagos R$ 1.679.735,88 − cancelados R$ 665.548,40 = **R$ 81.528,14**. Igual ao `Saldo k` declarado.
- Saldo total = R$ 0,00 + R$ 81.528,14 = **R$ 81.528,14**. Igual ao `Saldo Total L` declarado.

Todas as diferenças de conciliação foram de R$ 0,00. Os valores são estoques e movimentações de restos a pagar, não despesas pagas do orçamento de 2026.

## Limites

Validações aritméticas das rubricas selecionadas; não houve cotejo com documentos originais de outro fornecedor, nem verificação de todas as contas e eventuais retificações. Manter isolamento de staging e não promover automaticamente ao banco canônico ou à publicação.
