# Mapa do Tesouro

Aplicacao para processamento, auditoria, analise e visualizacao territorial de dados fiscais municipais, com foco inicial no FINBRA/SICONFI.

## Objetivos

- preservar a base bruta e cada etapa do processamento;
- documentar formulas, parametros, fontes e decisoes humanas;
- calcular agregacoes, indicadores reais e per capita;
- produzir mapas, planilhas e relatorios por fase e consolidados;
- permitir substituicao simples da fonte cartografica;
- manter nomes de pastas, scripts, funcoes e variaveis em portugues brasileiro sem acentos.

## Arquitetura inicial

```text
mapa_do_tesouro/
├── aplicacao.py
├── configuracoes/
├── dados/
├── interface/
├── nucleo/
├── processamentos/
├── relatorios/
├── testes/
└── execucoes/
```

## Fluxo previsto

entrada -> validacao -> normalizacao -> classificacao -> agregacoes -> deflacao -> indicadores -> cartografia -> relatorios -> auditoria

## Cartografia do prototipo

Na fase inicial, a aplicacao utiliza o arquivo `geojs-100-mun.json`, disponibilizado no projeto [tbrugz/geodata-br](https://github.com/tbrugz/geodata-br), como base cartografica leve para testes e visualizacao municipal.

Fonte utilizada pelo sistema:

```text
https://raw.githubusercontent.com/tbrugz/geodata-br/master/geojson/geojs-100-mun.json
```

**Credito:** base cartografica derivada disponibilizada por **tbrugz/geodata-br**. O arquivo e utilizado no prototipo sob as condicoes e informacoes de licenciamento do repositorio de origem.

A aplicacao nao incorpora essa base diretamente ao repositorio. Na primeira utilizacao, o modulo cartografico:

1. baixa o arquivo da fonte configurada;
2. valida a estrutura `FeatureCollection`;
3. grava uma copia em `dados/cartografia/cache/`;
4. calcula o hash SHA-256;
5. registra URL, fonte, credito e data do download;
6. reutiliza o cache nas execucoes seguintes, inclusive sem conexao.

A fonte cartografica e desacoplada dos demais modulos. A futura substituicao por malha oficial do IBGE, GeoPackage, shapefile ou outro provedor exigira apenas nova configuracao e implementacao do respectivo adaptador, sem alterar os calculos fiscais, os indicadores ou os relatorios.

## Configuracao cartografica

A configuracao padrao encontra-se em `configuracoes/configuracao_padrao.yml`:

```yaml
cartografia:
  provedor: geojson_remoto
  url: https://raw.githubusercontent.com/tbrugz/geodata-br/master/geojson/geojs-100-mun.json
  arquivo_cache: dados/cartografia/cache/geojs-100-mun.json
  campo_codigo: id
  campo_nome: name
  sistema_referencia: EPSG:4326
  fonte: tbrugz/geodata-br
  credito: Base cartografica derivada disponibilizada por tbrugz/geodata-br
  uso: prototipo
  permitir_substituicao_fonte: true
```

## Rastreabilidade cartografica

Cada processamento deve registrar:

- provedor e URL utilizados;
- identificacao e credito da fonte;
- caminho do arquivo em cache;
- data e hora da obtencao;
- hash SHA-256;
- quantidade de feicoes;
- campos usados para codigo e nome;
- codigos municipais encontrados e ausentes;
- recorte territorial gerado para o estudo.

## Execucao local

```bash
pip install -e .
streamlit run aplicacao.py
```

A base FINBRA deve ser selecionada pela interface. A cartografia padrao sera obtida automaticamente quando ainda nao existir no cache local.

## Estado

Versao `0.1.1`: estrutura inicial com fonte cartografica remota, cache local, validacao basica e registro de procedencia.
