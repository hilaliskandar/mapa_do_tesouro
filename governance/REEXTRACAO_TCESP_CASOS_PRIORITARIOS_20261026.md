# Reextração independente dos dez casos prioritários TCESP–DCA

Data do controle: 26/10/2026. Estado: **um caso concluído; nove casos em execução/espera**.

## Motivação e universo
A conciliação estadual 2023–2025 com DCA canônica identificou 55 divergências em 1.931 pares confrontáveis. Os dez maiores desvios absolutos concentram aproximadamente 90,22% da soma das diferenças. Objetivo desta diligência: testar independentemente se a primeira extração TCESP desses dez pares é reproduzível a partir do ZIP oficial bruto.

## Procedimento
1. Obter o ZIP original do TCESP por intervalos HTTP 206 verificando `Content-Range`, comprimento total e assinatura.
2. Verificar integridade ZIP (CRC) e SHA-256 do objeto completo.
3. Recalcular separadamente `valor liquidado` do grupo 44 em centavos, sem reutilizar os agregados do pipeline anterior.
4. Confrontar total novo, total antigo e hash de fonte anterior.
5. Não interpretar persistência de divergência TCESP–DCA como prova de erro em qualquer fonte.

## Evidências do piloto 2025
- Run GitHub [40345679633](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40345679633): **success**.
- Artefato de QA: `tcesp-2025-verified-range-reextract-qa` (ID `12664341829`).
- Fonte: `https://transparencia.tce.sp.gov.br/sites/default/files/conjunto-dados/despesas-2025.zip`.
- Tamanho oficial efetivamente obtido: **2.104.704.991 bytes**; ZIP CRC **pass**.
- SHA-256 antigo e novo: `ca4e0936c9d61d511aa0b778182a5ab3724503e0149ea84a8e0da17aae4b2d93`.
- Código IBGE: `3517901` (exercício 2025).
- Total liquidado TCESP anterior: **482.777.814 centavos** (R$ 4.827.778,14).
- Total independente reextraído: **482.777.814 centavos** (R$ 4.827.778,14).
- Diferença novo − anterior: **zero**.
- Valor DCA canônico usado na comparação: **422.548.920 centavos** (R$ 4.225.489,20).
- Divergência TCESP − DCA remanescente: **60.228.894 centavos** (R$ 602.288,94).

**Conclusão limitada:** o primeiro resultado TCESP desse par foi reproduzido, inclusive com hash idêntico da fonte bruta. A causa da diferença entre TCESP e DCA permanece indeterminada.

## Continuidade dos nove casos de 2023–2024
- Workflow: `.github/workflows/tcesp-2023-2024-range-reextract.yml`.
- Run [40357587853](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40357587853).
- Última consulta: **2023 em transferência integral por faixas; 2024 em fila**. `max-parallel: 1` para evitar concorrência.
- Pares 2023: `3548807`, `3545209`, `3502804`.
- Pares 2024: `3554102`, `3522158`, `3533254`, `3548906`, `3534708`, `3520301`.

## Critérios de desfecho
- Mesmo hash e mesmo total: reprodutibilidade da extração confirmada, divergência documental ainda pendente.
- Hash diferente e total igual: provável atualização de arquivo sem alteração do agregado examinado; verificar versões e procedência.
- Hash igual e total diferente: indício de problema de processamento, a localizar no código e nas linhas selecionadas.
- Hash diferente e total diferente: não atribuir causa antes da conciliação das versões da fonte.

As fontes brutas não foram alteradas; o novo relatório e o README são os únicos artefatos de documentação persistente desta atualização. Não houve publicação em produção.
