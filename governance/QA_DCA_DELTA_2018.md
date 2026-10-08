# QA — delta seletivo DCA 2018

Data: 2026-10-07/08.

## Execução

Workflow: `SICONFI SP 645 DCA Selective Delta`

Run ID: `37720130237`

Commit: `ed27f8c2fa4a2b62f46f03231017a4528d9f4551`

Municípios consultados:

- Anhumas — `3502408`;
- Monte Aprazível — `3531407`.

Anexos consultados:

- I-C;
- I-D;
- I-E.

Total: 6 respostas.

## Resultado operacional

- requisições concluídas: 6;
- falhas: 0;
- linhas normalizadas: 2;
- issues de normalização: 0;
- SHA-256 normalizado: `5e9aba6ee6d627eceeddd1e7648be8bd4abfe5476a34a339dd39da2ad2dd9a79`.

## Resultado substantivo

Nos seis artefatos brutos, o Siconfi retornou:

`items=[]`

Assim, nenhuma das lacunas do snapshot local de 2018 pôde ser preenchida pela API atual.

O CSV normalizado do delta contém as duas chaves município-ano, mas todas as 26 variáveis permanecem vazias.

## Interpretação

O run foi bem-sucedido do ponto de vista técnico. A ausência de valores não representa falha de coleta nem falha do normalizador.

A situação é classificada como:

`source_confirmed_absence`

Isso significa:

1. a lacuna está presente no snapshot histórico local;
2. a consulta atual ao Siconfi também não fornece observações;
3. não se deve preencher com zero;
4. não se deve repetir automaticamente a mesma consulta;
5. eventual recuperação futura exige outra fonte oficial ou nova versão do acervo.

## Decisão

2018 deixa a fila de complementação automática. Anhumas e Monte Aprazível permanecem ausentes nas variáveis DCA correspondentes, com proveniência explícita da ausência.
