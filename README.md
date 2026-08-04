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

## Versao 0.3.3

A aplicacao executa validacao estrutural, normalizacao semantica auditavel e qualificacao inicial dos codigos contabeis.

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

### Qualificacao de codigos

1. classifica registros como conta terminal, conta sintetica, total ou subtotal, indicador auxiliar ou nao classificado;
2. separa ausencia de codigo justificada de pendencia efetiva;
3. identifica funcao e subfuncao no bloco de despesa por funcao;
4. gera arquivos qualificados sem alterar os Parquet normalizados;
5. cria fila de revisao em formatos Parquet e Excel;
6. registra quantidade de observacoes, anos, municipios e valor absoluto acumulado;
7. ordena as pendencias pelo impacto financeiro estimado;
8. gera relatorios JSON e HTML e registra a etapa no manifesto.

A normalizacao e a qualificacao nao agregam contas nem alteram valores originais.

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
│   ├── receitas_qualificadas.parquet
│   ├── despesas_qualificadas.parquet
│   ├── despesa_por_funcao_qualificada.parquet
│   ├── pendencias_codigos_conta.parquet
│   ├── pendencias_codigos_conta.xlsx
│   ├── resultado_classificacao.json
│   └── relatorio_classificacao.html
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

## Referencias normativas e metodologicas

A formulacao dos procedimentos utiliza fontes oficiais, com controle temporal por exercicio. A documentacao completa esta em [`docs/referencias_normativas_e_procedimentos.md`](docs/referencias_normativas_e_procedimentos.md).

### Manual de Contabilidade Aplicada ao Setor Publico - MCASP

**Link:** https://www.gov.br/tesouronacional/pt-br/contabilidade-e-custos/manuais/manual-de-contabilidade-aplicada-ao-setor-publico-mcasp-1

Manual nacional que disciplina procedimentos orcamentarios, patrimoniais e especificos, PCASP e demonstracoes contabeis. Contribuiu para a separacao entre os aspectos orcamentario, patrimonial e fiscal; para a decomposicao das naturezas de receita e despesa; para os estagios de execucao; e para as regras de operacoes intraorcamentarias, restos a pagar, fontes e classificacao funcional.

### Manual de Demonstrativos Fiscais - MDF

**Link:** https://www.gov.br/tesouronacional/pt-br/contabilidade-e-custos/manuais/manual-de-demonstrativos-fiscais-mdf

Padroniza ARF, AMF, RREO e RGF e seus mapeamentos. Contribuiu para a interpretacao fiscal das contas, a classificacao de totais e subtotais, a separacao dos estagios da despesa, o controle de dupla contagem e o desenho das futuras conciliacoes com RREO e RGF.

### Manual de Analise Fiscal de Estados e Municipios 2026

**Link:** https://www.tesourotransparente.gov.br/publicacoes/manual-de-analise-fiscal-de-estados-e-municipios/2026/114?ano_selecionado=2026

Manual operacional da STN para analise comparavel da situacao fiscal dos entes. Contribuiu para as regras de conciliacao, para a definicao de receitas proprias e primarias, transferencias, Fundeb, intraorcamentarias, despesas, disponibilidade de caixa e versionamento temporal dos conceitos.

### Ementario da Receita Orcamentaria

**Link:** https://www.gov.br/tesouronacional/pt-br/contabilidade-e-custos/federacao/ementario-da-classificacao-por-natureza-de-receita-tabela-de-codigos

Tabela oficial de codigos, especificacoes, descricoes, normas, inclusoes, exclusoes e alteracoes da natureza da receita. Contribuiu para o desenho da validacao automatica dos codigos, sua decomposicao hierarquica, o campo `status_codigo_receita` e a necessidade de manter tabelas anuais.

### Portaria Interministerial STN/SOF n. 163/2001

**Link:** https://www.gov.br/planejamento/pt-br/assuntos/orcamento/legislacao-sobre-orcamento

Base normativa das classificacoes por natureza de receita e despesa e da consolidacao das contas publicas. Contribuiu para a hierarquia dos codigos e para a separacao entre contas sinteticas e terminais.

### Portaria MOG n. 42/1999 e alteracoes

**Link:** https://www.gov.br/planejamento/pt-br/assuntos/orcamento/legislacao-sobre-orcamento

Referencia da classificacao funcional. Contribuiu para a separacao de funcao e subfuncao, a validacao de combinacoes funcionais e o tratamento de `FUxx - Demais Subfuncoes` como agregado funcional residual.

### Plano de Contas Aplicado ao Setor Publico - PCASP

**Link:** https://www.gov.br/tesouronacional/pt-br/contabilidade-e-custos/federacao/plano-de-contas-aplicado-ao-setor-publico-pcasp-1

Relacao padronizada de contas e atributos contabeis. Contribuiu para o desenho das futuras conciliacoes patrimoniais, de disponibilidade de caixa, divida e integridade de saldos, sem confundir conta contabil com natureza da receita ou da despesa.

### Matriz de Saldos Contabeis - MSC

**Link:** https://siconfi.tesouro.gov.br/siconfi/pages/public/conteudo/conteudo.jsf?id=14103

Formato estruturado de envio ao Siconfi. Contribuiu para o desenho da futura reconciliacao entre conta contabil, natureza, fonte, funcao, subfuncao e mapeamentos fiscais.

## Principios consolidados dos procedimentos

- toda regra deve registrar fonte, edicao, periodo de vigencia e versao;
- regras de 2026 nao devem ser aplicadas automaticamente a 2013-2025;
- dados originais e resultados intermediarios devem ser preservados;
- ajustes e reclassificacoes nao podem substituir silenciosamente os valores de origem;
- contas terminais e sinteticas nao devem ser somadas simultaneamente;
- operacoes intraorcamentarias devem ser identificadas para evitar dupla contagem;
- funcao, subfuncao e agregados funcionais residuais devem ser tratados separadamente;
- a aplicacao deve produzir fila de pendencias para revisao humana;
- mudancas metodologicas devem ser registradas e refletidas nas notas de comparabilidade.

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

Versao `0.3.3`: normalizacao semantica, qualificacao de codigos, fila de revisao, reconciliacao quantitativa e controles de auditoria.
