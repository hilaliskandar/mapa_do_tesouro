# Historico de versoes

## Convencao

- `x.1`: grandes etapas funcionais do projeto.
- `x.x.1`: ajustes, aperfeicoamentos e correcoes dentro de uma etapa.
- `x.x.xa`, `x.x.xb`, `x.x.xc`: alternativas experimentais de um mesmo procedimento.

## 0.4.1 - Correcao da hierarquia contabil

- substituicao da regra generica de remocao do ultimo segmento por regras especificas para cada bloco;
- hierarquia posicional da receita com preenchimento progressivo por zeros e preservacao das larguras historicas;
- hierarquia da despesa por natureza baseada em prefixos conceituais de categoria, grupo, modalidade, elemento e desdobramento;
- manutencao da estrutura funcao e funcao-subfuncao no bloco funcional;
- geracao de nos conceituais quando os niveis intermediarios nao aparecem como registros declarados;
- separacao entre codigos observados e nos conceituais gerados;
- criacao dos campos `origem_no`, `codigo_observado`, `regra_hierarquia` e `utilizavel_em_agregacao`;
- substituicao dos totais acumulados ambiguos por `soma_nominal_registros_observados` e `soma_absoluta_para_auditoria`;
- ampliacao do manifesto e da interface com quantidades de codigos observados e nos conceituais;
- ampliacao dos testes para IPTU, despesa por natureza e classificacao funcional.

## 0.4.0 - Hierarquia e catalogo contabil

- encerramento da fase inicial de preparacao e qualificacao dos dados;
- criacao de `processamentos/construir_hierarquia_contabil.py`;
- construcao automatica de niveis hierarquicos e codigos-pai;
- identificacao calculada de contas sinteticas e terminais a partir da existencia de descendentes;
- geracao de `catalogo_contabil.parquet` e `catalogo_contabil.xlsx`;
- geracao de `relacoes_pai_filho.parquet`;
- registro de primeira e ultima ocorrencia, anos, municipios, frequencia e valores acumulados;
- integracao da nova etapa ao manifesto e a interface Streamlit;
- criacao de teste automatizado da hierarquia;
- ampliacao do README com finalidade, perguntas analiticas, limitacoes e fontes metodologicas;
- criacao de `docs/arquitetura_analitica.md`.

## 0.3.5 - Encerramento da qualificacao

- normalizacao textual de hifens, parenteses, espacos e caracteres corrompidos;
- reconhecimento de subtotais intraorcamentarios e exceto intraorcamentarios;
- recuperacao de codigos em rotulos malformados;
- classificacao detalhada de deducoes;
- eliminacao das pendencias efetivas na base de referencia.

## 0.3.4 - Qualificacao normativa inicial

- extracao de codigos de receita e despesa com ou sem hifen, travessao ou dois-pontos;
- reconhecimento de codigos funcionais `NN.NNN` e agregados residuais `FUxx`;
- classificacao de `Demais Subfuncoes` como agregado funcional residual com ausencia de codigo justificada;
- identificacao de operacoes intraorcamentarias pelas categorias 7 e 8 da receita, modalidade 91 da despesa e rotulos explicitos;
- identificacao preliminar de deducoes, restituicoes, retificacoes e registros associados ao Fundeb;
- ampliacao da taxonomia de totais e subtotais para registros intraorcamentarios e exceto intraorcamentarios;
- separacao entre registros com funcao, registros com subfuncao, funcoes distintas e subfuncoes distintas;
- motivos de pendencia mais precisos;
- ampliacao do relatorio HTML, da interface e da planilha de resumo;
- testes automatizados para codigos sem separador, modalidade 91, categorias 7 e 8 e agregados `FUxx`.

## 0.3.3 - Qualificacao de codigos e fila de revisao

- classificacao dos registros como conta terminal, conta sintetica, total ou subtotal, indicador auxiliar ou nao classificado;
- separacao entre ausencia de codigo justificada e pendencia efetiva de revisao;
- tratamento especifico de funcao e subfuncao no bloco de despesa por funcao;
- geracao de arquivos qualificados sem alterar os Parquet normalizados;
- criacao de `pendencias_codigos_conta.parquet` e `pendencias_codigos_conta.xlsx`;
- agrupamento das pendencias por cabecalho, estagio, descricao, origem e motivo;
- registro de quantidade de observacoes, anos, municipios e valor absoluto acumulado;
- ordenacao da fila de revisao pelo impacto financeiro estimado;
- relatorio JSON e HTML da qualificacao;
- integracao da etapa ao manifesto e a interface Streamlit;
- teste automatizado para totais, pendencias, funcao e subfuncao.

## 0.3.2 - Correcao semantica da normalizacao

- reconhecimento de `População` como variavel contextual, sem conversao em conta financeira;
- criacao de `dimensao_municipio_ano.parquet`;
- verificacao de consistencia populacional entre as tres matrizes contabeis;
- uso da aba `Dicionário` como fonte primaria de estagio, codigo e descricao da conta;
- regra de contingencia para cabecalhos ausentes do dicionario;
- separacao correta de cabecalhos no formato `Estagio | codigo - descricao`;
- reconciliacao entre celulas preenchidas na matriz e registros contabeis longos;
- controles de cabecalhos sem dicionario, registros sem codigo, registros sem estagio e duplicidades;
- separacao entre registros contabeis e celulas auxiliares nos relatorios e no manifesto;
- criterios de aprovacao semantica mais restritivos;
- ampliacao dos testes automatizados.

## 0.3.1 - Correcao da validacao cartografica

- validacao de `FeatureCollection` antes da leitura pelo GeoPandas;
- mensagem de erro deterministica para GeoJSON estruturalmente invalido.

## 0.3.0 - Normalizacao auditavel da base FINBRA

- conversao das abas `Receitas`, `Despesas` e `Despesa por função` do formato largo para o formato longo;
- padronizacao dos identificadores `uf`, `codigo_ibge`, `municipio` e `ano`;
- preservacao dos rotulos contabeis e valores originais;
- criacao de campo numerico separado, sem substituir a informacao de origem;
- decomposicao preliminar dos rotulos em estagio, codigo e descricao da conta;
- omissao somente de celulas ausentes, com contabilizacao explicita no relatorio;
- preservacao das abas auxiliares em arquivos Parquet separados;
- geracao de resultado JSON e relatorio HTML da normalizacao;
- registro da etapa no manifesto da execucao;
- exibicao das metricas da normalizacao na interface;
- teste automatizado inicial de preservacao de identificadores e valores.

## 0.2.1 - Aperfeicoamento da validacao estrutural

- normalizacao de acentos nos cabecalhos antes da identificacao de campos;
- reconhecimento de `Município`, `Código IBGE` e variantes equivalentes;
- classificacao das abas entre dados, auxiliares e desconhecidas;
- supressao de alertas indevidos em abas documentais e de dicionario;
- extracao de anos somente a partir de colunas explicitas `Ano` ou `Exercicio`;
- eliminacao do falso reconhecimento de 2012 em rotulos de contas;
- consolidacao de cobertura apenas a partir das abas de dados;
- exibicao de municipios, codigos IBGE e tipo de aba na interface.

## 0.2.0 - Ingestao e validacao funcional da base FINBRA

- preservacao do arquivo FINBRA no diretorio da execucao;
- calculo do hash SHA-256 e registro do tamanho do arquivo;
- leitura de todas as abas do Excel;
- levantamento de linhas, colunas, vazios e duplicidades;
- identificacao preliminar de anos, municipios e codigos IBGE;
- geracao de resultado estruturado em JSON;
- geracao de relatorio HTML da validacao;
- atualizacao do manifesto da execucao;
- resumo da validacao exibido na interface Streamlit.

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
