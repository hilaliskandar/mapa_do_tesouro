# Mapa do Tesouro

Aplicacao para processamento, auditoria, analise e visualizacao territorial de dados fiscais municipais, com foco inicial no FINBRA/SICONFI.

## Objetivos

- preservar a base bruta e cada etapa do processamento;
- documentar formulas, parametros, fontes e decisoes humanas;
- calcular agregacoes, indicadores reais e per capita;
- produzir mapas, planilhas e relatorios por fase e consolidados;
- permitir substituicao simples da fonte cartografica;
- manter nomes de pastas, scripts, funcoes e variaveis em portugues brasileiro sem acentos.

## Arquitetura inicial

```text
mapa_do_tesouro/
├── aplicacao.py
├── configuracoes/
├── dados/
├── interface/
├── nucleo/
├── processamentos/
├── relatorios/
├── testes/
└── execucoes/
```

## Fluxo previsto

entrada -> validacao -> normalizacao -> classificacao -> agregacoes -> deflacao -> indicadores -> cartografia -> relatorios -> auditoria

## Estado

Primeira versao estrutural em desenvolvimento.