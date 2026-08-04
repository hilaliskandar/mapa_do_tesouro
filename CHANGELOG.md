# Historico de versoes

## Convencao

- `x.1`: grandes etapas funcionais do projeto.
- `x.x.1`: ajustes, aperfeicoamentos e correcoes dentro de uma etapa.
- `x.x.xa`, `x.x.xb`, `x.x.xc`: alternativas experimentais de um mesmo procedimento.

Exemplos:

- `0.1.0`: estrutura inicial do projeto.
- `0.1.1`: primeira correcao da estrutura inicial.
- `0.2.0`: ingestao e validacao funcional da base FINBRA.
- `0.2.1`: aperfeicoamento da validacao.
- `0.2.1a`: alternativa A para uma regra de validacao.

## 0.2.0 - Ingestao e validacao FINBRA

- preservacao do arquivo enviado em `00_entrada`;
- calculo de hash SHA-256 da base FINBRA;
- leitura de todas as abas do arquivo Excel;
- registro de linhas, colunas, celulas vazias e campos identificadores;
- identificacao preliminar de exercicios, municipios e codigos IBGE;
- deteccao de abas vazias, colunas duplicadas e colunas sem nome;
- classificacao de alertas criticos e relevantes;
- geracao de resultado estruturado em JSON;
- geracao de relatorio HTML da validacao;
- atualizacao do manifesto da execucao;
- exibicao dos resultados na interface Streamlit.

## 0.1.1 - Cartografia remota e cache local

- configuracao do GeoJSON remoto do projeto tbrugz/geodata-br;
- credito e procedencia registrados no README e na configuracao;
- obtencao sob demanda com cache local;
- validacao basica da estrutura GeoJSON;
- hash SHA-256 e metadados da obtencao;
- verificacao de campos obrigatorios e codigos municipais duplicados;
- manutencao de adaptador cartografico substituivel;
- interface atualizada para tornar opcional o envio manual da cartografia.

## 0.1.0 - Estrutura inicial

- arquitetura modular em portugues brasileiro sem acentos;
- interface Streamlit inicial;
- registro auditavel de execucoes;
- configuracao externa da fonte cartografica;
- catalogo inicial de indicadores e formulas;
- dependencias e configuracao do projeto;
- regras para preservacao de dados e artefatos locais.
