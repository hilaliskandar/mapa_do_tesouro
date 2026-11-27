# Mapa do Tesouro — frentes e integração

**Referência:** 27/11/2026  
**Escopo:** exclusivamente o repositório `hilaliskandar/mapa_do_tesouro`.  
**Branch de integração:** `integration/mapa-tesouro-unificado-20261127`.  
**Situação:** integração em revisão; não mesclada à `main` e não publicada.

## Fonte canônica e regras de leitura

- A última base de produção documentada é a release `v0.6.0`, publicada e homologada em 25/11/2026. O README registra o run 45594094214 e o artefato 15012300428.
- `VERSION` é a versão da release do site e é validada pelo workflow de Pages. A versão em `pyproject.toml` identifica o pacote Python; elas têm funções diferentes e não devem ser comparadas como se fossem um único campo.
- A `main` e a linha de produção têm históricos diferentes. Esta branch parte da linha de produção mais recente e consolida os avanços selecionados da `main` e das frentes federais em um commit de integração; ela preserva o conteúdo integrado, não a cadeia completa de commits da `main`.
- `README.md`, `governance/PROJECT_STATE.md` e `governance/PENDING_TASKS.md` continham anotações de épocas distintas. Este documento passa a ser o quadro operacional atual; os registros anteriores ficam como histórico, não como fila vigente.

## O que foi reunido

| Frente | Avanços incorporados | Limite atual |
|---|---|---|
| Plataforma estadual | Linha da `v0.6.0`, atualização de recortes, calendários e ledger de refresh; gates de conservação regional e QA de release. | A branch unificada ainda precisa passar pelos workflows de CI e de prévia. |
| Catálogo territorial RMRP | Catálogo cadastral de 34 municípios e QA de navegador; script separado para respeitar a CSP. | É uma dimensão territorial. Não comprova valores nem execução de investimentos. |
| Transferegov estadual | Coletor/staging auditado, exportador agregado e interface por município proponente, exercício e etapa. Snapshot de entrada fixado por SHA-256. | O deploy da consulta ainda não ocorreu. A saída pública prevista não contém linhas de transação, identificadores de convênio ou favorecidos. |
| APIs federais reutilizáveis | Cliente GET limitado, staging imutável por hash/manifesto, modo amostral opt-in, classificação territorial por código IBGE e leitura canônica somente leitura. | As evidências G2/G3 são amostrais; não demonstram cobertura estadual completa nem conciliação financeira. |
| Segurança editorial | O carregador preserva `publicavel`/`ativo`, rejeita tipos inválidos e a API editorial falha de forma fechada para variáveis bloqueadas; regressões correspondentes adicionadas. | O conjunto FED04 completo ainda não foi mesclado. Foram portados os controles transversais pertinentes, não as investigações de fontes que não pertencem a esta publicação. |

## Estado dos dados e das consultas

### Transferegov — agregado estadual

- O snapshot de staging usado pelo exportador é o artefato `run_46006854691`, SHA-256 `d7c0d8758fca9434e5c348e8f2be8905d443b1737ecc31b6aaffa33ddeaf77cc`.
- A auditoria agregada `run_46015207806` registrou 47.392 eventos de desembolso em 645 municípios e 945.970 eventos de pagamento em 644 municípios. Existem cinco eventos negativos e 2.194 eventos de valor zero; a auditoria não classificou os negativos como estornos comprovados.
- A cobertura distingue ausência de pagamento de valor zero. Desembolso e pagamento são etapas diferentes e não devem ser somados como se fossem o mesmo fluxo.
- A autorização vigente é para publicar apenas o agregado estadual por município proponente, ano e etapa, sem registros individuais. A autorização não transforma os demais staging financeiros em dados homologados.

### SIAFEM e investimentos RMRP

- O registro mais recente da trilha estadual fora da RMRP indica 611 municípios consultados, 520 reconciliados e 91 inconclusivos. Os valores encontrados ainda não foram homologados como execução municipal.
- A PR #233 também reúne propostas, planos, empenhos, documentos hábeis, OP/OB, lançamentos de gestão e candidatos ObrasGov. Há lacunas de vínculo entre lançamento financeiro e plano/OB, além de triagem geográfica pendente.
- Esses dados continuam em staging, QA ou prévia. Não entram no build de produção apenas por estarem no branch de integração.

### ObrasGov e atualização recorrente

- O censo estadual completo e a validação sistemática de localização continuam pendentes. Candidatos encontrados por texto não são equivalentes a obras confirmadas no território.
- O calendário de refresh e o ledger estão implementados em modo controlado; o README indica que os agendamentos de produção seguem desabilitados.

## PRs e branches paralelos

| Referência | Decisão nesta integração |
|---|---|
| [PR #234](https://github.com/hilaliskandar/mapa_do_tesouro/pull/234) | Fechada e incorporada à linha da `main`; seus controles cadastrais e de navegador foram reunidos. |
| [PR #233](https://github.com/hilaliskandar/mapa_do_tesouro/pull/233) | Continua draft. Sua linha de trabalho forma a base operacional estadual desta branch, mas não é promovida inteira à produção. Dados sem homologação permanecem em staging. |
| [PR #232](https://github.com/hilaliskandar/mapa_do_tesouro/pull/232) | Continua draft. Os patches de segurança de catálogo/API e as regressões associadas foram portados seletivamente; os demais gates de fonte continuam separados. |
| [PR #213](https://github.com/hilaliskandar/mapa_do_tesouro/pull/213) | Continua draft. O cliente federal reutilizável, staging e normalização territorial foram portados; a evidência original foi amostral e não equivale a homologação SP645. |
| [PR #212](https://github.com/hilaliskandar/mapa_do_tesouro/pull/212) | Plano documental sobreposto. A arquitetura e os gates passam a ser mantidos neste quadro; não se importa outro README concorrente. |
| Branches `release/v0.6.1-transferegov-sp645` e `release/transferegov-sp645-v0.7.0` | As duas candidatas foram consolidadas: preserva-se a consulta visual da primeira e o versionamento/QA da segunda, adotando `VERSION=0.7.0`. |

## Sequência para concluir a integração

1. Conferir o diff da branch unificada e remover duplicações documentais sem apagar evidências rastreáveis.
2. Executar os gates CI existentes e a prévia isolada; verificar agregados, cobertura municipal, interface, CSP, API editorial e regressões do painel.
3. Confirmar que a publicação de produção contém somente o agregado autorizado do Transferegov e os elementos territoriais já aprovados.
4. Abrir/atualizar uma PR de integração com escopo claro. A `main` e a produção permanecem intactas até revisão e conclusão do QA.
5. Após merge, usar as condições em [`RELEASE_NOTES_V0_7_0.md`](RELEASE_NOTES_V0_7_0.md), criar a release `v0.7.0` e executar `pages-sp645-production`; só então atualizar este quadro com o run, artefato, SHA e QA remoto.

## Critério para novas tarefas

Cada avanço entra nesta trilha somente quando registra: fonte e SHA; transformação; grão territorial e temporal; cobertura; QA; status (`produção`, `prévia`, `staging` ou `pendente`); branch/PR responsável; e próximo gate. Uma nova tarefa deve ser vinculada a uma dessas frentes antes de alterar workflows, dados ou publicação.
