# Projeto — Integração de transferências e investimentos federais no Mapa do Tesouro

**Data de abertura:** 03/11/2026  
**Status:** G0 documentado; G1 inspeção inicial realizada; G2 cliente e testes unitários aprovados no CI anterior; smoke HTTP real criado, execução pendente de confirmação  
**Escopo territorial:** 645 municípios do Estado de São Paulo, com identificador IBGE de sete dígitos  
**Branch:** `feat/integracao-transferencias-federais-pac-20261103`

## Objetivo e problema

Ampliar o portal Finanças Municipais SP / Mapa do Tesouro para acompanhar (i) transferências federais destinadas a entes e entidades municipais e (ii) investimentos federais localizados no território municipal, preservando a distinção entre receita efetivamente recebida, empenho, transferência financeira, investimento e execução física. Integrar exclusivamente dados públicos e operações de consulta, inicialmente em ambiente isolado e **sem alterar DCA/FINBRA, TCESP, API publicada ou a rotina de produção**.

O programa Novo PAC constitui uma **dimensão de classificação a comprovar por fonte oficial**, não uma propriedade inferível do nome do projeto ou do município. O MCMV também não equivale automaticamente à carteira do PAC.

## Inventário preliminar de fontes

| Fonte oficial / URL | Objeto da consulta | Estado da evidência | Prioridade |
|---|---|---|---|
| [Transferegov — Gestão de Parcerias](https://api-publica.transferegov.gestao.gov.br/parcerias/openapi.json) | Programa, proposta, parceria, empenho, ordem de pagamento, situação | OpenAPI 3.1 e GETs públicos já testados em investigação do projeto radar | P0 |
| [Transferegov — Transferências Especiais](https://api-publica.transferegov.gestao.gov.br/especiais/openapi.json) | Beneficiário, plano de ação, empenho, ordem bancária e gestão financeira | OpenAPI 3.1 e data de atualização testados; pagamentos ainda não validados nesta integração | P0 |
| [Obrasgov — API pública](https://api-publica.obrasgov.gestao.gov.br/obras/openapi.json) | Projeto, empenho, execução física, contrato, geometria | OpenAPI e GETs públicos testados; chaves internas projeto→empenhos/execução confirmadas em amostras | P0 |
| [Casa Civil — transparência Novo PAC](https://www.gov.br/casacivil/pt-br/novopac/transparencia) | Carteira declarada do programa e investimentos | Página oficial identificada; planilhas binárias ainda não inspecionadas | P1 |
| [MCID — dados MCMV](https://www.gov.br/cidades/pt-br/acesso-a-informacao/acoes-e-programas/habitacao/programa-minha-casa-minha-vida/bases-de-dados-do-programa-minha-casa-minha-vida) | Empreendimentos subsidiados/financiados e dicionários | Arquivos ZIP/CSV identificados, esquema não inspecionado | P1 |
| [Portal Brasileiro de Dados Abertos](https://dados.gov.br/v3/api-docs) | Descoberta de conjuntos de dados e recursos | OpenAPI recuperada; GET de registros ainda não homologado | P2 |

Os testes prévios foram conduzidos no projeto [radar](https://github.com/hilaliskandar/radar). **Não são testes de execução ou persistência deste repositório.** Repetir em ambiente controlado e registrar provas antes de marcar qualquer gate aprovado.

## Arquitetura e limites de domínio

```text
APIs públicas GET / arquivos oficiais
    ↓ aquisição paginada, imutável, retries e hashes
snapshots brutos isolados no R2 privado / armazenamento de teste
    ↓ validação de esquema, datas, identificadores e cardinalidade
tabelas auxiliares de projetos, propostas, instrumentos, empenhos e pagamentos
    ↓ crosswalk territorial IBGE e ligações apenas por chaves verificadas
agregações de transferência municipal | investimentos localizados
    ↓ QA, proveniência, cobertura, reconciliação e não regressão
SQLite de candidato + JSON static-first opt-in
    ↓ prévia isolada Cloudflare Pages → promoção explícita
```

A arquitetura deve respeitar `governance/ARCHITECTURE.md`, `governance/DATA_MODEL.md`, `governance/QA_CHECKLIST.md` e o baseline existente. Não introduzir D1 nem serviços em tempo real sem necessidade comprovada.

### Entidades candidatas, sem migração de produção

- `fonte_versao`: fonte, URL consultada, parâmetros, timestamp de coleta, data-base publicada, MIME, versão do esquema, SHA-256, status, cursor e erro.
- `programa_federal`: sistema, identificador nativo, órgão, modalidade, nome oficial e classificação PAC **somente quando documentada**.
- `proposta_federal`: sistema, identificador, `id_programa`, ente proponente, código IBGE validado e situação.
- `instrumento_federal`: identificador nativo de parceria/convênio/plano; vínculo com proposta quando presente.
- `empenho_federal`: sistema de origem, identificador, UG, exercício, número, valor, situação e referência nativa; **1:N** para instrumento/projeto quando comprovado.
- `pagamento_federal`: identificador de ordem/pagamento e valor efetivo, sem confundir com empenho.
- `projeto_investimento_federal`: identificador nativo Obrasgov, natureza, execução, órgão, fonte, localização e data-base.
- `execucao_fisica_federal`: identificador do registro, projeto, percentual nullable, data de atualização; preservar histórico por snapshot, sem supor que cada registro equivale a período independente.
- `vinculo_fonte`: entidade A/B, IDs, tipo de vínculo, prova documental, regra, confiança e estado (confirmado/candidato/rejeitado). **Não promover candidato fuzzy a confirmado**.
- `relacao_territorial`: código IBGE, tipo (beneficiário, executor, localização de obra, localização aproximada), fonte e precisão.

As tabelas são proposta conceitual: nomes e migração dependem do exame do esquema real antes de código SQL.

### Regras de reconciliação

1. **Receita municipal reconhecida** (DCA/FINBRA/TCESP) é conceito diferente de empenho federal ou investimento físico localizado.
2. Não somar `empenhado + liquidado + pago`; são estágios, não parcelas adicionais de um mesmo repasse. Nunca somar financiamento FGTS, investimento privado e OGU sem tipologia e eliminação de duplicidades.
3. Identificador IBGE identifica território, **não comprova que operações de bases distintas são o mesmo repasse**.
4. Códigos IBGE inválidos, capitais ou casos multiterritoriais precisam de diagnóstico explícito; jamais converter ausência em zero.
5. Valor nominal e exercício/data de referência sempre explícitos; séries reais apenas com deflator identificado.
6. Uma obra situada no município não constitui automaticamente ingresso em sua receita.
7. Respostas do Obrasgov demonstraram em amostras `id_projeto_investimento` 1:N empenhos; `percentual_execucao_fisica` pode ser `null`.
8. Usar datas da **fonte** e da **consulta** separadamente, com refresh incremental apenas após checkpoint confirmado.

## Gates e critérios de aceite

| Gate | Entrega | Evidência exigida | Estado em 03/11/2026 |
|---|---|---|---|
| G0 — planejamento | Contrato conceitual, fontes, riscos e README | Arquivos e PR revisáveis | **Documentado neste PR** |
| G1 — inspeção do repositório | Ponto de extensão, esquemas e testes existentes | Inventário de caminhos e decisão de desenho | **Parcial — arquitetura canônica lida** |
| G2 — adaptadores GET | Cliente comum para tres APIs, com allowlist, paginacao, timeout e retries | Testes por mocks adicionados; CI e amostras reais neste repo a verificar | **CI unitario aprovado; HTTP real pendente** |
| G3 — staging e dados | JSON canônico local e manifesto SHA-256, R2/SQLite isolado ainda pendente | Testes simulados adicionados; CI e lote real por validar | **Implementação local inicial; não homologado** |
| G4 — vínculo e cobertura SP | Normalizador estrito para códigos IBGE de recebedor; cadastro SP645 completo ainda não carregado | Testes simulados criados, CI e cobertura estadual a conferir | **Código inicial implementado; não homologado** |
| G5 — conciliação | Transferido × empenhado × pago × obra × DCA, sem dupla contagem | Amostra auditada e diferenças explicadas | Pendente |
| G6 — consulta e visualização | API editorial JSON v2/v3 em prévia isolada e filtros territoriais | Contrato, testes de regressão e navegação | Pendente |
| G7 — promoção | Release pública e monitoramento | QA remoto JSON, aprovação expressa, SHA e rollback | **Bloqueado** |

### Ordem de trabalho

1. Reproduzir uma amostra pública de cada API em ambiente experimental e inspecionar todos os parâmetros OpenAPI úteis.
2. Registrar decisão de modelagem conforme esquema real existente e elaborar migration apenas para staging.
3. Testar identificadores nativos dentro de cada API; nunca assumir joins interbases.
4. Territorializar por IBGE e verificar os 645 municípios, com atenção a códigos e municípios ausentes.
5. Construir visão separada: `transferencias_recebidas` versus `investimentos_no_territorio`.
6. Confrontar séries e contratos contábeis com DCA/Siconfi/TCESP e indicar divergências.
7. Disponibilizar prévia isolada opt-in; só após QA/aceite promover.

## Protocolo contínuo de documentação

**A cada etapa**, atualizar cumulativamente o [README raiz](../README.md), esta matriz de gates e [diário de validação](INTEGRACAO_FEDERAL_VALIDACOES.md), informando: data/hora, branch/commit, fonte e endpoint, amostra, contagem, critérios, artefatos/hashes, falhas, decisão `pass/fail/bloqueado`, próximo passo. Não declarar 'concluído' com base apenas na criação de código, no status HTTP 200 ou na existência de arquivos no R2; exigir validação de conteúdo e QA. Se houver mudança de escopo, registrar motivo, impacto sobre o baseline e novos critérios antes de implementar.

## Não objetivos deste PR

Não executa coleta estadual nem modifica o SQLite canônico. Foi acrescentado um workflow de smoke HTTP isolado, acionável por PR e manualmente, com GET limitado a duas linhas por serviço, sem publicação de dados ou Cloudflare Pages. Não cria agendamento e não libera indicador de Novo PAC sem vínculo oficial validado.

## Incremento de 03/11/2026 — verificação HTTP pública

Arquivos adicionados: [smoke opt-in](../tests/test_federal_public_api_live.py) e [workflow isolado](../.github/workflows/federal-public-api-smoke.yml). Três consultas GET mínimas foram previamente verificadas fora do código deste repositório com Crawl2AI, todas com `tamanho_da_pagina=2` e dados válidos: `obrasgov/projeto-investimento?uf_principal=SP` (total_items 20.837), `parcerias/proposta?sg_uf_recebedor=SP` (13.434) e `especiais/programas-especiais` (16). São totais de sistemas e amostras distintas, não contagem de PAC nem de 645 municípios. **A execução HTTP do novo cliente pelo workflow ainda não foi comprovada** e permanece pendente. Após sucesso, conferir logs/sha do run e só então homologar a conectividade G2. A introdução do workflow representa mudança de escopo documental em relação ao PR original, sem afetar produção.

## Incremento de 03/11/2026 — persistência local G3

O módulo [federal_staging.py](../pipeline/acquire/federal_staging.py) mantém **snapshots locais imutáveis por SHA-256** e manifestos de lote, com verificador de integridade e diferenciação entre valor nulo e zero. O destino deve ser caminho absoluto explícito e **não há escrita no R2, SQLite nem publicação**. [Testes de staging](../tests/test_federal_staging.py) cobrem idempotência, conteúdo modificado, corrupção e rejeição de entrada inválida. A execução dos testes no CI e a persistência de resposta HTTP real pelo cliente do repositório **ainda não foram confirmadas**; portanto, G3 continua pendente de homologação. Retenção, proteção de dados, gestão de snapshots e sincronização com R2 privado exigem deliberação e evidências antes de qualquer migração.

## Incremento de 03/11/2026 — pipeline amostral executável G2/G3

[Runner de amostra](../pipeline/acquire/federal_sample_staging.py) realiza três GETs controlados e salva conteúdo em diretório local explícito usando [staging](../pipeline/acquire/federal_staging.py) e SHA-256, interrompendo a carga se uma das fontes não retornar registros. [Testes com cliente simulado](../tests/test_federal_sample_staging.py) cobrem idempotência e rejeição de carga incompleta. O [workflow isolado](../.github/workflows/federal-public-api-smoke.yml) foi adaptado para executar os testes, um smoke HTTP real e uma carga de até seis registros no diretório efêmero `RUNNER_TEMP`, sem publicar nem enviar arquivos. **O histórico de execuções ainda não comprovou sucesso desse workflow na revisão atual.** Assim, G3 não está homologado, embora o caminho de execução esteja implementado. A chave `cd_ibge_recebedor` está presente nas propostas Transferegov consultadas; não se comprovou correspondente código IBGE em amostras de Obrasgov, devendo sua localização municipal passar por procedimento territorial próprio.

## Incremento territorial G4 — 03/11/2026

O módulo [federal_territory.py](../pipeline/normalize/federal_territory.py) verifica `cd_ibge_recebedor` do Transferegov contra conjunto explícito de códigos IBGE canônicos, preservando o papel **ente recebedor da proposta**. Registro sem código ou formato inválido permanece `em_revisao`; código fora do cadastro fica `fora_do_universo`; correspondência exata gera `confirmado_recebedor`, não pagamento nem localização de obra. Proibido utilizar cidade/UF por nome como junção definitiva. [Testes](../tests/test_federal_territory.py) foram adicionados, mas ainda sem resultado do CI nesta revisão. A próxima homologação exige leitura do cadastro SP645 da aplicação, verificação de cobertura e unicidade e regras específicas de geolocalização das obras Obrasgov. A execução de workflows não foi comprovada; G2/G3 também permanecem pendentes.
