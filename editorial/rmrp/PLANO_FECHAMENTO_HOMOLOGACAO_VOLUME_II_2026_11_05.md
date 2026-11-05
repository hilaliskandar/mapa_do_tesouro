# Plano de trabalho para fechamento e homologação do Volume II — RMRP
**Versão:** 1.0 · 05/11/2026 · **Marco de partida:** Lote 105 · **Documento de referência:** Volume II Lote 98 (66 páginas)

## Objeto e decisão
Concluir o Volume II sem reabrir a reconstrução geral do diagnóstico. O trabalho passa a ter dois trilhos articulados: **A — fechamento do conteúdo já consolidado** e **B — saneamento documental de exceções**, com alteração do relatório apenas após decisão técnica fundamentada. O marco Lote 105, a matriz de oito gates e a edição Lote 98 permanecem preservados.

**Produto pretendido:** relatório final revisado em DOCX e PDF, acervo de dados e fontes, matriz de QA e termo de homologação técnica. **Não confundir versão de revisão interna, versão publicável com ressalvas e versão plenamente homologada.**

## Etapa 0 — Congelamento e inventário de versão
**Entrada:** Lote 98; dossiê Lote 105; bases Lotes 93–95, 99, 103–104.  
**Procedimentos:** gerar manifesto do acervo com nome, local, versão, SHA-256, estado de QA, dependências; conferir disponibilidade efetiva de todos os binários, especialmente DOCX/PDF Lote 98 e planilha Lote 94 com fórmulas IPCA; separar fontes brutas, tratamento e publicações. Nenhum arquivo-fonte deve ser sobrescrito.  
**Entregas:** inventário assinado por hash, lista de fontes e manifesto de versão inicial.  
**Gate G0:** arquivos-base recuperáveis, cadeia de versões íntegra e limites da consolidação explicitados.

## Etapa 1 — Auditoria quantitativa e metodológica final
**Frente A1 (dados homologáveis agora):** validar 34 códigos IBGE, chave município–ano, 374 linhas DCA, 369 rubricas observadas, cinco NA; verificar 132 índices IPCA, média anual e fator de deflação; recomputar os agregados do painel de 30 municípios/330 observações e comparar 2024–2025 nos universos 30 e 34. Registrar arredondamento e fonte.  
**Frente A2 (coerência do relatório):** confrontar cada indicador-chave entre base, tabela, mapa, gráfico, resumo executivo e conclusão. Manter separadas receita de capital bruta, transferência de capital, investimentos liquidados, empenhos, pagamentos e estoques. Não misturar preços médios de 2025 com setembro de 2026.  
**Entregas:** matriz indicador–fonte–fórmula–período–universo–página e relatório de reconciliação.  
**Gate G1:** todos os números utilizados nas conclusões principais são reproduzíveis; cinco ausências permanecem NA documentadas; divergências abertas são identificadas e excluídas de juízos normativos.

## Etapa 2 — Saneamento seletivo das exceções substantivas
Subordinar cada correção ao critério de encerramento da matriz consolidada, com responsável pela prova, prazo ou condição, resultado e eventual efeito no texto.

| Código | Tema | Prova decisiva | Encaminhamento se não obtida |
|---|---|---|---|
| FIS-01 | Pontal RCL/DTP 2025 | RGF versões protocolizadas + notas de retificação + conciliação DO/RREO | Restringir percentuais de LRF e registrar conflito documental |
| FIS-02 | Pontal DCL | RGF Anexo 02 e composição das deduções/caixa | Registrar explicação aritmética, não homologar causa administrativa |
| FIS-03 | Barrinha RGF 2025/2026 | PDF do Executivo, histórico de retificação RE, Anexos 02/06 | Quarentena dos campos divergentes |
| FIS-04 | Orlândia RGF 2025/2026 | Versões Audesp/DO/Siconfi e protocolo de transmissão | Quarentena dos campos divergentes |
| FED-01 | Guariba FNDE | Extrato de desembolso + empenho/liquidação/pagamento municipal | Não afirmar valores efetivamente pagos ou transferidos |
| TRI-01 | IBS 2027–2030 | ISS e cota ICMS 2019–2026 conforme LC 227 + coeficientes oficiais quando divulgados | Manter cenários condicionais sem impactos monetários |
| DAT-01 | Cinco lacunas DCA | Retificação ou esclarecimento oficial de rubrica | NA e painel equilibrado, sem imputação |
| EDI-01 | QA final | Checklist jurídico, editorial e visual 100% cumprido | Bloquear homologação externa |

**Gate G2:** cada exceção tem decisão formal `SANADA / RESSALVADA COM ISOLAMENTO / DEPENDE DE FONTE FUTURA`, prova e impacto explicitados. Não transformar impossibilidade de obtenção de prova em valor zero ou em conformidade legal presumida.

## Etapa 3 — Revisão jurídica, institucional e dos cenários
**Controle jurídico:** citar dispositivos vigentes, competência, período e status; rever a transição IBS à luz da LC 214/2025 e LC 227/2026 e atos posteriores identificados com fonte oficial. Não utilizar fator IPCA na atualização legal da receita média de referência, que tem regra própria; não produzir perdas ou ganhos de IBS por município sem parâmetros homologados.  
**Controle analítico:** 39 matrizes SWOT preservadas, mas conferir coerência entre diagnóstico, tese, vulnerabilidade, oportunidade, recomendação e evidência. Cada cenário 2027–2030 deve apresentar premissas, gatilhos, incerteza e distinção entre previsão e hipótese.  
**Gate G3:** ausência de conclusões normativas sem fundamento e de projeções apresentadas como resultados observados.

## Etapa 4 — Fechamento editorial e cartográfico
**Redação:** leitura contínua de todo o relatório; retirar metainformações, redundâncias, notas internas e ressalvas excessivamente repetitivas sem reduzir conteúdo; padronizar títulos, siglas, unidades, datas-base, notas metodológicas e referências ABNT.  
**Visual:** revisão manual de **todas as 66 páginas** da base, após atualização de paginação; conferir 45 tabelas, mapas/legendas, figuras, escala, CRS, fontes, citações, paginação, índice e contrastes, com prioridade para mapa 15. Testar exportação DOCX→PDF e estabilidade de quebras de página.  
**Gate G4:** checklist integral página a página sem defeitos críticos, todos os elementos ancorados e tabelas sem truncamentos.

## Etapa 5 — Homologação e disponibilização controlada
**Pacote:** (i) relatório DOCX e PDF, (ii) sumário executivo, (iii) bases analíticas auditadas, (iv) caderno metodológico e referências, (v) matriz de pendências resolvidas ou ressalvadas, (vi) manifesto SHA-256, (vii) termo de homologação técnica.  
**Critérios de decisão:** `APTO PARA REVISÃO INTERNA` quando G0–G1 concluídos e bloqueios conhecidos; `APTO PARA PUBLICAÇÃO COM RESSALVAS` somente se G0–G4 concluídos e todo P0 tiver sido sanado **ou isolado de forma que não contamine as conclusões**; `HOMOLOGAÇÃO PLENA` somente com pendências materiais resolvidas e aprovação técnica competente. Na ausência de coeficientes do IBS ainda futuros, os cenários prospectivos podem ser divulgados apenas como **condicionais e não monetizados**, caso essa limitação esteja editorialmente explícita e aceita.

**Gate G5:** manifesto íntegro, revisão técnica aprovada e decisão de divulgação registrada com data, responsável e ressalvas.

## Ordem operacional e dependências
**Caminho crítico:** G0 (inventário) → G1 (conferência indicadores) → G3 (revisão substantiva) → G4 (QA editorial e visual) → G5 (decisão).  
**Trilho paralelo:** G2 diligências Pontal/Barrinha/Orlândia/Guariba/IBS/DCA, cuja resolução altera a redação **somente se produzir novo fato documental**. Antes da versão de publicação, avaliar quais pendências remanescentes podem ser isoladas e quais exigem retenção do produto.

**Marcos sem cronograma artificial:** M1 inventário fechado; M2 indicadores reconciliados; M3 exceções classificadas; M4 minuta de circulação revisada; M5 decisão formal de homologação. A duração de cada marco depende do acesso efetivo às fontes externas e da decisão de revisão; não há promessa de prazo sem essas dependências.

## Responsabilidades
- **Equipe técnica de dados:** execução dos testes e manifestação sobre integridade, séries e mapas.
- **Revisão jurídico-institucional:** validação de dispositivos, repartição de competências e condicionantes IBS.
- **Revisão editorial/cartográfica:** revisão integrada, figuras, tabelas, paginação e referências.
- **Coordenação responsável:** aceite das ressalvas, aprovação da versão para circulação e registro formal da decisão. A preparação documental não substitui assinatura ou competência decisória.

## Primeira ordem de execução
1. Recuperar e verificar o arquivo binário do **Volume II Lote 98** e a planilha de deflação Lote 94; produzir manifesto de versões e hashes.
2. Consolidar uma **matriz de proveniência dos indicadores efetivamente citados no Volume II**, começando por receita de capital, RGF e cenários IBS.
3. Aplicar o checklist de fechamento nos trechos de maior risco: resumo executivo, limites de informação, figuras fiscais, mapa 15, transição IBS, conclusões.
4. Elaborar uma minuta de decisão de ressalvas para os P0, sem alterar numeradores, denominadores ou inferir desembolsos.

## Registro permanente
- Documento-base: `editorial/rmrp/MARCO_CONSOLIDADO_VOLUME_II_LOTE105_2026_11_05.md`.
- Matriz única: `editorial/rmrp/MATRIZ_UNICA_PENDENCIAS_MARCO105_2026_11_05.csv`.
- Este plano: `editorial/rmrp/PLANO_FECHAMENTO_HOMOLOGACAO_VOLUME_II_2026_11_05.md`.

**Status deste plano:** aprovado como proposta de execução do fechamento; não equivale à conclusão de qualquer gate nem à homologação do relatório.


### 05/11/2026 — G0 concluído: inventário, hashes e pacote congelado do Volume II
Primeira tarefa do Plano de Fechamento **executada**: 25/25 arquivos essenciais localizados em `/mnt/data`, SHA-256 individual calculado, DOCX/PDF base **Lote98** íntegros (Word 321 parágrafos, 45 tabelas, 15 mídias; PDF 66/66 páginas com texto; 66 PNG renderizadas). **Hashes de referência**: DOCX `fffd21bb65251d89caee484c2cabf7b813a7884760f60943c95919e608249df4`; PDF `0f366b6238d569bb206e02f0e5c64dc5ea0877ee8c11606b5a897c2325995743`. Mídias L97→L98 **15/15 com hashes idênticos**. Planilha original **Lote94 com fórmulas** recuperada: 12 abas, **1.278 fórmulas**, SHA `71c03c45fd31f1767800d6682cf649c6999af15104845b14a009d700f856dc74`. Manifesto JSON/CSV e script criados em `/mnt/data/RMRP_FECHAMENTO_G0`; pacote congelado ZIP com 15 entradas, **4.397.963 bytes**, `testzip()` sem erros. **Arquivado no Drive com confirmação de metadados/tamanho**: ZIP `1eROu1DKokcGlxwv_qRZZLYJAyo__XmeK`, manifesto CSV `1ftn53gAhbO0ODbiyirJ9FMjWA2URNjVU`, pasta `1ywdJpIzgXWC9otX9Rq0HBQqYTjzUnRSK`; não foi executado re-hash por download remoto. Dossiê completo `editorial/rmrp/FECHAMENTO_G0_MANIFESTO_INTEGRIDADE_2026_11_05.md`, commit `22ff6e59dbd1bababfe5afaa3a98f968522841e3`. **Gate G0 aceito para inventário e integridade local, NÃO representa homologação do conteúdo**; próximo G1: validar fórmulas/cobertura IPCA/DCA, reproduzir taxas 2024–25 e conferir proveniência de números nas 66 páginas. Nenhum original foi alterado.


### 05/11/2026 — Fechamento G1-1: auditoria quantitativa DCA/IPCA e painel longitudinal
Executada a primeira frente G1 sobre o arquivo **original** do Lote 94 e o painel do Lote 95, com confronto ao Volume II Lote 98. **Resultado 1.278/1.278 fórmulas aritmeticamente coerentes**, mas a origem tinha **49 caches vazios** (46 em `COBERTURA_ANUAL` e 3 em `PONTAL_QA_RGF_RREO`). Gerada **cópia independente** com os 49 caches completados, conservando todas as fórmulas, valores e estilos originais: **1.278/1.278 fórmulas com cache validado**; original não modificado. **374 chaves únicas**, 34 municípios ×11 anos, **369 observações** e **cinco NA**, 132 IPCA mensais; **zero divergências** entre séries L94/L95, painel equilibrado 30 municípios × 11 =330. Reproduzidas quedas reais 2024–25: **30 municípios −13,4807577%** e **34 municípios −14,1625430%**, em reais médios de 2025, coincidentes à página 16 do Volume II. Criada matriz inicial de proveniência (nove grupos). **Pendência editorial nova na p.60:** quadro usa expressão “RGF/RREO com cobertura parcial”, enquanto p.16 documenta RGF Executivo 2025 **34/34**, com indicadores de Pontal/Barrinha/Orlândia ainda sob QA. Deve harmonizar termos, **sem presumir RREO 34/34**. **Drive upload e metadados conferidos:** cópia XLSX `1230GLvfK1zBJtHpNmt6Jx9KvJzdmBmws` (87.393 bytes); série CSV `1r19sn6UDT3JhXeKlQlzgqq1mAkufI5G5` (813 bytes); proveniência CSV `1YGqjXrefsDseNb-bR1bAWN1sAOdk8rgH` (3.172 bytes). Dossiê `editorial/rmrp/FECHAMENTO_G1_AUDITORIA_CAPITAL_IPCA_2026_11_05.md`, commit `13e2a8f397c71aed57bb60b93201723a37c031c7`. **G1-1 ACEITO; G1 integral AINDA ABERTO** para demais indicadores, tabelas e fonte cartográfica. Volume II não modificado.


### 05/11/2026 — Fechamento G1-2: auditoria de composição corrente e SWOT 2025
Reprocessado arquivo primário `receitas orçamentárias (anexo I-C) - municípios de sp 2025.csv` para **34 municípios**, contas sintéticas DCA I-C `Receitas Brutas Realizadas`, vínculo subregional conferido. **20/20 percentuais** da Tabela de composição (RMRP e quatro sub-regiões × tributação/ISS/IPTU/FPM) e **50/50 afirmações numéricas** de tributação/FPM em 34 SWOT municipais foram conferidos sem divergências. **Achado metodológico: “FPM/receita” no Volume II é apenas cota mensal**, código `RO1.7.1.1.51.1.0` (RMRP **12,84%**), enquanto o FPM total inclui cotas extraordinárias (RMRP **14,23%**; diferença agregada R$164.553.493,49). **EDI-03 aberta** para explicitar o numerador, sem mudar silenciosamente a série. A linha de cotas extraordinárias está ausente para Jaboticabal e Orlândia: não preencher como zero observado. Foram mapeadas **98 ocorrências percentuais** nas 34 SWOT; 50 verificadas, as demais não homologadas nesta frente. Resta auditar despesa corrente liquidada, investimentos, índices reais per capita 2015–2025, cartografia e marcos jurídicos. **Volume II Lote98, 66 páginas, não alterado.** Dossiê `editorial/rmrp/FECHAMENTO_G12_AUDITORIA_COMPOSICAO_RECEITAS_SWOT_2026_11_05.md`, commit `a794201242d883ca9dad913e7b1e2cdae5c4b6c9`. Arquivos no Drive, metadados verificados: tabela 20 testes `1HmclVw1Vt1-KwjrlQWoMSFlV_TELPh8x`; 50 SWOT `1AqytTJD03pEnFJhKyS1fQPLlwz1xdpl1`; matriz ampliada de 17 eixos `1TOz689OEczWeBkMiP405PVbQq5S7dlnc`. **Aceite apenas da composição da receita corrente 2025; G1 integral continua aberto.** Próxima frente: conferir dados de despesa liquidada 2023–25 e indicadores de investimento, sem confundir com receita de capital.
