# FED00 — Inventário técnico inicial da integração federal SP645

**Data:** 2026-11-09. **Estado:** inventário documental e de contratos do código concluído; verificação operacional dos arquivos federais e do SQLite de build ainda pendente. **Não houve ingestão estadual, deploy, migration ou escrita no R2.**

## Arquitetura comprovada no código

1. `data/schema/001_initial.sql`: tabelas `municipio`, `universo`, `universo_municipio`, `fonte`, `variavel`, `crosswalk_variavel`, `observacao`, `cobertura`, `build`, `build_source`. Chave lógica da observação anual: `(codigo_ibge, ano, variavel_id)`; estados `observado`, `ausente`, `nao_aplicavel`, `em_revisao`.
2. `data/schema/004_provenance.sql`: `artefato_fonte`, `observacao_proveniencia`, hashes, campos e ligações com `build`.
3. `data/schema/006_tcesp_investimentos.sql`: extensão específica com `tcesp_lote`, `tcesp_investimento_programa` e `tcesp_investimento_acao`, conservando `observacao` DCA sem sobregravação. É precedente de separação entidade/evento antes da agregação.
4. `deployment/fetch_r2_snapshot.py`: leitor de snapshots R2 por manifesto, com validação de SHA e conteúdo, dependente de `CLOUDFLARE_ACCOUNT_ID`, `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_R2_BUCKET`. **Nenhuma listagem live do bucket foi realizada**.
5. `editorial/rmsjrp/enumerar_propostas_g06f2.py`: coleta paginada de `/parcerias/proposta` por `cd_ibge_recebedor` e `/discricionarias/propostas` por `cod_munic_ibge` (`pagina`, `tamanho_da_pagina=50`); geovalidação, deduplicação dentro de módulo–município e QA; hardcoded aos 37 municípios, precisa parametrização SP645. G06-F2 obteve 9.338 propostas nas 231 páginas das 74 consultas, não pagamentos.
6. `editorial/rmsjrp/RELATORIO_G06F3_VINCULOS_2026_11_09.md`: vínculo `id_proposta → id_parceria → empenho` em pilotos; sem ligação comprovada com ordem de pagamento, crédito ou liquidação. A proposta 398 e sete empenhos são casos de regressão, não demonstração de cobertura estadual.

**Decisão de modelagem:** registros de propostas, instrumentos, execução, beneficiários e obras exigem tabelas normalizadas **complementares**; indicadores anuais aprovados podem ser derivados em `observacao`. Não introduzir D1 antes de necessidade demonstrada. R2 canônico existente: `financas-municipais-sp-canonico`, segundo documentação histórica; identificação live e permissões não foram sondadas aqui.

## Inventário federal — resultados documentais

A matriz vinculada `MATRIZ_FONTES_FEDERAIS_SP645.csv` contém **11 linhas de fonte/conjunto** (não é contagem de APIs nem de transferências), com link oficial, método de acesso, chaves esperadas, evidência anterior, estado, bloqueio e próxima diligência.

- O catálogo Transferegov anuncia APIs de Parcerias, Especiais, Discricionárias e Fundo a Fundo e download CSV Discricionárias. Confirmado em https://api-publica.transferegov.gestao.gov.br/ e https://www.gov.br/transferegov/pt-br/ferramentas-gestao/api-de-dados-abertos-transferegov.br . Cronograma oficial para Discricionárias: instrumentos 2026-11 a 2027-02; financeiro 2027-03 a 2027-06; obras 2027-07 a 2027-10. A primeira entrega de atos preparatórios foi anunciada em outubro de 2026. Não presumir que módulos futuros já estejam completos.
- Tesouro Transparente publica datasets de transferências obrigatórias por município (FPM, Fundeb, ITR, CIDE etc.) em CSV, e API de transferências constitucionais com consulta por município. Fonte https://www.tesourotransparente.gov.br/temas/estados-e-municipios/transferencias-a-estados-e-municipios e https://www.tesourotransparente.gov.br/ckan/dataset/api-de-transferencias-constitucionais . **Priorizar os CSVs completos e validar códigos, competência e valores antes de APIs individuais**.
- Portal da Transparência federal disponibiliza downloads de convênios semanalmente e documentação de empenho/liquidação/pagamento, recursos transferidos, emendas e documentos vinculados diariamente, conforme catálogo https://portaldatransparencia.gov.br/download-de-dados/ . Frequência publicada não significa disponibilidade imediata de cada evento.
- Obrasgov nova API em https://api-publica.obrasgov.gestao.gov.br ; a geolocalização do projeto não equivale ao município beneficiário ou credor. Fonte https://www.gov.br/obrasgov/pt-br/ferramentas-de-gestao-e-transparencia/api-de-dados-abertos-obrasgov-br_novo .

## Limites de evidência e próximos atos

**FED00 não está integralmente homologado**: ainda é necessário inspecionar o pipeline do SQLite de build, consultar manifestos de R2 *ao vivo*, descobrir datas, layouts e tamanhos dos arquivos CSV e testar downloads efetivos; nenhum número de registros federais SP645 pode ser declarado. A inspeção do repositório confirma o schema de origem, não o conteúdo de um banco materializado específico.

**Próxima ação exata:** (a) auditar montagem SQLite e índices nas migrations posteriores; (b) testar HEAD/GET ou metadados dos CSVs nacionais Transferegov/STN/CGU, incluindo tamanho, cabeçalho, periodicidade e cobertura histórica; (c) escolher um lote piloto não destrutivo e propor migrations de entidades federais, preservando integração com `municipio`, `artefato_fonte` e `build`; (d) validar os sete empenhos e a proposta 398 como sentinelas; (e) atualizar matriz e relatórios de QA e manter FED00 aberto até os testes.

**Segurança:** não substituir DCA, TCESP ou R2 existentes; não atribuir causalidade da LC 200/2023; zero não significa dado ausente; aprovações de propostas não são pagamentos.
