# G24 — Auditoria Audesp: RCL mensal, resultados fiscais e modelos LRF 2025

**Referência:** 05/11/2026. Continuidade dos controles G21–G23 para Pontal (3540200), Barrinha (3505609) e Orlândia (3534302). O Volume II G20 e o Lote 98 original não foram editados.

## Fontes primárias localizadas
1. **RCL mensal do Audesp:** https://www.transparencia.tce.sp.gov.br/sites/default/files/conjunto-dados/rcl_completo.zip . Catálogo: https://www.transparencia.tce.sp.gov.br/conjunto-de-dados . Fonte declarada: balancetes municipais; atualização informada no catálogo em 05/11/2026, tamanho 843,81 KB. **Sem dados municipais lidos nesta rodada**.
2. **Resultado das Análises Audesp (LRF, Ensino, Saúde):** https://www.transparencia.tce.sp.gov.br/sites/default/files/conjunto-dados/resultado_analises_audesp.zip . O catálogo inclui resultados de despesas com pessoal e indica atualização em 01/11/2026 (468,90 KB). **Nenhum registro extraído**.
3. **Modelos e metodologias LRF 2025:** https://www.tce.sp.gov.br/audesp/documentacao/demonstrativos-audesp-modelos-e-metodologias-calculo-lrf-2025 . Contém RCL 2025_V00, dívida consolidada líquida 2025_V01 e despesa de pessoal Executivo 2025_V02. **São modelos, não resultados individuais**. Esta é a URL correta para 2025; a referência anterior que incluía `de-calculo` no caminho não retornava a página pretendida.

## Resultado de acesso
Falha DNS do contêiner para baixar ZIP. Crawl2AI não processou ZIP. Firecrawl confirmou resposta de formato `application/zip` ao desabilitar validação TLS, mas a ferramenta não admite esse formato. Tentativas de Browserless não forneceram bytes. **0 registros municipais Audesp extraídos; quatro pendências FIS-01 a FIS-04 mantidas abertas.** A detecção do tipo MIME não é inspeção do conteúdo.

## Procedimento de reprodução
Foi produzido o arquivo `conferir_rcl_audesp_g24.py`, que inspeciona ZIP, exige escolha explícita das colunas depois da inspeção do leiaute, filtra dezembro de 2025 e os três códigos municipais e impede exportação se não houver 1 registro por município. **Validado apenas em ZIP sintético fictício**; o esquema da base real permanece desconhecido e poderá exigir adaptação.

O pacote técnico local `RMRP_G24_DOSSIE_AUDESP_2026_11_05.zip` contém relatório integral, roteiro CSV e código Python. A publicação deste registro não equivale ao upload dos ZIPs oficiais, que não foram obtidos.

## Estado de homologação
- Pontal RCL/DTP: **P0 aberto**, aguardando prova Audesp dezembro/2025, versões RGF e RREO.
- Pontal DCL/deduções: **P0 aberto**, sem memória protocolizada da disponibilidade de caixa entre exercícios.
- Barrinha RGF S2/2025: **P0 aberto**, sem PDF oficial lido e sem histórico da entrega `RE`.
- Orlândia DCL/DTP: **P0 aberto**, sem conciliação Audesp/Diário Oficial/Siconfi.

Nenhum valor é atribuído ao Audesp sem arquivo original conferido. Nenhuma hipótese é convertida em imputação de irregularidade, nem as pendências RGF contaminam os indicadores DCA já aprovados.

Próxima diligência: obter binariamente `rcl_completo.zip` e `resultado_analises_audesp.zip`, verificar sua estrutura e filtrar Pontal, Barrinha e Orlândia; comparar com os demonstrativos de 2025 sob critérios de competência, periodicidade, órgão e denominador.
