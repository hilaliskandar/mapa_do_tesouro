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

## Versao 0.3.2

A aplicacao executa validacao estrutural e normalizacao semantica auditavel.

### Validacao estrutural

1. recebe o arquivo FINBRA pela interface;
2. cria uma execucao auditavel e imutavel;
3. preserva o arquivo original em `00_entrada`;
4. calcula o hash SHA-256;
5. identifica abas, anos, municipios e codigos IBGE;
6. gera resultado JSON, relatorio HTML e registro no manifesto.

### Normalizacao semantica

1. converte `Receitas`, `Despesas` e `Despesa por função` do formato largo para o formato longo;
2. padroniza `uf`, `codigo_ibge`, `municipio`, `ano` e `populacao`;
3. retira a populacao do universo de contas e gera `dimensao_municipio_ano.parquet`;
4. usa a aba `Dicionário` como fonte primaria de estagio, codigo e descricao;
5. aplica regra de contingencia apenas quando um cabecalho nao consta no dicionario;
6. preserva rotulos e valores originais, alem do valor numerico;
7. reconcilia celulas preenchidas da matriz com registros longos;
8. detecta cabecalhos sem dicionario, codigos ausentes, estagios ausentes e duplicidades;
9. verifica divergencias populacionais entre as matrizes;
10. separa registros contabeis de celulas auxiliares nos relatorios e no manifesto.

A normalizacao nao agrega contas nem altera valores. A classificacao analitica sera executada na etapa seguinte.

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
│   ├── dimensao_municipio_ano.parquet
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

## Criterios de aprovacao da normalizacao

A etapa e reprovada quando ocorrer pelo menos uma destas situacoes:

- perda de registros preenchidos durante a conversao;
- populacao tratada como conta;
- divergencia populacional entre abas para o mesmo municipio e ano;
- ausencia de identificadores obrigatorios;
- duplicidade de observacoes contabeis.

Cabecalhos ausentes do dicionario, codigos ausentes, estagios ausentes e valores nao numericos geram alertas relevantes.

## Cartografia do prototipo

Na fase inicial, a aplicacao utiliza o arquivo `geojs-100-mun.json`, disponibilizado no projeto [tbrugz/geodata-br](https://github.com/tbrugz/geodata-br), como base cartografica leve para testes e visualizacao municipal.

Fonte utilizada pelo sistema:

```text
https://raw.githubusercontent.com/tbrugz/geodata-br/master/geojson/geojs-100-mun.json
```

**Credito:** base cartografica derivada disponibilizada por **tbrugz/geodata-br**. O arquivo e utilizado no prototipo sob as condicoes e informacoes de licenciamento do repositorio de origem.

A fonte cartografica e desacoplada dos modulos fiscais e podera ser substituida futuramente.

## Execucao local

Com o ambiente Conda ativo, na raiz do repositorio:

```powershell
git pull
pip install -e .
pytest
streamlit run aplicacao.py
```

## Controle de versoes

- `x.1`: grandes etapas funcionais;
- `x.x.1`: ajustes, aperfeicoamentos e correcoes;
- `x.x.xa`, `x.x.xb`: alternativas de procedimento.

## Estado

Versao `0.3.2`: normalizacao semantica com dimensao populacional, dicionario contabil, reconciliacao quantitativa e controles de auditoria.
