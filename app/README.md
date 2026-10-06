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
/data/manifest.json
```

Uso previsto:

- mapa e comparação anual: `annual/{ano}.json`;
- séries e perfil municipal: `municipalities/{codigo_ibge}.json`;
- dicionário e metodologia: catálogo documental;
- D1/API: somente para consultas não cobertas pelos artefatos estáticos.

O `manifest.json` registra SHA-256 dos artefatos gerados para controle de cache, paridade e publicação.
