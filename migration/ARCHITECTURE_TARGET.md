# Arquitetura alvo — Finanças Municipais SP

## Objetivo

Separar claramente dados, processamento, apresentação e documentação, mantendo rastreabilidade completa desde a fonte oficial até o indicador apresentado.

## Camadas

### 1. Fontes

DCA/FINBRA, RREO, RGF, CAPAG, IBGE e demais fontes oficiais incorporadas futuramente.

### 2. Pipeline

Etapas lógicas:

```text
ingest
→ validate
→ normalize
→ classify
→ hierarchy
→ harmonize
→ aggregate
→ indicators
→ coverage
→ build
→ QA
→ publish
```

Cada execução deve produzir um manifesto com versões, fontes, hashes e resultado de QA.

### 3. Banco canônico

SQLite em modelo predominantemente longo:

```text
municipios
universos
universo_municipio
variaveis
valores_fiscais
fontes
crosswalk
cobertura
capag
pares_municipais
build_metadata
```

A aplicação não editará o banco. Toda alteração decorre de nova execução do pipeline.

### 4. Publicação static-first

Consultas previsíveis serão materializadas em JSON: panorama, séries, mapas, rankings, indicadores, fontes e cobertura.

### 5. Consulta dinâmica

Cloudflare Worker + D1 apenas quando a combinação solicitada não estiver pré-computada ou quando houver exportação/consulta ad hoc.

### 6. Armazenamento

R2 para snapshots, exportações, GeoJSON e artefatos grandes. Git para código, regras, testes e documentação.

## Governança

Versões independentes:

- `schema_version`
- `data_version`
- `methodology_version`
- `app_version`

Cada build deverá registrar:

- timestamp;
- SHA-256 da base canônica;
- fontes e versões;
- cobertura;
- resultado dos testes;
- status de QA.

## Princípio de não regressão

A matriz de requisitos funcionais será executável por testes. Perder uma função obrigatória deve causar falha de QA em vez de produzir silenciosamente uma nova versão.
