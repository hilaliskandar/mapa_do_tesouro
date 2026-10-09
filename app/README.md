# Aplicação

Frontend static-first e camada opcional de API. O núcleo da interface não deve depender de configuração específica da Cloudflare.


## Contrato documental da interface

A interface não deve duplicar definições em HTML/JavaScript. O build gera:

```text
/data/catalog/variables.json
/data/catalog/variables/{variavel_id}.json
/data/methodology/index.json
/data/methodology/{secao_id}.json
/data/references.json
```

Cartões, tabelas, gráficos e mapas devem oferecer um link contextual para a documentação da variável. A rota humana poderá ser `/indicadores/{id}` ou `/variaveis/{id}`, mas o conteúdo deverá vir deste catálogo estático.


## Contrato de dados static-first

O frontend deve priorizar arquivos estáticos:

```text
/data/metadata.json
/data/municipalities.json
/data/annual/{ano}.json
/data/municipalities/{codigo_ibge}.json
/data/coverage.json
/data/coverage_sources.json
/data/manifest.json
```

Uso previsto:

- mapa e comparação anual: `annual/{ano}.json`;
- séries e perfil municipal: `municipalities/{codigo_ibge}.json`;
- dicionário e metodologia: catálogo documental;
- D1/API: somente para consultas não cobertas pelos artefatos estáticos.

O `manifest.json` registra SHA-256 dos artefatos gerados para controle de cache, paridade e publicação.


## Primeira interface candidata

A implementação inicial em `app/static/` cobre:

- panorama municipal;
- série histórica;
- comparação anual entre municípios;
- mapa temático SVG;
- dicionário navegável;
- metodologia navegável;
- links contextuais “Como ler”.

Não há dependência de framework JavaScript, CDN externa, Worker, D1 ou serviço Cloudflare para essas funções.

### Build local completo

```bash
python -m pipeline.build.build_analytical_database \
  FINBRA_TIC_TIM_30M_BASE_MULTIFONTES_2013_2025_v0_4.xlsx \
  --database data/financas_municipais_sp.sqlite \
  --site-output build/site \
  --geojson caminho/geojs-100-mun.json \
  --overwrite
```

### Visualização local

```bash
cd build/site
python -m http.server 8000
```

Abrir `http://localhost:8000`.

O site deve funcionar integralmente com os arquivos locais gerados.

`coverage.json` representa a cobertura final por variável, ano e universo. `coverage_sources.json` registra a contribuição observacional por fonte; derivados sem `fonte_id` são identificados como `DERIVADO_PIPELINE` e não são atribuídos a fonte oficial.
