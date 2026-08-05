# Versao 0.5.2 - ampliacao semantica das receitas

## Objetivo

A versao 0.5.2 amplia o catalogo semantico de receitas depois que a execucao 0.5.1 confirmou que a arquitetura estava correta, mas que a cobertura das receitas permanecia restrita aos tributos e transferencias inicialmente priorizados.

## Correcoes

A regra de taxas passou a excluir explicitamente o agregado `Impostos, Taxas e Contribuicoes de Melhoria`. Esse agregado permanece classificado no nivel de origem tributaria e nao pode ser interpretado como receita exclusiva de taxas.

## Novos conceitos

Foram acrescentados conceitos para:

- receitas correntes e de capital;
- receita tributaria;
- contribuicoes;
- receita patrimonial;
- receita agropecuaria;
- receita industrial;
- receita de servicos;
- transferencias correntes;
- outras receitas correntes;
- operacoes de credito;
- alienacao de bens;
- amortizacao de emprestimos;
- transferencias de capital;
- outras receitas de capital;
- Fundeb;
- Sistema Unico de Saude.

## Componentes tributarios

IPTU, ISS e ITBI passam a admitir correspondencias separadas para:

- principal;
- divida ativa;
- multas e juros;
- multas e juros da divida ativa.

Esses componentes nao devem ser somados indiscriminadamente. O uso depende da finalidade do indicador e deve preservar a distincao entre arrecadacao corrente e recuperacao de creditos.

## Estrutura de classificacao

Um mesmo registro pode receber correspondencias em grupos semanticos diferentes, por exemplo:

- origem `REV_TRANSFERENCIAS_CORRENTES`;
- transferencia especifica `REV_TRANSF_ICMS`.

Isso nao representa duplicidade de valor. Representa classificacoes complementares. A etapa posterior de agregacao devera escolher explicitamente o grupo e a finalidade adequados.

## Validacao

Foram incluidos testes para confirmar que:

- o agregado tributario amplo nao e classificado como taxas;
- uma conta especifica de taxas continua sendo reconhecida;
- uma cota-parte do ICMS recebe classificacao de transferencia corrente e de transferencia especifica;
- operacoes de credito sao reconhecidas na origem das receitas de capital.

## Limites

As regras continuam sendo um catalogo inicial. A consolidacao definitiva da serie 2013-2025 depende da incorporacao dos ementarios anuais e da verificacao das mudancas de codificacao por exercicio.