# Mapa semantico anual

## Finalidade

A hierarquia contabil informa como os codigos se relacionam dentro de cada classificacao. O mapa semantico responde a outra pergunta: quais codigos, em cada exercicio, representam o mesmo conceito analitico ao longo do tempo.

A etapa foi criada para permitir que mudancas de codificacao nao interrompam series historicas de conceitos como IPTU, ISS, ITBI, FPM, ICMS, investimentos, pessoal e funcoes territoriais.

## Fonte das regras

As regras ficam em `referencias/catalogos/mapa_semantico_inicial.yaml`. O arquivo e versionado e pode definir:

- identificador semantico estavel;
- grupo semantico;
- bloco de origem;
- prioridade;
- confianca;
- periodo de vigencia;
- expressao regular do codigo;
- termos obrigatorios, alternativos e proibidos na descricao;
- interpretacao do conceito.

As regras iniciais constituem um nucleo de alta ou media confianca para testar o mecanismo. Elas nao substituem os ementarios anuais, o MCASP, a Portaria STN/SOF n. 163/2001 nem as tabelas anuais do Siconfi.

## Unidade de aplicacao

O mapa e aplicado somente depois da selecao hierarquica sem dupla contagem. A unidade de analise preserva:

- bloco;
- codigo IBGE;
- municipio;
- ano;
- estagio;
- natureza da operacao;
- codigo da conta;
- valor do recorte;
- regra de selecao hierarquica.

## Tratamento das correspondencias

As regras sao avaliadas por grupo semantico. Quando mais de uma regra do mesmo grupo corresponde ao registro, prevalece a maior prioridade. Empates na maior prioridade sao mantidos e classificados como ambiguidade.

Registros sem correspondencia nao sao descartados. Eles permanecem na base com `status_mapeamento = nao_mapeado` e sao reunidos em planilha de pendencias ordenada pelo valor absoluto observado.

## Produtos

A etapa gera:

```text
06_mapa_semantico/
├── mapa_semantico_codigos.parquet
├── mapa_semantico_codigos.xlsx
├── registros_selecionados_semanticos.parquet
├── pendencias_mapa_semantico.xlsx
└── resultado_mapa_semantico.json
```

## Campos centrais

- `id_semantico`: conceito estavel ao longo do tempo;
- `grupo_semantico`: familia analitica;
- `confianca_mapeamento`: alta, media ou outra classificacao definida na regra;
- `prioridade_regra`: criterio de desempate dentro do grupo;
- `status_mapeamento`: mapeado, nao mapeado ou ambiguo;
- `interpretacao`: significado e cautela de uso;
- `ambiguidade`: indica correspondencias concorrentes nao resolvidas.

## Limites atuais

A versao inicial ainda nao cobre todas as contas. Seu objetivo e validar a arquitetura e produzir uma fila auditavel para expansao progressiva do catalogo. Os agregados definitivos somente devem ser calculados depois de:

1. incorporar tabelas e ementarios anuais;
2. revisar os registros nao mapeados de maior impacto;
3. validar equivalencias antes e depois das mudancas de classificacao;
4. separar principal, multas e juros, divida ativa e multas e juros da divida ativa;
5. registrar fonte, vigencia e versao de cada regra.
