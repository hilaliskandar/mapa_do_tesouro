# Gate B — complemento seletivo DCA

## Objetivo

Completar lacunas dos snapshots locais sem repetir aquisição estadual integral.

## Princípio

Toda execução externa de complemento deve receber uma lista explícita de códigos IBGE.

O mecanismo:

1. valida cada código contra a geometria paulista;
2. rejeita códigos desconhecidos;
3. limita cada execução a no máximo 100 municípios;
4. consulta somente I-C, I-D e I-E dos códigos solicitados;
5. preserva os artefatos brutos;
6. normaliza somente o delta;
7. registra manifesto, falhas e SHA-256;
8. não altera automaticamente o snapshot local nem o baseline público.

## Workflow

`SICONFI SP 645 DCA Selective Delta`

Inputs:

- `year`;
- `codes`: códigos IBGE de 7 dígitos separados por vírgula, espaço ou ponto e vírgula;
- `min_interval`: intervalo mínimo entre requisições.

## Ordem de prioridade sugerida

Começar pelos exercícios com lacunas pequenas:

- 2022: 1 município no I-C;
- 2018: 2 municípios;
- 2015: 2 municípios;
- 2016: lacunas diferentes por anexo, 2 códigos na interseção;
- 2019: 3 municípios;
- 2013: 7 municípios na interseção.

Depois:

- 2024: 15 municípios;
- 2025 local: 13 municípios, usando o Gate A como referência;
- 2014: 20 municípios na interseção.

## Regra de merge de dados

Snapshot original e delta são artefatos distintos.

A composição anual canônica deve:

1. preservar hash do snapshot original;
2. preservar hash do delta;
3. usar o delta somente para pares município/anexo ausentes ou explicitamente aprovados como revisão;
4. nunca substituir valor local existente sem QA de divergência;
5. registrar a origem final de cada observação na proveniência.

## Segurança operacional

O workflow seletivo é manual e não possui gatilho de push ou pull request.

Uma lista superior a 100 códigos é recusada. Se uma necessidade superar esse limite, deve-se reavaliar se existe fonte local adequada antes de fracionar consultas externas.
