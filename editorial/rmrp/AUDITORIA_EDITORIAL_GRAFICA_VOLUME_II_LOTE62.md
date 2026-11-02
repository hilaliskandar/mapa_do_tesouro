# Lote 62 — Auditoria editorial e gráfica do Volume II da RMRP

**Data:** 02/11/2026. **Objeto:** manuscrito `VOLUME_II_RMRP_SWOT_INTEGRADAS_LOTE61B.md`, SWOT consolidadas `SWOT_CONSOLIDADAS_ISS_ICMS_LOTE61A.md`, plano operacional e roteiros gráficos do Volume II. **Natureza:** auditoria de verificabilidade, integridade editorial e prioridades de apresentação; não homologação nem diagramação final.

## Parecer executivo

**E8 NÃO HOMOLOGADO.** A montagem contém capítulos substanciais de diagnóstico, SWOT, normas e cenários; porém não traz gráficos ou mapas materialmente incorporados e mantém informações de bastidor como "Próxima entrega: Lote 50", além de referências históricas que não refletem a última revisão das SWOT. A seção intitulada SWOT de 39 recortes apresenta **34 matrizes municipais e uma síntese textual metropolitana/sub-regional**, mas **não cinco matrizes formais atualizadas com os cinco quadrantes** na mesma versão. É preciso corrigir essa diferença antes de afirmar 39 SWOT finalizadas.

## Achados verificados, classificados

### A — Bloqueadores da publicação
1. **Figuras ainda não produzidas no próprio manuscrito.** O roteiro no fim do arquivo registra F1–F6 e M1 como "A produzir"/"A diagramar", sem qualquer imagem Markdown ou SVG/PNG efetivamente vinculada no manuscrito. Pesquisa por acervo gráfico nomeado no repositório não retornou correspondentes canônicos; ausência na pesquisa não prova ausência em todo o Drive. Exigir inventário de arquivos por ID e verificação visual/cálculo antes de declarar figuras prontas.
2. **SWOT agregadas não formalmente recompostas.** Parte II contém 34 fichas municipais e síntese geral; não contém quatro SWOT sub-regionais e uma metropolitana com quadrantes completos e fontes específicas. Escrever as cinco matrizes agregadas atualizadas ou alterar consistentemente a contagem, sem perder 39 como meta.
3. **Referências internas e metadados obsoletos.** No rodapé do manuscrito persistem a lista que aponta Lote 55 como principal fonte SWOT em vez do Lote 61A, texto de conclusão "Próximo procedimento: auditoria integrada Lote 51" e referências a "SWOT do Lote 47" no capítulo prospectivo. Esses vestígios não devem aparecer em edição externa.
4. **Grade numérica de cenários sem persistência externa verificada.** Lote 35 reporta 408 chaves municipais e 60 agregadas, mas o próprio manuscrito informa que CSV/XLSX/script não foram comprovadamente salvos. Sem esses arquivos e premissas não há simulação monetária homologável; cenários narrativos condicionais podem permanecer com transparência.

### B — Correções analíticas relevantes
5. **Duplicação editorial residual.** A inserção dos capítulos originais mantém títulos internos, introduções de lote, status operacionais e ressalvas repetidas na narrativa. As ressalvas essenciais devem ser centralizadas metodologicamente; notas locais apenas em casos anômalos.
6. **Enfoque jurídico das SWOT atualizado além dos capítulos III/IV.** Parte II emprega ISS principal e ICMS cota-parte de 2025 e mecanismos da LC 227/2026, enquanto os capítulos III/IV foram compostos a partir de Lotes 48/49 antes dos Lotes 58/59. Necessário incorporar explicitamente receita média de referência 2019–2026, acessórios, correção nominal legal, publicação/contestação de coeficientes e limites da série.
7. **Individualização municipal ainda parcial.** Fatores internos usam números próprios, mas oportunidades e ameaças são reiteradas, porque a norma federal é comum. Exigir que diferenças municipais apareçam não só nos valores, mas também em priorização administrativa, recurso institucional e carteira de projetos, sempre sustentadas por evidência.
8. **ISS principal não é ISS total; ISS+ICMS não é receita média legal de referência.** Preservar a distinção na legenda de F2 e qualquer gráfico sobre exposição ao IBS. Não classificar entes como "ganhadores/perdedores" sem cálculo legal.
9. **Regimes contábeis e preços.** Verificar em cada figura preços nominais ou reais (base set./2026), população dos mesmos anos e quocientes ponderados regionais; não confundir mediana municipal com razão dos agregados.
10. **RGF/RREO incompletos e Pontal.** Não inferir limites legais ou solvência dos percentuais DCA; observações anômalas segregadas.

### C — Pontos de apresentação
11. **Mapas.** Geometrias oficiais ainda não foram identificadas e validadas nesta rodada; não produzir cartografia fictícia nem apresentar mapas preliminares como oficiais. Exigir integridade de 34 polígonos e associação IBGE, CRS, cobertura e topologia; preferência por EPSG:4674.
12. **Caderno de figuras vinculado a partes.** Figura deve estar junto à interpretação: F1 junto ao crescimento de receita real; F2 composição; F3 dispersão tributação-FPM; F4 investimento; M1 desigualdades territoriais; F5 fluxo de mecanismos jurídico-fiscais; F6 matriz de cenários. Não montar atlas separado.

## Quadro de execução de figuras

| Item | Inserção | Evidência mínima exigida | Estado verificado |
|---|---|---|---|
| F1 | Parte I, receita real per capita | Série 2015–2025 por SR e agregado; índice de preços e população | Roteiro, figura não anexada |
| F2 | Parte I, composição da receita | ISS principal, IPTU, FPM e ICMS em 2025, mesmos denominadores; complementar investimentos em painel distinto | Roteiro, figura não anexada |
| F3 | Parte I, comparação municipal | 34 pontos, indicadores tributação/receita e FPM/receita do Lote 12; legendas | Roteiro, figura não anexada |
| F4 | Parte I, investimento | 2023/2025 reais per capita, fatores de deflação explícitos | Roteiro, figura não anexada |
| M1 | Parte I, territorialização | Geometria oficial, 34 chaves IBGE, CRS e QA topológico | Geometria não validada nesta rodada |
| F5 | Parte III, mecanismo institucional | Fluxo jurídico com ISS + ICMS de referência, coeficientes e limites de inferência | Roteiro, figura não diagramada |
| F6 | Parte IV, cenários condicionais | Comparação de hipóteses sem valores futuros inventados | Roteiro, figura não diagramada |

## Ordem de correção recomendada

**62A:** corrigir metadados obsoletos, atualizar sumário e bibliografia, recompor cinco SWOT agregadas, centralizar as ressalvas e integrar o mecanismo ISS+ICMS aos capítulos normativo/prospectivo.

**62B:** confeccionar F2 e F3 a partir das tabelas municipais existentes e conferidas; F1 e F4 com séries reais; F5 e F6 em diagrama original; M1 após geometrias verificadas. Produzir SVG ou figuras raster em repositório/Drive e vincular nos pontos do manuscrito após checagem visual.

**62C:** auditar completude do Lote 35, carteira de obras/programas, cobertura legal e referências; revisar voz editorial e fechar registro de evidências por figura, tabela e seção.

## Regras de saída

A presente auditoria é resultado verificável, não representa produção ou QA das figuras nem homologação E8. Não reextrair FINBRA/DCA, preservar fontes e versões, não prometer cálculo de perdas/ganhos IBS ainda sem parâmetros legais completos e dados oficiais.
