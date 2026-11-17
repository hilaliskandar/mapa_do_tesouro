# Auditoria documental de aquisição de investimentos — Transferegov, Obrasgov, CGU e SIAFEM-SP

**Data de referência:** 14/11/2026. **Escopo:** coletores do PR #233 na branch de desenvolvimento, sem promoção à base produtiva. **Método:** confronto direto de páginas governamentais e catálogo atual, leitura dos scripts `inv_rmrp_transferegov_join.py`, `inv_rmrp_fed02_crosswalk.py`, `inv_rmrp_fed03_payment_join.py`, `inv_rmrp_fed03_payment_layout.py`, e logs GitHub Actions. Distinguir evidência documental, falha comprovada e hipótese de aprimoramento.

## Falha comprovada P0 — nome de OBTV incorreto

O catálogo atual `https://api-publica.transferegov.gestao.gov.br/downloads` (65 ZIPs, atualização indicada 14/11/2026) oferece **`siconv_obtv_convenente.zip`**, e não `siconv_obtv.zip`. A execução 43612546925 obteve HTTP 404 porque usou nome pressuposto. NÃO atribuir o erro à indisponibilidade do módulo OBTV como um todo. **Correção aplicada** ao script FED03: `siconv_obtv_convenente`, com sondagem adicional de `siconv_dl` e `siconv_empenho_desembolso`, commit `c3880361955e809988c71c758bc034763b202399`. Execução de verificação: https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43618166707 . Só considerar a correção validada se o job e seus manifests confirmarem schema e integridade.

O mesmo catálogo oferece arquivos essenciais ainda fora da cadeia: `siconv_itens_dl.zip`, `siconv_pagamento_tributo.zip`, `siconv_ingresso_contrapartida.zip`, `siconv_coordenadas_obra.zip`, `siconv_dados_obrasgov_geral.zip`, `siconv_contrato_cipi.zip`, `siconv_acomp_obras_contratos_medicoes_modulo_empresas.zip` e `siconv_acomp_obras_valores_itens_medicao_modulo_empresas.zip`. **Não presumir a chave** de nenhuma dessas relações sem ler o layout real.

## Alerta P0 — semântica dos pagamentos

O CSV nacional `siconv_pagamento` apresentou **7.575.512 linhas** (execução 43617744602), com colunas `NR_MOV_FIN`, `NR_CONVENIO`, `IDENTIF_FORNECEDOR`, `NOME_FORNECEDOR`, `TP_MOV_FINANCEIRA`, `DATA_PAG`, `NR_DL`, `DESC_DL`, `VL_PAGO`, `ID_DL`, `DATA_EMISSAO_DL`. O script FED03 atual conta linhas por convênio, **não verifica domínio e sinais de `TP_MOV_FINANCEIRA`**, não verifica unicidade de `NR_MOV_FIN`, não avalia cancelamentos/estornos, não confere separadamente data do documento versus data do pagamento, nem vincula os itens de DL à natureza econômica do PAD. Portanto, usar apenas como **movimentações documentadas**. Não denominar `28.503` linhas de 'pagamentos líquidos' ou 'investimentos'.

A execução 43617824183 confirmou `28.503` linhas nacionais vinculadas a **1.286** convênios dos proponentes RMRP (34/34 municípios), com total nacional 7.575.512. Não somar o valor de OBTV, desembolso, documento de liquidação e pagamento em uma mesma medida: podem ser etapas de uma só cadeia financeira.

O tutorial oficial de pagamento por OBTV diferencia situação, valor original da DL, valor bruto e valor pago ao favorecido. O tutorial de Documento de Liquidação mostra, adicionalmente, tributos, contribuições, retenções e **itens do documento relacionados a itens do Plano de Aplicação**. Essa é a trilha promissora para identificar aplicação de capital **sem rateio presumido**: `NR_CONVENIO -> ID_DL -> itens DL -> ID_ITEM_PAD`, caso os identificadores reais do CSV suportem a junção. Não assumir equivalência entre `VL_PAGO` e valor do GND4 sem verificar a cadeia.

## Alerta P1 — horizonte e modalidades

O comunicado oficial 24/2026 informa implantação gradual da API de Discricionárias/Legais: atos preparatórios até 31/10/2026, instrumentos até 28/02/2027, execução financeira até 30/06/2027 e obras até 31/10/2027. A primeira entrega de atos preparatórios foi anunciada em 28/10/2026. **Não substituir a série histórica CSV nacional pela API parcialmente implantada.** Manter conectores independentes de Transferências Especiais, Parcerias, Fundo a Fundo e TED; cada modalidade exige identidade do beneficiário, execução e natureza de capital próprias, sem assumir equivalência metodológica.

A dimensão física Obrasgov é **não aditiva** aos fluxos de financiamento. O portal novo `https://api-publica.obrasgov.gestao.gov.br/obras` descreve atualização pelos gestores, situação, execução física e financeira e localização. A localização do projeto não é automaticamente o município proponente/beneficiário, e um projeto pode ter financiamento de múltiplos entes. Confrontar IDs CIPIs e documentos, não apenas proximidade espacial ou semelhança de nomes.

## Alerta P1 — fonte estadual SIAFEM

A página de Pesquisa Composta informa expressamente que só apresenta convênios com alguma liberação **desde agosto de 2007**, independentemente da assinatura, e que valores negativos são **cancelamentos ou estornos de pagamentos**. Assim, ausência de convênio no resultado **não** prova inexistência de convênio celebrado. O filtro `Tipo = Investimento` autoriza identificar o universo de **liberações estaduais classificadas como investimento pela fonte**, não investimentos liquidados pelo município. Guardar pagamento bruto, estorno, montante líquido, período de referência, situação do convênio e atualização declarada da página.

## Alerta P1 — dupla contagem e fonte CGU

O Portal da Transparência publica o download de convênios com arquivos **Convênios** e **Convênios_OrdensBancarias**, com dicionário; publica documentos de empenho/liquidação/pagamento e emendas, com periodicidades próprias. Esses arquivos devem ser utilizados como **conciliação independente**, e não automaticamente adicionados aos eventos Transferegov: a mesma ordem bancária pode aparecer em mais de uma base.

## Alerta P1 — ingestão e reprodutibilidade

O auxiliar `download()` atual escreve diretamente no arquivo de destino, baixa sem backoff documentado de HTTP 429/5xx, não verifica hash de um snapshot previamente conhecido e usa sempre a versão corrente da fonte. Recomenda-se download para arquivo temporário, verificação de ZIP CRC, manifesto com origem e momento da consulta, checksum SHA256, membros e layout, **commit atômico** no staging e readback após persistência R2. Anotar versão, data de atualização da fonte, competência histórica e data local da extração separadamente. Evitar reler arquivos nacionais pesados em vários workflows independentes; baixar uma vez por versão e alimentar etapas dependentes com cópias privadas imutáveis. Não usar `errors="replace"` na decodificação silenciosamente sem contar/reprovar caracteres substituídos.

## Alerta P2 — cobertura e territorialização

As consultas por `COD_MUNIC_IBGE` na base de propostas abrangem **proponentes**, não necessariamente todos os investimentos executados na RMRP. Complementar por `MUNICIPIO` e UF dos itens PAD, Obrasgov e programas com beneficiário multiterritorial. Documentar que 7.891 itens aprovados GND4 têm correspondência nominal com RMRP, 20 apontam para outras localidades de SP e seis para outras UFs; sete dos 7.891 registram destino RMRP diverso do proponente. Correspondência nominal exige confirmação por chave oficial; município fora do recorte pode não ser erro na origem.

A QA de campo `GND4` e `SIT_ITEM=APROVADO` mede um plano aprovado, **não sua execução**. Filtro da situação deve ser aplicado sem transformar valores vazios em 'aprovado'. A versão atual falha em caso de qualquer mudança nas contagens históricas `6.410`, `1.793` ou `7.917`: tratar o desvio como sinalização de nova fotografia ou retificação a auditar, e não necessariamente falha de dados.

## Ordem corrigida de implementação

**P0** Corrigir e testar nomes de arquivos contra catálogo oficial; classificar `TP_MOV_FINANCEIRA` e documentar sinais/cancelamentos; ler `siconv_dl`, `siconv_itens_dl`, `siconv_obtv_convenente`, `siconv_empenho_desembolso` antes de formular junções monetárias.

**P1** Implementar ingestão nacional imutável e incremental no R2 privado com manifestos/checksums/readback; aplicar cruzamento real de IDs DL/item PAD, reconciliação com CGU; auditar amostra de cada classe de movimento; garantir não aditividade de fonte e estágio.

**P2** Completar projetos/território com Obrasgov, coordenadas de obra e execução direta estadual, avaliar modalidades fora de convênio e validação de municípios pelo cadastro nacional. Publicar só depois dos gates documentados.

## Fontes consultadas em 14/11/2026

- Portal e catálogo novo: https://api-publica.transferegov.gestao.gov.br/ e https://api-publica.transferegov.gestao.gov.br/downloads
- Dicionário de dados CSV apontado pelo portal novo: https://www.gov.br/transferegov/pt-br/ferramentas-gestao/paineis-gerenciais/arquivos/modelo-dados-csvs-discricionarias-e-legais.zip/@@display-file/file
- API e cronograma: https://www.gov.br/transferegov/pt-br/ferramentas-gestao/api-de-dados-abertos-transferegov.br e https://www.gov.br/transferegov/pt-br/comunicados/comunicados-gerais/2026/comunicado-24-2026-cronograma-de-disponibilizacao-da-apis-de-dados-abertos-do-discricionarias-legais
- Tutorial pagamento OBTV: https://www.gov.br/transferegov/pt-br/manuais/transferegov/discricionarias/execucao/9-tutorial_pagamento-de-fonecedores-por-meio-de-obtv_convenios_convenente.pdf
- Tutorial Documento Liquidação: https://www.gov.br/transferegov/pt-br/manuais/transferegov/discricionarias/execucao/8-tutorial_documento-de-liquidacao_convenios_convenente.pdf
- Obrasgov: https://api-publica.obrasgov.gestao.gov.br/ e https://www.gov.br/obrasgov/pt-br/ferramentas-de-gestao-e-transparencia/api-de-dados-abertos-obrasgov-br_novo
- Sefaz-SP: https://www.fazenda.sp.gov.br/TransferenciaVoluntaria/Sistema/Novo/PesquisaComposta.aspx
- CGU: https://portaldatransparencia.gov.br/download-de-dados/ e https://portaldatransparencia.gov.br/download-de-dados/convenios

**Limites:** foram lidos os catálogos e documentação HTML, e verificados os logs e scripts do repositório; não foi extraído integralmente o modelo de dados ZIP nesta auditoria, nem o conteúdo linha a linha de `siconv_dl` e `siconv_itens_dl`. As chaves de junção sugeridas permanecem hipóteses de trabalho até inspecionar esses esquemas.
