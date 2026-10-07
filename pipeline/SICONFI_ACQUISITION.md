# Aquisição direta do SICONFI

A camada de aquisição consulta a API de Dados Abertos do SICONFI sem transformar a semântica dos registros.

Documentação oficial:

- https://www.tesourotransparente.gov.br/consultas/consultas-siconfi/siconfi-api-de-dados-abertos
- https://apidatalake.tesouro.gov.br/docs/siconfi/

Endpoint inicial:

- `GET https://apidatalake.tesouro.gov.br/ords/siconfi/tt/dca`

Parâmetros usados:

- `an_exercicio`
- `id_ente`
- opcionalmente `no_anexo`

## Princípios

1. aquisição e normalização são etapas separadas;
2. o artefato bruto é preservado por município-ano;
3. a paginação segue o link `next` fornecido pela API;
4. a coleta respeita intervalo mínimo de 1,05 segundo entre requisições;
5. a existência de um artefato bruto válido permite retomada sem nova chamada;
6. falhas são registradas no manifesto e não são convertidas em zero;
7. o crosswalk contábil será aplicado apenas na etapa posterior de normalização.

## Uso

```bash
python -m pipeline.acquire.siconfi_dca \
  --geojson build/sp.geojson \
  --years 2024 2025 \
  --output raw/siconfi/dca
```

A coleta estadual completa deve ser executada como processo de aquisição controlado. O smoke test de CI faz apenas uma chamada para verificar o contrato vivo da API.


## Coleta estadual SP 645

A coleta estadual é executada por exercício, separada do deploy do painel.

O orquestrador `pipeline.acquire.siconfi_dca_state` consulta sequencialmente os anexos I-C, I-D e I-E, normaliza os resultados pelo crosswalk DCA canônico e gera hashes SHA-256 para a árvore bruta e para o produto normalizado.

O workflow manual `.github/workflows/siconfi-sp645-year.yml` valida os 645 códigos IBGE paulistas, executa a aquisição oficial e preserva o resultado como artefato de QA. A execução é serial e mantém intervalo mínimo de 1,05 segundo entre requisições.

## Paginação ORDS

Quando uma resposta indica `hasMore=true`, o cliente calcula o próximo `offset` e reconstrói a chamada usando sempre o endereço público oficial. Ele não depende do hostname presente no link `next` devolvido pela infraestrutura ORDS.

## Endpoints

Base pública:

`https://apidatalake.tesouro.gov.br/ords/siconfi/tt`

A camada prevê:

- `/entes` — cadastro de entes;
- `/dca` — Declaração de Contas Anuais;
- `/rreo` — Relatório Resumido da Execução Orçamentária;
- `/rgf` — Relatório de Gestão Fiscal.

A expansão estadual começa pela DCA. RREO e RGF permanecem camadas independentes para preservar anexos, periodicidade e indicadores oficiais.
