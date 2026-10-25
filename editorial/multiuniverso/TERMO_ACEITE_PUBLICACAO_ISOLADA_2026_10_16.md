# Termo de aceite da publicação E2 em ambiente isolado

Data: 16 de outubro de 2026.

**Objeto:** dez boletins regionais, 280 fichas municipais e API de referência embarcada, no projeto Cloudflare Pages exclusivo `financas-e2-homologacao`.

## Resultado comprovado
A execução [38940681266](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/38940681266) terminou com conclusão `success`. O verificador `editorial/multiuniverso/qa_http_all_editorial.py` leu o manifesto do pacote homologado, consultou por HTTP o domínio `https://financas-e2-homologacao.pages.dev` e comparou o SHA-256 de cada arquivo remoto com seu correspondente no pacote.

- Boletins HTML: **10/10** aprovados.
- Fichas HTML: **280/280** aprovadas.
- Índice JSON da API: **1/1** aprovado.
- Total: **291/291** respostas HTTP 200 e conteúdo de hash idêntico; **zero divergências**.
- O teste independente de três caminhos (índice JSON, boletim e ficha) também foi aprovado no run `38937391048`.
- Evidência retida: artifact `qa-http-all-editorial-e2`, ID `12062149360`, do run `38940681266`.

## Decisão e limites
**APROVADOS E PUBLICADOS NO AMBIENTE ISOLADO DE HOMOLOGAÇÃO.** Esta expressão não equivale a publicação definitiva no portal estadual, a merge do PR, nem a promoção do projeto RMJ.

Os controles fiscais anteriores aprovam seus recortes especificados na matriz; os testes HTTP cobrem todos os HTMLs e o índice JSON, **não** cada JSON municipal individualmente. A integridade do pacote API/HTML foi verificada antes do deploy. Não transformar o aceite em afirmação de cobertura universal de demonstrativos ou de exercícios não auditados.

A incorporação do XLSX oficial CAPAG ao R2 privado para a auditoria recorrente continua pendente e não invalida a aprovação documental individual já efetuada.

## Proteção dos ambientes atuais
Não alterar `finbra-tic-tim-referencia`, `financas-rmj` nem seu conteúdo sem autorização específica. Manter o PR #198 sem merge automático.

Próximas providências: adicionar página inicial de navegação no ambiente isolado, testar a integridade HTTP de todos os JSONs de referência, completar transferência segura CAPAG e somente depois formular proposta de promoção à produção para decisão expressa.
