# FED14/FED15 — disponibilidade da API pública Obrasgov e integração privada de proveniência

**Data da consulta:** 16/11/2026, conforme relógio UTC do runner. **Data declarada de atualização da API:** 13/11/2026. **Status:** controle de cobertura da fonte concluído; sem homologação de localização de execução.

## Fonte oficial

A [nova API de dados abertos do Obrasgov](https://api-publica.obrasgov.gestao.gov.br/obras) apresenta documentação OpenAPI em [`/obras/openapi.json`](https://api-publica.obrasgov.gestao.gov.br/obras/openapi.json) e endpoints `/projeto-investimento`, `/geometria`, `/execucao-fisica`, `/empenho` e `/contrato`. A página institucional [API de Dados Abertos Obrasgov](https://www.gov.br/obrasgov/pt-br/ferramentas-de-gestao-e-transparencia/api-de-dados-abertos-obrasgov-br_novo) confirma o novo ambiente. A API foi efetivamente consultada com HTTPS; não se inferiram valores a partir de apenas textos de documentação.

O identificador `id_projeto_investimento` é filtro oficial de todos os módulos analisados. Foram consultados os **19 projetos** cujo vínculo documental com proposta e discrepância territorial já havia sido confirmado em FED12.

## Resultado dos 19 projetos

| Consulta na API nova | Resultado |
|---|---:|
| Projetos localizados por ID em `projeto-investimento` | **19/19** |
| Projetos com endereço cadastral no retorno | **0/19** |
| Projetos com CEP cadastral | **0/19** |
| Projetos com `pins` cadastrados na resposta | **0/19** |
| Projetos com geometria retornada em `geometria` | **0/19** |
| Projetos com execução física retornada em `execucao-fisica` | **0/19** |
| Projetos com contratos retornados em `contrato` | **0/19** |

As situações atuais do registro de projeto são **7 Concluída, 7 Em execução e 5 Cadastrada**. O vínculo entre os 19 IDs consultados e os IDs retornados foi confirmado exatamente. Cada consulta utilizou `tamanho_da_pagina=200`; os retornos tinham HTTP 200 e estrutura JSON válida.

### Controle de cobertura geral — essencial para interpretação

Foram realizadas consultas **sem filtro de projeto** e com uma linha por página nos cinco módulos. Os retornos foram:

| Módulo | `total_items` na consulta sem filtros |
|---|---:|
| `projeto-investimento` | **155.792** |
| `geometria` | **0** |
| `execucao-fisica` | **0** |
| `empenho` | **0** |
| `contrato` | **0** |

`/data-atualizacao` indicou `2026-11-13T00:00:00`. Foram efetuadas consultas adicionais a `/geometria` por `cod_ibge=3543402`, por `sg_uf=SP` e sem filtros; todas retornaram zero linhas. A conclusão permitida é: **a nova API respondeu com cadastro de projetos amplo, mas seus módulos complementares estavam sem dados disponíveis nessas consultas**, não que os projetos não tenham geometria ou execução física em outros sistemas.

**Regra obrigatória:** não preencher `0` em indicador de execução física porque o endpoint global está vazio. Não substituir os registros oficiais de execução física do Transferegov do FED08C por ausência de linhas em outra API. Tampouco promover como ponto de obra uma descrição que apenas mencione município ou praça.

## Persistência e reprodutibilidade

O script [`pipeline/qa/audit_rmrp_fed14_obrasgov_api.py`](../pipeline/qa/audit_rmrp_fed14_obrasgov_api.py) consolida as 19 respostas por ID, os hashes SHA-256 dos corpos HTTP recebidos, URLs de consulta, retorno geral dos módulos e QA agregado. Os registros integrais e identificadores individuais ficam **somente no ZIP privado**.

[**FED14 — respostas oficiais e QA privado**](https://drive.google.com/file/d/1HK6kxOGrw8weQKDtLd_ECWuqAzZfJJCz/view): **30.031 bytes**, SHA-256 `f6d140092f7ea962478cdc8749683bbbaac47525198aed326c83cf30f3da273b`. Acesso `shared=false`, pasta privada `186Cxxs2wZas55LlEPPoD-G2_nJfGmfU9`; hash e CRC verificados após download de retorno do Drive.

## FED15 — incorporação à prévia privada

A rotina [`deployment/build_rmrp_fed15_private.py`](../deployment/build_rmrp_fed15_private.py) restaurou o pacote FED13 e acrescentou aos **19 JSON de projetos** a seção `cobertura_api_publica_obrasgov_fed15`, com:

- correspondência do ID de projeto oficial e situação registrada;
- indicação de ausência de endereço, CEP e pontos no retorno **desta API**;
- distinção de `status_endpoint_geometria=sem_registros_na_api_global`, `status_endpoint_execucao_fisica=sem_registros_na_api_global` e `status_endpoint_contratos=sem_registros_na_api_global`;
- aviso de que a falta de linhas **não prova ausência da obra**, execução, pagamentos ou geometrias em fontes alternativas.

O manifesto conserva `public_release_authorized=false`. Os **218 projetos** continuam com `localizacao_fisica.pontos=[]` e `valores_investimento_pago_centavos=null`. O materializador não modificou as séries, os grupos de natureza do empenho nem o cadastro anterior, e opera apenas sobre árvore privada.

**QA FED15:** **1.603 verificações da API aprovadas** e **288 respostas HTTP 200** em servidor local, com **285 JSON válidos**, sem falhas. Não houve teste visual de navegador ou deploy Cloudflare Pages.

[**FED15 — prévia privada com qualidade da fonte Obrasgov**](https://drive.google.com/file/d/1i4nRAlyzVddW_cQq8GbgtbDO7pz2E8Pq/view), **814.554 bytes**, SHA-256 `f90e71e6be34fa7e7625153048268769b128e66e9b7d81fad483a7aa90ad0a10`, CRC e SHA-256 confirmados em readback. Acesso `shared=false`, pasta privada da RMRP.

## Próximos passos

1. Priorizar **fonte documental independente com endereço e execução** (extrato de projeto, peças de projeto básico, contratos, medições, imagens/documentos e registros municipais) para os 19 casos. Não insistir em endpoints globalmente vazios como se fossem consultas por ID negativas.
2. Monitorar atualização e eventual preenchimento dos módulos da nova API, sem criar nova rotina redundante com automações existentes.
3. Rever os dois desembolsos FED11 pelo identificador SIAFI e vínculo documental efetivo; a coincidência de R$ 88 mil permanece hipótese.
4. Efetuar QA de navegador, cache e versão restrita do Pages com aceite antes da promoção de campos cadastrais públicos; **não** promover GND4 pago nem pontos físicos sem documentação suficiente.

**Estado da release:** `public_release_authorized=false`; nenhuma atualização da produção executada.
