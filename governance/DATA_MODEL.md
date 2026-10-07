# Modelo de dados 0.2.0

## Decisão central

O núcleo usa modelo longo. Município, ano e variável formam a chave lógica das observações publicadas.

A estrutura evita colunas específicas para cada indicador e permite ampliar o universo de 30 para 645 municípios sem alterar o esquema.

## Estados de observação

- `observado`: existe valor numérico ou categórico;
- `ausente`: a fonte/recorte deveria permitir observação, mas não há valor utilizável;
- `nao_aplicavel`: a variável não se aplica ao caso;
- `em_revisao`: valor retido do consumo público até conclusão do QA.

Zero é sempre um valor observado. Nunca representa ausência.

## Crosswalk

`crosswalk_variavel` registra, por faixa de exercícios:

- fonte;
- demonstrativo;
- estágio;
- código;
- descrição;
- campo bruto;
- finalidade;
- regra de harmonização;
- prioridade;
- confiança.

A finalidade diferencia `totalizacao`, `decomposicao`, `indicador` e `auditoria`. Essa separação preserva o princípio herdado do mapa semântico: uma conta-pai pode ser adequada para totalização sem substituir folhas necessárias a indicadores temáticos.

## Variáveis

Os tipos aceitos são:

- conta_oficial;
- agregado_analitico;
- indicador_derivado;
- indicador_legal;
- classificacao_oficial;
- contextual.

Isso impede que uma classificação oficial como CAPAG seja confundida com um escore produzido pelo projeto e que indicadores legais sejam substituídos silenciosamente por proxies.

## Versionamento

A tabela `build` registra versões de dados, metodologia, schema e aplicação, além do SHA-256 da base e do resultado de QA.


## Proveniência e linhagem

A versão 0.2.0 adiciona duas estruturas de auditoria:

- `artefato_fonte`: identifica o arquivo ou artefato efetivamente usado em uma carga, com fonte lógica, versão, hash SHA-256, data de obtenção e tipo MIME;
- `observacao_proveniencia`: registra a origem de cada observação, inclusive quando o valor final é ausente ou não aplicável.

A proveniência distingue três tipos:

- `campo_fonte`: observação importada de um campo de um artefato, preservando aba, campo e referência de linha;
- `observacao`: observação derivada de outras variáveis do mesmo ou de outro recorte, com a regra de transformação aplicada;
- `regra`: regra metodológica sem componente observacional direto, reservada para transformações que não possam ser representadas por arestas entre observações.

A linhagem de uma observação derivada é registrada independentemente do seu status. Assim, um agregado `ausente` continua auditável: é possível identificar quais componentes eram esperados e qual regra produziu a ausência.

A tabela `observacao` continua sendo o contrato de valores. Proveniência não altera valor, status ou fonte preferencial; apenas documenta como o registro foi produzido.
