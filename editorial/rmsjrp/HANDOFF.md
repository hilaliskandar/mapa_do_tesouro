# Handoff — Fase I RMSJRP
**Data:** 2026-11-09 | **Branch de execução:** `audit/rmsjrp-fase-i-2026-11-09`.

## Entregas verificadas
- Fonte DCA estadual Drive 2013–2025 efetivamente lida, 481 pares RMSJRP e 351 combinações variável/ano de cobertura; `MATRIZ_COBERTURA_DCA_2013_2025.csv`.
- Fonte Gate C 2025 e Gate D 2025 efetivamente lidas. 774 valores DCA vs Gate C conciliados (zero divergências acima de R$ 0,01); `MATRIZ_COBERTURA_LEGAL_2025.csv`.
- Sub-regiões PDUI: São José do Rio Preto 14; José Bonifácio 11; Tanabi 6; Nova Granada 6; mapeadas por IBGE em `MUNICIPIOS_SUBREGIOES_2025.csv`.
- Relatório substantivo: `RELATORIO_FASE_I_2026_11_09.md`.
- TCESP: workflow read-only executado com sucesso no run `42559912064` e artifact `13648618790`. R2 readback SHA aprovado para três produtos privados. 111/111 investimentos liquidados observados e 111/111 pares TCESP × DCA com diferença zero centavos. Recurso permanente: `rmsjrp/fase1/2026_11_09/tcesp/`.
- Nenhum arquivo de origem alterado; nenhuma publicação realizada.

## Bloqueadores e pendências
- TCESP confirmado; não executar nova coleta. Verificar somente as fontes legais faltantes por cobertura variável (RREO 18/37, DTP 18/37, DC/RCL 17/37, DCL 18/37; CAPAG 37/37).
- Bases RREO/RGF têm cobertura de 17–18/37 para vários indicadores legais em 2025; verificar complementos internos. CAPAG 37/37.
- Deflator, população por ano, geometria e CRS para fechar G01.
- Hash DCA recalculado da cópia binária R2 e aprovado no run `42559912064`; a leitura de Drive foi textual.

## Próxima ação exata
Após incorporar o PR desta Fase I, começar G04 com exame interno das ausências RREO/RGF, definição do IPCA médio anual e base de setembro/2026, série populacional e geometria EPSG:4674. Não recolher DCA/TCESP. Atualizar relatório e status ao encerrar cada gate; verificar PR/commit na main.


## Continuidade após G04 — 09/11/2026
- **Execução:** [run 42561177880](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42561177880) `success`, artifact `13648798649`; script `editorial/rmsjrp/build_indicadores_g04.py`; `IPCA_MEDIA_ANUAL_SET2026.csv`.
- **Resultados:** 481 séries município-ano e 65 território-ano (quatro sub-regiões + total RMSJRP), 2013–2025; ausência preservada. Receitas correntes 2023/2024/2025: R$ 5.928.863.624,96 / 6.618.138.707,79 / 7.252.878.267,79 nominais. Investimentos liquidados nominais R$ 444.230.252,48 / 480.737.206,37 / 208.056.124,00; investimentos reais set/2026 R$ 513.232.108,92 / 532.167.431,30 / 219.312.039,99.
- **Persistência:** R2 privado `rmsjrp/g04/2026_11_09/`, três objetos com hashes/readback no `RELATORIO_G04_2026_11_09.md`. Não reconstruir dados de fonte externa.
- **Ressalvas:** fatores do IPCA média anual reproduzidos do Lote 17 RMRP (referência setembro/2026 7695,82); denominação populacional 2025 é repetição numérica de 2024 para 37/37 municípios, não nova estimativa observada. Falta definir cartografia métrica EPSG:4674 e ampliar RREO/RGF apenas a partir de acervo disponível, se possível.
- **Próxima ação:** executar G05 em lotes: tabela 2023–2025 regional e por quatro sub-regiões; explorar contribuições municipais para variação real 2023–2025; mapas somente com CRS comprovado; nenhuma atribuição causal antes de investigação. Iniciar novo chat lendo este arquivo, README e relatório G04, verificar commit atual de `main` e readback R2; após lote atualizar todos os registros de estado.


## Continuidade após G05-A/B/C — 09/11/2026
- **GitHub Actions comprovados:** [G05-A run 42561961530](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42561961530), [G05-B run 42562212589](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42562212589) e [G05-C run 42562450625](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42562450625), todos `success`, artifacts `13649986299`, `13649449797` e `13650151673`.
- **Dados e QA:** R2 privado `rmsjrp/g05/2026_11_09/`: 15 território-ano 2023–2025, 15 variações territoriais, 111 contribuições municipais, 6 comparações polo/demais e 3 contagens de tendência; todos com paridade 111 pares TCESP/DCA. 2024–2025 investimento real regional −R$ 312,86 milhões; 29 municípios com queda, oito com aumento; polo −R$ 220,83 milhões. Fonte IPCA: média anual RMRP Lote 17, preços setembro/2026.
- **Programas e ações:** scripts e CSVs auditados 4.884 movimentos por chave órgão/programa/ação, 480 movimentos ranqueados. R2 `rmsjrp/g05/2026_11_09/programas_acoes/`, três arquivos com hashes descritos no relatório G05. Atenção a recodificações e estágios; cifras programáticas são NOMINAIS, enquanto quadro metropolitano é REAL.
- **Cartografia:** IBGE malha SP municipal 2022 (`SP_Municipios_2022.zip`, SHA `341664fdb610df9b92a8f01546e1a83474135cf686c4dcf6c2e0ea91552b0013`), CRS da PRJ EPSG:4674, 37/37 geometrias válidas, sem simplificação; dois mapas PNG e GeoJSON recortado no R2 `rmsjrp/g05/2026_11_09/cartografia/`. QA espacial de CRS, validade e cardinalidade, não auditoria topológica integral. Conferência visual realizada.
- **Relatório de resultados e hashes:** [`RELATORIO_G05_LOTE_A_2026_11_09.md`](RELATORIO_G05_LOTE_A_2026_11_09.md), incluindo complementos G05-B/C.
- **Situação atual:** G05-A/B/C QA técnico aprovado; **G05-D ainda PENDENTE**. A análise substantiva dos programas/ações mais relevantes deve confrontar contas, orçamentos, obras, contratos e classificações antes de afirmar causas. Especial atenção a programas Prefeitura SJR 9, Olímpia 45 e SEMAE SJR 31.
- **Ação exata seguinte:** revisar possível recodificação e documentos primários dos programas principais; após confronto, produzir análise G05-D; integrar mapas junto às respectivas seções do relatório, sem mover todas as figuras para atlas isolado; atualizar README, STATUS e manifesto. Não iniciar G06 ou fichas sem qualificar conclusões como preliminares.


## Handoff G05-D — verificação documental parcial — 09/11/2026
- **Produtos na `main` após PR desta etapa:** `RELATORIO_G05D_DOCUMENTAL_2026_11_09.md`, `MATRIZ_EVIDENCIAS_G05D_2026_11_09.csv`, `qa_g05d_evidencias.py`; método e links de fontes documentados em cada registro.
- **QA efetivo:** [run 42563455585](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42563455585) `success`, artifact `13650855090`, 10/10 lançamentos nominais coincidindo com G05-B R2 em centavos, SHA da matriz `04fdb0b0867e1e9386dcf50108c1cce1d1b3a8649fae2684b8693488b4ea6036`. Original TCESP R2 intacto.
- **Achados:** Rio Preto Prefeitura programa 9 concentração em obras urbanas, ações 1003/1004; SeMAE tem obras materialmente em andamento em 2025 confirmadas por ARES-PCJ 34/2025. Olímpia possui concessão Sabesp desde 2023, programa 45 com liquidação 2024 e sem mesma chave em 2025; programa 31 aumentou mas não se comprovou equivalência. Monte Aprazível ação 1010 tem leis de crédito estadual e federal em 2024, que NÃO representam liquidação.
- **Fontes primárias:** PPA São José do Rio Preto, parecer ARES-PCJ, contrato 398/2023 da Prefeitura de Olímpia, portal municipal de obras, leis 3.978/2024 e 3.997/2024 de Monte Aprazível, todos com URLs no relatório e matriz. Consulta Crawl2AI falhou; recuperação alternativa utilizada. Screenshots dos PDFs falharam; somente extração textual foi conferida.
- **Status:** G05-D `in_progress` por falta de vínculo contrato–empenho–medição de algumas chaves; não afirmar efeito causal da LC 200/2023. **Próxima ação exata:** recuperar documentos de contratos e execução física das dez chaves selecionadas; cotejar cronologia e códigos; após qualificar evidências, encerrar G05-D editorialmente. Preservar G05-A/B/C, mapas e hashes; então abrir G06 com hipóteses condicionais.


## Handoff — G05-D, segunda diligência contratual — 09/11/2026
- **Estado precedente:** G05-A/B/C com QA e R2; G05-D com matriz inicial de dez chaves, [run 42563455585](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42563455585) aprovado, 10/10 correspondentes em centavos ao TCESP.
- **Novos produtos:** `RELATORIO_G05D_DILIGENCIAS_COMPLEMENTARES_2026_11_09.md` e `G05D_DILIGENCIAS_COMPLEMENTARES_2026_11_09.csv`, sete entradas sobre contratos, outorga, obras e caminhos de diligência. Registro GitHub versionado, não alterações na base fiscal.
- **Olímpia:** SEC 20-F Sabesp 2024 confirma empréstimo para outorga fixa, segunda parcela R$ 80,707 milhões; portal de dados abertos tem recursos JSON de obras 2024/2025. **Não comprovado** pareamento com TCESP programa 45 ou migração para 31.
- **Monte Aprazível:** contrato 08/2024, R$ 1.772.387,89, aditivo de R$ 395.147,63, vigência até junho/2025, e concorrência 01/2024 R$ 635.499,00. **Ainda ausente** correlação com empenhos, medições e liquidação ação 1010.
- **São José do Rio Preto:** não foi identificada correspondência com contratos individuais das ações 1003/1004 ou SeMAE 1029. Não inferir causalidade ou confundir empenhos/contratos com liquidações.
- **Método:** descoberta web e documentos oficiais priorizados; Crawl2AI falhou tecnicamente; screenshots de PDFs de diários também falharam. Excertos textuais e URLs registrados; não declarar renderização validada.
- **Próxima ação exata:** recuperar JSON 2024/2025 de obras Olímpia, identificar códigos de contrato e comparar com TCESP; buscar empenhos e medições de Monte Aprazível 08/2024 e concorrência 01/2024; localizar pagamentos/liquidações por código de ação da Prefeitura Rio Preto 1003/1004 e SeMAE 1029. Atualizar relatório, matriz e README, conservando estado G05-D `in_progress` até evidência adicional.


## Retomada após verificação documental — 09/11/2026
- PR #219 verificado como incorporado à main (commit `fb97fca60a0b4702005ffe4a25720a98dfb48c21`); arquivos README, relatório, matriz de sete fontes e status recuperados.
- Ver [`VERIFICACAO_CONSISTENCIA_G05D_2026_11_09.md`](VERIFICACAO_CONSISTENCIA_G05D_2026_11_09.md). URLs oficiais de obras Olímpia `.../obras/2024` e `.../obras/2025` respondem JSON, mas são listagens com projetos iniciados em outros anos e atualizados retrospectivamente; ausência de identificadores de empenho/ação TCESP. Usar apenas como fonte auxiliar de identificação de obras, não somar como despesa anual.
- Contrato Olímpia 398/2023 e aditivo Monte Aprazível 08/2024 conferidos em páginas oficiais; não se demonstrou pareamento com liquidações.
- Controle G01 corrigido: malha EPSG:4674 está auditada no G05-C; permanecem ressalvas sobre população 2025 e deflator IPCA.
- **Estado fiel:** G05-A/B/C QA aprovado, G05-D `in_progress`. Ação: capturar dados oficiais de obras com hash, cruzar por contrato/empenho/medição e nunca converter valores de contrato em despesas liquidadas. Atualizar README e matriz ao concluir cada lote.


## Handoff — extração de obras de Olímpia (G05-D), 09/11/2026
- O endpoint de obras de Olímpia **foi recuperado de forma efetiva** por workflow [42565405140](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42565405140), status `success`, artifact temporário `13651640345`. São **57 registros indexados em 2024**, **25 em 2025**, 82 entradas e 70 títulos distintos, com 12 títulos comuns e valores cadastrais iguais nos dois conjuntos.
- QA temporal: 27/57 obras com início anterior a 2024; 15/25 com início anterior a 2025; 20 atualizações posteriores a 2024 e oito posteriores a 2025. **Não são snapshots anuais da despesa ou liquidação**, e não há chave de contrato, ação TCESP ou empenho nos oito campos recuperados.
- Fonte: `https://www.olimpia.sp.gov.br/portal/dados-abertos/obras/2024` e `.../2025`. Quatro produtos com SHA e readback aprovados no R2 `rmsjrp/g05d/2026_11_09/olimpia_obras/`; CSV normalizado de 82 linhas SHA `c9c304f6a3b0e83dcd168ebd2ceb539c43c934cd08ef384ddc3d6b62eea51689`. [Relatório específico](RELATORIO_G05D_OBRAS_OLIMPIA_2026_11_09.md).
- **Próxima ação exata:** identificar recursos do conjunto de dados oficiais de contratos Olímpia; confrontar objeto/título como **candidatura apenas**, exigindo contrato/processo/empenho/medição e documento de prova antes de casar com as despesas TCESP. Em paralelo, continuar diligências Monte Aprazível 08/2024 e Rio Preto 1003/1004/SeMAE 1029. Manter G05-D `in_progress`. Atualizar README e matriz de evidências após cada vínculo validado.


## Handoff — contratos de Olímpia e comparação com obras — 09/11/2026
- **Run 42566965367** `success`: `auditar_contratos_olimpia_g05d.py` recuperou endpoints oficiais 2024/2025, 1.396 + 1.116 linhas, **543 sobreposições de chaves compostas entre endpoints**, **1.958 chaves compostas distintas**. 11 campos, nenhum objeto/descrição, empenho, medição ou ação TCESP. Fontes CKAN download/API retornaram 404 no Actions; não insistir na coleta quebrada sem diagnóstico. Inventário R2 `rmsjrp/g05d/2026_11_09/olimpia_contratos/`, CSV SHA `e62c12c555843d8a3600b223096921cfe6e742987d1c9b0a65fd2ea1e6eb0b8f`; JSONs e QA com hashes em [relatório](RELATORIO_G05D_CONTRATOS_OLIMPIA_2026_11_09.md).
- **Run 42567153224** `success`: `qa_g05d_vinculos_contratos_obras.py` verificou 3/3 candidatos por número do contrato, processo, fornecedor e valor contra R2; contratos 558/2023 anel viário, 189/2024 recape CBUQ, 115/2024 duplicação da Via João Custódio. Duas entradas por título no cadastro de obras; duplicidade não significa execução dupla. Matriz [G05D_OBRAS_CONTRATOS_CANDIDATOS_2026_11_09.csv](G05D_OBRAS_CONTRATOS_CANDIDATOS_2026_11_09.csv). QA persistido no R2 `rmsjrp/g05d/2026_11_09/olimpia_vinculos/`.
- **Proibições:** não somar listagens dos endpoints, não chamar 1.958 de contratos jurídicos únicos sem reconciliação, não confundir valor de contrato/obra com liquidação TCESP, não atribuir programas 45/31 aos três casos. Não inferir efeitos da LC 200/2023.
- **Próxima operação:** localizar empenhos e medições dos processos 136344/2023, 137300/2023, 140113/2023 e cruzar com ação orçamentária; prosseguir em paralelo Rio Preto e Monte Aprazível. G05-D `in_progress`; sem deploy público.


## Retomada após a diligência de aditivos — 09/11/2026
- **Novos arquivos:** `RELATORIO_G05D_ADITIVOS_2026_11_09.md` e `G05D_ADITIVOS_OLIMPIA_2024_2025.csv` (oito aditivos selecionados, não um censo de todos). Fonte direta: fichas oficiais Prefeitura de Olímpia contratos 558/2023, 189/2024, 115/2024. Nenhuma alteração das bases TCESP/DCA.
- **Evidência:** anel viário tem cinco aditivos datados de 2025, entre eles prorrogação por chuvas e serviços de drenagem e referência expressa a reprogramação sem novo empenho no aditivo de 26/08/2025. CBUQ: acréscimo R$ 1.198.286,05 em 15/04/2025 e prorrogação em 13/06/2025; duplicação João Custódio: aditivo em 26/11/2024 com acréscimo/supressão. A ficha marca licitação concluída, NÃO conclusão física.
- **Bloqueio de conciliação:** não se identificaram empenhos, medições e liquidações individuais por esses contratos. SMARAPD não carregou no Browserless; Crawl2AI falhou; anexos PDF dos termos não foram recuperados. Não declarar acesso ou conferência de PDFs inexistentes; não declarar que não houve pagamentos.
- **Estado:** G05-A/B/C aprovados tecnicamente; G05-D documental parcial. A análise fiscal pode prosseguir **descritivamente** e G06 poderá trabalhar cenários condicionais, sem causalidade identificada. Próxima diligência baseada em exportação de despesas por contrato/empenho ou e-SIC e nos casos Monte Aprazível e Rio Preto. Persistir cada novo vínculo no README e matriz.


## Handoff G06 — primeiro lote numérico 2027–2030, 09/11/2026
- **Fonte de verdade:** `editorial/rmsjrp/RELATORIO_G06_CENARIOS_CONDICIONAIS_2026_11_09.md`, configuração `PARAMETROS_G06_2027_2030.json`, script `build_cenarios_g06.py`. Cópia documental no Drive: https://docs.google.com/document/d/19n2b2cYYnT-fdG0MAKOXaJdD1JFrUxnwJ_Ju6sYiTAM/edit?usp=drivesdk; ID `19n2b2cYYnT-fdG0MAKOXaJdD1JFrUxnwJ_Ju6sYiTAM`, readback textual confirmado.
- **Run [42569549086](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42569549086)** `success`, artifact `13652304360`; 444 cenários municipais e 60 territoriais, 2027–2030; base 2025 G04 com 37/37 cobertura das variáveis essenciais; três outputs com readback SHA no R2 privado `rmsjrp/g06/2026_11_09/cenarios_v1/`. Não refazer coleta DCA/TCESP.
- **Método:** preços set/2026; 2026 é ponte de **hipóteses** e não observação; cenários adverso, continuidade, favorável com taxas de receita/despesa e razão de investimentos específicas; dados futuros de população/per capita ficam vazios. Receita menos despesa corrente não é resultado fiscal. Choque hipotético de -10% no FPM é sensibilidade independente, não corte legal.
- **Base legal:** LC 200/2023 aplica-se à União, com exclusões relativas a transferências constitucionais (art. 3º, §2º, I); PLOA 2027 (PLN 24/2026) e PLDO 2027 (PLN 2/2026) ainda tramitam em 09/11/2026; IBS em transição não foi quantificado. Nenhum efeito causal federal atribuído.
- **2030 condicional, R$ milhões reais set/2026:** investimentos 177,28 adverso; 236,26 continuidade; 453,27 favorável. Hipóteses experimentais, não previsão probabilística.
- **Próxima ação:** G06-B QA de sensibilidade ±1 p.p. para receita/despesa, inspeção de extremos municipais, efeito polo; atualizar registro e cópia Drive. G05-D pode continuar em paralelo apenas quando houver prova financeira de contratos/medições. Não iniciar 37 fichas sem matriz de fatos e QA municipal.
