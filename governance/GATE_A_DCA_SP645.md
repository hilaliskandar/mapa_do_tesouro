# Gate A — DCA estadual SP 645

## Objetivo

Executar uma aquisição completa de um exercício do DCA diretamente do Siconfi para os 645 municípios paulistas, sem publicar ou alterar o baseline TIC-TIM 30.

## O que o workflow faz

O workflow manual `SICONFI SP 645 Full DCA Gate A`:

1. baixa a geometria estadual pinada;
2. valida 645 códigos municipais;
3. consulta os anexos DCA I-C, I-D e I-E;
4. preserva respostas brutas comprimidas;
5. normaliza uma linha por município;
6. exige 645 linhas normalizadas e 1.935 arquivos brutos;
7. falha se houver requisições não resolvidas;
8. calcula SHA-256 da árvore bruta e do CSV normalizado;
9. gera cobertura por variável;
10. publica artifacts temporários de QA.

## Parâmetros

- `year`: exercício do DCA;
- `min_interval`: intervalo mínimo entre requisições ao Siconfi.

O default inicial é 2025 com 1,05 segundo entre requisições.

## Critério de aceite

O Gate A só é aprovado se:

- a geometria contiver 645 municípios;
- os 645 municípios forem solicitados;
- não houver falhas após retries;
- existirem 1.935 respostas brutas;
- o normalizado tiver 645 códigos únicos;
- hashes forem registrados;
- cobertura por variável for produzida;
- o resultado permanecer isolado do baseline publicado.

## O que o Gate A não faz

- não cria release estadual;
- não publica no Cloudflare Pages;
- não recalcula tipologias;
- não recalcula pares;
- não integra população;
- não integra RREO, RGF ou CAPAG;
- não substitui o snapshot piloto 2020–2023.

## Gate seguinte

Depois de avaliar cobertura, tempo e estabilidade de uma execução completa, a série DCA pode ser expandida exercício a exercício, preservando os mesmos contratos de aquisição, hash e cobertura.
