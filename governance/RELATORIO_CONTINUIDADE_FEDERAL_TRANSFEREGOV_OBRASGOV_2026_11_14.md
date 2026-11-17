# Retomada da investigação de investimentos federais — Transferegov, Obrasgov e conciliação

**Data:** 14/11/2026. **Branch:** `investimentos-territoriais-sp645-20261111`. **Escopo:** SP645 como universo de aquisição, RMRP34 como piloto de reconciliação. **Status:** coleta de layouts complementares efetivamente executada e confirmada; inspeção do arquivo nacional de itens DL independente em andamento. Nenhuma escrita em SQLite/D1 produtivo, R2, Pages ou publicação.

## Evidências reaproveitadas e pontos de partida

- RUN [43618166707](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43618166707) validou nacionalmente os esquemas `siconv_pagamento` (7.575.512), `siconv_obtv_convenente` (3.113.841), `siconv_dl` (7.710.768) e `siconv_empenho_desembolso` (393.062). Os números são **linhas nacionais**, não investimentos pagos.
- Para RMRP34 proponente, os trabalhos anteriores localizaram 6.410 propostas, 1.793 convênios, 28.456 itens PAD (7.917 GND4 aprovados) e 28.503 movimentos de pagamento relacionados a 1.286 convênios. A identidade do município de execução segue distinção independente da sede do proponente.
- Os **645 municípios IBGE7** e seus recortes 16 RA, 43 RG, 9 RM e 1 AU já estão preparados na dimensão `governance/DIM_SP645_IBGE_RA_RG_RM_AU_CONSOLIDADA_2026_11_14.csv`, com QA de fonte oficial. Essas classificações são alternativas, não aditivas.

## Novos arquivos oficiais realmente inspecionados

Catálogo oficial confirmado em https://api-publica.transferegov.gestao.gov.br/downloads (arquivos listados em 14/11/2026).

A rotina de auditoria `pipeline/acquire/inv_sp645_transferegov_new_source_layout.py` usa download temporário atômico, retry limitado para 429/5xx e problemas transitórios, SHA-256, um único membro CSV, conferência completa de CRC, cabeçalhos e amostra estrita (1000 linhas), sem imprimir microdados de convenentes ou fornecedores. O ZIP é removido do runner após a inspeção; o artefato de Actions **contém apenas metadados**. Não equivale a staging nacional persistido em R2.

**Workflow concluído com SUCCESS:** [43629864912](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43629864912).

| Arquivo | Cabeçalho oficial real verificado | Implicação |
|---|---|---|
| `siconv_pagamento_tributo` | `NR_CONVENIO`, `DATA_TRIBUTO`, `VL_PAG_TRIBUTOS` | É registro de tributos por convênio; **não** apresenta `NR_MOV_FIN` nem `ID_DL`. Não vincular ingenuamente a movimento individual |
| `siconv_ingresso_contrapartida` | `NR_CONVENIO`, `DT_INGRESSO_CONTRAPARTIDA`, `VL_INGRESSO_CONTRAPARTIDA` | Evento de ingresso de contrapartida. Não somar como pagamento de despesa GND4 |
| `siconv_coordenadas_obra` | `ID_PROPOSTA`, `NOME_PROJETO_CADASTRO_OBRA`, `LATITUDE_CADASTRO_OBRA`, `LONGITUDE_CADASTRO_OBRA` | Candidato a georreferência de obra no contexto de proposta, requer validação de coordenadas, cardinalidade e localização administrativa; não assumir que cada coordenada equivale a um projeto distinto |
| `siconv_contrato_cipi` | `ID_CONTRATO`, `NR_CONTRATO`, `ID_PROJETO_INVESTIMENTO` e outros 18 campos, incluindo situação, valor global e datas | Ponte documental potencial entre contrato e projeto Obrasgov; **valor global do contrato não equivale a pagamento federal** |
| `siconv_dados_obrasgov_geral` | `id_projeto_investimento`, `nr_instrumento`, `programa_governo`, `link_transparencia` | Ponte adicional entre número de instrumento e projeto Obrasgov, sujeita a cardinalidade e revisão de qualidade |

**Dados de estágio distintos**: tributos, ingressos de contrapartida, parcelas de transferências, documentos de liquidação, despesas do convenente e pagamentos do Tesouro não são automaticamente aditivos. Manter valores por evento e não produzir soma de investimentos enquanto estiverem sem prova de natureza econômica.

## Arquivo prioritário ainda em inspeção

`siconv_itens_dl.zip`, 523,1 MB declarados no catálogo, é a fonte candidata à ponte documental DL→itens do plano. Executado isoladamente no workflow [43629868488](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43629868488), com CRC integral e apenas cabeçalho/amostra como saída. **Não afirmar os nomes de colunas até esse job terminar e o manifesto confirmar.**

## Etapas seguintes

1. Conferir o esquema real e a integridade de `siconv_itens_dl` na execução acima. Verificar se existe `ID_DL` e identificador efetivo do item PAD; se não houver, analisar alternativa documental, nunca deduzir ligação por proximidade.
2. Fazer inventário de tipos `TP_MOV_FINANCEIRA` e sinais/situações com contagem por domínio, sem imprimir microdados. Reconciliar `siconv_pagamento` × OBTV e DL, com testes de cardinalidade/fan-out.
3. Testar ligações `ID_PROPOSTA`→coordenadas, `ID_CONTRATO`→CIPI e `NR_CONVENIO`/número de instrumento→projeto Obrasgov, registrando duplicatas, inconsistências e municípios que não são proponentes.
4. Reaproveitar fontes externas: API Obrasgov para localização física, CGU convênios/ordens bancárias para controles, SIAFEM-SP para liberações estaduais, e Transferegov Especiais/Parcerias como modalidades distintas.
5. Capturar e manter **uma versão nacional única por fonte** em staging privado imutável, checksum, CRC e readback; derivar SP645 e RMRP34 desse mesmo conjunto.
6. Agregar apenas valores financeiros de mesmo estágio e natureza homologada e preservar dados indeterminados como ausência, não zero.

## Critérios de governança

- No fluxo SP645, municípios são atribuídos por código IBGE de proponente/beneficiário/local da obra **com papel registrado**; RA/RG/RM/AU decorrem exclusivamente desse código.
- Não presumir geolocalização física de investimento a partir de sede do fornecedor.
- Não produzir total de investimento executado usando GND4 aprovado do PAD como substituto de pagamento.
- Os workflows são isolados, conservam apenas relatórios sem nomes, CNPJ ou linhas de pagamento, e não promovem a base canônica.


## Fechamento da inspeção do `siconv_itens_dl`

**Run [43629868488](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43629868488): SUCCESS**, com CRC do ZIP nacional verificado e inspeção estrita de cabeçalho/amostra; manifesto de metadados arquivado. Cabeçalho real:

`ID_ITEM_DL;NOME_ITEM_DL;QTD_ITEM_DL;UNIDADE_ITEM_DL;VALOR_TOTAL_ITEM_DL;DESCRICAO_ITEM_DL;ID_DL`.

**Conclusão documental P0:** a chave `ID_DL` existe no item e na tabela de DL; **`ID_ITEM_PAD` não consta do CSV `siconv_itens_dl`**. A cadeia `pagamento → DL → item da DL` tem chave candidata, mas a cadeia `item da DL → item PAD GND4` **NÃO tem chave direta documentada neste esquema**. A presença do nome/descrição não autoriza equiparar os itens por correspondência textual ou valor idêntico. Os valores `VALOR_TOTAL_ITEM_DL` não são ainda comprovadamente pagamentos líquidos; retenções/tributos e status da DL precisam ser auditados.

A análise dos arquivos pequenos também demonstra que `siconv_pagamento_tributo` e `siconv_ingresso_contrapartida` têm `NR_CONVENIO`, **não têm `NR_MOV_FIN` ou `ID_DL`**, impossibilitando atribuição direta a movimento individual pela chave disponível. `siconv_coordenadas_obra` oferece `ID_PROPOSTA`; `siconv_contrato_cipi` oferece `ID_CONTRATO` e `ID_PROJETO_INVESTIMENTO`, e `siconv_dados_obrasgov_geral` usa `id_projeto_investimento` e `nr_instrumento`, aptos a testes de cardinalidade posteriores.

**Situação de contagens:** esta coleta foi schema+amostra de 1.000 registros por arquivo + CRC integral. A contagem total de linhas nacionais desses novos arquivos **não foi calculada**, e não deve ser inferida de seu tamanho.


## Auditoria de cardinalidade nacional Obrasgov/CIPI — executada

[Workflow 43630077789](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43630077789), `SUCCESS`; relatório agregador de chaves no artefato `inv-sp645-obrasgov-cipi-cardinality` ID `14127537342`. Código `pipeline/qa/audit_inv_sp645_obrasgov_cipi_join.py`. Foram baixados e verificados com CRC três arquivos nacionais, contados os vínculos sem imprimir identificadores ou nomes. Valores **não** foram somados.

| Controle da fonte | Resultado |
|---|---:|
| `siconv_dados_obrasgov_geral`, linhas / projetos únicos | 48.086 / 48.086 |
| Projetos repetidos na tabela geral | 0 |
| Números de instrumento distintos na tabela geral | 48.086 |
| `siconv_contrato_cipi`, linhas | 39.099 |
| Projetos distintos nessa tabela de contratos | 27.458 |
| Contratos com ID de projeto ausente | 0 |
| Linhas de contratos com ID de projeto encontrado na tabela geral | **39.099** |
| Projetos com múltiplos registros de contratos | **3.715** |
| Cardinalidade resultante de join pela chave de projeto, em linhas | 39.099 (sem fan-out adicional, pois tabela geral tem projeto único) |
| `siconv_coordenadas_obra`, linhas | 132.102 |
| Propostas distintas com coordenadas | 61.819 |
| Propostas com duas ou mais linhas de coordenadas | **10.343** |
| Linhas sem `ID_PROPOSTA` | 0 |

**Cuidado:** a tabela geral nacional `siconv_dados_obrasgov_geral` é apenas o conjunto correspondente disponível no Transferegov. Não afirmar que cobre todos os projetos do portal Obrasgov ou todas as obras federais. Contrato CIPI→projeto é uma relação N:1; projeto→coordenadas não foi unido no presente teste porque a tabela de coordenadas se relaciona pela `ID_PROPOSTA`, não pela chave CIPI. Um convênio ou proposta pode ter várias localizações.

**Próxima operação:** vincular os IDs documentais dos instrumentos e das propostas a proponentes paulistas por IBGE7, segregar valores de contrato de pagamentos, conferir geolocalizações e coordenadas externas. Este QA demonstra viabilidade de junção, não o volume de investimento executado.


## Domínio nacional de movimentações financeiras — execução completa

[Run 43630172358](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43630172358) concluído com `SUCCESS`. Arquivo nacional `siconv_pagamento.zip` adquirido sob código `pipeline/acquire/inv_sp645_payment_type_domain.py` em runner temporário, ZIP CRC verificado, leitor integral de linhas e metadados de contagem sem beneficiários, sem valores individuais e sem totais monetários.

- **7.575.512 linhas nacionais examinadas**, conciliando o total anteriormente observado no FED03.
- `TP_MOV_FINANCEIRA`: **`PAGAMENTO A FAVORECIDO COM OBTV` 5.734.760** e **`PAGAMENTO A FAVORECIDO` 1.840.752**, sem outros códigos/denominações na extração.
- `VL_PAGO` — mera classificação léxica do sinal/zero: **7.549.033 não negativos diferentes de zero; 26.451 zeros textuais; 28 negativos textuais**. **Não é valor de pagamento líquido**, nem classifica estorno: exige verificação documental e situação financeira. O algoritmo de sinais não substitui conversão de moeda com Decimal e precisão de centavos.
- Nenhum vazio nas colunas `NR_MOV_FIN`, `NR_CONVENIO`, `TP_MOV_FINANCEIRA`, `VL_PAGO`, `DATA_PAG` e `ID_DL` neste arquivo nacional, segundo o inventário de valores textuais vazios.
- **Limite:** este resultado não verifica unicidade global de `NR_MOV_FIN`, cardinalidade com OBTV, ocorrência de cancelamentos fora da série de pagamento, nem execução de capital. Não produzir soma de dinheiro sem classificação e prova documental.


## Continuidade operacional — segundo ciclo em 14/11/2026

**CGU:** a página oficial https://portaldatransparencia.gov.br/download-de-dados/convenios foi recuperada pelo Crawl2AI e confirma geração de dois conjuntos distintos `Convenios` e `Convenios_OrdensBancarias`, com estrutura/dicionário de dados associado. A seleção por competência ocorre por interface dinâmica; o crawler não extraiu nesta consulta os próprios arquivos ou competências completas. **Não declarar importação de ordens bancárias**. Uso previsto: conciliação da ocorrência de transferências com as etapas Transferegov por chaves documentais; jamais soma automática.

**Obrasgov e especiais:** nesta rodada os endereços gerais https://api-publica.obrasgov.gestao.gov.br/obras e https://api-publica.transferegov.gestao.gov.br/especiais falharam no mecanismo de extração Crawl2AI. Os arquivos Transferegov `siconv_contrato_cipi` e `siconv_dados_obrasgov_geral` tiveram captura e auditoria efetivas via ZIP, **mas não demonstram a cobertura integral da API Obrasgov**. Registrar status como `extração de API pendente`, não como inexistência de registros.

**Nova operação em execução:** auditoria nacional de cardinalidade pagamento/OBTV, código `pipeline/acquire/inv_sp645_payment_obtv_cardinality.py` e workflow `.github/workflows/inv-sp645-payment-obtv-cardinality.yml`, [run 43630776308](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43630776308). A rotina baixa uma vez por dataset `siconv_pagamento` e `siconv_obtv_convenente` no runner isolado, valida CRC integral e utiliza SQLite **temporário** para examinar `NR_MOV_FIN`: cardinalidade de cada lado, chaves repetidas, conflitos entre convênios e documentos, matches e expansão potencial de join. Os identificadores pessoais, documentos, dados bancários e valores individuais **não são exportados**; o SQLite temporário e os ZIPs são descartados. Só o manifesto agregado é arquivado. **Status inicial: workflow acionado, resultado sujeito a confirmação de conclusão e QA.**

As duas fontes são eventos relacionados, nunca devem ser somadas como dinheiro distinto. Se `NR_MOV_FIN` tiver duplicatas ou colisões, nenhuma junção 1:1 será promovida sem prova adicional de chave composta.

**Qualidade e repetibilidade:** a nova rotina faz download temporário com retry limitado, hash SHA-256, controle de domínio e checagem de cardinalidade. Continua pendente um **snapshot bruto durável em R2 privado** e readback; o artefato de CI contém apenas metadados, não o dado nacional persistido. A obtenção de todas as linhas nacionais repetidamente em testes distintos não deve ser naturalizada como estratégia final: consolidar cache/versionamento privado após validação técnica e autorização da gravação.

### Dependência funcional de 72 universos

A validação do build SP645 com RA/RG descobriu que o verificador legado da API v2 exigia somente os 13 universos antigos. A alteração no verificador agora valida a composição completa **72**, derivando as contagens RA/RG da dimensão SEMIL por IBGE7, sem permitir seleção parcial. Outra falha de import de módulo em execução por script (`deployment`) foi corrigida em `deployment/qa_api_v2.py`. Um novo build privado foi iniciado [run 43630697231](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43630697231); aprovação depende de conclusão de todas as verificações, sem implantação pública.

### Gates vigentes

- **Confirmados:** layout de pagamentos/OBTV/DL, ausência de chave PAD no arquivo itens-DL, cardinalidade nacional CIPI↔Obrasgov geral, domínio de tipos e sinais de pagamento, 645 códigos IBGE e novos universos.
- **Em execução:** cardinalidade real pagamento↔OBTV, build privado completo dos 72 universos.
- **Pendentes:** ligação paga↔GND4 comprovada; município de execução comprovado; classificação de estornos e retenções; captura API Obrasgov completa; conciliação CGU por ordens bancárias; SP645 monetário por estágio; persistência imutável e readback em R2 privado.
- **Bloqueados para promoção:** soma de investimentos federais pagos, agregados financeiros por RA/RG/RM/AU e atualização dos dados exibidos ao público.

## Gate técnico territorial encerrado — 14/11/2026

O build privado SP645 com os **72 universos e dados fiscais reais** terminou com `SUCCESS` no [run 43630697231](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43630697231). A validação `deployment/qa_sp645_pages.py --site build/site-sp645` e `deployment/qa_api_v2.py --site build/site-sp645` foi concluída. Contagens do manifesto real: 72 seleções, 16 RA, 43 RG, 645 municípios nas RA, 645 nas RG, `SP_645` como padrão. **A aprovação é do build privado; não significa divulgação dos valores federais de investimento ou implantação pública.** Fonte IBGE7 permanece SEMIL/Seade, sem vínculo com zonas eleitorais.


## Gate R2 de cardinalidade pagamento–OBTV confirmado — execução 43630776308

[GitHub Actions 43630776308](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43630776308), **SUCCESS**, análise nacional com SQLite temporário, ZIPs originais com SHA-256/CRC, descarte de microdados ao término e manifesto agregado em artefato; script `pipeline/acquire/inv_sp645_payment_obtv_cardinality.py`.

| Métrica | Contagem |
|---|---:|
| Linhas nacionais `siconv_pagamento` | 7.575.512 |
| `NR_MOV_FIN` distintos nos pagamentos | **7.575.512** |
| `NR_MOV_FIN` repetidos na tabela de pagamentos | **0** |
| Pagamentos com tipo rotulado `COM OBTV` | 5.734.760 |
| Linhas nacionais `siconv_obtv_convenente` | 3.113.841 |
| `NR_MOV_FIN` distintos na tabela OBTV | **367.022** |
| IDs `NR_MOV_FIN` da OBTV repetidos nessa tabela | **63.364** |
| IDs distintos da OBTV encontrados na tabela de pagamentos | **367.022** |
| Linhas OBTV com correspondência a pagamento | **3.113.841** |
| Linhas OBTV sem correspondência à tabela de pagamentos | **0** |
| Combinações OBTV ↔ pagamentos `SEM OBTV` | **0** |
| IDs de pagamento com colisão de convênio ou `ID_DL` | **0** |

**Implicação metodológica P0:** a correspondência `NR_MOV_FIN` é **um pagamento→muitas linhas OBTV** em parte do corpus, não 1:1. Existem apenas **367.022 movimentações de pagamento** representadas pelas 3.113.841 linhas OBTV. **A multiplicação de linhas de um join não pode multiplicar o valor `VL_PAGO`**, que permanece associado a uma única movimentação; o campo `VL_PAGO_OBTV_CONV` possui unidade e semântica distintas, sujeitas a conciliação de retenções/parcelas. **Não somar as duas fontes** como se fossem despesas independentes.

A distinção dos **5.734.760** pagamentos rotulados `COM OBTV` frente às **367.022** movimentações que aparecem no arquivo `siconv_obtv_convenente` exige investigação de cobertura/modalidade, não supor inconsistência ou ausência de pagamento. `siconv_obtv_convenente` descreve módulo específico da OBTV do convenente, não inventário completo de pagamentos OBTV.

**Regra de agregação futura:** preservar uma tabela de eventos pagos por `NR_MOV_FIN`, em seu grão único, e uma tabela filha dos eventos OBTV com cardinalidade 1:N. A materialização unificada deve fornecer métricas de origem separadas, e eventual reconciliação de valores em inteiros de centavos, sem fan-out de pagamentos. A classificação GND4 ainda requer suporte documental independente.

### Coleta subsequente iniciada

Foi acionada a rotina `pipeline/acquire/inv_sp645_proponent_obrasgov_regional_coverage.py`, workflow [43630964784](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43630964784), para cruzar os ZIPs nacionais de propostas, convênios, coordenadas e pontes CIPI/Obrasgov com a **dimensão IBGE7 SP645**, derivando contagens de cobertura por RA, RG e RM/AU **exclusivamente pelo município proponente**. Ela não classifica localização física nem publica valores monetários. Registrar como resultado pendente até conferir conclusão e manifesto QA.


## Fechamento da cobertura documental territorial SP645 — 14/11/2026

[Run 43630964784](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43630964784), `SUCCESS`. Cinco arquivos nacionais da plataforma Transferegov foram lidos: `siconv_proposta`, `siconv_convenio`, `siconv_coordenadas_obra`, `siconv_dados_obrasgov_geral` e `siconv_contrato_cipi`. As chaves empregadas foram `ID_PROPOSTA`→`NR_CONVENIO`→`nr_instrumento`→`id_projeto_investimento` e `ID_PROPOSTA`→coordenadas, respeitando a natureza e o grão de cada conjunto. O **único papel territorial comprovado neste cruzamento é o município proponente IBGE7**, extraído da proposta com UF SP; não localização física da obra.

| Universo e fato documental | Estado SP645 por proponente | RMRP34 por proponente |
|---|---:|---:|
| Propostas distintas | **134.452** | **6.410** |
| Convênios distintos ligados a propostas | **34.447** | **1.793** |
| Linhas de coordenadas vinculadas à proposta | **10.567** | **441** |
| Projetos Obrasgov ligados por número exato de instrumento e ID CIPI | **4.212** | **218** |
| Linhas de contratos CIPI ligadas aos projetos do passo anterior | **3.730** | **150** |

A seleção nacional de propostas continha 1.160.558 linhas, e a de convênios 288.852. Os 134.452 registros paulistas correspondem a municípios proponentes, não à totalidade das intervenções federais fisicamente localizadas em SP. Os dados de coordenadas somam 10.567 registros relacionados a **5.169 propostas paulistas distintas**, mas o fato de haver lat/long preenchidas não garante geocodificação válida ou localização dentro do município proponente. O recorte de 4.212 projetos deriva de correspondência **exata de identificadores de instrumento** nessa série; exclui modalidades ou projetos não representados nesse encadeamento documental. **Não foram somados valores monetários**.

A classificação regional foi derivada de **645 códigos IBGE7 oficiais**, com composição alternativa de 16 RA, 43 RG, 9 RM e uma AU. As 69 linhas de contagem regional e metadados SHA-256 dos cinco ZIPs estão **persistidas em arquivo versionado permanente**:

[governance/INV_SP645_COBERTURA_REGIONAL_TRANSFEREGOV_OBRASGOV_2026_11_14.json](INV_SP645_COBERTURA_REGIONAL_TRANSFEREGOV_OBRASGOV_2026_11_14.json)

O arquivo foi recuperado do artefato agregado do workflow original `14127424244`, validado novamente e gravado na branch por [run 43631104395](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43631104395), concluído com `SUCCESS`, sem baixar novamente os grandes ZIPs nem persistir dados pessoais. Esse resultado evita a perda documental após o vencimento do artefato de CI.

**Regra analítica:** universos RA e RG cobrem cada um os 645 municípios, mas são classificações alternativas; as contagens por RA não se somam às contagens por RG ou RM/AU. A RMRP aparece como recorte entre as 10 RM/AU, com seus **34 municípios e 218 projetos candidatos** vinculados por proponente, sem caráter de investimento executado.

### Próximos testes concretos

1. Criar uma amostra auditável de projetos RMRP com `ID_PROPOSTA`, `NR_CONVENIO` e `id_projeto_investimento` **em staging privado**, conferindo objetos, valores por etapa e a localização física documental; não expor microdados indiscriminadamente no repositório.
2. Relacionar, sem multiplicação, os pagamentos únicos `NR_MOV_FIN` aos contratos/objetos e `ID_DL`; utilizar OBTV como relação 1:N e manter registros sem conclusão como `nao_classificado`.
3. Consultar Obrasgov por projeto CIPI para obter município executor, obra, estágio, percentual físico, fonte orçamentária e eventual multiplicidade territorial.
4. Conciliar CGU (ordens bancárias) e dados estaduais SIAFEM no mesmo instrumento, com proveniência separada e sem soma de fontes de observação redundantes.
5. Criar snapshot privado versionado das fontes nacionais com SHA-256 e **readback R2**, desde que o workflow tenha credenciais e autorização adequadas. Os resultados preservados em GitHub são **agregados**, não substituem os ZIPs nacionais.


## Retomada em 14/11/2026 — consulta direta à API Obrasgov e amostra de projetos RMRP

A documentação oficial da nova API foi recuperada diretamente de `https://api-publica.obrasgov.gestao.gov.br/obras/openapi.json` (OpenAPI 3.1). Foram identificados, sem suposição de rotas, os endpoints públicos:

- `/obras/data-atualizacao` (última atualização);
- `/obras/projeto-investimento` (inclui `id_projeto_investimento`, `uf_principal`, `pagina` e `tamanho_da_pagina`);
- `/obras/geometria` (aceita identificador do projeto e código IBGE);
- `/obras/execucao-fisica`, `/obras/empenho`, `/obras/contrato`, `/obras/historico-situacao-cancelada-paralisada` e `/obras/estudo-viabilidade`.

Consulta pública a `/obras/data-atualizacao` retornou `2026-11-13T00:00:00`, data declarada **pelo sistema**, distinta da data da consulta e do arquivo Transferegov de novembro. O filtro real de um projeto por `id_projeto_investimento` retornou resposta JSON paginada com campos de nome, situação, espécie, UF, organização responsável e datas; o endpoint de geometria pode retornar conjunto vazio mesmo para projeto existente. Portanto, **ausência de geometria não é prova de ausência física da obra**.

Foi implementada inspeção opcional de amostra de até 218 projetos diretamente ligados por `nr_instrumento` aos municípios proponentes da RMRP no script `pipeline/acquire/inv_sp645_proponent_obrasgov_regional_coverage.py` (opção `--api-sample`). A rotina consulta separadamente `projeto-investimento` e `geometria`, confere o mesmo ID do projeto e conta situação, UF principal, presença de geometria e código IBGE da geometria comparado ao IBGE do proponente. Não armazena nomes ou identificadores dos projetos em manifesto público nem confunde localização do projeto com proponente. Solicitações paginadas usam limite de resposta, timeouts e backoff controlado.

A execução amostral de **40 projetos** foi iniciada no [run 43661453030](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43661453030). **Resultado de situação/geometria deve ser declarado somente após a conclusão do job e verificação do log e do manifesto**. A amostra corresponde aos primeiros 40 identificadores em ordem determinística, não é amostragem probabilística, não fundamenta estimativa de incidência populacional para os 218 projetos.

**Gates seguintes:** revisão integral e versionada dos IDs dos 218 projetos em staging privado, cobertura de localização física (sem converter municípios de proponentes em sítio da obra), verificação de execução física e despesas por projeto, reconciliação de ordens bancárias CGU e desembolsos com status documental. Não agregar pagamentos a despesas de capital sem chave/semântica comprovada.

## Auditoria Obrasgov RMRP — amostra de 40 concluída e exame integral em execução

A execução [43661453030](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43661453030) terminou **SUCCESS** e consultou diretamente a API oficial do Obrasgov por `id_projeto_investimento`, para os primeiros 40 projetos em ordem determinística dentre os 218 associados a proponentes da RMRP. O produto com os agregados e sua procedência foi validado e persistido pelo workflow [43661590440](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43661590440), em `governance/INV_RMRP_OBRASGOV_API_AMOSTRA_40_2026_11_14.json`.

- Correspondências da API de projetos: **40/40**, com **0 erros** e **0 IDs ausentes**.
- Situação declarada: **21 Concluída, 16 Cadastrada, 2 Inacabada e 1 Em execução**; a UF principal foi SP nos 40.
- A consulta de `/obras/geometria` dos 40 IDs retornou **0 linhas de geometria**, com **0 erros de API**. Isso **não significa ausência física de obra ou falta absoluta de coordenadas em outra fonte**; há 441 registros de coordenadas das propostas RMRP no módulo específico `siconv_coordenadas_obra`, que não foram individualmente confrontados nesta amostra.
- A amostra corresponde aos **primeiros 40 IDs em ordem lexicográfica**, portanto **não é aleatória**. Não extrapolar proporções de situação aos 218 projetos nem às 21.068 entradas de `uf_principal=SP` da API.

A consulta à nova API `/obras/projeto-investimento?uf_principal=SP&pagina=1&tamanho_da_pagina=1` retornou **21.068 projetos** para a UF principal SP (consulta em 14/11/2026, fonte com atualização declarada 13/11/2026). A série tem abrangência e definições diferentes dos 4.212 projetos identificados pela cadeia documental de convênios de proponentes paulistas.

**A próxima verificação já foi iniciada** em [run 43661628931](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43661628931), que amplia a consulta da API para **os 218 IDs vinculados à RMRP**, preservando apenas agregados de situação, UF principal e presença de geometria. O resultado completo não deve ser divulgado como concluído sem auditoria da execução e persistência do manifesto.

O novo endpoint do Obrasgov confirma que a ausência de geometria nessa rota não invalida a análise documental de projetos e contratos. Para efetiva territorialização física, a alternativa técnica é avaliar as coordenadas das propostas (incluindo suas multiplicidades), `/obras/geometria` quando presente, e registros identificados por outro campo administrativo de local de execução, com QA de limites e CRS.
