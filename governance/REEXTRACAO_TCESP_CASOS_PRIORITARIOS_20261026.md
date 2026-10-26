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

## Atualização: 2023 concluído, 2024 em processamento
- Workflow [40357587853](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40357587853): tarefa 2023 `success`; tarefa 2024 ainda `in_progress` no último exame, sem comparação concluída.
- ZIP oficial de 2023: **2.103.701.773 bytes**, CRC **pass**, membro `despesas-2023.csv`, hash SHA-256 novo e histórico **idênticos**: `78de6ad8c031240a81c789d5e1379d12efd0a44536c62dbfbaba2c6e45f893d0`.
- Comparação independente dos três casos de 2023, em centavos: **3502804** antigo 3.251.316.801 / novo 3.251.316.801; **3545209** antigo 3.989.889.344 / novo 3.989.889.344; **3548807** antigo 14.717.318.849 / novo 14.717.318.849. Todas as diferenças novo − antigo: **zero** (`all_totals_equal: true`).
- Somando o caso de 2025 já validado, **quatro de dez** casos prioritários tiveram a leitura TCESP reproduzida a partir do ZIP oficial com hash idêntico. A divergência original TCESP–DCA não foi resolvida nem atribuída a uma fonte.
