# Arquitetura analitica do Mapa do Tesouro

## Finalidade

O Mapa do Tesouro e uma aplicacao auditavel para transformar dados fiscais municipais detalhados em informacao comparavel, territorializada e reproduzivel. O foco inicial e o FINBRA/Siconfi, mas a arquitetura foi desenhada para receber outros estados, outros conjuntos de municipios e fontes complementares.

O sistema nao pretende atribuir imediatamente uma nota unica aos municipios. O objetivo e preservar dimensoes distintas de capacidade fiscal, autonomia, dependencia, equilibrio corrente, rigidez, investimento, execucao, divida, liquidez, esforco territorial e qualidade dos dados.

## Perguntas analiticas centrais

1. O municipio gera receitas proprias compativeis com sua base economica e territorial?
2. Quanto depende de transferencias constitucionais, finalisticas e extraordinarias?
3. As receitas correntes sustentam as despesas correntes e geram poupanca?
4. Ha espaco para investir sem comprometer pessoal, divida, liquidez e continuidade dos servicos?
5. O orcamento autorizado se converte em despesa liquidada e paga?
6. Os recursos sao direcionados as funcoes associadas a pressoes urbanas, habitacionais, ambientais e de mobilidade?

## Camadas do sistema

```text
00_entrada
01_validacao_estrutural
02_normalizacao
03_classificacao_contabil
04_hierarquia_contabil
05_mapa_semantico
06_agregacoes
07_deflacao
08_indicadores
09_series_historicas
10_cartografia
11_analises_municipais
12_analise_regional
13_relatorios
```

### Base detalhada

Preserva conta, rotulo, estagio, valor, arquivo, municipio, ano e proveniencia. Nenhuma agregacao substitui a declaracao original.

### Normalizacao

Converte as matrizes largas em registros longos, separa dimensoes contextuais, aplica o dicionario de origem e registra inconsistencias.

### Classificacao contabil

Distingue contas, totais, subtotais estruturais, agregados funcionais, deducoes, operacoes intraorcamentarias, funcoes e subfuncoes.

### Hierarquia contabil

Constroi niveis, relacoes pai-filho, contas terminais e sinteticas e um catalogo mestre com ocorrencia temporal, cobertura municipal e valores acumulados. Esta camada serve para impedir soma simultanea entre conta-pai e descendentes.

### Mapa semantico

Associara cada conta valida por exercicio a conceitos analiticos estaveis, permitindo que codigos diferentes ao longo do tempo alimentem a mesma serie conceitual.

### Agregacoes e indicadores

Os agregados serao declarativos e versionados. Cada indicador devera registrar formula, unidade, fonte, periodo de vigencia, regra de inclusao, regra de exclusao, estagio contabil, necessidade de deflacao e denominador populacional.

## Principios de processamento

- preservar os valores nominais e os rotulos originais;
- nao transformar ausencia em zero;
- nao somar conta-pai e contas-filhas simultaneamente;
- manter operacoes intraorcamentarias separadas na visao consolidada;
- separar receita principal, multas e juros, divida ativa e acrescimos da divida ativa;
- aplicar deducoes apenas as receitas correspondentes;
- nao misturar empenhado, liquidado e pago no mesmo indicador;
- tratar testes de consistencia como alertas, nao como correcoes automaticas;
- registrar mudancas de classificacao e quebras de serie;
- manter versoes nominais, reais, per capita e relativas sem apagar a origem.

## Comparabilidade temporal e territorial

Os valores monetarios deverao ser preservados em valores nominais e convertidos para uma data-base comum pelo numero-indice do IPCA. Indicadores monetarios tambem poderao ser publicados por habitante. Razoes entre grandezas do mesmo exercicio nao precisam de deflacao.

A leitura municipal deve combinar:

- historia do proprio municipio;
- municipios de porte e perfil semelhantes;
- mediana e distribuicao regional;
- referencias nacionais;
- alertas de cobertura e qualidade.

## Limitacoes estruturais

Os anexos de despesa por natureza e despesa por funcao nao permitem identificar diretamente a intersecao entre natureza e funcao. Assim, o sistema pode medir investimento total e despesa total em urbanismo, mas nao deve inferir automaticamente investimento em urbanismo sem uma base que contenha ambas as classificacoes.

Da mesma forma, medidas oficiais de despesa total com pessoal, liquidez, disponibilidade de caixa e capacidade de pagamento dependem de RGF, RREO, MSC ou demonstracoes patrimoniais. Quando calculadas somente com FINBRA, devem ser identificadas como aproximacoes.

## Produtos previstos

- catalogo contabil e mapa semantico versionado;
- planilhas nominais, reais, per capita e relativas;
- series historicas com media movel, volatilidade, persistencia e marcadores de quebra;
- fichas municipais anuais e plurianuais;
- analise regional por medianas, distribuicoes e tipologias;
- mapas coropleticos e tematicos;
- relatorios de auditoria, cobertura e confianca;
- modulo especifico para ITBI e dinamica imobiliaria formal.
