# Coleta RREO 2026 — Buritizal — 3º bimestre

Fonte: API Siconfi/Tesouro `https://apidatalake.tesouro.gov.br/ords/siconfi/tt/rreo`, recuperada por Crawl2AI, cod_ibge 3508207, exercício 2026, período 3, esfera M. JSON reserializado após extração; não representa cópia binária da resposta HTTP.

| Anexo | Registros | Chaves compostas distintas | Tipos de valor não numéricos | Git blob SHA-1 |
|---|---:|---:|---:|---|
| 01 | 276 | 276 | 0 | `97a49e8533c50e29a23ede8ca6d1d5f8365c6a88` |
| 02 | 482 | 482 | 0 | `94ecc7e1dfeabc5665ca24cda2bed365c76337df` |
| 03 | 369 | 369 | 0 | `360f773dce6cc42b04db9876034e1b61c88ff879` |
| 07 | 27 | 27 | 0 | `55470d5c5310f9e677bad92808cfdb752b27331e` |

Verificadas as identidades município/exercício/período/anexo antes do salvamento. Chave candidata: município, exercício, período, anexo, rótulo, coluna, código e descrição da conta. Os quatro arquivos foram relidos no GitHub.

**Comparação entre Anexos 01 e 02, despesas exceto intraorçamentárias:** dotação inicial R$ 62.840.000,00; dotação atualizada R$ 64.570.000,00; empenhado até o bimestre R$ 28.962.150,17; liquidado até o bimestre R$ 24.948.746,61. Quatro pares coincidentes, diferença R$ 0,00.

**Limitações:** não houve auditoria contábil integral, validação por fonte externa, normalização em base central, verificação SHA-256 dos bytes de origem nem publicação. As contas do Anexo 02 são hierárquicas e não podem ser somadas indiscriminadamente.
