# Piloto estadual SP 645 — receitas 2020-2023

## Finalidade

Este piloto testa a escala de ingestao para os 645 municipios paulistas sem alterar o baseline TIC-TIM 30 nem antecipar equivalencias semanticas ainda nao auditadas.

## Fonte

O artefato estadual existente contem 2.580 combinacoes municipio-ano, cobrindo 645 municipios e os exercicios 2020, 2021, 2022 e 2023.

O arquivo possui receitas, despesas e outros campos. Nesta etapa entram apenas cinco campos de receita preservados com IDs proprios:

- receitas correntes;
- receita tributaria total;
- IPTU;
- ITBI;
- ISS.

## Exclusoes deliberadas

Nao entram neste piloto:

- despesas empenhadas reconstruidas;
- investimentos derivados desse mesmo criterio;
- populacao_2024;
- indicadores per capita;
- equivalencias com as variaveis DCA harmonizadas do baseline.

A razao e metodologica: o dicionario do artefato nao permite afirmar que esses campos sejam intercambiaveis com as series liquidadas e harmonizadas do painel principal.

## Infraestrutura

O rebuild manual usa fonte privada armazenada em R2. O workflow recebe apenas referencias por GitHub Actions Variables:

- CLOUDFLARE_R2_CANONICAL_BUCKET;
- SP645_PILOT_SOURCE_OBJECT;
- SP645_PILOT_SOURCE_SHA256.

O token Cloudflare permanece em Secret e nao e versionado.

## Contrato de QA

Uma execucao valida deve produzir:

- 645 municipios;
- 4 exercicios;
- 2.580 linhas municipio-ano;
- 5 variaveis;
- 12.900 observacoes;
- universo SP_645_RECEITAS_PILOTO.

Este piloto e uma prova de escala de ingestao. A primeira base estadual analitica plena continua condicionada a uma base multifuentes estadual 2013-2025 semanticamente conciliada.
