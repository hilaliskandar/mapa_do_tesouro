# Fontes e referências

## Fontes fiscais principais

- FINBRA / Siconfi — DCA;
- RREO — inclusive RCL quando aplicável;
- RGF Anexo 01 — Despesa Total com Pessoal;
- RGF Anexo 02 — dívida consolidada e dívida consolidada líquida;
- RGF Anexo 05 — disponibilidade de caixa e restos a pagar;
- Tesouro Transparente — CAPAG.

## Acervo local FINBRA

O projeto dispõe de acervo local no Google Drive que deve ser consultado antes de qualquer coleta externa em massa:

`https://drive.google.com/drive/folders/1K_Raj0pKEyktVY5BVa_raOZ4cQdJ8HQ4`

Conteúdo já verificado:

- pastas anuais de 2013 a 2025;
- anexos DCA estaduais de São Paulo;
- `FINBRA_DCA_CANONICA_FINAL_2013_2025_2026-09-26`;
- caderno metodológico;
- crosswalks, QA, reconciliações e produtos intermediários.

Exemplos recentes:

- 2023: I-C, I-D e I-E em XLSX;
- 2024: I-C, I-D e I-E em XLSX;
- 2025: I-C, I-D e I-E em CSV.

## Regra de prioridade

Para reconstrução histórica e processamento em lote:

1. usar primeiro o acervo local do Drive;
2. preservar hash e metadados do arquivo efetivamente ingerido;
3. usar Siconfi externo para validação por amostra, atualização incremental, auditoria e investigação de discrepâncias;
4. somente repetir coleta externa integral quando não houver equivalente local adequado ou houver necessidade explícita de reaquisição.

A existência de arquivo local não dispensa a rastreabilidade da fonte oficial; apenas evita reconsultas externas desnecessárias.

## Fontes contextuais

- IBGE — população, IPCA e demais denominadores/contextos quando incorporados.

## Referências metodológicas herdadas

A documentação do projeto `mapa_do_tesouro` já reuniu referências relevantes como MCASP, MDF, Ementário da Receita, Portaria STN/SOF 163/2001, Portaria MOG 42/1999, PCASP, MSC, IFGF, Ranking Siconfi, IEG-M, Multi Cidades, PEFA, OCDE e PMAT.

Essas referências serão verificadas e atualizadas antes de serem consideradas catálogo normativo canônico da nova plataforma.
