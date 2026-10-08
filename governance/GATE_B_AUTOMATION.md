# Gate B — orquestração automática

## Objetivo

Eliminar o acionamento manual repetitivo dos deltas seletivos DCA.

## Funcionamento

O workflow `Gate B DCA Auto Orchestrator`:

1. lê `data/catalogs/dca_sp_delta_queue.yml`;
2. seleciona o próximo exercício pendente por prioridade;
3. resolve somente os pares município–anexo faltantes;
4. evita nova execução se já houver PR automático aberto para o exercício;
5. consulta somente o delta necessário;
6. registra respostas vazias separadamente de falhas;
7. classifica o resultado;
8. atualiza a fila versionada em branch própria;
9. gera registro de QA em `governance/auto/`;
10. abre PR automático;
11. solicita auto-merge por squash após os checks.

## Frequência

O orquestrador roda:

- por `workflow_dispatch`, quando se quiser execução imediata;
- a cada hora, no minuto 17.

Quando não houver itens pendentes, ele termina sem fazer consultas externas.

## Classificações automáticas

### source_confirmed_absence

Todos os pares solicitados retornaram `items=[]`.

A ação automática:

- retira o exercício da fila;
- preserva a lacuna como ausência;
- registra run, hash e pares consultados;
- não cria valores;
- não repete a mesma consulta automaticamente.

### delta_recovered_pending_merge

Ao menos um par retornou observações.

A ação automática:

- retira o exercício da fila de coleta;
- preserva o artifact;
- registra QA e hash;
- **não** substitui valores do snapshot;
- mantém o resultado pendente de composição fill-only e revisão de conflitos.

## Trava humana

A automação deliberadamente para antes de substituir qualquer valor já observado.

Conflitos entre snapshot local e delta externo continuam exigindo QA explícito. Essa é a única etapa que não deve ser automatizada sem revisão.

## Segurança

- máximo de 100 municípios por execução;
- fila versionada é a fonte de verdade;
- aquisição limitada aos anexos realmente faltantes;
- nenhuma execução estadual integral;
- artifacts retidos por 30 dias;
- toda alteração de fila ocorre via PR;
- PRs automáticos são identificados pelo prefixo `[gate-b-auto]`;
- nenhum valor histórico é sobrescrito pelo orquestrador.
