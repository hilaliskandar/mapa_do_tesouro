# QA — cartografia estadual SP645

Data: 2026-10-08.

## Fonte pinada

- repositório: `tbrugz/geodata-br`;
- commit: `c39dfb040bfd466fe2a476bafed00749c5c42f16`;
- arquivo: `geojson/geojs-35-mun.json`;
- Git blob SHA: `05d28607a949ee195b4cca2ab59989ca0c3fafb7`.

Essa é a mesma geometria municipal usada pelos workflows e testes estaduais do projeto.

## Validação estrutural

- features: 645;
- códigos municipais únicos: 645;
- códigos inválidos: 0;
- códigos duplicados: 0;
- geometrias nulas: 0;
- tipo geométrico: 645 Polygon.

## Paridade com o universo SP645

A lista ordenada de códigos da geometria foi comparada ao universo de 645 municípios materializado no artifact de teste de escala do próprio repositório.

Assinaturas dos dois conjuntos:

- quantidade: 645;
- primeiro código: `3500105`;
- último código: `3557303`;
- soma numérica dos códigos: `2276010133`;
- FNV-1a 64 bits da lista ordenada: `4f8bce5efa826743`.

As assinaturas são idênticas.

Decisão:

- municípios faltantes na geometria: 0;
- municípios extras na geometria: 0;
- cartografia apta ao universo `SP_645`.

## Regra de uso

O GeoJSON não declara CRS no payload. Portanto:

- pode ser usado como camada cartográfica web e para união por código IBGE;
- não deve substituir uma camada analítica oficialmente documentada em EPSG:4674;
- operações métricas, áreas e distâncias exigem camada territorial com CRS explícito.

## Decisão

A camada cartográfica estadual está aprovada para o build privado do painel SP645.
