# Lote 87 — Recuperação da cartografia corrigida e aprofundamento probatório da escola FNDE de Guariba

**Data:** 04/11/2026. **Volume:** RMRP, Volume II, etapa de pré-homologação. **Edição de trabalho:** Lote 87, sem sobrescrever Lote 85.

## 1. Achado cartográfico: o mapa 15 já estava reclassificado no acervo

O relatório `editorial/rmrp/QA_MAPA_15_RECLASSIFICACAO_2026_10_29.md` comprova que, em 29/10/2026, o mapa 15 **já havia sido corrigido e inserido** no documento nativo de cartografia do Volume I (Google Docs `19qwSxQuy_1N4XEPqfpWgJrNB371WxiJwLfQad6oaIsI`). A correção foi produzida da DCA canônica `DCA_SP_645_2013_2025_CANONICO.csv`, Drive `1BtXY_FxydMREEbMACJtaoW2n24ohVH33`, e malha IBGE 2022, EPSG:4674, com 34 geometrias conferidas. O mapa novo registra comparação da média anual real de investimento liquidado 2023–2025 / 2020–2022, IPCA dezembro de cada exercício corrigido para setembro de 2026.

**Classes da figura efetivamente recuperada:** queda superior a 50% (3 municípios); queda de 20% a 50% (9); queda inferior a 20% (7); alta de 0% a 50% (5); alta superior a 50% (10). **19 reduções e 15 aumentos**, sem classe cruzando zero; extremos aproximados -68,5332% e +254,9829%. Dados e método sustentados também por `editorial/rmrp/QA_TRIENIOS_2026_10_29.md`.

O Google Doc cartográfico de 16 imagens e 52 tabelas foi exportado como DOCX diretamente do Drive (3.700.732 bytes). Localizou-se o mapa efetivamente corrigido entre os objetos gráficos, extraído como `image7.png` (2048 × 1795 px), preservando sua arte, legenda e notas. O mapa foi inspecionado integralmente e **substituiu somente o objeto gráfico antigo** do mapa 15 na cópia local do Volume II Lote 85, gerando `RMRP_VOLUME_II_MAPA15_CORRIGIDO_LOTE87.docx`. As legendas e dois textos de referência foram adequados para evitar a ressalva obsoleta da classe ambígua.

**Diferença metodológica explicitada na nova versão:** a cartografia trienal aplica IPCA com referência de **dezembro** por exercício, enquanto parte do texto analítico do Volume II usa média mensal anual do IPCA. As duas convenções **não devem ser confundidas**; a figura corrigida é consistente com seu próprio cálculo documentado e não substitui indicadores de outra janela ou deflacionamento.

## 2. Guariba — escola integral FNDE 959097/2024 e Contrato 043/2025

A página oficial do município lista diretamente os seguintes arquivos: termo de compromisso inicial, extrato no DOU, edital, homologação, **Contrato Administrativo 043/2025**, extrato contratual e autorização de início da obra: https://www.guariba.sp.gov.br/portal-da-transparencia/convenios/termo-de-compromisso-9590972024 . Leitura do portal executada por **Crawl2AI MCP** em 04/11/2026, com URLs dos anexos recuperadas.

**Contrato integral identificado:** `https://ecrie.com.br/sistema/conteudos/arquivo/a_39_2_5_04092025115646.pdf`. Arquivo de **27 páginas**, disponibilizado diretamente no portal da Prefeitura. A primeira página foi efetivamente aberta e inspecionada, confirmando **Contrato Administrativo 043/2025**, Processo 006/2025, Concorrência Eletrônica 001/2025, contratada **ARCON Engenharia e Serviços Ltda.**, construção de escola padrão FNDE de nove salas (3.589,39 m²) e adequações do terreno/equipamentos. **Não foi realizada leitura verificada das 27 páginas**, em razão das falhas de recuperação/screenshot posteriores; não classificar como contrato integral P0 auditado, apesar de a íntegra estar localizada.

O **extrato no Diário Oficial Municipal** confirma **R$ 8.576.160,36**, assinatura em **29/05/2025** e validade inicial de 28 meses: https://dosp.com.br/exibe_do.php?i=NjYxNzAw . O extrato foi publicado em 04/06/2025. Esse valor corresponde ao documento de contratação e não pode ser somado ou igualado mecanicamente ao valor total do instrumento FNDE, à contrapartida ou aos pagamentos.

A fonte oficial municipal declara **R$ 2.340.800,05 repassados até 24/04/2026**, mas trata-se de declaração do portal, sem conciliação bancária realizada nesta rodada.

**Termos de compromisso e aditivos:** o Lote 86 registra o extrato original de 2024 em R$ 9.874.832,63 e aditivos do DOU de 08 e 25/09/2025, incluindo repasse R$ 9.675.808,83 e contrapartida R$ 82.942,62. As datas e cifras não devem ser tomadas como versão final atual sem confrontar o termo integral e demais aditivos. A página do Município usa campos do resumo e do corpo com versões ainda divergentes, razão para exigir reconciliação de instrumentos, e não pressupor irregularidade.

O portal municipal disponibiliza também **ordem de início da obra** em `https://ecrie.com.br/sistema/conteudos/arquivo/a_39_0_1_29042026112213.pdf`, mas não foi possível abrir e inspecionar o PDF nesta rodada. A existência de link e título não prova a data de efetivo início, execução física, liquidação ou pagamento.

## 3. Resultado de edição e QA

Produzido DOCX de trabalho do Lote 87 e sua prova PDF, em diretório local próprio. A renderização concluiu **63 páginas**, mantendo **45 tabelas**, **14 imagens**, **39 matrizes SWOT** e **34 fichas municipais**. Página 11 foi inspecionada visualmente: figura corrigida, legenda cromática e explicação estão juntas, sem corte aparente. A conferência automática de limites das caixas de texto do PDF não identificou palavras fora da página; o número de imagens por página permaneceu inalterado em relação à prova PDF do Lote 85.

**Limite de QA:** não foi concluída conferência visual em ampliação individual de 100% das 63 páginas. Não atribuir estado 'homologado', 'publicável' ou '100% revisado'. Os demais mapas permanecem herdados da versão anterior e os dados fiscais não foram recalculados.

## 4. Próximas diligências

1. Recuperar e ler integralmente os 27 fólios do Contrato 043/2025, cláusulas financeiras, fiscalização, cronograma, assinaturas e aditivos; cotejar com o termo FNDE e com empenhos e ordens bancárias;
2. Confrontar oficialmente o termo de compromisso 959097/2024, os aditivos de 2025 e eventuais aditivos posteriores, separando valores de origem federal, contrapartida e contratação em cada versão;
3. Certificar no PNCP e no portal municipal os contratos de Cravinhos, Orlândia e Santa Cruz da Esperança, registrando os respectivos estágios; conferir a fonte do concedente FID de Cássia dos Coqueiros;
4. Reexaminar o uso de índices de dezembro e média mensal anual entre o Volume I e o Volume II para impedir comparação não homogênea;
5. Verificar visualmente todas as 63 páginas e compatibilidade dos gráficos, tabelas e legendas; revisar corpus jurídico vigente antes de emitir versão externa;
6. Preservar os Lotes 83/85 e não reclassificar município inteiro como P0 a partir de apenas um extrato ou uma página.

**Nota de correção histórica:** o Lote 86 consignou o mapa 15 como pendência de recriação; o presente Lote 87 verificou que a recreação **já estava concluída em 29/10/2026**, faltando apenas aproveitar a imagem corrigida no Volume II. Este registro substitui **somente** a interpretação anterior de indisponibilidade da imagem, sem apagar as evidências e restrições do Lote 86.
