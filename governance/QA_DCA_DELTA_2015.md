# QA — delta seletivo DCA 2015

Data: 2026-10-08.

## Execução

Workflow: `SICONFI SP 645 DCA Selective Delta`

Run ID: `37720988539`

Municípios consultados:

- Ferraz de Vasconcelos — `3515707`;
- Tanabi — `3553401`.

Pares município–anexo solicitados: 6.

## Resultado

- requisições concluídas: 6;
- falhas: 0;
- linhas normalizadas: 2;
- variáveis no esquema: 26;
- issues de normalização: 0;
- pares com fonte vazia: 6;
- SHA-256 normalizado: `b4e0e5df5329a7eb0883914711103f870f5973049aafc9fe114db4bf735f1178`.

Nos seis payloads, o Siconfi retornou `items=[]`.

O CSV normalizado preserva as duas chaves município-ano, com todas as variáveis vazias.

## Classificação

`source_confirmed_absence`

A ausência é confirmada tanto no snapshot histórico local quanto na consulta atual ao Siconfi. Não deve ser convertida em zero nem reconsultada automaticamente.

## Decisão

2015 sai da fila automática de complemento. Eventual recuperação futura depende de outra fonte oficial ou de nova versão do acervo.
