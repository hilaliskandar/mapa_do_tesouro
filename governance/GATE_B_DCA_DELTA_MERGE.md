# Gate B — composição fill-only de snapshot e delta

## Regra

O delta externo é complemento, não substituição automática do snapshot histórico.

A composição normalizada aplica:

- base ausente + delta observado → preencher;
- base observada + delta ausente → preservar base;
- base observada = delta observado → preservar base;
- base observada ≠ delta observado → preservar base e registrar conflito;
- chave município-ano inexistente na base → rejeitar.

## Consequência

Revisões posteriores do Siconfi não substituem silenciosamente valores do snapshot local.

Um conflito exige decisão de QA e, se aprovado como revisão, deve ser tratado em processo separado com registro de proveniência.

## Artefatos

A composição gera:

- CSV composto;
- SHA-256 da base;
- SHA-256 do delta;
- SHA-256 da saída;
- número de células preenchidas;
- preenchimentos por variável;
- lista completa de conflitos;
- lista das células efetivamente preenchidas.

## Uso esperado

1. normalizar o snapshot local com universo de 645 municípios;
2. executar o workflow seletivo somente para códigos faltantes;
3. normalizar o delta;
4. executar `pipeline.normalize.dca_delta_merge`;
5. exigir zero conflitos para promoção automática;
6. revisar manualmente conflitos antes de qualquer substituição de valor observado.
