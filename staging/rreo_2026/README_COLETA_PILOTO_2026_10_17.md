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

## Auditoria estrutural dos cinco arquivos — 17/10/2026

Arquivos GitHub consultados novamente e decodificados. Chave candidata para unicidade: `(cod_ibge, exercicio, periodo, anexo, rotulo, coluna, cod_conta, conta)`. **Não** usar apenas `cod_conta`: no Anexo 02, ele se repete legitimamente entre funções e subfunções distintas. Contas hierárquicas e respectivos desdobramentos não podem ser somados em conjunto.

| IBGE | Anexo | Registros/contagem declarada | Chaves distintas | Identidades inválidas | Valores não numéricos | Git blob SHA-1 |
|---|---|---:|---:|---:|---:|---|
|3503901|01|293/293|293|0|0|`d367c6d81d9a988e79687a3dd0e119d1b590fdac`|
|3503901|02|419/419|419|0|0|`3e8af1ba3e1274ced5fa36b7caa9eb33f352b1fc`|
|3503901|03|346/346|346|0|0|`7069e7e0c898ecc4d73817449558b4c431e7823f`|
|3503901|07|48/48|48|0|0|`922395c2c671fd1a7f82fc7ebafb1c8a1e7dfe8e`|
|3500758|01|298/298|298|0|0|`5226a0a2c92f7f24892493e3032e8898756b5267`|

Total de 1.404 registros: 1.404 chaves distintas sob chave candidata, sem inconsistência nas identidades de município/exercício/bimestre/anexo nem valores com tipo não numérico; em todos os cinco arquivos `hasMore=false`. Os identificadores acima são **hashes Git blob SHA-1**, não hashes SHA-256 nem fingerprints do tráfego HTTP de origem. Os valores são numéricos, mas **não** passaram por reconciliação contábil substantiva nem auditoria de escala/unidade, saldos, agregados e hierarquias.
