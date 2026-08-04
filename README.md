# Mapa do Tesouro

Aplicacao para processamento, auditoria, analise e visualizacao territorial de dados fiscais municipais, com foco inicial no FINBRA/SICONFI.

## Objetivos

- preservar a base bruta e cada etapa do processamento;
- documentar formulas, parametros, fontes e decisoes humanas;
- calcular agregacoes, indicadores reais e per capita;
- produzir mapas, planilhas e relatorios por fase e consolidados;
- permitir substituicao simples da fonte cartografica;
- manter nomes de pastas, scripts, funcoes e variaveis em portugues brasileiro sem acentos.

## Fluxo previsto

entrada -> validacao -> normalizacao -> classificacao -> agregacoes -> deflacao -> indicadores -> cartografia -> relatorios -> auditoria

## Versao 0.2.0

A aplicacao ja executa a primeira etapa funcional do processamento:

1. recebe o arquivo FINBRA pela interface;
2. cria uma execucao auditavel e imutavel;
3. preserva o arquivo original em `00_entrada`;
4. calcula o hash SHA-256;
5. le todas as abas do Excel;
6. registra dimensoes, campos identificadores, anos e municipios reconhecidos;
7. detecta abas vazias, colunas duplicadas e colunas sem nome;
8. classifica alertas criticos e relevantes;
9. grava o resultado em JSON;
10. gera relatorio HTML em `01_validacao_estrutural`;
11. atualiza o `manifest.json` da execucao.

Esta etapa nao altera contas nem valores. A classificacao contabil e os calculos serao incorporados nas etapas seguintes.

## Estrutura de uma execucao

```text
execucoes/<id_execucao>/
├── 00_entrada/
├── 01_validacao_estrutural/
│   ├── resultado_validacao.json
│   └── relatorio_validacao.html
├── 02_normalizacao/
├── 03_classificacao_contabil/
├── 04_agregacoes/
├── 05_deflacao/
├── 06_per_capita/
├── 07_indicadores/
├── 08_series_historicas/
├── 09_cartografia/
├── 10_analises_municipais/
├── 11_analise_regional/
├── 12_relatorios/
├── logs/
├── manifest.json
└── README.md
```

## Cartografia do prototipo

Na fase inicial, a aplicacao utiliza o arquivo `geojs-100-mun.json`, disponibilizado no projeto [tbrugz/geodata-br](https://github.com/tbrugz/geodata-br), como base cartografica leve para testes e visualizacao municipal.

Fonte utilizada pelo sistema:

```text
https://raw.githubusercontent.com/tbrugz/geodata-br/master/geojson/geojs-100-mun.json
```

**Credito:** base cartografica derivada disponibilizada por **tbrugz/geodata-br**. O arquivo e utilizado no prototipo sob as condicoes e informacoes de licenciamento do repositorio de origem.

A aplicacao nao incorpora essa base diretamente ao repositorio. Na primeira utilizacao, o modulo cartografico baixa, valida, registra a procedencia e grava uma copia em cache local. A fonte podera ser substituida futuramente sem alterar os modulos fiscais.

## Execucao local

Com o ambiente Conda ativo, na raiz do repositorio:

```powershell
pip install -e .
streamlit run aplicacao.py
```

Para atualizar uma instalacao local:

```powershell
git pull
pip install -e .
streamlit run aplicacao.py
```

A base FINBRA deve ser selecionada pela interface. A cartografia alternativa e opcional.

## Controle de versoes

- `x.1`: grandes etapas funcionais;
- `x.x.1`: ajustes, aperfeicoamentos e correcoes;
- `x.x.xa`, `x.x.xb`: alternativas de procedimento.

## Estado

Versao `0.2.0`: ingestao, preservacao da entrada, validacao estrutural, hash, manifesto e relatorios JSON/HTML.
