# Arquitetura de documentação e dicionário de dados

## Princípio

Documentação de variável, metodologia e fonte são parte do produto e devem ser versionadas junto com o código e os dados.

O painel v7 já contém uma camada documental madura:

- 25 indicadores com fórmula, fonte, período, como ler, limitações, componentes, regra de ausência e URL;
- 50 contas e agregações com grupo, natureza, fórmula/definição, fonte, leitura e regra de ausência;
- catálogo de fontes;
- quadro de cobertura;
- lista de contas prioritárias;
- regras metodológicas e de leitura.

Essa camada não deve permanecer presa ao XLSX/HTML legado.

## Modelo

### `variavel`

Identidade técnica e semântica da variável.

### `variavel_documentacao`

Conteúdo explicativo destinado ao usuário:

- título público;
- unidade exibida;
- fórmula legível;
- componentes;
- fonte;
- período;
- como ler;
- limitações e cautelas;
- regra de ausência;
- URL da fonte;
- grupo/natureza de apresentação;
- prioridade;
- versão documental.

### `documentacao_secao`

Textos gerais que depois serão expostos na interface:

- metodologia;
- convenções;
- regras de ausência;
- valores monetários;
- comparabilidade temporal;
- crosswalk;
- indicadores legais;
- CAPAG;
- rankings e pares;
- cobertura e QA;
- governança e versões.

### `referencia_documental`

Catálogo de fontes, normas, notas técnicas e referências metodológicas.

## Interface

Cada indicador/conta terá uma rota estável, por exemplo:

```text
/indicadores/investimento_pct_receita_corrente
/indicadores/dtp_pct_rcl
/variaveis/dca_iptu_principal
/metodologia/ausencia
/metodologia/crosswalk
```

Em cartões, tabelas, gráficos e mapas, o rótulo deverá oferecer um link discreto:

```text
Investimentos / receita corrente   ⓘ Como ler
```

O conteúdo do link virá da mesma tabela `variavel_documentacao`, evitando divergência entre documentação e interface.

## Regra de fonte única

A documentação não será copiada manualmente em templates. O frontend consulta um catálogo gerado/versionado. Alterações de fórmula ou interpretação exigem atualização da versão documental e teste de consistência.

## Baseline documental v7

O XLSX v7 é o baseline de migração da documentação. Seu conteúdo será preservado literalmente como referência antes de qualquer revisão editorial.

Após a migração, melhorias textuais deverão ser registradas no changelog; o baseline v7 continuará disponível em `reference/legacy`.
