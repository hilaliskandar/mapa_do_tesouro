# QA — prontidão de indicadores SP645 2025

A base multifuentes integrada contém 645 municípios e 64 campos.

Artifact privado no Google Drive:

- file ID: `12XfaN7ati-wGgw_a5puwechp7ipFdWRG`;
- SHA-256: `ffd626cfde3fa1c79d7a552d5b3a8ad2e3509dce5efcc9c62c39eb76c3796566`.

## Cobertura efetiva dos indicadores prioritários

| Indicador | Municípios com todos os insumos | Cobertura |
|---|---:|---:|
| Receita tributária / receita corrente | 644 | 99,84% |
| IPTU por habitante | 643 | 99,69% |
| ITBI por habitante | 641 | 99,38% |
| ISS por habitante | 643 | 99,69% |
| FPM / receita corrente | 643 | 99,69% |
| ICMS / receita corrente | 644 | 99,84% |
| IPVA / receita corrente | 643 | 99,69% |
| Tributos imobiliários / receita tributária | 641 | 99,38% |
| Transferências selecionadas / receita corrente | 643 | 99,69% |
| Investimentos / receita corrente | 644 | 99,84% |
| Investimento por habitante | 644 | 99,84% |
| DTP / RCL oficial | 530 | 82,17% |
| Dívida Consolidada / RCL oficial do RGF02 | 476 | 73,80% |
| Dívida Consolidada Líquida / RCL | 530 | 82,17% |
| Caixa após RPNP / RCL RREO | 528 | 81,86% |
| CAPAG Indicador 1 | 645 | 100,00% |
| CAPAG Indicador 2 | 645 | 100,00% |
| CAPAG Indicador 3 | 645 | 100,00% |

## Indicadores territoriais

Os indicadores baseados no agregado estrito:

`Urbanismo + Habitação + Saneamento + Gestão Ambiental + Transporte`

têm os cinco componentes simultaneamente presentes em apenas 65/645 municípios, ou 10,08%.

Isso é consequência da regra metodológica `strict_complete`. Não se deve preencher funções ausentes com zero apenas para aumentar a cobertura.

## Decisão

Já é possível iniciar o Gate D de cálculo estadual:

- indicadores fiscais derivados do DCA: cobertura praticamente estadual;
- indicadores legais RGF: cobertura parcial e explicitamente documentada;
- CAPAG: cobertura integral;
- indicadores territoriais: calcular apenas nos 65 municípios completos até que exista fonte equivalente e rastreável para as funções ausentes.
