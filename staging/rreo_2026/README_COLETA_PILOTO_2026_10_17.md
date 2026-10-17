# Piloto de preservação do RREO 2026 — 17/10/2026

Fonte: API Siconfi/Tesouro Nacional, endpoint `https://apidatalake.tesouro.gov.br/ords/siconfi/tt/rreo`.
Extração via Crawl2AI, parâmetro exercício=2026, bimestre=3, esfera=M. A resposta estruturada JSON foi recuperada do Markdown do crawler e serializada novamente como JSON compacto; **não há garantia de identidade byte a byte com a resposta HTTP original**. Nunca chamar estes arquivos de dumps HTTP originais.

| IBGE | Município | Anexo | Registros | Caminho |
|---|---|---|---:|---|
|3503901|Arujá|01|293|`staging/rreo_2026/3503901/rreo_2026_b3_anexo_01.json`|
|3503901|Arujá|02|419|`staging/rreo_2026/3503901/rreo_2026_b3_anexo_02.json`|
|3503901|Arujá|03|346|`staging/rreo_2026/3503901/rreo_2026_b3_anexo_03.json`|
|3503901|Arujá|07|48|`staging/rreo_2026/3503901/rreo_2026_b3_anexo_07.json`|
|3500758|Alambari|01|298|`staging/rreo_2026/3500758/rreo_2026_b3_anexo_01.json`|

**Verificação realizada:** objetos JSON decodificados; o código IBGE, exercício, período e identificação do anexo foram cotejados em todos os registros; todos correspondentes. Total: 1.404 registros em cinco conjuntos. `hasMore` foi informado como falso nos resultados coletados anteriormente. Não foi feita auditoria independente de valores e contas nem reconciliação de agregados. Como os dados vêm de fonte dinâmica, preservar data da consulta e parâmetros e registrar digest de bytes da versão serializada ao realizar ingestão.

**Situação editorial:** staging exclusivo da ramificação E2, não homologado para publicação; não altera DCA 2013-2025 nem versão pública do painel. Não substituir outros arquivos historicamente aprovados.
