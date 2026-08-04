# Mapa semantico anual

## Finalidade

A hierarquia contabil informa como os codigos se relacionam dentro de cada classificacao. O mapa semantico identifica quais codigos, em cada exercicio, representam o mesmo conceito analitico ao longo do tempo.

A partir da versao 0.5.1, o mapa e aplicado a todos os registros qualificados com codigo, antes de qualquer selecao de totalizacao. Essa ordem preserva contas detalhadas como IPTU, ISS, ITBI, FPM e ICMS, mesmo quando uma conta-pai conciliada seja suficiente para representar o total do ramo.

## Fluxo

```text
qualificacao
-> hierarquia
-> mapa semantico dos codigos e registros
-> selecao de totalizacao
-> selecao de decomposicao
-> agregacoes e indicadores
```

## Fonte das regras

As regras ficam em `referencias/catalogos/mapa_semantico_inicial.yaml`. O arquivo pode definir:

- identificador semantico estavel;
- grupo e nivel semanticos;
- finalidade: totalizacao, composicao, indicador ou auditoria;
- bloco de origem;
- prioridade e confianca;
- periodo de vigencia;
- expressao regular do codigo;
- termos obrigatorios, alternativos e proibidos na descricao;
- interpretacao do conceito;
- blocos obrigatorios e limite minimo de cobertura.

As regras iniciais nao substituem ementarios anuais, MCASP, Portaria STN/SOF n. 163/2001 ou tabelas anuais do Siconfi.

## Selecoes por finalidade

A selecao hierarquica gera dois produtos independentes:

- `selecao_totalizacao.parquet`: usa conta-pai conciliada quando possivel e evita dupla contagem;
- `selecao_decomposicao.parquet`: preserva folhas observadas para composicao e indicadores tematicos.

A conciliacao entre pais e filhos e registrada separadamente em `conciliacao_hierarquica.parquet`.

## Produtos do mapa semantico

```text
05_mapa_semantico/
├── mapa_semantico_codigos.parquet
├── mapa_semantico_codigos.xlsx
├── registros_qualificados_semanticos.parquet
├── registros_selecionados_semanticos.parquet
├── pendencias_mapa_semantico.xlsx
└── resultado_mapa_semantico.json
```

O arquivo `registros_selecionados_semanticos.parquet` e mantido apenas como alias de compatibilidade; seu conteudo agora corresponde aos registros qualificados classificados semanticamente.

## Cobertura e status

O resultado informa, por bloco:

- cobertura de registros;
- cobertura de codigos;
- cobertura do valor absoluto;
- conceitos distintos;
- ambiguidades;
- registros e codigos nao mapeados.

O status e reprovado quando um bloco obrigatorio possui cobertura zero. Cobertura parcial ou ambiguidades geram `aprovado_com_alertas`.

## Limites atuais

O catalogo ainda deve ser ampliado com ementarios e tabelas anuais, especialmente para separar principal, multas e juros, divida ativa e deducoes. A correspondencia semantica nao autoriza, por si so, o calculo de agregados definitivos sem validacao de vigencia, estagio, sinal e finalidade.
