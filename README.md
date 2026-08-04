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

## Versao 0.3.0

A aplicacao executa duas etapas funcionais:

### Validacao estrutural

1. recebe o arquivo FINBRA pela interface;
2. cria uma execucao auditavel e imutavel;
3. preserva o arquivo original em `00_entrada`;
4. calcula o hash SHA-256;
5. le todas as abas do Excel;
6. identifica anos, municipios, codigos IBGE e tipos de aba;
7. detecta problemas estruturais;
8. grava resultado JSON e relatorio HTML;
9. atualiza o manifesto da execucao.

### Normalizacao

1. converte `Receitas`, `Despesas` e `Despesa por função` do formato largo para o formato longo;
2. padroniza `uf`, `codigo_ibge`, `municipio` e `ano`;
3. preserva o rotulo e o valor originais de cada conta;
4. cria um campo numerico separado;
5. decompoe preliminarmente o rotulo em estagio, codigo e descricao;
6. omite apenas celulas ausentes e registra sua quantidade;
7. preserva as abas auxiliares em arquivos Parquet;
8. gera resultado JSON e relatorio HTML da etapa;
9. registra arquivos, metricas, alertas e status no manifesto.

A normalizacao nao agrega contas, nao corrige valores e nao produz interpretacoes. A classificacao contabil sera realizada em etapa posterior.

## Estrutura de uma execucao

```text
execucoes/<id_execucao>/
├── 00_entrada/
├── 01_validacao_estrutural/
│   ├── resultado_validacao.json
│   └── relatorio_validacao.html
├── 02_normalizacao/
│   ├── receitas_longo.parquet
│   ├── despesas_longo.parquet
│   ├── despesa_por_funcao_longo.parquet
│   ├── auxiliar_cobertura.parquet
│   ├── auxiliar_dicionario.parquet
│   ├── auxiliar_fontes.parquet
│   ├── auxiliar_leia_me.parquet
│   ├── resultado_normalizacao.json
│   └── relatorio_normalizacao.html
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

A normalizacao pode consumir alguns minutos e memoria proporcional ao numero de contas. Os arquivos Parquet resultantes tendem a ser menores e mais adequados para as etapas seguintes.

## Testes

```powershell
pytest
```

## Controle de versoes

- `x.1`: grandes etapas funcionais;
- `x.x.1`: ajustes, aperfeicoamentos e correcoes;
- `x.x.xa`, `x.x.xb`: alternativas de procedimento.

## Estado

Versao `0.3.0`: validacao estrutural e normalizacao auditavel para formato longo, com arquivos Parquet e relatorios JSON/HTML por etapa.
