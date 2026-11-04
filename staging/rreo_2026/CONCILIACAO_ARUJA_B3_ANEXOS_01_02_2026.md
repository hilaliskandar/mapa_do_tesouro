# Conciliação dos Anexos 01 e 02 do RREO — Arujá, 2026, 3º bimestre

**Origem:** JSONs Siconfi preservados nesta branch em `3503901/rreo_2026_b3_anexo_01.json` e `3503901/rreo_2026_b3_anexo_02.json` (caminho relativo à pasta `staging/rreo_2026`).

**Chave de comparação:** município 3503901; 2026; bimestre 3; despesa *exceto intraorçamentária*. No Anexo 01, `cod_conta=DespesasExcetoIntraOrcamentarias`. No Anexo 02, `conta=DESPESAS (EXCETO INTRA-ORÇAMENTÁRIAS) (I)`. Comparar colunas semanticamente correspondentes; letras das colunas diferem.

| Medida | Anexo 01 | Anexo 02 | Valor em ambos R$ | Divergência R$ |
|---|---|---|---:|---:|
| Dotação inicial | DOTAÇÃO INICIAL (d) | DOTAÇÃO INICIAL | 760.000.000,00 | 0,00 |
| Dotação atualizada | DOTAÇÃO ATUALIZADA (e) | DOTAÇÃO ATUALIZADA (a) | 838.830.581,27 | 0,00 |
| Empenhado no bimestre | DESPESAS EMPENHADAS NO BIMESTRE | DESPESAS EMPENHADAS NO BIMESTRE | 118.218.641,99 | 0,00 |
| Empenhado acumulado | DESPESAS EMPENHADAS ATÉ O BIMESTRE (f) | DESPESAS EMPENHADAS ATÉ O BIMESTRE (b) | 567.130.723,80 | 0,00 |
| Saldo a empenhar | SALDO (g) = (e-f) | SALDO (c) = (a-b) | 271.699.857,47 | 0,00 |
| Liquidado no bimestre | DESPESAS LIQUIDADAS NO BIMESTRE | DESPESAS LIQUIDADAS NO BIMESTRE | 132.813.524,05 | 0,00 |
| Liquidado acumulado | DESPESAS LIQUIDADAS ATÉ O BIMESTRE (h) | DESPESAS LIQUIDADAS ATÉ O BIMESTRE (d) | 383.150.645,94 | 0,00 |
| Saldo a liquidar | SALDO (i) = (e-h) | SALDO (e) = (a-d) | 455.679.935,33 | 0,00 |

**Resultado:** 8 pares avaliados, todos iguais ao centavo. Saldos também conferem aritmeticamente: dotação atualizada menos empenho acumulado = saldo a empenhar; dotação atualizada menos liquidação acumulada = saldo a liquidar.

**Limites:** comparação entre dois anexos de mesma origem Siconfi, não validação independente da prestação de contas. Exclui despesa intraorçamentária, demais rubricas, conciliação de restos a pagar e verificação da hierarquia função/subfunção. Despesas pagas não possuem par equivalente no Anexo 02, portanto ficam fora do cotejo. Não agrega totais e desdobramentos. Sem alteração de painel nem da base canônica.
