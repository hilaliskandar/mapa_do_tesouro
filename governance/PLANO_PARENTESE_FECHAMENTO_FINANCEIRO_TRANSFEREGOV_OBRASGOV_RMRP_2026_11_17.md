# Parêntese operacional — fechamento financeiro Transferegov e Obrasgov para RMRP34

**Decisão de priorização:** 17/11/2026. **Projeto:** `hilaliskandar/mapa_do_tesouro`; branch `investimentos-territoriais-sp645-20261111`; PR #233 permanece em rascunho. **Regra de release:** `public_release_authorized=false`.

## Atualização executada F00 em 17/11/2026

O inventário F00 foi executado: metadados atuais do Google Drive confirmaram **nove objetos privados** na pasta canônica, incluindo **sete ZIPs nacionais**, staging FED03C/FED04B e pacote FED08B, sem mudança de compartilhamento. O relatório de 15/11 comprova SHA/CRC de readback dos sete ZIPs, **não recalculado nesta sessão**. São 28.503 pagamentos selecionados, 28.256 DL, 39.498 itens DL e 395 registros OBTV associados, já materializados em SQLite privado. Ver [auditoria F00](INV_RMRP_F00_AUDITORIA_ACERVO_FEDERAL_2026_11_17.md) e [inventário verificável](controls/investimentos_sp645/F00_RMRP_FEDERAL_PACOTES_VERIFICADOS_2026_11_17.csv). **F00 concluído no nível de metadados e proveniência; F01 e F02 continuam pendentes de recálculo monetário real.**

## Atualização executada F01/F02 em 17/11/2026

Foram recuperados e validados por SHA-256/CRC os **dois pacotes SQLite reais** FED08B e FED03C; QA `integrity_check=ok` e FKs válidas. Um processamento independente produziu **505 linhas município-ano observadas** para 34 municípios, separando evento de desembolso e movimento de pagamento. **Desembolsos:** 2.537 operações-pai, valor bruto total R$ 714.989.114,47; 2.535 reconciliadas com grupos de empenho, R$ 714.319.393,67; duas exceções mantidas sem correção forçada (R$ 475 mil com diferença de R$ 88 mil e R$ 194.720,80 sem ponte). **Pagamentos nominais brutos:** 28.503 movimentos distintos, R$ 627.287.678,10, sem homologação líquida nem capital GND4 pago. A matriz privada CSV por município-ano, resumo anual e QA foram salvos no Drive privado e recuperados por readback SHA-256 idêntico.

[Relatório F01/F02, SQL, números e restrições](INV_RMRP_F01_F02_MATRIZ_FINANCEIRA_REAL_2026_11_17.md). [Pacote privado Drive](https://drive.google.com/file/d/1fM3fw-jnWEAE5EpUoJk7JTMJAkmzA4YL/view), 10.976 bytes, SHA-256 `5bf3385d7e170cd4e7b7911e933eb97c3be08db4aa677d0c8d1a4502aa3e4913`. **F01/F02 parciais**, pendentes duas exceções, conciliação líquida de estornos/devoluções, natureza efetivamente paga e modalidades F03. `public_release_authorized=false`.

## Repriorização de 17/11/2026 — aquisição antes de reconciliação

A orientação vigente suspende **temporariamente as reconciliações F01/F02**, sem desconsiderar o que foi apurado ou excluir exceções. **Priorizar exclusivamente recuperação e compilação dos dados oficiais ainda ausentes**: (a) valores financeiros das Transferências Especiais e de Gestão de Parcerias no Transferegov; (b) campos de valor de projetos Obrasgov e registros CIPI existentes; (c) completar recortes por município, exercício e modalidade. Não é necessário detalhar localização/execução física.

**Execução inicial efetivada:** compilados do SQLite privado 150 registros de contrato CIPI (134 chaves distintas, R$ 201.335.149,95 de valor global, sem inferir pagamento) e 257 empenhos CIPI (R$ 147.402.874,08, não aditivos), distribuídos por 218 projetos e municípios proponentes. As 743 propostas de Parcerias foram classificadas, **sem valores monetários disponíveis na tabela atual**. Ver [relatório F03/F04](INV_RMRP_F03_F04_COMPILACAO_VALORES_EXISTENTES_SEM_RECONCILIACAO_2026_11_17.md). A execução local das APIs federais encontrou falha DNS e Browserless esgotou cotas; **nenhuma aquisição remota inédita foi confirmada**. Brutos existentes preservados em Drive; artefato ZIP novo gerado localmente, ainda não enviado para Drive/R2.

**Gate de interpretação:** valor do contrato, empenho, desembolso e pagamento são estágios separados e não devem ser somados. Dados sem totalizador, campos ausentes ou endpoints vazios permanecem `null`/pendentes, nunca zero presumido. Suspensão de reconciliação não autoriza chamar esses valores de investimento executado. A expansão estadual SIAFEM externa permanece suspensa no offset 420; `public_release_authorized=false`.

## Atualização de aquisição API em 17/11/2026 — F03/F04

**Acesso oficial recuperado via Crawl2AI; a limitação DNS do executor local não impede as consultas.** Foram efetivamente consultados e preservados, na branch de desenvolvimento, os valores previstos em três módulos:
- **Transferências Especiais:** 628 beneficiários em SP em quatro páginas, 34 identificadores municipais RMRP correspondentes; **284 planos, IDs distintos e 34/34 municípios**, previstos **R$ 93.046.325,06 investimento e R$ 3.257.000,00 custeio**, 2020–2026.
- **Gestão de Parcerias:** **743 propostas distintas**, 34/34 municípios, 2024–2026; `nr_vlr_total=null` em 743/743; `vl_total_planejamento_gastos` presente em **672/743**, somando **R$ 256.473.787,83** de planejamento misto (não pagamento ou capital confirmado).
- **Obrasgov:** **218/218 IDs existentes** consultados por `id_projeto_investimento`, com investimento **previsto federal R$ 416.531.252,99**, anos de cadastro 2022–2026. Os registros por ID estão em 11 lotes, sem erro. Projeto por proponente **não** comprova local físico.

[**Relatório detalhado, QA e referências aos 23 CSVs por fonte**](INV_RMRP_F03_F04_AQUISICAO_API_34_MUNICIPIOS_218_PROJETOS_2026_11_17.md). São três medidas **não aditivas entre si e com FINBRA/SIAFEM/convênios/desembolsos**, por serem estágios previstos ou de planejamento. Nenhum valor foi promovido a investimento executado nem ao painel público; `public_release_authorized=false`.

**Próxima prioridade:** obter eventos monetários de empenhos/ordens bancárias de Especiais e Parcerias, sem reconciliação aprofundada por ora. Novo workflow R2 foi preparado na branch, mas o dispatch retornou 404 (não registrado no catálogo de workflows da branch padrão); não afirmar execução, upload R2 ou readback deste workflow. Dados resumidos filtrados e URLs foram preservados no GitHub; fonte oficial permanece acessível.

## 1. Objetivo e limite do parêntese

Suspender **novos disparos manuais** de lotes SIAFEM da expansão estadual fora da RMRP para priorizar o fechamento da **coleta, conciliação e classificação monetária** das fontes federais **Transferegov e Obrasgov**, usando a RMRP (34 municípios, quatro sub-regiões) como piloto de integração à série FINBRA/SICONFI, TCESP e SIAFEM-SP. Sem necessidade de investigar contratos, endereços, geometrias, status físico, fotos, medições ou cada obra individual.

**Estado preservado no momento da suspensão:** SIAFEM da RMRP tem 238/238 combinações município-ano 2020–2026, 752 instrumentos, 889 convênios-ano, 1.017 pagamentos e R$ 305.521.029,20 em liberações líquidas/estornos, corte 12/11/2026, diferença zero em QA. A expansão SIAFEM externa, exercício 2025, possui **420/611 municípios consultados, 363 reconciliados, 57 inconclusivos, 191 não consultados**, R$ 716.144.696,19 em liberações líquidas/estornos; **próximo offset reservado 420, limit 25**. Não cancelar workflows alheios nem apagar snapshots; antes de retomar a expansão, verificar se houve runs adicionais após 17/11 e sincronizar controles.

## 2. Fotografia federal e o que NÃO deve ser recolhido

**Transferegov:** 6.410 propostas discricionárias, 743 registros de Parcerias, 1.793 convênios, 2.537 desembolsos (2.535 com grupos de empenho reconciliados e duas exceções), 1.240 emendas; extração nacional de pagamentos identificou 28.503 linhas de movimentação associadas a 1.286 convênios de proponentes RMRP. Cobertura territorial de proponentes 34/34 NÃO equivale a cobertura de beneficiários ou execução financeira líquida homologada. Os pacotes já adquiridos e manifestos devem ser reutilizados sem repetição de 80 páginas/API ou downloads integrais quando não exigidos por versão/retificação.

**Obrasgov:** 218 projetos candidatos associados ao município **proponente** RMRP, com pacote privado preservado; **não** equivalem ao universo territorial de obras nem a 218 valores adicionais aos repasses do Transferegov. A fonte de projetos é auxiliar de classificação, vínculo e estágio financeiro, e seus valores só poderão ser apresentados como série isolada se demonstrados por identificador, data, natureza e não duplicação. Um resultado vazio nos módulos de execução financeira não equivale a valor zero.

**Séries já prontas:** FINBRA/SICONFI e TCESP homologadas segundo contrato fiscal existente; SIAFEM estadual RMRP34 2020–2026 exato; não reconsultar nem reescrever produção.

## 3. Programa focal de fechamento

| Bloco | Prioridade | Tarefa executável | Produto e gate |
|---|---|---|---|
| F00 — inventário | P0 | Localizar pacotes originais Transferegov/Obrasgov, hashes, manifests, status Drive/R2 e SQL staging já usados em FED01–FED21; reconciliar inventário por modalidade | Uma linha por fonte-modalidade-ano e função territorial; snapshot de origem conferido, sem redownload desnecessário |
| F01 — desembolso D/L | P0 | Reutilizar os 1.793 convênios/2.537 desembolsos e concluir as duas exceções; montar tabela de fluxo para cada `NR_CONVENIO`/data/município com negativos e sinais preservados | 2.537/2.537 reconciliados ou cada exceção documentada e isolada; não confundir desembolso com pagamento ao fornecedor |
| F02 — pagamento/OBTV/DL | P0 | Inspecionar domínios reais de `TP_MOV_FINANCEIRA`, `NR_MOV_FIN`, `NR_CONVENIO`, `ID_DL` em `siconv_pagamento`, `siconv_obtv_convenente`, `siconv_dl`, `siconv_itens_dl`; fechar cardinalidade 1:N, reversões e tributos | Tabela monetária líquida sem repetição do fato-pai; dicionário de sinais, datas, falhas e teste de amostra por classe. Se vínculo a GND4 final não é comprovável, manter `gnd4_pago=null` |
| F03 — modalidades adicionais | P0 | Fechar recortes de Parcerias e Especiais; conferir transferências legais e modalidades pertinentes via fontes independentes; classificar registros apenas quando beneficiário/valor/ano e chaves oficiais verificáveis | Matriz das modalidades com `completo`, `parcial`, `nao_coberto` ou `erro`; valores disponíveis em fatos separados; sem presumir completude da API D/L em implantação |
| F04 — Obrasgov financeiro | P1 | Inventariar módulos e campos de valor oficiais, paginação e 218 candidatos preservados; identificar IDs/CIPI e vínculos documentados a instrumentos federais; testar cobertura territorial por proponente/beneficiário/executor sem exigir pin geográfico | Tabela por projeto e natureza do valor (estimado, contratado, repassado, executado), ano e fonte, com `null` explícito quando indisponível; cardinalidade e deduplicação; **não adicionar** Obrasgov ao total de transferência federal por simples coincidência |
| F05 — agregação RMRP | P0 | Integrar em SQLite **isolado** eventos de origem municipal, estadual e federal, por 34 municípios e quatro sub-regiões, com estágio e fonte distintos; QA financeiro e de territorialidade | Matriz RMRP34 × ano × governo × modalidade × estágio, valores e cobertura com `null` para ausentes; SQL de regressão com soma dos 34 e sub-regiões e prevenção de dupla contagem |
| F06 — prévia e aceite | P1 | Produzir consulta e tabelas privadas com duas perspectivas: financiamento e execução; documentar lacunas e limites | Relatório de aceite por indicador, seção comparativa RMRP e prévia API v3 privada; sem deploy sem autorização expressa |

## 4. Critério de totalização e não aditividade

**Perspectiva A — financiamento e transferências:** exibir, lado a lado, (1) investimentos realizados pelos municípios por estágio de despesa; (2) repasses estaduais SIAFEM líquidos; (3) repasses federais Transferegov líquidos; (4) demais modalidades identificáveis, com conciliação e fonte. **Não apresentar soma direta de (1)+(2)+(3) como investimento total territorial**, pois repasses podem financiar a despesa municipal.

**Perspectiva B — investimento público efetivamente executado no território:** despesas municipais executadas no conceito e exercício definidos **mais** despesas de execução direta estadual e federal territorialmente demonstradas, **somente** com vínculos e regras de não sobreposição. Ausência de fatos de execução direta deve gerar cobertura incompleta, não zero inferido.

Distinções obrigatórias: previsto/celebrado; empenhado; desembolsado/transferido; pago ao fornecedor; liquidado/executado pelo município; custo/valor de projeto Obrasgov. O mesmo evento financeiro pode figurar em mais de uma plataforma. Agregação requer ID oficial de origem e vínculo, sem junção por valor ou data. `GND4` do plano aprovado não comprova pagamento de capital. O recorte por proponente não equivale a localização ou beneficiário.

## 5. Regras metodológicas e QA

- Níveis de confiança por `fonte, modalidade, municipio_IBGE7, ano, etapa`; chave natural de evento e versão do snapshot; leitura de ZIP CRC, SHA256 e readback privados.
- Financeiro em **centavos inteiros**, retenções e estornos explicitados; deduplicação `NR_MOV_FIN` e cardinalidade do par pagamento–OBTV–DL; evitar repetição de `VL_PAGO` em tabela filha.
- Recorte territorial: distinguir proponente, beneficiário e executor; associar a RMRP somente com vínculo oficial. Restringir o escopo da primeira entrega a valores associados documentalmente aos 34 municípios, não afirmar que são todos os investimentos territorialmente ocorridos.
- Temporalidade: manter o período real de cada fonte; não impor falsos zeros em exercícios sem consulta ou sem disponibilização. Usar coluna `fonte_atualizada_em`.
- Gate de bloqueio por indicador, e não por relatório inteiro. Dados de convênio ou desembolso reconciliados podem integrar prévia privada mesmo se não houver GND4 final.
- Não requerer prova de execução física de obra, geocodificação ou investigação de cada contrato para a **fase financeira**; exceções passam à trilha E01 se afetarem número material ou ligação essencial.

## 6. Sequência imediata e ponto de retomada

1. **F00:** inventariar e verificar bytes/hash de pacotes RMRP já preservados e os manifestos FED; classificar o que falta coletar e o que falta somente conciliar.
2. **F01–F02:** fechar desembolsos e semântica de movimentos a partir dos **sete ZIPs oficiais já preservados e auditados**, inclusive `siconv_itens_dl` de 548.549.412 bytes, cujo SHA-256 de readback foi registrado em 15/11/2026. Não redownload, salvo prova de retificação/versionamento ou indisponibilidade da cópia privada.
3. **F03–F04:** fechar modalidades financeiras e Obrasgov somente quanto a valores; registrar módulos sem cobertura como indisponíveis, não como ausência de obras.
4. **F05–F06:** produzir quadro anual integrado e prévia privada, com limites explícitos e gate de homologação.
5. Retomar SIAFEM externa no **offset 420** somente após o encerramento deste parêntese ou nova decisão de prioridade; preservar as 57 consultas inconclusivas em fila separada.

**Fontes documentais:** [plano operacional vigente](PLANO_OPERACIONAL_COLETA_SISTEMATICA_TRANSFERENCIAS_SP645_2026_11_16.md), [auditoria documental](AUDITORIA_DOCUMENTAL_APIS_TRANSFEREGOV_OBRASGOV_SIAFEM_2026_11_14.md), [relatório Obrasgov RMRP](INV_RMRP_FED04A_AUDITORIA_LOCALIZACAO_2026_11_15.md), [série exata SIAFEM RMRP34](RELATORIO_INV_RMRP_SIAFEM_SERIE_ANUAL_EXATA_2020_2026_2026_11_12.md), [série externa até offset 395](INV_SP645_S03_LOTES_25_OFFSET_370_395_2025_2026_11_17.md), README da RMRP.
