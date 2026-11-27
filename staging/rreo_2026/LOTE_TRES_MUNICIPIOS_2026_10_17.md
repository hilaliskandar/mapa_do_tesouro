# Lote ampliado RREO 2026 — Americana, Cubatão e Alumínio

Coleta via Crawl2AI da API Siconfi/Tesouro, exercício 2026, bimestre 3, esfera municipal; arquivos JSON reserializados em `staging/rreo_2026/<codigo_ibge>/rreo_2026_b3_anexo_<numero>.json`. Os 12 arquivos foram relidos após gravação no GitHub.

| Município | IBGE | A01 | A02 | A03 | A07 | Total |
|---|---|---:|---:|---:|---:|---:|
| Americana | 3501608 | 493 | 970 | 410 | 54 | 1927 |
| Cubatão | 3513504 | 495 | 939 | 421 | 96 | 1951 |
| Alumínio | 3501152 | 284 | 529 | 354 | 54 | 1221 |

Validação inicial antes de gravar: identificação de IBGE, exercício, período e anexo em todos os registros, sem indicação de paginação pendente. Quatro cotejos de despesa exceto intraorçamentária entre Anexos 01 e 02 em cada município, 12 de 12 pares iguais: dotação inicial, atualizada, empenhado acumulado e liquidado acumulado.

| Município | Inicial R$ | Atualizada R$ | Empenhado acumulado R$ | Liquidado acumulado R$ |
|---|---:|---:|---:|---:|
| Americana | 1517431900,00 | 1618574611,06 | 1113480902,42 | 732838238,10 |
| Cubatão | 2034543375,46 | 2308371521,25 | 1424853391,01 | 882361461,26 |
| Alumínio | 165040379,07 | 173888668,66 | 101067483,68 | 68597303,87 |

**Limites:** dados reserializados do Siconfi via Crawl2AI, não cópias HTTP byte a byte; comparações internas da mesma fonte, sem validação independente externa, sem QA exaustivo de rubricas e sem integração à base canônica. A versão pública do painel e a DCA 2013–2025 não foram alteradas.
