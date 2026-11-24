# Finanças Municipais SP v0.4.1 — dimensão cadastral RMRP

**release_universe: SP_645**

**Candidata técnica em 23/11/2026, ainda não publicada no ambiente de produção.**

## Escopo estritamente incremental

A release v0.4.1 parte da v0.4.0 e mantém a base estadual de 645 municípios, 13 universos analíticos, API editorial v1 e API v2, indicadores fiscais e cartografia. Acrescenta apenas:

- consulta territorial de 34 municípios da Região Metropolitana de Ribeirão Preto, organizada em quatro sub-regiões;
- catálogo JSON com códigos IBGE7, nomes e sub-regiões legais, sem campos financeiros;
- JavaScript servido em arquivo próprio, compatível com a CSP estrita `script-src 'self'`;
- ligação à consulta no cabeçalho da página inicial, sem alterar filtros e indicadores fiscais;
- manifesto operacional e testes automatizados de totalizadores regionais, unicidade, CSP, publicação HTTP e navegação com Chromium desktop e mobile.

## Restrições semânticas

Este cadastro **não** comprova que uma obra está fisicamente situada no município, nem configura desembolso, pagamento, liquidação, ou investimento executado. Os datasets SIAFEM/SP, Transferegov, Obrasgov e indicadores de investimento ainda em revisão não entram na release. Ausência permanece distinta de zero.

## Cadeia de testes

- [QA estadual e da API v2 com overlay cadastral](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/45285817646) — sucesso.
- [QA da branch isolada](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/45286673670) — sucesso.
- [Falha de instalação Chromium em Ubuntu 26](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/45293324821) — corrigida pelo pin Ubuntu 24.04.
- [Falha de navegador por CSP](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/45293614540) — corrigida com JS externo.
- Teste final de candidata deve comprovar a navegação a partir da home, 34 municípios, quatro sub-regiões, filtros, responsividade e JSON, além dos gates estaduais/API v2; registrar run aprovado e SHA antes de produzir a tag.

## Política de promoção

Somente considerar a release aprovada após a PR 234 ser mesclada à `main`, testes finais sem falhas e criação de uma **tag/release v0.4.1** vinculada ao commit aprovado. O workflow `pages-sp645-production.yml` exige release formal e entrada explícita `include_rmrp_territory=true`. Revalidar a produção depois do deploy e manter a v0.4.0 disponível para rollback.

A release não pode ser usada para desbloquear dados monetários em revisão.
