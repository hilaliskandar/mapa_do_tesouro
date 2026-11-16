# FED07 — homologação técnica parcial e prévia privada de integração API v3 da RMRP

**Data:** 16/11/2026. **Situação:** testes de consistência concluídos; **prévia restrita apta à homologação funcional**, mas **sem autorização de produção pública**. Este relatório distingue aceites técnicos automatizados de homologação substantiva da execução fiscal e territorial.

## Fontes e contrato conferidos

- Contrato `governance/CONTRATO_CONSULTAS_INVESTIMENTOS_RMRP_API_V3_2026_11_11.md`, especialmente estágio de pagamento, papel territorial, natureza da despesa, `qa_status`, 34 municípios, quatro sub-regiões, proibição de aditividade de estágios e oito grupos de testes de publicação.
- Prévia original FED06C, [ZIP privado](https://drive.google.com/file/d/1twgK_RpEKkLvCQ8-Xbsdu-5ieWy35m4c/view), SHA-256 `4ecfb4ff6c7fc504ea5f09a878b184b9195aee0507dc958eff4bd94cd3fa3d23`.
- SQLite derivado de dados nacionais oficiais FED04D/FED03E, [ZIP privado](https://drive.google.com/file/d/1qQ2nidb5u3M8fXEULYhQoHBVKI_g4ETH/view), SHA-256 `e398a4aed54867a218b5e8a3b37c688d621bc360cb7839e347dedc2c029f86f3`.
- Fontes originais Transferegov (7 ZIPs), Obrasgov, legislação estadual das quatro sub-regiões e malha IBGE/SP 2024 (EPSG:4674), todas arquivadas no Drive privado e previamente verificadas.

## Alterações realmente materializadas na API de desenvolvimento

Os **34 arquivos municipais** receberam `evidencias_auditadas` separado dos valores contratuais do endpoint, com:
- 28.503 pagamentos a favorecidos, em **1.286 convênios distintos**, distribuídos por município **proponente**; total de **62.728.767.810 centavos (R$ 627.287.678,10)** de eventos nominais brutos com `natureza_despesa=nao_classificado` e `qa_status=em_revisao`; **não** constam como investimento executado ou transferência federal líquida;
- 441 registros de coordenadas de propostas, por município proponente, sem usar geocodificação candidata em mapas de obras;
- 218 projetos com identificador documental explícito de instrumento e proposta, sem dupla atribuição territorial.

Cada um dos **218 JSON de projeto** passou a conter `instrumentos_vinculados` por `id_projeto_investimento → nr_instrumento → convenio → proposta`, evidência cadastral quantitativa de coordenadas da proposta associada e aviso de ausência de localização física comprovada. Não foram publicados pontos ou valores de investimento pago.

O `manifest.json` recebeu novos hashes das fontes, contagens, cobertura e razões de bloqueio; `pendencias.json` foi atualizado para não afirmar falsamente que pagamentos e coordenadas continuam sem coleta. Os 19 arquivos anuais preservam a série de transferências ao convenente como **estágio diferente de pagamento a favorecido**. As quatro sub-regiões oficiais e os dados originais da interface HTML local continuam preservados.

**Campos monetários de investimento federal direto e transferências federais líquidas homologadas permanecem `null`.** `public_release_authorized=false`.

## Testes executados

1. Bateria de construção FED07: **561 verificações** de municípios, sub-regiões, exercícios, projetos, conservação monetária e bloqueios de localização, sem falha.
2. Script independente versionado [`pipeline/qa/validate_rmrp_api_v3_fed07.py`](../pipeline/qa/validate_rmrp_api_v3_fed07.py), executado a partir do arquivo do GitHub sobre a prévia gerada: **1.603 verificações aprovadas**; cada município obriga (GND4=\mathrm{null}), (transferencias\_federais\_creditadas=\mathrm{null}), `compoe_investimento_executado=false`, `natureza_despesa=nao_classificado`; cada projeto obriga ponte documental e ausência de pin de execução. Conservação do total de 28.503 pagamentos, 62.728.767.810 centavos, 441 coordenadas e 218 projetos.
3. ZIP gerado passou no CRC da origem; arquivo enviado ao Drive privado, download de conferência e SHA-256 iguais.

### Rastreabilidade do pacote

[**RMRP_FED07_PREVIA_API_V3_PRIVADA_2026-11-16.zip**](https://drive.google.com/file/d/1ZgwVepB-zpJGw3BsSPviYADy8PbMEdma/view), ID `1ZgwVepB-zpJGw3BsSPviYADy8PbMEdma`, **686.402 bytes**, SHA-256 `79a193e46f8d8280aed875396fe7e42fa122dc6bc704faeaa332acb88d3eece7`; pasta `186Cxxs2wZas55LlEPPoD-G2_nJfGmfU9`, `shared=false`, CRC e readback SHA-256 aprovados. Contém os JSON e a interface HTML de inspeção local; **a interface HTML existente não foi redesenhada para expor todos os campos FED07**, que estão disponíveis nos JSON.

## Matriz de homologação para incorporação

| Objeto | Resultado FED07 | Pode entrar na plataforma pública como investimento executado? |
|---|---|---|
| 34 municípios, quatro sub-regiões legais | Integridade e chaves verificadas | **Sim**, apenas como dimensão territorial, após regressão frontend |
| 218 projetos e ponte de instrumento/proposta | Correspondência documental por chaves oficiais | **Sim**, como cadastro de carteira por proponente, com status; **não** como obra executada |
| 28.503 pagamentos e 1.286 convênios | Eventos de pagamento conciliados, valor nominal bruto preservado | **Não**, sem natureza de despesa, líquido e local de execução |
| 441 coordenadas de propostas | Interseção IBGE e vínculo documental qualificados | **Não**, para mapa de execução física; no máximo cobertura/QA identificada como cadastral |
| R$ 627.287.678,10 em pagamentos brutos | Soma não duplicada de 28.503 eventos | **Não**, para agregado de investimento pago, nem soma a transferências ao convenente |
| Transferências ao convenente, 2.537 eventos | Staging anterior com estágio rotulado | **Não**, enquanto estornos, recebedor e regras de não aditividade não homologados |
| TCESP e indicadores municipais existentes | Não retestados nesta rodada | **Não modificar** até regressão completa |
| Prévia estática FED07 | QA estrutural de 1.603 verificações | **Sim**, para teste privado, **não** como publicação |

## Gates substanciais ainda necessários

1. **Financeiro:** tratar movimentação de estornos/devoluções por fonte oficial, status de DL e possíveis reclassificações, comprovar natureza GND4 efetivamente paga por documento e evitar somar pagamentos de favorecidos aos repasses aos convenentes. O controle de 8 pagamentos positivos vinculados a DL não `Ativo` (R$ 272.120,91) permanece em revisão, não é suspeita conclusiva.
2. **Territorial:** averiguar 20 coordenadas divergentes com vínculo a projetos; confrontar as demais coordenadas com documentação de obra, e somente então alterar `localizacao_fisica.qa_status` de `nao_comprovada` para `homologado`, se demonstrado.
3. **Plataforma:** verificar regressão TCESP 2023–2025 e ressalva Guatapará/2023, renderização/responsividade, valores ausentes, API v1, testes HTTP/cache e validação em prévia restrita do Cloudflare Pages. O teste do ZIP local não representa esse aceite.
4. **Deploy:** nenhuma gravação no build produtivo ou D1, e nenhum gate `public_release_authorized` foi alterado. É necessária publicação controlada de prévia e aceite final por responsável de projeto.

**Encaminhamento:** priorizar integração estática de informações cadastrais, dimensões oficiais e indicadores de cobertura, preservando como `null` todo valor de capital pago sem lastro; somente promover frontend e produção após regressão e revisão de conteúdo.


## Incorporação aditiva na prévia da plataforma e testes de regressão

A arquitetura atual do repositório já contém `deployment/materialize_investimentos_preview.py` e seis JSON de outras prévias em `app/static/data/api/v3/investimentos/rmrp/`. Por isso, o FED07 foi **acrescentado**, não substituído, em uma cópia isolada de `app/static`:

- A contagem correta dos JSON do próprio FED07 é **279**, não 280: 1 manifesto, 1 índice municipal, 34 fichas municipais, 19 anos, 218 projetos, 1 pendências, 1 índice sub-regional e 4 fichas de sub-região. Essa divergência de **um arquivo** em inventários anteriores foi identificada durante teste e corrigida no gate. Os seis JSON de outras prévias preexistentes foram preservados, resultando em **285 JSON** na pasta API v3 da cópia integrada.
- Foi criada a rotina de overlay [`deployment/materialize_rmrp_fed07_private.py`](../deployment/materialize_rmrp_fed07_private.py), que exige `index.html` e o marcador `.rmrp-fed07-private-preview`, recusa escrita na árvore do repositório ou em diretórios públicos e **bloqueia sobrescritas**. O marcador foi exigido apenas na execução privada; o pacote distribuído não contém credencial de autenticação nem foi publicado em Cloudflare Pages.
- A suíte específica [`tests/test_fed07_private_overlay.py`](../tests/test_fed07_private_overlay.py) foi integrada às quatro suítes existentes `test_pages_deployment_contract.py`, `test_frontend_contract.py`, `test_build_static_site.py` e `test_export_regional_api_v2.py`, totalizando **20 testes aprovados**, sem falhas (com `PYTHONPATH=.`). O validador de conteúdo FED07 passou novamente em **1.603 verificações** sobre a árvore integrada.
- **O overlay preserva os seis endpoints antigos; não executa nem substitui o materializador público de investimentos**, não modifica produção e não transfere automaticamente o pacote para um build Cloudflare Pages.

### Entrega integrada

[**RMRP_FED07_SITE_PREVIA_PRIVADA_2026-11-16.zip**](https://drive.google.com/file/d/1whZO3RZABn9aIS3SrF5_8DqGdyBSwTZT/view), ID `1whZO3RZABn9aIS3SrF5_8DqGdyBSwTZT`, com `index.html` e recursos de frontend já existentes mais **285 endpoints JSON** no diretório da API v3; **296 membros** ao todo, tamanho **788.460 bytes**, SHA-256 `60b7ef5b23aa048b407939ce3678a559e84c4806cbc06e1bb1699f2625d45e4d`. Drive em pasta privada, `shared=false`; readback SHA-256/CRC íntegro. A distribuição é um **artefato técnico local para teste**, não uma URL de implantação web nem comprovação de responsividade/browser QA.

**Gate de implantação pública:** permanece **bloqueado**, especialmente para dados financeiros de capital e pinos de obra. Antes de implantar a camada cadastral sem valores, executar teste de build Pages restrito completo, controle de cache e navegação efetiva, revisão de regressão TCESP/Guatapará, verificação de conteúdo e aprovação responsável da release. O usuário solicitou prosseguir na homologação, não há evidência suficiente para declarar publicada a plataforma.
