# FED04 — Confronto oficial DCA 2025 × fomento Fundeb ETI (Portaria MEC 669/2025): 18 maiores casos

**Data:** 10/11/2026. **Situação:** correspondência documental federal/municipal exata; comprovação bancária ainda não executada. **Não homologar como pagamento comprovado.**

## 1. Descoberta metodológica
O conjunto original de 191 municípios "sem correspondência FNDE VAAT/VAAR" foi construído sobre um universo de modalidades incompleto. A Portaria MEC nº 669, de 1º de outubro de 2025, que alterou a Portaria MEC nº 605/2025, estabelece o **fomento à criação de matrículas em tempo integral (ETI)** financiado por complementação da União ao Fundeb. Seu **Anexo II** individualiza os valores por código IBGE, rede municipal, total e repasses mensais estimados.

Cronograma do art. 7º, §2º: **outubro 2025: 42,5%; novembro: 21,25%; dezembro: 21,25%; janeiro 2026: 15%**; total previsto até dezembro de 2025 **85%**. O Anexo II é cronograma autorizado, sujeito à disponibilidade e a ajustes, não extrato bancário.

**Fonte federal primária:** https://www.gov.br/fnde/pt-br/acesso-a-informacao/acoes-e-programas/financiamento/fundeb/legislacao/2025/portaria-mec-no-669-de-1o-de-outubro-de-2025/@@display-file/file (arquivo do Diário Oficial da União, seção 1, 02/10/2025, Portaria MEC nº 669/2025, Anexo II; páginas digitais 39–42 para municípios SP).
**Fonte DCA:** `governance/FED04_18_MAIORES_PENDENTES_DCA_2024_2025_API_2026_11_10.csv`, rubrica `RO1.7.1.5.00.0.0`, coluna receita bruta realizada 2025, consultada anteriormente na API SICONFI.
**Corroboração municipal direta:** São José dos Campos — Balancete da Receita dezembro/2025, natureza 17155301000, Diário Municipal nº 3.642 de 30/01/2026; ver `governance/FED04_SJC_ETI_CONCILIACAO_DOCUMENTAL_2026_11_10.md`.

## 2. Resultado para os 18 maiores
| # | Código IBGE | Município | DCA 2025 (R$) | ETI total previsto na portaria (R$) | 85% previsto para 2025 (R$) | Delta (R$) |
|---:|---|---|---:|---:|---:|---:|
| 1 | 3549904 | São José dos Campos | 3304327.61 | 3887444.25 | 3304327.61 | 0,00 |
| 2 | 3551009 | São Vicente | 3271812.78 | 3849191.50 | 3271812.78 | 0,00 |
| 3 | 3552809 | Taboão da Serra | 2670875.53 | 3142206.51 | 2670875.53 | 0,00 |
| 4 | 3516200 | Franca | 2577016.74 | 3031784.40 | 2577016.74 | 0,00 |
| 5 | 3516408 | Franco da Rocha | 2389643.17 | 2811344.90 | 2389643.17 | 0,00 |
| 6 | 3515004 | Embu das Artes | 2265628.90 | 2665445.76 | 2265628.90 | 0,00 |
| 7 | 3541000 | Praia Grande | 1861363.29 | 2189839.17 | 1861363.29 | 0,00 |
| 8 | 3510500 | Caraguatatuba | 1745520.08 | 2053553.04 | 1745520.08 | 0,00 |
| 9 | 3524402 | Jacareí | 1731254.16 | 2036769.60 | 1731254.16 | 0,00 |
| 10 | 3530706 | Mogi Guaçu | 1617746.78 | 1903231.50 | 1617746.78 | 0,00 |
| 11 | 3509502 | Campinas | 1594674.60 | 1876087.76 | 1594674.60 | 0,00 |
| 12 | 3531803 | Monte Mor | 1461545.05 | 1719464.76 | 1461545.05 | 0,00 |
| 13 | 3555406 | Ubatuba | 1254283.38 | 1475627.51 | 1254283.38 | 0,00 |
| 14 | 3554003 | Tatuí | 1193304.33 | 1403887.45 | 1193304.33 | 0,00 |
| 15 | 3507001 | Boituva | 1155374.34 | 1359263.93 | 1155374.34 | 0,00 |
| 16 | 3529401 | Mauá | 1127449.91 | 1326411.66 | 1127449.91 | 0,00 |
| 17 | 3552403 | Sumaré | 934884.37 | 1099863.96 | 934884.37 | 0,00 |
| 18 | 3541406 | Presidente Prudente | 891681.86 | 1049037.48 | 891681.86 | 0,00 |

**QA:** exatamente 18/18 pares de chaves IBGE7 com diferença zero ao centavo entre DCA 2025 e 85% do total ETI do Anexo II, aplicando arredondamento monetário. Soma DCA = **R$ 33.048.386,88**; soma estimada = **R$ 33.048.386,88**; diferença agregada = R$0,00. Arquivo computável: `governance/FED04_18_PRIORITARIOS_CONFRONTO_ETI_PORTARIA_669_2026_11_10.csv`.

O valor de cada 2025 é a proporção 85% do total oficial; **a correspondência exata não substitui comprovação de que as três parcelas foram efetivamente pagas e creditadas**.

## 3. Interpretação e reclassificação cautelar
- Originalmente havia 191 municípios no estrato sem vínculo FNDE VAAT/VAAR 2024/2025, R$65.353.959,01 em DCA 2025. Os 18 maiores somavam **R$33.048.386,88**, isto é, os 50,5683% do valor original priorizado.
- Os 18 deixam de ser "sem referência federal de fomento" e passam a **`ETI_2025_CRONOGRAMA_OFICIAL_85PCT_CONCILIADO_DCA`**; conservar flag independente de **pagamento bancário não comprovado**.
- O remanescente aritmético dos **173 outros registros** do grupo original é **R$32.305.572,13**, ainda não testado contra o anexo ETI. **Não afirmar que os 173 são divergências**: esta etapa não analisou o grupo integral.
- O bloco dos 106 anteriormente associados a listas FNDE de 2024 também requer teste ETI 2025; a evidência de 2024 não é necessária para explicar a receita 2025 enquanto a causa ETI não for descartada.
- As modalidades VAAT, VAAR, VAAF e **ETI** exigem identidade de classificação, modalidade e competência; **ETI decorre de destinação especial de parte das complementações** (art. 212-A, XIV, Constituição/EC 135/2024), não deve ser somada novamente às receitas de Fundeb.
- Nos casos de 2024 com rubrica positiva, manter a auditoria histórica separada; não atribuir retroativamente o mecanismo ETI/2025 ao valor DCA 2024.

## 4. Próxima execução
1. **Cruzar os 173 restantes por código IBGE7 contra o mesmo Anexo II**, computando `delta = DCA2025 - ROUND(0,85 * ETI_TOTAL,2)` em centavos. Verificar também **todos os 297 originalmente DCA-only**, e depois todo o SP645 para falsos negativos, componente misto e valores ETI com outras modalidades.
2. Separar situação `CRONOGRAMA_ETI_CONCILIADO` de `REPASSE_BANCARIO_HOMOLOGADO`; conferir extratos FNDE/SIGEF e eventuais ajustes, mês a mês, outubro 2025–janeiro 2026.
3. Verificar 16 casos inversos FNDE VAAT/VAAR contra ETI, mas não usar o valor ETI para substituir classificação VAAT/VAAR.
4. Ajustar crosswalk de natureza 171553 e suas versões, com fonte, competência, agregação e antidupla-contagem.
5. Manter **FED04 in_progress** e **PR #232 draft**, sem merge, migração, deploy ou mudanças na produção.

## 5. Rastreabilidade
O confronto foi construído de leitura de 18 linhas do Anexo II do PDF oficial (páginas 39–42, códigos IBGE7 individuais), comparadas aos 18 registros DCA já versionados no repositório; não foi gerada declaração de execução de consulta bancária.
