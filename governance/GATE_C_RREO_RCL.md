# Gate C-R1 — RREO RCL estadual

## Contrato

A primeira expansão estadual do Gate C usa exclusivamente:

- endpoint: RREO;
- anexo: RREO-Anexo 03;
- período: 6;
- esfera: municipal;
- conta: `ReceitaCorrenteLiquida`;
- coluna: `TOTAL (ÚLTIMOS 12 MESES)`.

Saída canônica:

- `cod_ibge`;
- `ano`;
- `rreo_rcl_total_12m`;
- `populacao_rreo`;
- `qa_issue_count`.

## Regras

- uma linha por município-ano;
- match exato por conta e coluna;
- ausência permanece vazia;
- múltiplos matches viram issue de QA;
- conflito de população vira issue;
- não derivar RCL a partir do DCA;
- não confundir a RCL anual do RREO com o denominador legal do RGF.

## Execução

1. `Gate C RREO RCL Smoke`: 5 municípios, exercício 2025, automático após merge de mudanças relevantes;
2. `Gate C RREO RCL SP645`: workflow separado para carga estadual após smoke aprovado.

A carga estadual não publica nem altera o painel.
