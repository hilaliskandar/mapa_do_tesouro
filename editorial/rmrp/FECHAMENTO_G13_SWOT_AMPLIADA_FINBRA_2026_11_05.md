# RMRP — G1-3 — Auditoria ampliada de alegações nas SWOT (05/11/2026)

## Objeto e fonte
Revisão de 34 seções municipais do texto-fonte `SWOT_CONSOLIDADAS_ISS_ICMS_LOTE61A.md`, confrontadas com `DCA_SP_645_2013_2025_CANONICO.csv` (Drive ID `1BtXY_FxydMREEbMACJtaoW2n24ohVH33`, universo 645 municípios × 13 exercícios = 8.385 registros). Denominador populacional: **`populacao_dca` da própria base FINBRA em cada ano**, sem substituir pela Tabela IBGE 6579. Fatores reais: média anual IPCA (2015, 2023, 2025), setembro/2026, Lote 17.

## Testes
- **34/34 municípios** com chave correspondente e campos recuperáveis.
- **35 enunciados quantitativos** de variação real per capita expressos sob padrões textuais especificados: **14** de receita corrente 2015–2025 em 14 municípios; **21** de investimento 2023–2025 em 20 municípios.
- **35/35** enunciados compatíveis com cálculo independente pela base canônica FINBRA/DCA; tolerância 0,015 ponto percentual para arredondamento editorial.
- Desvio máximo observado: **0.004994** ponto percentual.
- Uma matriz pode apresentar mais de uma alegação; Santa Rosa de Viterbo repete o crescimento de investimento em duas afirmações, contabilizadas como dois enunciados, não dois municípios.

## Interpretação e limitação
Este teste reproduz **aritmeticamente** os enunciados efetivamente capturados por duas categorias de variação per capita; não é varredura de todos os percentuais da SWOT, nem revisão de justificativas causais, projetos, repasses, RGF ou legislação. Não houve divergência numérica nas 35 afirmações testadas. A convenção de população do FINBRA está preservada; verificações com estimativas demográficas de outra base não constituem motivo para substituir denominadores nem para bloquear esta conferência numérica. O metadado institucional/TCU pode ser complementado a partir da documentação existente, sem nova coleta.

A comprovação literal no DOCX/PDF **Lote 98 (66 páginas)** permanece separada: até este registro, o arquivo binário exato não foi recuperado nesta sessão. O corpus auditado é o Lote 61A, não a versão final congelada. Não declarar o Lote 98 revisado integralmente.

## Próxima decisão
Aprovar **a consistência numérica da amostra dirigida de 35 enunciados no Lote 61A**, mantendo em aberto a correspondência textual com o Lote 98 e a revisão de outras famílias de indicadores. Não reabrir a pesquisa populacional como requisito. Preservar o DOCX/PDF Lote 98 inalterados.

[CSV dos testes individuais](G13_AUDITORIA_SWOT_AMPLIADA_FINBRA_PER_CAPITA_2015_2025.csv).
