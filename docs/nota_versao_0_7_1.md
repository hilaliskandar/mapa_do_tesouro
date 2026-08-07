# Versao 0.7.1

A versao 0.7.1 trata dois problemas identificados na execucao real da 0.7.0.

## Universo aplicavel dos indicadores

O motor de indicadores passa a respeitar filtros declarados no catalogo YAML para `estagios_validos`, `naturezas_validas` e, quando necessario, `anos_validos`.

A cobertura deixa de usar todos os recortes contabeis da base como denominador. Ela passa a ser calculada apenas entre as observacoes em que a formula e aplicavel.

Para receitas, os indicadores iniciais aceitam `Receitas Realizadas` e `Receitas Brutas Realizadas`, sempre com `natureza_operacao = orcamentaria`. Deducoes e operacoes intraorcamentarias deixam de compor o universo dos indicadores principais.

Para despesas, os indicadores iniciais aceitam despesas empenhadas, liquidadas e pagas, preservando o estagio na chave analitica. Inscricoes de restos a pagar deixam de integrar o universo principal desses indicadores.

Ausencia de componente continua sendo tratada como dado insuficiente, nunca como zero automatico.

## Reconciliacao dos alertas da normalizacao

A normalizacao permanece conservadora e continua registrando os alertas observados antes da qualificacao. Esses alertas nao sao apagados.

Foi criada uma etapa de reconciliacao posterior. Ela verifica se alertas de cabecalhos fora do dicionario e registros sem codigo foram resolvidos ou justificados pela etapa de qualificacao.

Na base de referencia, os cinco alertas da normalizacao decorriam de 36 cabecalhos fora do dicionario e 15.233 registros inicialmente sem codigo. Como a qualificacao terminou com zero registros e zero cabecalhos pendentes, esses alertas passam a ser registrados como resolvidos no resultado reconciliado.

O produto `resultado_normalizacao_reconciliada.json` preserva o status inicial, o status final, a quantidade de alertas resolvidos e pendentes e a justificativa individual de cada reconciliacao.
