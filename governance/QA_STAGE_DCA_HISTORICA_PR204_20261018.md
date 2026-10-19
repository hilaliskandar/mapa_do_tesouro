# Extensao historica candidata na API v2 — 18/10/2026

O PR 204 foi aprovado por Core CI, SP645 Scale Test e Pages Preview e integrado a main no commit `719595248982031f0e5c04a0b617bf51522b8454`.

Foi preparada e verificada de forma independente uma arvore candidata `data/api/v2/history/dca/` e o catalogo `data/api/v2/catalog/historical_sources.json` a partir do pacote real previamente gerado. Conferidos 645 JSONs municipais, 13 exercicios, 26 variaveis, 218010 celulas, 177221 observadas e 40789 ausentes. A soma por variavel e status corresponde integralmente ao manifesto. O manifesto principal v2 em arvore isolada foi preservado sem alteracoes.

SHA-256 da fonte DCA verificado: `67a94313e0f0557bc23f48c78a1396fd02ae10ad7923ea2ac2e5c9f2726f65d5`. A validacao foi feita com script independente sobre os JSONs existentes. A funcao `stage()` integrada a main nao foi literalmente executada sobre o pacote real nesta etapa. Nao houve deploy nem mudanca na API publica. O catalogo historico permanece explicitamente candidato e nao autorizado para publicacao.

Pendencias: execucao literal de `stage()` sobre o pacote real, verificacao do caminho de implantacao opt-in, testes de compatibilidade temporal e contabilidade entre API v2 atual e historia DCA 2021-2025, qualificacao editorial do catalogo e gate de publicacao.
