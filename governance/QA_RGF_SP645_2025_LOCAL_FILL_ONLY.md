# QA — RGF SP645 2025 — ausências e composição fill-only local

## Ausência na fonte Siconfi

A inspeção dos 1.290 payloads brutos dos Anexos 01 e 05 mostra:

- Anexo 01: 115 municípios com `items=[]`;
- Anexo 01: zero casos com payload não vazio sem a linha canônica de DTP;
- Anexo 05: 117 municípios com `items=[]`;
- 115 municípios têm `items=[]` nos dois anexos;
- os dois casos adicionais de ausência apenas no Anexo 05 são:
  - Mairinque — 3528403;
  - Oscar Bressane — 3534500.

Portanto, as 115 ausências de DTP/RCL legal são ausências do payload da fonte consultada, não falha de normalização.

## Relação com o RREO

- RCL ausente no RREO 2025: 114 municípios;
- DTP/RCL legal ausente no RGF Anexo 01: 115;
- interseção: 114;
- único caso adicional no RGF: Jandira — 3525003.

No snapshot oficial CAPAG, Jandira possui a observação:

> Ente não publicou último RGF de 2025

Essa justificativa é válida para Jandira. Ela não é generalizada aos demais municípios, porque o snapshot não traz a mesma observação para eles.

## Composição fill-only com o snapshot CAPAG/RGF local

O snapshot CAPAG contém campos semanticamente idênticos a parte do Anexo 05. Foi aplicada composição estritamente fill-only:

- valor Siconfi observado nunca é substituído;
- suplemento só preenche célula vazia;
- conflito entre dois valores observados bloquearia a composição;
- resultado encontrado: zero conflitos.

Preenchimentos adicionais:

| Variável | Células preenchidas |
|---|---:|
| Caixa bruta não vinculada | 109 |
| RP liquidados anteriores não vinculados | 74 |
| RP liquidados do exercício não vinculados | 89 |
| RP não liquidados anteriores não vinculados | 79 |
| Demais obrigações não vinculadas | 15 |

Cobertura resultante:

| Variável | Observados após fill-only | Cobertura |
|---|---:|---:|
| DTP legal | 530/645 | 82,17% |
| RCL denominador legal | 530/645 | 82,17% |
| Percentual DTP/RCL | 530/645 | 82,17% |
| Caixa bruta não vinculada | 635/645 | 98,45% |
| RP liquidados anteriores | 478/645 | 74,11% |
| RP liquidados do exercício | 501/645 | 77,67% |
| RP não liquidados anteriores | 490/645 | 75,97% |
| Demais obrigações | 108/645 | 16,74% |
| Caixa líquida antes RPNP | 528/645 | 81,86% |
| RP não liquidados do exercício | 410/645 | 63,57% |
| Caixa líquida após RPNP | 528/645 | 81,86% |

Hashes:

- base RGF normalizada: `9f3ced721fa2c767d24cdec8e464215b30932e820e01601f24bac9b1e76486ba`;
- snapshot CAPAG: `1b1379a5a531920223f1d448be155b70f51eb50180d8c819f1b7da3575a8eb11`;
- composto fill-only: `48b50b2df44eaddc2fc1c4ed096c057c2bea5d61cb850b37dc23e6037962aa24`.

## Decisão

O composto é uma camada derivada de análise e não substitui o snapshot bruto do Siconfi.

Não há justificativa para repetir imediatamente as 115 consultas do Anexo 01: os payloads já registram ausência da fonte. Qualquer tentativa de recuperação deve usar outra fonte oficial ou uma atualização temporal posterior, não uma repetição cega da mesma consulta.
