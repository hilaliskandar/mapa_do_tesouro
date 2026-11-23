# Mapa do Tesouro — auditoria de elegibilidade para atualização da plataforma

**Data:** 23/11/2026. **Solicitação:** destacar endereço público nos READMEs e atualizar a plataforma com tudo que estiver validado. **Situação:** READMEs atualizados; publicação pública de novas camadas condicionada aos gates próprios.

## Endereços e versão comprovados

- Produção estadual: **https://finbra-tic-tim-referencia.pages.dev/**
- Prévia PR 233: **https://pr-233.finbra-tic-tim-referencia.pages.dev/**
- Cloudflare Pages projeto `finbra-tic-tim-referencia`, branch de produção `main`.
- A última implantação de **produção** registrada na Cloudflare ocorreu em **09/10/2026**, no commit `27f2b5056cbba56a9075a18b51013acbee597cea`, release `v0.4.0`. Não presumir publicação posterior.
- A implantação de **prévia** da PR 233 em 23/11/2026 (commit `cc298dc1bba9f80f821f0bcdc892f280c547a928`) teve estágio Cloudflare `deploy=success` e job GitHub `build-deploy-qa=success`. O job independente `rmj-browser-qa` foi **cancelado**, não aprovado.
- Os workflows de produção exigem **release tag** existente, testam a versão e materializam o snapshot publicado aprovado; PR 233 está **aberta em rascunho**, não pode ser confundida com release.

## Matriz de elegibilidade

| Conjunto | Evidência e escopo | Situação | Condição para promoção |
|---|---|---|---|
| Núcleo fiscal estadual v0.4.0, API editorial v1, 13 universos | Release aprovada e implantação Cloudflare comprovada | **Já público** | Preservar versão/manifesto e testar regressão em qualquer próxima implantação |
| 34 códigos IBGE7 da RMRP, quatro sub-regiões legais (15+6+6+7) | Dimensão oficial e QA de unicidade documentadas em FED06B/FED07 | **Candidato a publicação cadastral** | Regressão frontend e navegação, rótulo territorial correto, contrato estático estável |
| 218 vínculos de projeto–instrumento–proposta Obrasgov | Chaves documentais auditadas em FED07 | **Candidato a catálogo por proponente** | Não identificar como obra executada, não publicar pontos/valores pagos sem comprovação, regressão e revisão de conteúdo |
| FED07: 28.503 movimentos e R$ 627.287.678,10 em pagamentos nominais brutos | Unicidade preservada, mas classificação da natureza, estornos e estágio final pendentes | **Não homologado como investimento executado** | Prova de natureza GND4, valor líquido, estornos e não aditividade |
| 441 coordenadas de propostas e 224 itens exploratórios Obrasgov na prévia | QA espacial de triagem; pontos não equivalem ao lugar físico da obra | **Não homologado para mapa físico de investimento** | Prova documental de localização material |
| Transferegov Especiais: 284 planos e cadeia OP/OB | Consulta exploratória; ordem enviada à instituição bancária não prova crédito | **Não homologado como pagamento efetivo** | Evidência de crédito e adequação por estágio |
| Gestão de Parcerias: 743 propostas | Registros de propostas, parte com valores planejados e situações não aprovadas | **Cadastral preliminar** | Controles de status/competência/duplicação e revisão para exposição pública |
| SIAFEM RMRP: 238 consultas município-ano, 889 convênios-ano na prévia | Conciliação com totalizador; `qa_status=preview_transferencias_estaduais_em_revisao_nao_execucao_municipal` | **Prévia com ressalva; não execução municipal homologada** | Auditoria de estágios financeiros, semântica do líquido/estorno, QA de publicação |
| SIAFEM externo à RMRP, 2025: 525/611 consultados, 445 reconciliados, 80 inconclusivos | Acervo R2 privado e controles atualizados, R$ 960.744.783,60 nas respostas validadas | **Não homologado como série estadual pública** | Cobertura, tratamento das 80 inconclusivas ou explicitação de lacunas, QA independente de valores e política de publicação |

## Diagnóstico da implantação

A produção não recebe automaticamente todos os arquivos tecnicamente inspecionados. O `pages-production.yml` só aceita uma release formal, materializa a prévia aprovada e valida o site; a PR 233 de investimentos utiliza `materialize_investimentos_preview.py`, que obriga marcadores **não homologados** e permanece deliberadamente isolado da implantação principal.

O relatório FED07 especifica que a **dimensão territorial e os vínculos cadastrais podem ser candidatos**, mas exigem regressão de frontend e revisão de conteúdo. O bloco financeiro (capital efetivamente pago, valores líquidos, localização física) permanece bloqueado.

**Decisão operacional:** não publicar automaticamente a prévia integral nem criar release a partir da PR 233 como um todo. O pedido de atualizar a produção autoriza avançar na preparação de um corte seguro, mas não substitui os testes e evidências de homologação de cada indicador.

## Próxima implantação segura, com escopo mínimo

1. Derivar da PR 233 apenas **34 municípios, quatro sub-regiões e cadastro de vínculos oficiais de projetos** como dimensão **cadastral**, sem movimentos monetários provisórios e sem pinos físicos presumidos. Criar manifesto com fonte e `qa_status` por entidade.
2. Gerar candidato de release isolado a partir da versão produtiva aprovada `v0.4.0` e overlay apenas dos arquivos elegíveis, sem incorporar a branch inteira.
3. Testar regressão dos 13 universos, API v1 e indicadores TCESP/DCA, além de testes de frontend/navegação/links/carga/JSON e comparação com os resultados do PR 233.
4. Publicar em prévia específica para aceite; após aprovação dos gates, emitir release e executar `pages-production.yml`, documentando URL, hashes e resultado remoto.
5. Atualizar separadamente outros conjuntos conforme a homologação de cada fonte. Nunca promover `qa_status` experimental a execução paga ou obra fisicamente localizada.

**Estado final desta auditoria:** URL documentada nos READMEs; produção existente comprovada como v0.4.0; prévia da PR 233 disponível; **nenhuma atualização de dados foi implantada na produção nesta etapa**.
