# Referencias normativas e formulacao dos procedimentos

Este documento consolida as fontes normativas e metodologicas utilizadas na formulacao dos procedimentos do Mapa do Tesouro. O objetivo e tornar explicita a origem de cada regra, permitir auditoria e assegurar que alteracoes temporais sejam aplicadas apenas aos exercicios correspondentes.

## Principio geral

A aplicacao deve distinguir tres planos de informacao:

1. **orcamentario**, referente a previsao e execucao de receitas e despesas;
2. **patrimonial**, referente a ativos, passivos e variacoes patrimoniais;
3. **fiscal**, referente aos indicadores e demonstrativos exigidos pela Lei de Responsabilidade Fiscal.

As regras nao devem ser aplicadas retroativamente sem verificacao. Cada referencia normativa deve registrar, quando possivel:

```text
fonte
ato_normativo
edicao
ano_inicio
ano_fim
pagina_ou_tabela
regra_aplicada
versao_da_regra
```

## 1. Manual de Contabilidade Aplicada ao Setor Publico - MCASP

**Link oficial:** https://www.gov.br/tesouronacional/pt-br/contabilidade-e-custos/manuais/manual-de-contabilidade-aplicada-ao-setor-publico-mcasp-1

**Documento utilizado:** 11a edicao, valida a partir de 2025.

**Descricao:** manual nacional de observancia obrigatoria para Uniao, estados, Distrito Federal e municipios. Reune os procedimentos contabeis orcamentarios, patrimoniais e especificos, o Plano de Contas Aplicado ao Setor Publico e as demonstracoes contabeis aplicadas ao setor publico.

**Contribuicao para os procedimentos:**

- definiu a separacao entre os aspectos orcamentario, patrimonial e fiscal;
- orientou a estrutura da classificacao da receita por natureza;
- orientou a estrutura da despesa por categoria economica, grupo de natureza, modalidade de aplicacao, elemento e desdobramento;
- definiu os estagios da receita e da despesa;
- fundamentou o tratamento de deducoes, transferencias, restos a pagar e operacoes intraorcamentarias;
- fundamentou a separacao entre funcao e subfuncao;
- orientou o tratamento de fontes ou destinacoes de recursos;
- estabeleceu que descentralizacoes financeiras nao devem ser confundidas com receitas ou despesas intraorcamentarias;
- forneceu as regras de integridade e estrutura do PCASP para fases posteriores.

## 2. Manual de Demonstrativos Fiscais - MDF

**Link oficial:** https://www.gov.br/tesouronacional/pt-br/contabilidade-e-custos/manuais/manual-de-demonstrativos-fiscais-mdf

**Descricao:** manual que harmoniza a elaboracao do Anexo de Riscos Fiscais, Anexo de Metas Fiscais, Relatorio Resumido da Execucao Orcamentaria e Relatorio de Gestao Fiscal. A pagina oficial mantem edicoes anteriores, anexos e mapeamentos.

**Contribuicao para os procedimentos:**

- definiu a interpretacao fiscal dos dados contabeis;
- orientou a composicao de receita corrente liquida, resultado primario, despesa com pessoal, divida e disponibilidade de caixa;
- confirmou a necessidade de distinguir despesas empenhadas, liquidadas e pagas;
- fundamentou a classificacao de linhas estruturais de demonstrativos como totais e subtotais;
- orientou a eliminacao de dupla contagem em operacoes intraorcamentarias;
- forneceu referencia para conciliacao futura com RREO e RGF;
- indicou a necessidade de utilizar os mapeamentos de cada edicao para reconciliar contas da MSC com linhas dos demonstrativos.

## 3. Manual de Analise Fiscal de Estados e Municipios 2026

**Link oficial:** https://www.tesourotransparente.gov.br/publicacoes/manual-de-analise-fiscal-de-estados-e-municipios/2026/114?ano_selecionado=2026

**Descricao:** manual operacional da Secretaria do Tesouro Nacional para analise da situacao fiscal de estados, Distrito Federal e municipios, inclusive para avaliacao da capacidade de pagamento e acompanhamento de programas da Uniao.

**Contribuicao para os procedimentos:**

- reforcou que a analise deve observar o MCASP e o MDF vigentes em cada exercicio;
- definiu a necessidade de comparacao entre entes sob criterios uniformes;
- listou fontes de conciliacao, como DCA, RREO, RGF, MSC, balancetes e balancos gerais;
- ofereceu criterios operacionais para receitas correntes, receitas de capital, receitas primarias e receita corrente liquida;
- contribuiu para a definicao de receitas de arrecadacao propria;
- detalhou o tratamento de transferencias constitucionais e deducoes do Fundeb;
- orientou a classificacao de receitas e despesas intraorcamentarias;
- indicou ajustes e conciliacoes necessarios para despesas primarias, pessoal, disponibilidade de caixa, ativos e passivos;
- fundamentou a regra de versionamento temporal dos conceitos e mapeamentos.

## 4. Ementario da Receita Orcamentaria

**Link oficial:** https://www.gov.br/tesouronacional/pt-br/contabilidade-e-custos/federacao/ementario-da-classificacao-por-natureza-de-receita-tabela-de-codigos

**Documento utilizado:** Ementario da Natureza de Receita 2026, associado a Portaria STN/MF n. 1.458, de 4 de julho de 2025, e a Portaria Conjunta STN/SOF n. 2, de 13 de marco de 2026.

**Descricao:** tabela oficial de codigos, especificacoes, descricoes, normas correspondentes, inclusoes, exclusoes e alteracoes da classificacao por natureza da receita aplicavel aos entes da Federacao.

**Contribuicao para os procedimentos:**

- forneceu uma tabela estruturada para validacao automatica dos codigos de receita;
- permitiu decompor categoria economica, origem, especie, detalhamentos e tipo;
- possibilitou associar cada codigo a sua descricao, portaria e norma correspondente;
- permitiu distinguir codigos vigentes, alterados e excluidos;
- fundamentou a criacao do campo `status_codigo_receita`;
- orientou a criacao de tabelas anuais de referencia para evitar aplicacao indevida de codigos de 2026 a toda a serie 2013-2025.

## 5. Portaria Interministerial STN/SOF n. 163/2001

**Pagina oficial de referencia:** https://www.gov.br/planejamento/pt-br/assuntos/orcamento/legislacao-sobre-orcamento

**Descricao:** norma basica da consolidacao das contas publicas e das classificacoes por natureza de receita e despesa, posteriormente atualizada por portarias conjuntas.

**Contribuicao para os procedimentos:**

- forneceu a base normativa das estruturas de natureza da receita e da despesa;
- fundamentou a hierarquia dos codigos utilizada na normalizacao e classificacao;
- orientou a separacao entre categorias sinteticas e contas terminais;
- serviu de referencia para os dicionarios anuais e para validacoes de compatibilidade.

## 6. Portaria MOG n. 42/1999 e alteracoes

**Pagina oficial de referencia:** https://www.gov.br/planejamento/pt-br/assuntos/orcamento/legislacao-sobre-orcamento

**Descricao:** norma que estabelece os conceitos e a classificacao funcional por funcao e subfuncao, alem de programa, projeto, atividade e operacao especial.

**Contribuicao para os procedimentos:**

- fundamentou a separacao entre `codigo_funcao` e `codigo_subfuncao`;
- orientou a validacao dos codigos funcionais;
- impediu que combinacoes atipicas entre funcao e subfuncao fossem classificadas automaticamente como erro;
- fundamentou o tratamento de registros `FUxx - Demais Subfuncoes` como agregados funcionais residuais;
- orientou a construcao de tabela temporal de funcoes e subfuncoes.

## 7. Plano de Contas Aplicado ao Setor Publico - PCASP

**Link oficial:** https://www.gov.br/tesouronacional/pt-br/contabilidade-e-custos/federacao/plano-de-contas-aplicado-ao-setor-publico-pcasp-1

**Descricao:** relacao padronizada de contas e atributos contabeis utilizada para uniformizar registros e permitir a consolidacao nacional das contas publicas.

**Contribuicao para os procedimentos:**

- forneceu referencia para interpretar contas patrimoniais e de controle;
- orientou a futura reconciliacao com ativos, passivos, disponibilidade de caixa e divida;
- fundamentou regras de integridade e consistencia de saldos;
- indicou que a natureza da receita e da despesa nao deve ser confundida com a conta contabil do PCASP.

## 8. Matriz de Saldos Contabeis - MSC e mapeamentos

**Link de referencia:** https://siconfi.tesouro.gov.br/siconfi/pages/public/conteudo/conteudo.jsf?id=14103

**Descricao:** formato estruturado de envio de informacoes contabeis e fiscais ao Siconfi, combinando contas contabeis e informacoes complementares.

**Contribuicao para os procedimentos:**

- orientou o desenho futuro de reconciliacao entre conta contabil, natureza de receita, natureza de despesa, fonte, funcao e subfuncao;
- indicou a necessidade de preservar as informacoes complementares;
- forneceu base para conciliacao automatica com RREO e RGF;
- reforcou a necessidade de manter versoes anuais de leiautes e mapeamentos.

## 9. Base cartografica do prototipo

**Repositorio:** https://github.com/tbrugz/geodata-br

**Arquivo utilizado:** https://raw.githubusercontent.com/tbrugz/geodata-br/master/geojson/geojs-100-mun.json

**Descricao:** GeoJSON leve com limites municipais, utilizado apenas como base cartografica inicial do prototipo.

**Contribuicao para os procedimentos:**

- permitiu testar mapas municipais sem exigir uma infraestrutura geoespacial mais complexa;
- motivou o desacoplamento entre fonte cartografica e modulos fiscais;
- orientou a criacao de um adaptador substituivel para futura incorporacao de malhas oficiais do IBGE.

## Regras consolidadas para o processamento

### Normalizacao

- preservar o arquivo de entrada e calcular hash;
- manter os rotulos originais;
- separar variaveis contextuais, como populacao, das contas contabeis;
- utilizar o dicionario da propria base como primeira fonte de decomposicao;
- utilizar expressoes regulares apenas como contingencia;
- manter ano, municipio e codigo IBGE como chaves estruturais;
- reconciliar o numero de celulas preenchidas com os registros produzidos.

### Classificacao

- distinguir conta terminal, conta sintetica, subtotal, total, indicador auxiliar e registro nao classificado;
- reconhecer codigos de receita com ou sem hifen entre codigo e descricao;
- distinguir natureza da operacao entre orcamentaria e intraorcamentaria;
- reconhecer modalidade de aplicacao 91 como indicio de despesa intraorcamentaria;
- reconhecer categorias economicas 7 e 8 como receitas intraorcamentarias;
- separar funcao e subfuncao;
- tratar `FUxx - Demais Subfuncoes` como agregado funcional residual;
- nao somar simultaneamente contas sinteticas e terminais;
- nao somar indiscriminadamente operacoes intraorcamentarias em totais consolidados.

### Temporalidade

- associar cada regra ao periodo em que estava vigente;
- manter tabelas anuais de receita, despesa, funcao, subfuncao, fonte e mapeamentos;
- nao aplicar automaticamente o ementario de 2026 aos anos anteriores;
- registrar mudancas metodologicas e seus efeitos na comparabilidade;
- apresentar notas metodologicas quando houver ruptura de serie.

### Auditoria

- registrar fonte, versao, pagina ou tabela e regra aplicada;
- preservar resultados intermediarios;
- produzir relatorios por fase;
- manter fila de pendencias para revisao humana;
- distinguir ausencia de codigo justificada de erro de extracao;
- registrar cada ajuste ou reclassificacao sem substituir silenciosamente o valor original.

## Documentos ainda necessarios para completar a serie historica

- edicoes historicas do MCASP aplicaveis a 2013-2024;
- edicoes historicas do MDF e seus mapeamentos;
- ementarios anuais da receita para 2013-2025;
- rois anuais da natureza da despesa;
- tabelas anuais de funcoes e subfuncoes;
- leiautes anuais da DCA e da MSC;
- mapeamentos anuais do RREO e do RGF;
- PCASP e PCASP Estendido por exercicio.

Esses materiais devem ser incorporados como referencias versionadas, e nao como regras atemporais.
