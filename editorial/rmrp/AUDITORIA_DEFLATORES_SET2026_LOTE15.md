# RMRP Volume II - Lote 15 - recuperacao e auditoria dos deflatores

Data 01/11/2026. Restricao: somente plataforma e acervo ja constituido, sem pesquisa externa.

## Evidencia encontrada

Arquivo previamente existente no Drive: [RM_RIBEIRAO_PRETO_IPCA_SET2026.xlsx](https://docs.google.com/spreadsheets/d/16ssO4FZGm5wGlG9TxGSpN-3yCPsjAMBV/edit), criado em 19/10/2026. Contem numeros-indice IPCA de dezembro dos anos 2013-2025, referencia setembro/2026 igual a 7695,82, agregados nominais e atualizados da RMRP e quatro sub-regioes, e matriz de cobertura de contas e anos. Estado da propria planilha: candidata analitica, nao homologada.

Fonte de parametros tambem existente: [FINBRA_PARTE5_parametros_temporais_IPCA_populacao_2013_2025](https://docs.google.com/spreadsheets/d/1ZiX9B2qgkUFcqibztgvGgvMdScqJGOvKLgL5nZfq6_I/edit). Esse arquivo usa em outra versao IPCA de junho/2026, nao de setembro/2026. Nao misturar bases monetarias.

## Divergencia de metodo a resolver antes da homologacao

A candidata RMRP registra V_real(ano) = V_nominal(ano) x [IPCA setembro/2026 / IPCA dezembro do ano], o que toma o nivel de precos de dezembro para deflacionar um fluxo anual completo. A convencao mais recente do projeto TIC-TIM utiliza a media aritmetica dos doze numeros-indice mensais do ano para os fluxos anuais. Essa ultima convencao corresponde melhor a valores acumulados durante todo o ano, mas so deve substituir a anterior apos recuperar e validar os 12 indices mensais de cada exercicio a partir do acervo ja disponivel.

IPCA setembro/2026 registrado no arquivo: 7695,82. IPCA dezembro/2023: 6773,27; dezembro/2025: 7403,29. Fatores da candidata: 1,13620 e 1,03951, aproximadamente. Esses fatores NAO equivalem aos fatores com indice medio anual.

## Dados de 2023 a 2025 ja atualizados na candidata, por metodo dezembro

RMRP, receitas correntes: R$ 11.159.950.266,01 (2023) e R$ 12.303.849.712,40 (2025) em precos de setembro/2026, usando dezembro como referencia. Investimentos liquidados: R$ 551.000.563,96 (2023) e R$ 314.246.905,22 (2025). Esses valores apenas registram as cifras ja presentes na planilha, nao recalculo homologado nem metodo selecionado para Volume II.

## QA e decisao

- Preservar planilha de 19/10 como versao historica/candidata. Nao confundir 'IPCA set/2026' com metodo de deflacao anual.
- Nao republicar variacoes reais do Volume I ou gerar serie 2013-2025 de nova autoria sem decidir a convencao e conferir fatores.
- Para comparar 34 municipios no proprio exercicio 2025, utilizar montantes nominais, indicadores per capita e proporcionais: o fator comum do ano nao muda a ordem dos municipios; para comparar os anos, utilizar a mesma convencao real.
- RREO janeiro-agosto 2025/2026 requer indices apropriados aos meses comparados, nao fatores de dezembro de ano completo.
- Lacunas em series continuam ausencias, nunca zeros; totais de subregiao so quando cobertura completa.

**Status:** localizado o arquivo existente, identificado o conflito real de versao e documentado o bloqueio. E2/E4 em andamento. Proxima diligencia restrita ao acervo: localizar indices mensais/medias anuais ja processadas e reconciliar a serie real com o caderno da RMRP, sem alterar a fonte original.
