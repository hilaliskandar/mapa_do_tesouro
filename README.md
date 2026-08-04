# Mapa do Tesouro

Aplicacao auditavel para processamento, classificacao, analise e visualizacao territorial de financas municipais, com foco inicial no FINBRA/Siconfi.

## Finalidade

O projeto transforma bases fiscais detalhadas em informacao comparavel, reproduzivel e territorializada sem descartar a granularidade original. Cada resultado deve poder ser reconstruido a partir da conta de origem, do exercicio, do estagio contabil, da regra aplicada e da versao metodologica.

A arquitetura foi iniciada para 30 municipios do corredor TIC/TIM, mas foi desenhada para ser reutilizada em outros recortes territoriais, inclusive fora do Estado de Sao Paulo.

## Perguntas que orientam a analise

1. O municipio gera receitas proprias compativeis com sua base economica e territorial?
2. Quanto depende de transferencias constitucionais, finalisticas e extraordinarias?
3. As receitas correntes sustentam as despesas correntes e geram poupanca?
4. Ha espaco para investir sem comprometer pessoal, divida, liquidez e continuidade dos servicos?
5. O orcamento autorizado se converte em despesa liquidada e paga?
6. Os recursos sao direcionados as funcoes associadas as pressoes urbanas, habitacionais, ambientais e de mobilidade?

A aplicacao nao produz, nesta fase, uma nota unica de desempenho. As dimensoes permanecem separadas para evitar compensacoes artificiais entre fragilidades e resultados favoraveis.

## Fluxo do processamento

```text
entrada
-> validacao estrutural
-> normalizacao
-> classificacao contabil
-> hierarquia contabil
-> mapa semantico anual
-> agregacoes auditaveis
-> deflacao
-> indicadores
-> series historicas
-> cartografia
-> analises municipais e regionais
-> relatorios
```

A descricao metodologica ampliada esta em [`docs/arquitetura_analitica.md`](docs/arquitetura_analitica.md).

## Versao 0.4.0

A versao 0.4.0 encerra a primeira fase de preparacao dos dados e inicia a camada analitica com a construcao da hierarquia e do catalogo contabil.

### Validacao estrutural

- preserva o arquivo original em `00_entrada`;
- calcula hash SHA-256;
- reconhece abas, anos, municipios e codigos IBGE;
- verifica campos identificadores e cobertura;
- gera JSON, HTML e registro no manifesto.

### Normalizacao

- converte receitas, despesas e despesa por funcao do formato largo para o formato longo;
- separa populacao das contas financeiras;
- usa o dicionario da base como fonte primaria de metadados;
- preserva rotulos, valores e proveniencia;
- reconcilia registros preenchidos;
- verifica duplicidades, divergencias populacionais e ausencias relevantes.

### Classificacao contabil

- recupera codigos em diferentes formatos;
- distingue contas, totais, subtotais estruturais e agregados funcionais;
- separa receitas e despesas intraorcamentarias;
- identifica deducoes e sua natureza;
- separa funcao e subfuncao;
- produz fila auditavel de revisao;
- considera aprovada a etapa apenas quando nao ha pendencias efetivas.

### Hierarquia e catalogo contabil

A nova etapa `04_hierarquia_contabil` produz:

- `catalogo_contabil.parquet`;
- `catalogo_contabil.xlsx`;
- `relacoes_pai_filho.parquet`;
- `resultado_hierarquia.json`.

O catalogo registra, para cada codigo:

- bloco contabil;
- descricao;
- nivel hierarquico;
- codigo-pai;
- existencia de filhos;
- classificacao calculada como sintetica ou terminal;
- primeira e ultima ocorrencia;
- quantidade de anos e municipios;
- numero de registros;
- valor nominal e absoluto acumulados;
- natureza da operacao;
- funcao e subfuncao, quando aplicaveis.

Essa etapa prepara o controle contra dupla contagem e a futura construcao do mapa semantico anual.

## Estrutura de uma execucao

```text
execucoes/<id_execucao>/
├── 00_entrada/
├── 01_validacao_estrutural/
├── 02_normalizacao/
├── 03_classificacao_contabil/
├── 04_hierarquia_contabil/
├── 05_mapa_semantico/
├── 06_agregacoes/
├── 07_deflacao/
├── 08_indicadores/
├── 09_series_historicas/
├── 10_cartografia/
├── 11_analises_municipais/
├── 12_analise_regional/
├── 13_relatorios/
├── logs/
├── manifest.json
└── README.md
```

## Principios de processamento

- preservar dados brutos e resultados intermediarios;
- nao transformar ausencia em zero;
- nao alterar silenciosamente valores declarados;
- nao somar conta-pai e contas-filhas simultaneamente;
- manter intraorcamentarias separadas na visao consolidada;
- separar principal, multas e juros, divida ativa e acrescimos;
- aplicar deducoes somente as receitas correspondentes;
- nao misturar empenhado, liquidado e pago;
- registrar fonte, edicao, vigencia e versao de cada regra;
- tratar mudancas classificatorias como possiveis quebras de serie;
- usar alertas e niveis de confianca, e nao correcoes automaticas, nos testes de consistencia.

## Fontes normativas, metodologicas e comparadas

A documentacao detalhada permanece em [`docs/referencias_normativas_e_procedimentos.md`](docs/referencias_normativas_e_procedimentos.md). As fontes abaixo contribuíram de formas diferentes para a formulacao do projeto.

### Manual de Contabilidade Aplicada ao Setor Publico - MCASP

**Link:** https://www.gov.br/tesouronacional/pt-br/contabilidade-e-custos/manuais/manual-de-contabilidade-aplicada-ao-setor-publico-mcasp-1

Forneceu a base para distinguir aspectos orcamentario, patrimonial e fiscal; interpretar naturezas de receita e despesa; separar estagios da execucao; tratar intraorcamentarias, restos a pagar e classificacao funcional; e exigir controle temporal entre edicoes.

### Manual de Demonstrativos Fiscais - MDF

**Link:** https://www.gov.br/tesouronacional/pt-br/contabilidade-e-custos/manuais/manual-de-demonstrativos-fiscais-mdf

Ajudou a interpretar RREO e RGF, totais e subtotais, operacoes intraorcamentarias, estagios da despesa e futuras conciliacoes de RCL, pessoal, caixa, divida e limites fiscais.

### Ementario da Classificacao por Natureza da Receita

**Link:** https://www.gov.br/tesouronacional/pt-br/contabilidade-e-custos/federacao/ementario-da-classificacao-por-natureza-de-receita-tabela-de-codigos

Orientou a decomposicao dos codigos de receita, a identificacao de principal, multas, juros e divida ativa, o controle de inclusoes e exclusoes anuais e a necessidade de um mapa semantico versionado por exercicio.

### Portaria Interministerial STN/SOF n. 163/2001

**Link:** https://www.gov.br/planejamento/pt-br/assuntos/orcamento/legislacao-sobre-orcamento

Fundamentou a estrutura das naturezas da receita e da despesa e a consolidacao das contas publicas. Contribuiu para o desenho da hierarquia e para a separacao entre categorias, grupos, modalidades, elementos e desdobramentos.

### Portaria MOG n. 42/1999 e alteracoes

**Link:** https://www.gov.br/planejamento/pt-br/assuntos/orcamento/legislacao-sobre-orcamento

Fundamentou a separacao entre funcao e subfuncao, a leitura das despesas por politica publica e o tratamento de agregados residuais como `FUxx - Demais Subfuncoes`.

### Plano de Contas Aplicado ao Setor Publico - PCASP

**Link:** https://www.gov.br/tesouronacional/pt-br/contabilidade-e-custos/federacao/plano-de-contas-aplicado-ao-setor-publico-pcasp-1

Contribuiu para o desenho das futuras conciliacoes patrimoniais e de caixa, sem confundir conta contabil com natureza orcamentaria.

### Matriz de Saldos Contabeis - MSC

**Link:** https://siconfi.tesouro.gov.br/siconfi/pages/public/conteudo/conteudo.jsf?id=14103

Mostrou como conta contabil, natureza, fonte, funcao e subfuncao se combinam no envio estruturado ao Siconfi. Tambem fundamentou a necessidade de marcar possiveis rupturas na comparabilidade entre 2018 e 2019.

### Indice Firjan de Gestao Fiscal - IFGF

**Link:** https://www.firjan.com.br/ifgf/

Contribuiu com uma referencia multidimensional organizada em autonomia, pessoal, liquidez e investimentos. O projeto aproveita a separacao das dimensoes e parte das formulas, mas nao assume pesos iguais nem transforma o IFGF em unico criterio de avaliacao. Tambem reforcou a necessidade de distinguir autonomia tributaria estrita, receita propria ampliada e capacidade economica local.

### Capacidade de Pagamento - CAPAG

**Link:** https://www.tesourotransparente.gov.br/temas/estados-e-municipios/capacidade-de-pagamento-capag

Contribuiu para separar endividamento, poupanca corrente e liquidez e para reconhecer que medidas oficiais de risco de credito dependem de RGF, RREO e dados patrimoniais. As aproximacoes produzidas apenas com FINBRA devem ser identificadas como proxies.

### Ranking da Qualidade da Informacao Contabil e Fiscal - Siconfi

**Link:** https://ranking-municipios.tesouro.gov.br/

Contribuiu para tratar qualidade da informacao como dimensao propria. O ranking deve servir como sinalizador de confianca e consistencia, nunca como medida direta de saude fiscal.

### IEG-M e Rede Indicon

**Link:** https://irbcontas.org.br/iegm/

Contribuiu para ampliar a compreensao de capacidade municipal para alem do equilibrio contabil, incluindo planejamento, tecnologia, ambiente, protecao dos cidadaos e resultados de politicas. O projeto nao tenta reproduzir o indice apenas com FINBRA.

### Multi Cidades

**Link:** https://multicidadesonline.com.br/

Contribuiu para a comparacao per capita, a leitura por porte municipal e ciclos de governo e a separacao entre origem do financiamento e execucao do investimento. Tambem reforcou a necessidade de verificar o estagio da despesa em cada comparacao.

### PEFA para governos subnacionais

**Link:** https://www.pefa.org/resources/pefa-framework

Contribuiu com a ideia de avaliar confiabilidade do orcamento, previsibilidade, gestao de ativos e passivos, contabilidade, controles e auditoria como dimensoes distintas. Parte desses componentes depende de documentos adicionais ao FINBRA.

### OCDE - descentralizacao fiscal

**Link:** https://www.oecd.org/tax/federalism/

Contribuiu para distinguir participacao orcamentaria, receita diretamente arrecadada e autonomia legal sobre bases, aliquotas e uso dos recursos. O sistema nao deve inferir autonomia legal apenas a partir da composicao da receita.

### BNDES - PMAT

**Link:** https://www.bndes.gov.br/wps/portal/site/home/financiamento/produto/pmat

Contribuiu para compreender capacidade fiscal como resultado tambem de cadastro, fiscalizacao, cobranca, tecnologia, patrimonio, planejamento e controle. Isso orienta futuras combinacoes entre despesas administrativas e evolucao da arrecadacao.

### IBGE - IPCA e populacao

**Links:**

- https://www.ibge.gov.br/estatisticas/economicas/precos-e-custos/9256-indice-nacional-de-precos-ao-consumidor-amplo.html
- https://sidra.ibge.gov.br/

O IBGE fornece os denominadores populacionais e o numero-indice necessario para converter valores nominais em precos constantes. O projeto preservara simultaneamente valores nominais, reais, per capita e relativos.

## Limites interpretativos importantes

- Receita observada nao equivale automaticamente a potencial tributario.
- ITBI e indicador auxiliar da atividade imobiliaria formal, nao medida pura de numero de transacoes ou valorizacao.
- Despesa por funcao mede esforco funcional, nao necessariamente investimento.
- Os anexos separados de funcao e natureza nao permitem inferir diretamente investimento em determinada funcao.
- Grupo 3.1 e proxy de pessoal, nao substituto automatico da Despesa Total com Pessoal da LRF.
- Empenhado menos pago pode aproximar compromissos transferidos, mas nao substitui o estoque oficial de restos a pagar.
- Valores per capita devem ser apresentados junto com valores absolutos e participacoes relativas.

## Cartografia do prototipo

A aplicacao utiliza inicialmente `geojs-100-mun.json`, disponibilizado por [tbrugz/geodata-br](https://github.com/tbrugz/geodata-br).

```text
https://raw.githubusercontent.com/tbrugz/geodata-br/master/geojson/geojs-100-mun.json
```

A fonte cartografica e desacoplada dos modulos fiscais e podera ser substituida por malhas oficiais ou bases estaduais sem alterar o processamento fiscal.

## Execucao local

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

## Estado atual

Versao `0.4.0`: validacao, normalizacao, classificacao sem pendencias, catalogo contabil e construcao inicial das relacoes hierarquicas pai-filho.
